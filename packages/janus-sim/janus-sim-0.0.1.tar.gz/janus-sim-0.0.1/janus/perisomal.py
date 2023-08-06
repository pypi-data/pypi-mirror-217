import json
from collections import defaultdict
import numpy as onp
import jax
import jax.numpy as jnp
import jax.scipy as jscipy
import equinox as eqx
from jaxtyping import Array, Float
from typing import Tuple, OrderedDict, Dict, List, NamedTuple, Type, Union
from models.channels import ALLEN_CHANNEL_NAMES, ALLEN_ION_NAMES, Ion, IonChannel, ChannelGroup
from models.compartments import PassiveCompartmentGroup, CaCompartment, CaCompartmentState

import tensorflow_probability.substrates.jax as tfp
tf = tfp.tf2jax
tfd = tfp.distributions


SQ_CENTI_PER_SQ_MICRO = 1e-8
MILLI_PER_MICRO = 1e-3

Scalar = Float[Array, ""]

class PerisomalState(NamedTuple):
  vs: Float[Array, " num_compartments"]
  soma_state: CaCompartmentState


class PerisomalModel(eqx.Module):

  soma: CaCompartment
  passive_groups: OrderedDict[str, PassiveCompartmentGroup]

  num_compartments: int = eqx.static_field()
  temp_celsius: float = eqx.static_field()
  dt: float = eqx.static_field()

  expL: Float[Array, "num_compartments num_compartments"] = eqx.static_field()

  def __init__(self,
               group_params: Dict,
               edges: List[Tuple[int, int, float]],
               soma_channels: List[Tuple[Type[IonChannel], float]],
               ion_reversals: Dict[Ion, Scalar],
               leak_reversal: Scalar,
               temp_celsius: float,
               dt: float):
    """Construct a perisomal model.

    Args:
      group_params: A dictionary mapping group names to parameter dictionaries. Each parameter
        dictionary should contain the following keys and values:
          * A list of nodes under the key "nodes" containing both compartments and junction
            nodes. Each element must be a 3-tuple containing a globally unique node id, the
            surface area in square microns, and a boolean that is true if it is a junction node.
            The surface areas of junction nodes are ignored.
          * Specific membrane capacitance in microfarads per square centimeter under key "cm"
          * Leak conductance density in siemens per square centimeter under key "g_leak"
      edges: A list of connections between nodes. Each element of the list should be a
        three-tuple containing the adjacent node ids (as specified in group_params) as well as
        the resistance of the connection in megaohms.
      soma_channels: A list of tuples representing the soma ion channels and their
        conductance density. Each tuple should be length 2 and contain an IonChannel followed
        by the conductance density in siemens per square centimeter.
      ion_reversals: A dictionary mapping Ions to floats representing their reversal potential
        in millivolts. This is shared across compartments
      leak_reversal: The reversal potential of the leak channel for all comparts in millivolts.
      temp_celsius: The temperature in kelvin, shared across all compartments.
      dt: The integration timestep in milliseconds.
    """
    # Check that the parameters were specified correctly
    group_name_set = set(group_params.keys())
    assert len(group_name_set) == len(group_params), "Specified a group name more than once."
    assert "soma" in group_name_set, "Must specify a soma compartment."
    for name in group_name_set:
      assert "nodes" in group_params[name], f"Must specify nodes for group '{name}'."
      assert "cm" in group_params[name], \
              f"Must specify membrane capacitance under key 'cm' for group '{name}'"
      assert "g_leak" in group_params[name], \
              f"Must specify leak conductance density key 'g_leak' for group '{name}'"

    self.temp_celsius = temp_celsius
    self.dt = dt

    # TODO: Check graph topology is correct.
    # * is a connected tree
    # * node ids unique
    # * all edges are between known nodes
    # * junction nodes are never adjacent

    # Compute number of junction nodes and compartment nodes
    num_junc_nodes = 0
    num_comp_nodes = 0
    for _, params in group_params.items():
      for _, _, is_junc in params["nodes"]:
        if is_junc:
          num_junc_nodes += 1
        else:
          num_comp_nodes += 1
    tot_num_nodes = num_junc_nodes + num_comp_nodes
    self.num_compartments = num_comp_nodes

    # Check that the graph has the right number of edges for a connected tree
    assert len(edges) == tot_num_nodes - 1, "Cannot be a connected tree, # of edges incorrect."

    # Layout the nodes, soma first followed by the passive groups.
    # This layout does not reorder compartment nodes within groups, but can reorder the
    # groups themselves.
    node_layout_map = {}
    num_junc_nodes_seen = 0
    num_comp_nodes_seen = 0
    # Specify an ordering on the groups.
    group_names = ["soma"] + list(group_name_set.difference({"soma"}))
    for name in group_names:
      for og_node_id, _, is_junc in group_params[name]["nodes"]:
        if is_junc:
          node_layout_map[og_node_id] = num_comp_nodes + num_junc_nodes_seen
          num_junc_nodes_seen += 1
        else:
          node_layout_map[og_node_id] = num_comp_nodes_seen
          num_comp_nodes_seen += 1

    assert num_junc_nodes_seen == num_junc_nodes
    assert num_comp_nodes_seen == num_comp_nodes
    assert len(node_layout_map) == tot_num_nodes

    # Construct the soma
    assert len(group_params["soma"]["nodes"]) == 1, "Soma can only have 1 node"
    soma_sa_sq_um = group_params["soma"]["nodes"][0][1] # square microns
    soma_sa_sq_cm = soma_sa_sq_um * SQ_CENTI_PER_SQ_MICRO
    assert soma_sa_sq_cm > 0., "Somal compartment must have non-zero surface area."
    soma_channel_types = [x[0] for x in soma_channels]
    num_channels = len(soma_channel_types)
    soma_channel_densities = jnp.array([x[1] for x in soma_channels]).reshape([num_channels])
    self.soma = CaCompartment(
            ChannelGroup(soma_channel_types),
            jnp.array(soma_sa_sq_cm), # cm^2
            self.temp_celsius, # celsius
            group_params["soma"]["cm"] * MILLI_PER_MICRO, # millifarads / cm^2
            group_params["soma"]["g_leak"], # siemens / cm^2
            leak_reversal, # millivolts
            ion_reversals, # millivolts
            soma_channel_densities, # siemens / cm^2
            group_params["soma"]["cao"], # millimolar
            group_params["soma"]["cai_min"], # millimolar
            group_params["soma"]["ca_buff_depth"], # micrometers
            group_params["soma"]["ca_decay_rate"], # milliseconds
            group_params["soma"]["free_ca_perc"]) # unitless

    # Construct the passive groups
    passive_group_names = group_names[1:]
    self.passive_groups = OrderedDict()
    for name in passive_group_names:
      # Only the non-junction (compartment) nodes are actually constructed.
      group_comp_nodes = [n for n in group_params[name]["nodes"] if not n[2]]
      group_num_comps = len(group_comp_nodes)
      assert group_num_comps > 0, f"Group {name} has no compartments."
      group_sas_sq_um = jnp.array([n[1] for n in group_comp_nodes])
      group_sas_sq_cm = group_sas_sq_um * SQ_CENTI_PER_SQ_MICRO
      group_cm_mf_per_sq_cm = group_params[name]["cm"] * MILLI_PER_MICRO
      group_g_leak = group_params[name]["g_leak"]
      self.passive_groups[name] = PassiveCompartmentGroup(
            group_num_comps,
            group_sas_sq_cm, # cm^2
            group_cm_mf_per_sq_cm, # millifarads / cm^2
            group_g_leak, # siemens / cm^2
            leak_reversal) # millivolts

    # Construct the matrix for the inter-compartment ODE.
    # Start by making the matrix that produces all node voltages
    # from only compartment node voltages.

    # The matrix will be a num_comps x num_comps identity matrix concatenated with
    # a num_junc_nodes x num_comps matrix. To construct the bottom matrix we need to
    # iterate over junction nodes and set the corresponding row values.

    # First, make a map from nodes to their neighbors. The graph will operate on the
    # provided ids, not the layout ids.
    graph = defaultdict(list)
    for u, v, r in edges:
      graph[u].append((v,r))
      graph[v].append((u,r))

    M = onp.zeros([num_junc_nodes, num_comp_nodes])
    for _, params in group_params.items():
      for node_id, _, is_junc in params["nodes"]:
        if is_junc:
          for neighb_id, edge_resistance in graph[node_id]:
            node_layout_id = node_layout_map[node_id]
            row = node_layout_id - num_comp_nodes
            # Junction nodes will never be adjacent to other junction nodes, so this will
            # always be less than num_comp_nodes.
            neighb_layout_id = node_layout_map[neighb_id]
            assert neighb_layout_id < num_comp_nodes
            # Units don't matter here because we normalize to unitless quantities below.
            conductance = 1. / edge_resistance
            M[row, neighb_layout_id] = conductance

    # Normalize by row sums.
    M = M / onp.sum(M, axis= 1, keepdims=True)
    J = onp.concatenate([onp.eye(num_comp_nodes), M], axis=0)
    assert J.shape == (tot_num_nodes, num_comp_nodes)

    # Construct the laplacian for the expanded graph.
    L = onp.zeros([num_comp_nodes, tot_num_nodes])
    for u, v, r in edges:
      u_layout_id = node_layout_map[u]
      v_layout_id = node_layout_map[v]
      r_ohm = float(r) * 1e6 # megaohms -> ohms
      assert r_ohm >= 0., "All resistances must be positive."
      cond = 1. / r_ohm # ohms -> siemens
      if u_layout_id < num_comp_nodes:
        L[u_layout_id, v_layout_id] = cond
      if v_layout_id < num_comp_nodes:
        L[v_layout_id, u_layout_id] = cond

    # Set the diagonal to the negative row sums
    onp.fill_diagonal(L, -onp.sum(L, axis=1))

    # Compute the capacitances of each compartment to scale the Laplacian.
    sa_list = [jnp.array(self.soma.surface_area).reshape([1])]
    cm_list = [jnp.array(self.soma.specific_membrane_capacitance).reshape([1])]
    for _, g in self.passive_groups.items():
      sa_list.append(g.surface_area)
      cm_list.append(jnp.full([g.num_compartments], g.specific_membrane_capacitance))
    # surface areas in cm^2
    all_sas = jnp.concatenate(sa_list)
    # membrane specific capacitances in millifarads / cm^2
    all_cms = jnp.concatenate(cm_list)
    # membrane capacitances in millifarads
    all_Cs = all_sas * all_cms
    assert all_Cs.shape == (num_comp_nodes,)
    final_M = jnp.diag(1. / all_Cs) @ (L @ J)
    self.expL = jscipy.linalg.expm(final_M * (dt / 2.))

  @classmethod
  def from_allen_json(cls, filepath: str, dt: float):
    """Create a PerisomalModel from a processed Allen Institute JSON file.

    Args:
      filepath: Path to the JSON file.
      dt: The integration timestep in milliseconds.
    """
    with open(filepath, "r") as f:
      cfg = json.load(f)

    soma_channels = []
    for channel_name, gbar in cfg["groups"]["soma"]["channel_conductance_densities"].items():
      soma_channels.append((ALLEN_CHANNEL_NAMES[channel_name], float(gbar)))

    ion_reversals = {}
    for ion_name, rev_pot in cfg["ion_reversals"].items():
      ion_reversals[ALLEN_ION_NAMES[ion_name]] = float(rev_pot)

    group_params = cfg["groups"]
    del group_params["soma"]["channel_conductance_densities"]

    model = cls(group_params,
                cfg["edges"],
                soma_channels,
                ion_reversals,
                cfg["leak_reversal"],
                cfg["temperature_celsius"],
                dt)
    return model

  def init_state(self, v: Union[Scalar, float]) -> PerisomalState:
    """Create a resting state for the model.

    Args:
      v: The resting voltage, in millivolts.
    Returns:
      The state of the model.
    """
    _, soma_init_state = self.soma.init_state(v)
    init_vs = jnp.full([self.num_compartments], v)
    return PerisomalState(vs=init_vs, soma_state=soma_init_state)

  def intra_compartment_step(
          self,
          dt: float,
          t: Scalar,
          soma_ext_current: Scalar,
          prev_vs: Float[Array, " num_compartments"],
          prev_soma_state: CaCompartmentState
          ) -> Tuple[Float[Array, " num_compartments"], CaCompartmentState]:
    """Perform one integration step for each compartment.

    Args:
      dt: Integration step in milliseconds.
      t: Current time in milliseconds.
      soma_ext_current: External current applied to the soma in milliamps.
      prev_vs: The previous voltage of each compartment in millivolts.
      prev_soma_state: The previous state of the soma.
    Returns:
      new_vs: The new voltages of each compartment in millivolts,
        an array of shape [num_compartments]
      new_soma_state: The new state of the soma.
    """
    soma_vs = prev_vs[0]
    new_soma_v, new_soma_state = self.soma.step(
            dt, t, soma_ext_current, soma_vs, prev_soma_state)

    comp_dims = [x.num_compartments for x in self.passive_groups.values()]
    comp_inds = onp.cumsum(comp_dims)
    comp_vs = jnp.split(prev_vs[1:], comp_inds)
    new_passive_vs = []
    for c, v in zip(self.passive_groups.values(), comp_vs):
      # Passive compartments don't have any injected current.
      c_ext_current = jnp.zeros([c.num_compartments])
      new_passive_vs.append(c.step(dt, t, c_ext_current, v))

    new_vs = jnp.concatenate([new_soma_v.reshape([1])] + new_passive_vs)
    return new_vs, new_soma_state

  def step(
          self,
          dt: float,
          t: Scalar,
          soma_ext_current: Scalar,
          prev_state: PerisomalState) -> PerisomalState:
    """Integrate the model for one timestep.

    Args:
      dt: The step length in milliseconds.
      t: The current time in milliseconds.
      soma_ext_current: The external current applied to the soma in milliamps.
      prev_state: The previous state of the model.
    Returns:
      The state of the model at time t + dt.
    """
    # Do an inter-compartment step
    vs = self.expL @ prev_state.vs
    # Do a step within each compartment
    vs, soma_state = self.intra_compartment_step(
            dt, t, soma_ext_current, vs, prev_state.soma_state)
    # Another inter-compartment step
    vs = self.expL @ vs
    return PerisomalState(vs=vs, soma_state=soma_state)

  def run_sweep(
          self,
          dt: float,
          soma_ext_current: Float[Array, " num_steps"],
          init_v: Scalar) -> PerisomalState:
    """Integrate the model for a sequence of external currents.

    Args:
      dt: The step length in milliseconds.
      soma_ext_current: The external current applied to the soma in milliamps at each
        timestep, an array of shape [num_steps].
      init_v: The initial resting voltage of the model in millivolts
    Returns:
      The state of the model over time.
    """
    num_steps = soma_ext_current.shape[0]
    T = dt * (num_steps - 1)
    ts = onp.linspace(0, T, num=num_steps)
    init_state = self.init_state(init_v)

    def scan_fn(prev_state, inp):
      t, ext_current = inp
      new_state = self.step(dt, t, ext_current, prev_state)
      return new_state, new_state

    _, out_states = jax.lax.scan(scan_fn, init_state, (ts, soma_ext_current))
    return out_states
