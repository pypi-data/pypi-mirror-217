import jax
import jax.numpy as jnp
import jax.scipy as jscipy
import equinox as eqx
from jaxtyping import Array, Float
from typing import Tuple, Dict, Union, NamedTuple
from models.channels import Ion, ChannelGroup, ALLEN_CHANNEL_NAMES, ALLEN_ION_NAMES
from util import exprel
import json

FARADAY = 96489.
GAS_CONST = 8.31441
ZERO_CELSIUS_IN_KELVIN = 273.15
SQ_CENTI_PER_SQ_MICRO = 1e-8
MILLI_PER_MICRO = 1e-3
MILLI_PER_STANDARD = 1_000

Scalar = Float[Array, ""]

def exp_euler(dt: Union[Scalar, float],
              a: Float[Array, " state_dim"],
              b: Float[Array, " state_dim"],
              x: Float[Array, " state_dim"]) -> Float[Array, " state_dim"]:
  ha = a * dt
  hb = b * dt
  out = jnp.exp(ha) * x + exprel(ha) * hb
  return out


def expm_2x2_lt(A):
  ea = jnp.exp(A[0,0])
  ed = jnp.exp(A[1,1])
  off_diag = A[1,0] * ed * exprel(A[0,0] - A[1,1])
  return jnp.array([[ea, 0.], [off_diag, ed]])


def exp_euler_2x2_ltA(
        dt: Union[Scalar, float],
        A: Float[Array, "state_dim state_dim"],
        b: Float[Array, " state_dim"],
        x: Float[Array, " state_dim"]) -> Float[Array, " state_dim"]:
  hA = A * dt
  expAh = expm_2x2_lt(hA)
  out = expAh @ x + (expAh - jnp.eye(x.shape[0])) @ jnp.linalg.solve(A, b)
  return out


def passive_voltage_dynamics(
        leak_reversal_potential: Scalar,
        leak_conductance_density: Scalar,
        specific_membrane_capacitance: Scalar,
        ext_current: Scalar,
        surface_area: Scalar):
  """Compute the voltage linear ODE terms for a passive compartment.

  The ODE is commonly given as

    c_m dv/dt = I_ext / sa - g_l (v - E_l)

  where:
    * c_m is the specific membrance capacitance in millifarads / cm^2.
    * dv/dt is the derivative of voltage with respect to time in millivolts per millisecond.
    * I_ext is the external current applied to the compartment in milliamps.
    * sa is the surface area of the compartment in cm^2.
    * g_l is the compartment leakage conductance density in seimens / cm^2.
    * v is the voltage in millivolts.
    * E_l is the leakage channel reversal potential in millivolts.

  This ODE can be rewritten as

    dv/dt = av + b

  where

    a = -g_l / c_m
    b = (I_ext / sa + g_l * E_l)) / c_m

  Args:
    leak_reversal_potential: The leak channel reversal potential, E_l, in millivolts.
    leak_conductance_density: The leak channel conductance density, g_l, in seimens / cm^2.
    specific_membrane_capacitance: The specific membrance capacitance c_m, in millifarads / cm^2.
    ext_current: The external current I_ext in milliamps.
    surface_area: The membrane surface area of the compartment, sa, in cm^2.
  Returns:
    a: the weight in the linear voltage ODE
    b: the drift in the linear voltage ODE
  """
  a = - leak_conductance_density / specific_membrane_capacitance
  b = leak_conductance_density * leak_reversal_potential
  b += ext_current / surface_area
  b = b / specific_membrane_capacitance
  return a, b


def active_voltage_dynamics(
        leak_reversal_potential: Scalar,
        leak_conductance_density: Scalar,
        specific_membrane_capacitance: Scalar,
        ext_current: Scalar,
        surface_area: Scalar,
        channels: ChannelGroup,
        max_channel_conductance_densities: Float[Array, " num_channels"],
        channel_state: Float[Array, " channel_state_dim"],
        ion_reversal_potentials: Dict[Ion, Scalar],
        ) -> Tuple[Scalar, Scalar, Float[Array, " num_channels"]]:
  """Compute the voltage linear ODE terms for a compartment with voltage-gated ion channels.

  The ODE is commonly given as

    c_m dv/dt = I_ext / sa - g_l * (v - E_l) - sum_i g_i * a_i * (v - E_[ion_i])

  where:
    * c_m is the specific membrance capacitance in millifarads / cm^2.
    * dv/dt is the derivative of voltage with respect to time in millivolts per millisecond.
    * I_ext is the external current applied to the compartment in milliamps.
    * sa is the surface area of the compartment in cm^2.
    * g_l is the compartment leakage conductance density in seimens / cm^2.
    * v is the voltage in millivolts.
    * E_l is the leakage channel reversal potential in millivolts.
    * g_i is the max conductance density of ion channel i in seimens / cm^2.
    * a_i is the 'activation' of ion channel i, a unitless value computed as a nonlinear
        function of the ion channel state.
    * E_[ion_i] is the reversal potential of the ion carried by the ith ion channel,
      in millivolts.

  This ODE can be rewritten as

    dv/dt = av + b

  where

    a = (-g_l  - sum_i g_i * a_i) / c_m
    b = ((I_ext / sa) + (g_l * E_l) + (sum_i g_i * a_i * E_[ion_i])) / c_m

  Args:
    leak_reversal_potential: The leak channel reversal potential, E_l, in millivolts.
    leak_conductance_density: The leak channel conductance density, g_l, in seimens / cm^2.
    specific_membrane_capacitance: The specific membrance capacitance c_m, in millifarads / cm^2.
    ext_current: The external current I_ext in milliamps.
    surface_area: The membrane surface area of the compartment, sa, in cm^2.
    channels: A ChannelGroup describing the voltage-gated channels active in this compartment.
    max_channel_conductance_densities: The maximum conductance density for each channel in
      seimens / cm^2, an array of shape [num_channels].
    channel_state: The state of the ion channels in this compartment,
      an array of shape [channel_state_dim].
    ion_reversal_potentials: A dict mapping ions to their reversal potentials in millivolts.
  Returns:
    a: the weight in the linear voltage ODE
    b: the drift in the linear voltage ODE
    channel_conductances: The conductance density for each channel in seimens  / cm^2.
  """
  # The active compartment has a passive component
  a, b = passive_voltage_dynamics(
          leak_reversal_potential,
          leak_conductance_density,
          specific_membrane_capacitance,
          ext_current,
          surface_area)
  # (num_channels)
  activations = channels.activation(channel_state)
  # (num_channels)
  channel_conductances = activations * max_channel_conductance_densities
  # (num_channels)
  channel_reversals = channels.reversal_potentials(ion_reversal_potentials)
  a += - jnp.sum(channel_conductances) / specific_membrane_capacitance
  b += jnp.sum(channel_reversals * channel_conductances) / specific_membrane_capacitance
  return a, b, channel_conductances


def voltage_and_cai_dynamics(
      leak_reversal_potential: Scalar,
      leak_conductance_density: Scalar,
      specific_membrane_capacitance: Scalar,
      ext_current: Scalar,
      surface_area: Scalar,
      channels: ChannelGroup,
      max_channel_conductance_densities: Float[Array, " num_channels"],
      channel_state: Float[Array, " channel_state_dim"],
      ion_reversal_potentials: Dict[Ion, Scalar],
      E_ca: Scalar,
      free_ca_perc: Scalar,
      ca_decay_rate: Scalar,
      ca_buffer_depth: Scalar,
      cai_min: Scalar
      ) -> Tuple[Float[Array, "2 2"], Float[Array, " 2"]]:
    """Compute the conditionally linear voltage dynamics for a single compartment.

    Args:
      channel_state: The state of the ion channels in the compartment.
      E_ca: The calcium reversal potential in millivolts.
      free_ca_perc: The percentage of free calcium.
      ca_decay_rate: The decay rate of calcium in milliseconds.
      ext_current: The external current applied to this compartment, in milliamps.
      max_channel_conductance_densities: The max conductance density of each channel
        in the compartment, in seimens / cm^2.
      surface_area: The membrane surface area of the compartment in cm^2.
    Returns:
      A: The 2x2 matrix in the linear ODE.
      b: The 2-dimensional drift vector in the linear ODE.
    """
    assert max_channel_conductance_densities.ndim == 1
    assert channel_state.ndim == 1
    ion_reversals = ion_reversal_potentials.copy()
    #TODO: Check that this is OK under vmap
    ion_reversals[Ion.Ca] = E_ca
    # First, compute the contribution from the passive and active channels
    a, b, channel_conductances = active_voltage_dynamics(
            leak_reversal_potential,
            leak_conductance_density,
            specific_membrane_capacitance,
            ext_current,
            surface_area,
            channels,
            max_channel_conductance_densities,
            channel_state,
            ion_reversals)
    # Sum the current contributions from each calcium channel
    ca_conductance = jnp.sum(channels.ca_mask() * channel_conductances)
    # Compute calcium dynamics constants
    k = 10_000 * (free_ca_perc / (2 * FARADAY * ca_buffer_depth))
    # Put together the dynamics matrices
    A_mat = jnp.array([[a, 0.], [- k * ca_conductance, - 1. / ca_decay_rate]])
    b_vec =  jnp.array([b, k * ca_conductance * E_ca + (cai_min / ca_decay_rate)])
    return A_mat, b_vec


def nernst(temp_celsius: Scalar, cai: Scalar, cao: Scalar) -> Scalar:
    """Compute the reversal potential of calcium in millivolts using the Nernst equation."""
    E_ca = ((GAS_CONST * (temp_celsius + ZERO_CELSIUS_IN_KELVIN)) /
            (2 * FARADAY)) * jnp.log(cao / cai)
    E_ca *= MILLI_PER_STANDARD # volts to millivolts
    return E_ca


class PassiveCompartmentGroup(eqx.Module):
  """A group of compartments with a leak channel."""

  num_compartments: int = eqx.static_field()
  surface_area: Float[Array, " num_compartments"] = eqx.static_field()  # cm^2

  # Shared across compartments
  specific_membrane_capacitance: Scalar # millifarads / cm^2
  leak_reversal_potential: Scalar  # millivolts
  log_leak_conductance_density: Scalar # seimens / cm^2

  def __init__(self,
               num_compartments: int,
               surface_area: Float[Array, " num_compartments"],
               specific_membrane_capacitance: Scalar,
               leak_conductance_density: Scalar,
               leak_reversal_potential: Scalar):
    """Create a passive compartment group.

    Args:
      num_compartments: The number of compartments in the group.
      surface_area: The surface area of each compartment in cm^2, a [num_compartments] array.
      specific_membrane_capacitance: The specific membrane capacitance in millifarads / cm^2,
        shared across all compartments.
      leak_conductance_density: The density of the leak conductance channel in seimens / cm^2,
        shared across all compartments.
      leak_reversal_potential: The reversal potential in millivolts, shared across all
        compartments.
    """
    self.num_compartments = num_compartments
    self.surface_area = surface_area
    assert surface_area.shape == (num_compartments,)
    self.specific_membrane_capacitance = specific_membrane_capacitance
    self.leak_reversal_potential = leak_reversal_potential
    self.log_leak_conductance_density = jnp.log(leak_conductance_density)

  def init_state(self, v: Scalar) -> Float[Array, " num_compartments"]:
    """Creates a resting state for the compartment group.

    Args:
      v: The resting voltage, in millivolts
    Returns:
      The resting state of the compartment group.
    """
    return jnp.full([self.num_compartments], jax.lax.stop_gradient(v))

  def step(self,
           dt: Union[Scalar, float],
           t: Scalar,
           ext_current: Float[Array, " num_compartments"],
           prev_state: Float[Array, " num_compartments"]
           ) -> Float[Array, " num_compartments"]:
    """Integrate the state of the compartment group for one step of size dt.

    Args:
      dt: The stepsize in milliseconds.
      t: The current time in milliseconds.
      ext_current: The external current applied to each compartment in milliamps, an array of
        size num_compartments.
      prev_state: The state of the compartment group at the previous timestep.
    Returns:
      The compartment group state at time t + dt
    """
    del t
    a, b = jax.vmap(passive_voltage_dynamics, in_axes=(None, None, None, 0, 0))(
            self.leak_reversal_potential,
            jnp.exp(self.log_leak_conductance_density),
            self.specific_membrane_capacitance,
            ext_current,
            self.surface_area)
    new_vs = exp_euler(dt, a, b, prev_state)
    return new_vs


ActiveCompartmentState = Float[Array, " num_channels"]

class ActiveCompartment(eqx.Module):
  """A compartment with voltage-gated ion channels."""

  channels: ChannelGroup = eqx.static_field()
  surface_area: Scalar = eqx.static_field() # cm^2

  # Shared across compartments
  leak_reversal_potential: Scalar = eqx.static_field() # millivolts
  ion_reversal_potentials: Dict[Ion, Scalar] = eqx.static_field() # millivolts
  specific_membrane_capacitance: Scalar = eqx.static_field() # millifarads / cm^2

  log_leak_conductance_density: Scalar # seimens / cm^2

  # Per-compartment, seimens / cm^2
  log_max_channel_conductance_densities: Float[Array, " num_channels"]

  def __init__(self,
               channels: ChannelGroup,
               surface_area: Scalar,
               specific_membrane_capacitance: Scalar,
               leak_conductance_density: Scalar,
               leak_reversal_potential: Scalar,
               ion_reversal_potentials: Dict[Ion, Scalar],
               max_channel_conductance_densities: Float[Array, " num_channels"]):
    """Create a compartment with voltage-gated ion channels.

    Args:
      channels: A ChannelGroup containing voltage-gated ion channels.
      surface_area: The surface area of the compartment in cm^2.
      specific_membrane_capacitance: The specific membrane capacitance in millifarads / cm^2.
      leak_conductance_density: The density of the leak conductance channel in seimens / cm^2.
      leak_reversal_potential: The reversal potential in millivolts.
      ion_reversal_potentials: The reversal potentials of each ion in millivolts.
      max_channel_conductance_densities: The conductance densities of each channel
        in seimens / cm^2, an array of shape [num_channels].
    """
    self.surface_area = surface_area
    self.channels = channels
    self.specific_membrane_capacitance = specific_membrane_capacitance
    self.leak_reversal_potential = leak_reversal_potential
    self.ion_reversal_potentials = ion_reversal_potentials
    self.log_leak_conductance_density = jnp.log(leak_conductance_density)
    self.log_max_channel_conductance_densities = jnp.log(max_channel_conductance_densities)

  def init_state(
          self,
          v: Union[Scalar, float]
          ) -> Tuple[Scalar, ActiveCompartmentState]:
    """Creates a resting state for the compartment group.

    Args:
      v: The resting voltage, in millivolts
    Returns:
      init_vs: The initial voltage of each compartment, an array of shape [num_compartments].
      init_state: The initial state of each compartment, an ActiveGroupState.
    """
    sg_v = jax.lax.stop_gradient(jnp.array(v))
    channel_state = self.channels.resting_state(v, None)
    return sg_v, channel_state

  def step(
          self,
          dt: Union[Scalar, float],
          t: Scalar,
          ext_current: Scalar,
          prev_v: Scalar,
          prev_state: ActiveCompartmentState,
          ) -> Tuple[Scalar, ActiveCompartmentState]:
    """Integrate the state of the compartment group for one step of size dt.

    Args:
      dt: The stepsize in milliseconds.
      t: The current time in milliseconds.
      ext_current: The external current applied to the compartment in milliamps.
      prev_vs: The voltage in millivolts of the compartment at the previous timestep.
      prev_state: The state of the compartment at the previous timestep.
    Returns:
      new_voltage: The voltage of the compartment at time t + dt.
      new_state: The compartment state at time t + dt.
    """
    del t
    v_a, v_b = self.voltage_dynamics(ext_current, prev_state)
    new_v = exp_euler(dt / 2., v_a, v_b, prev_v)

    channel_A_diags, channel_bs = self.channels.state_dynamics(new_v, None)
    new_channel_state = exp_euler(dt, channel_A_diags, channel_bs, prev_state)

    v_a, v_b = self.voltage_dynamics(ext_current, new_channel_state)
    new_v = exp_euler(dt / 2., v_a, v_b, new_v)
    return new_v, new_channel_state

  def voltage_dynamics(
          self,
          ext_current: Scalar,
          channel_state: ActiveCompartmentState
          ) -> Tuple[Scalar, Scalar]:
    """Compute the conditionally linear voltage dynamics for this compartment.

    Args:
      ext_current: The external current applied to the compartment in milliamps.
      channel_state: The state of the ion channels in the compartment at the previous timestep.

    Returns:
      a: The a multiplier.
      b: The drift b.
    """
    a, b, _ = active_voltage_dynamics(
            self.leak_reversal_potential,
            jnp.exp(self.log_leak_conductance_density),
            self.specific_membrane_capacitance,
            ext_current,
            self.surface_area,
            self.channels,
            jnp.exp(self.log_max_channel_conductance_densities),
            channel_state,
            self.ion_reversal_potentials)
    return a, b


class ActiveGroupState(NamedTuple):
  channel_state: Float[Array, "num_compartments channel_state_dim"]


class ActiveCompartmentGroup(eqx.Module):
  """A group of compartments with voltage-gated ion channels."""

  num_compartments: int = eqx.static_field()
  channels: ChannelGroup = eqx.static_field()
  surface_area: Float[Array, " num_compartments"] = eqx.static_field() # cm^2

  # Shared across compartments
  leak_reversal_potential: Scalar = eqx.static_field() # millivolts
  ion_reversal_potentials: Dict[Ion, Scalar] = eqx.static_field() # millivolts
  specific_membrane_capacitance: Scalar = eqx.static_field() # millifarads / cm^2

  log_leak_conductance_density: Scalar # seimens / cm^2

  # Per-compartment, seimens / cm^2
  log_max_channel_conductance_densities: Float[Array, "num_compartments num_channels"]

  def __init__(self,
               num_compartments: int,
               channels: ChannelGroup,
               surface_area: Float[Array, " num_compartments"],
               specific_membrane_capacitance: Scalar,
               leak_conductance_density: Scalar,
               leak_reversal_potential: Scalar,
               ion_reversal_potentials: Dict[Ion, Scalar],
               max_channel_conductance_densities: Float[Array, "num_compartments num_channels"]):
    """Create a compartment group with voltage-gated ion channels.

    Args:
      num_compartments: The number of compartments in the group.
      channels: A ChannelGroup containing voltage-gated ion channels.
      surface_area: The surface area of each compartment in cm^2, a [num_compartments] array.
      specific_membrane_capacitance: The specific membrane capacitance in millifarads / cm^2,
        shared across all compartments.
      leak_conductance_density: The density of the leak conductance channel in seimens / cm^2,
        shared across all compartments.
      leak_reversal_potential: The reversal potential in millivolts, shared across all
        compartments.
      ion_reversal_potentials: The reversal potentials of each ion in millivolts, shared
        across all compartments.
      max_channel_conductance_densities: The conductance densities of each channel in each
        compartment in seimens / cm^2, an array of shape [num_compartments, num_channels].
    """
    self.num_compartments = num_compartments
    self.surface_area = surface_area
    self.channels = channels
    self.specific_membrane_capacitance = specific_membrane_capacitance
    self.leak_reversal_potential = leak_reversal_potential
    self.ion_reversal_potentials = ion_reversal_potentials
    self.log_leak_conductance_density = jnp.log(leak_conductance_density)
    self.log_max_channel_conductance_densities = jnp.log(max_channel_conductance_densities)

  def init_state(
          self,
          v: Union[Scalar, float]
          ) -> Tuple[Float[Array, " num_compartments"], ActiveGroupState]:
    """Creates a resting state for the compartment group.

    Args:
      v: The resting voltage, in millivolts
    Returns:
      init_vs: The initial voltage of each compartment, an array of shape [num_compartments].
      init_state: The initial state of each compartment, an ActiveGroupState.
    """
    sg_v = jax.lax.stop_gradient(v)
    channel_state = self.channels.resting_state(v, None)
    channel_state = jnp.tile(channel_state[jnp.newaxis, :], [self.num_compartments, 1])
    vs = jnp.full([self.num_compartments], sg_v)
    return vs, ActiveGroupState(channel_state=channel_state)

  def step(
          self,
          dt: Union[Scalar, float],
          t: Scalar,
          ext_current: Float[Array, " num_compartments"],
          prev_vs: Float[Array, " num_compartments"],
          prev_state: ActiveGroupState
          ) -> Tuple[Float[Array, " num_compartments"], ActiveGroupState]:
    """Integrate the state of the compartment group for one step of size dt.

    Args:
      dt: The stepsize in milliseconds.
      t: The current time in milliseconds.
      ext_current: The external current applied to each compartment in milliamps, an array of
        size num_compartments.
      prev_vs: The voltage in millivolts of each compartment at the previous timestep,
        an array of size num_compartments.
      prev_state: The state of the compartment group at the previous timestep.
    Returns:
      new_voltage: The voltage of each compartment at time t + dt.
      new_state: The compartment group state at time t + dt.
    """
    del t
    assert ext_current.shape == (self.num_compartments,)
    assert prev_vs.shape == (self.num_compartments,)
    # (num_compartments), (num_compartments)
    v_A_diag, v_b = self.voltage_dynamics(ext_current, prev_state.channel_state)
    # (num_compartments)
    new_v = exp_euler(dt / 2., v_A_diag, v_b, prev_vs)

    # (num_compartments, channel_state_dim), (num_compartments, channel_state_dim)
    channel_A_diags, channel_bs = jax.vmap(self.channels.state_dynamics)(new_v, None)
    new_channel_state = jax.vmap(exp_euler, in_axes=(None, 0, 0, 0))(
            dt, channel_A_diags, channel_bs, prev_state.channel_state)

    # (num_compartments), (num_compartments)
    v_A_diag, v_b = self.voltage_dynamics(ext_current, new_channel_state)
    # (num_compartments)
    new_v = exp_euler(dt / 2., v_A_diag, v_b, new_v)
    return new_v, ActiveGroupState(channel_state=new_channel_state)

  def voltage_dynamics(
          self,
          ext_current: Float[Array, " num_compartments"],
          channel_state: Float[Array, "num_compartments channel_state_dim"]
          ) -> Tuple[Float[Array, " num_compartments"], Float[Array, " num_compartments"]]:
    """Compute the conditionally linear voltage dynamics for all compartments in the group.

    Args:
      ext_current: The external current applied to each compartment in milliamps, an array of
        size num_compartments.
      channel_state: The state of the ion channels of each compartment in the group at the
        previous timestep.

    Returns:
      a: The a multiplier for each compartment, an array of shape [num_compartments].
      b: The drift b for each compartment, an array of shape [num_compartments].
    """

    def v_dyn(ext_current, sa, states):
      return active_voltage_dynamics(
              self.leak_reversal_potential,
              jnp.exp(self.log_leak_conductance_density),
              self.specific_membrane_capacitance,
              ext_current,
              sa,
              self.channels,
              jnp.exp(self.log_max_channel_conductance_densities),
              states,
              self.ion_reversal_potentials)

    a, b, _ = jax.vmap(v_dyn)(ext_current,
                              self.surface_area,
                              channel_state)
    return a, b


class CaCompartmentState(NamedTuple):
  channel_state: Float[Array, " channel_state_dim"]
  cai: Scalar


class CaCompartment(eqx.Module):
  """A compartment with voltage- and calcium-gated ion channels and simple ca dynamics.

  Calcium dynamics are computed using an exponential decay ODE (see ca_decay rate and cai_min).
  The calcium reversal potential is computed using the Nernst equation.
  """

  channels: ChannelGroup = eqx.static_field()
  temp_celsius: Scalar = eqx.static_field() # Celsius

  log_surface_area: Scalar  # cm^2
  specific_membrane_capacitance: Scalar # millifarads / cm^2

  leak_reversal_potential: Scalar# = eqx.static_field() # millivolts

  cao: Scalar = eqx.static_field() # millimolar
  cai_min: Scalar = eqx.static_field() # millimolar
  ca_buffer_depth: Scalar = eqx.static_field() # micrometers

  ion_reversal_potentials: Dict[Ion, Scalar]# = eqx.static_field() # millivolts

  log_max_channel_conductance_densities: Float[Array, " num_channels"] # seimens / cm^2
  log_leak_conductance_density: Scalar # seimens / cm^2

  log_ca_decay_rate: Scalar  # millisecond
  logit_free_ca_perc: Scalar  # unitless

  def __init__(self,
               channels: ChannelGroup,
               surface_area: Scalar,
               temp_celsius: float,
               specific_membrane_capacitance: Scalar,
               leak_conductance_density: Scalar,
               leak_reversal_potential: Scalar,
               ion_reversal_potentials: Dict[Ion, Scalar],
               max_channel_conductance_densities: Float[Array, " num_channels"],
               cao: float,
               cai_min: float,
               ca_buffer_depth: float,
               ca_decay_rate: float,
               free_ca_perc: float):
    """Create a compartment group with calcium dynamics.

    Args:
      channels: A ChannelGroup containing voltage- and calcium-gated ion channels.
      surface_area: The surface area of the compartment in cm^2.
      temp_celsius: The temperature in celsius.
      specific_membrane_capacitance: The specific membrane capacitance in millifarads / cm^2.
      leak_conductance_density: The density of the leak conductance channel in seimens / cm^2.
      leak_reversal_potential: The reversal potential in millivolts.
      ion_reversal_potentials: The reversal potentials of each ion in millivolts.
      max_channel_conductance_densities: The conductance densities of each channel
        in seimens / cm^2, an array of shape [num_channels].
      cao: The extracellular calcium concentration in millimolar.
      cai_min: The minimum intracellular calcium concentration in millimolar.
      ca_buffer_depth: The depth of the calcium buffer, in micrometers.
      ca_decay_rate: The decay rate of calcium in milliseconds.
      free_ca_perc: The percent of free calcium.
    """
    self.temp_celsius = jnp.array(temp_celsius)
    self.log_surface_area = jnp.log(surface_area)
    self.channels = channels
    self.specific_membrane_capacitance = specific_membrane_capacitance
    self.log_max_channel_conductance_densities = jnp.log(max_channel_conductance_densities)
    self.log_leak_conductance_density = jnp.log(leak_conductance_density)
    self.leak_reversal_potential = leak_reversal_potential
    self.ion_reversal_potentials = ion_reversal_potentials
    # Calcium params
    self.cao = jnp.array(cao)
    self.cai_min = jnp.array(cai_min)
    self.ca_buffer_depth = jnp.array(ca_buffer_depth)
    self.log_ca_decay_rate = jnp.log(ca_decay_rate)
    self.logit_free_ca_perc = jscipy.special.logit(free_ca_perc)

  @classmethod
  def from_allen_json(cls, filepath: str):
    """Create a PerisomalModel from a processed Allen Institute JSON file.

    Args:
      filepath: Path to the JSON file.
    """
    with open(filepath, "r") as f:
      cfg = json.load(f)

    channels = []
    densities = []
    for channel_name, gbar in cfg["groups"]["soma"]["channel_conductance_densities"].items():
      channels.append(ALLEN_CHANNEL_NAMES[channel_name])
      densities.append(jnp.array(float(gbar)))
    num_channels = len(channels)
    channel_densities = jnp.array(densities).reshape([num_channels])

    ion_reversals = {}
    for ion_name, rev_pot in cfg["ion_reversals"].items():
      ion_reversals[ALLEN_ION_NAMES[ion_name]] = jnp.array(float(rev_pot))

    group_params = cfg["groups"]
    del group_params["soma"]["channel_conductance_densities"]

    sa = jnp.array(group_params["soma"]["nodes"][0][1] * SQ_CENTI_PER_SQ_MICRO)
    cm = jnp.array(group_params["soma"]["cm"] * MILLI_PER_MICRO)
    leak_conductance_density  = jnp.array(group_params["soma"]["g_leak"])
    leak_reversal = jnp.array(cfg["leak_reversal"])
    temp_celsius = cfg["temperature_celsius"]
    model = cls(ChannelGroup(channels),
                sa,
                temp_celsius,
                cm,
                leak_conductance_density,
                leak_reversal,
                ion_reversals,
                channel_densities,
                group_params["soma"]["cao"],
                group_params["soma"]["cai_min"],
                group_params["soma"]["ca_buff_depth"],
                group_params["soma"]["ca_decay_rate"],
                group_params["soma"]["free_ca_perc"])
    return model


  def init_state(
          self,
          v: Union[Scalar, float]
          ) -> Tuple[Scalar, CaCompartmentState]:
    """Creates a resting state for the compartment group.

    Args:
      v: The resting voltage, in millivolts
    Returns:
      init_vs: The initial voltage of the compartment, a scalar.
      init_state: The initial state of the compartment, a CaGroupState.
    """
    v = jnp.array(v)
    cai = jnp.array(self.cai_min)
    channel_state = self.channels.resting_state(v, self.cai_min)
    return v, CaCompartmentState(channel_state=channel_state, cai=cai)

  def step(
          self,
          dt: Union[float, Scalar],
          t: Scalar,
          ext_current: Scalar,
          prev_v: Scalar,
          prev_state: CaCompartmentState
          ) -> Tuple[Scalar, CaCompartmentState]:
    """Integrate the state of the compartment for one step of size dt.

    Args:
      dt: The stepsize in milliseconds.
      t: The current time in milliseconds.
      ext_current: The external current applied to the compartment in milliamps.
      prev_v: The voltage of the compartment at the previous timestep in millivolts.
      prev_state: The state of the compartment at the previous timestep.
    Returns:
      new_voltage: The voltage of the compartment at time t + dt.
      new_state: The compartment state at time t + dt.
    """
    del t
    # Do a voltage/calcium half step
    E_ca = nernst(self.temp_celsius, prev_state.cai, self.cao)
    v_and_cai_As, v_and_cai_bs = self.voltage_and_cai_dynamics(
            prev_state.channel_state, E_ca, ext_current)
    v_and_cai = jnp.stack([prev_v, prev_state.cai], axis=0)
    new_v_and_cai = exp_euler_2x2_ltA(dt / 2., v_and_cai_As, v_and_cai_bs, v_and_cai)
    new_v, new_cai = new_v_and_cai.T

    # Now do a channel state step
    # (num_compartments, subunit_dim), (num_compartments, subunit_dim)
    channel_state_A_diags, channel_state_bs = self.channels.state_dynamics(new_v, new_cai)
    new_channel_state = exp_euler(
            dt, channel_state_A_diags, channel_state_bs, prev_state.channel_state)

    # Now another voltage/calcium step
    E_ca = nernst(self.temp_celsius, new_cai, self.cao)
    v_and_cai_As, v_and_cai_bs =  self.voltage_and_cai_dynamics(
            new_channel_state, E_ca, ext_current)
    new_v_and_cai = exp_euler_2x2_ltA(dt / 2., v_and_cai_As, v_and_cai_bs, new_v_and_cai)
    new_v, new_cai = new_v_and_cai.T
    new_state = CaCompartmentState(channel_state=new_channel_state, cai=new_cai)
    return new_v, new_state

  def voltage_and_cai_dynamics(
      self,
      channel_state: Float[Array, " channel_state_dim"],
      E_ca: Scalar,
      ext_current: Scalar,
      ) -> Tuple[Float[Array, "2 2"], Float[Array, " 2"]]:
    """Compute the conditionally linear voltage dynamics for the compartment.

    Args:
      channel_state: The state of the ion channels.
      E_ca: The calcium reversal potential in millivolts.
      ext_current: The external current applied to the compartment in milliamps.
    Returns:
      A: The [2, 2] matrix in the system of linear ODEs.
      b: The [2] drift vector in the system of linear ODEs.
    """
    return voltage_and_cai_dynamics(
                    self.leak_reversal_potential,
                    jnp.exp(self.log_leak_conductance_density),
                    self.specific_membrane_capacitance,
                    ext_current,
                    jnp.exp(self.log_surface_area),
                    self.channels,
                    jnp.exp(self.log_max_channel_conductance_densities),
                    channel_state,
                    self.ion_reversal_potentials,
                    E_ca,
                    jax.nn.sigmoid(self.logit_free_ca_perc),
                    jnp.exp(self.log_ca_decay_rate),
                    self.ca_buffer_depth,
                    self.cai_min)


  def run_sweep(
          self,
          dt: float,
          ext_current: Float[Array, " num_steps"],
          init_v: Scalar) -> Tuple[Float[Array, " num_steps"], CaCompartmentState]:
    """Integrate the model for a sequence of external currents.

    Args:
      dt: The step length in milliseconds.
      ext_current: The external current applied to the compartment in milliamps at each
        timestep, an array of shape [num_steps].
      init_v: The initial resting voltage of the model in millivolts
    Returns:
      vs: The voltages over time
      state: The compartment state over time.
    """
    num_steps = ext_current.shape[0]
    T = dt * (num_steps - 1)
    ts = jnp.linspace(0, T, num=num_steps)
    init_state = self.init_state(init_v)

    def scan_fn(
            prev_state: Tuple[Scalar, CaCompartmentState],
            t_and_i_ext: Tuple[Scalar, Scalar]
            ) -> Tuple[Tuple[Scalar, CaCompartmentState], Tuple[Scalar, CaCompartmentState]]:
      prev_v, prev_comp_state = prev_state
      t, ext_current = t_and_i_ext
      new_state = self.step(dt, t, ext_current, prev_v, prev_comp_state)
      return new_state, new_state

    _, out_states = jax.lax.scan(scan_fn, init_state, (ts, ext_current))
    return out_states


class CaGroupState(NamedTuple):
  channel_state: Float[Array, "num_compartments channel_state_dim"]
  cai: Float[Array, " num_compartments"]


class CaCompartmentGroup(eqx.Module):
  """Compartments with voltage- and calcium-gated ion channels and simple ca dynamics.

  Calcium dynamics are computed using an exponential decay ODE (see ca_decay_rate and cai_min).
  The calcium reversal potential is computed using the Nernst equation.
  """

  num_compartments: int = eqx.static_field()
  temp_celsius: Scalar = eqx.static_field() # Celsius
  channels: ChannelGroup = eqx.static_field()

  cao: Scalar = eqx.static_field() # millimolar
  cai_min: Scalar = eqx.static_field() # millimolar
  ca_buffer_depth: Scalar = eqx.static_field() # micrometers

  surface_area: Float[Array, " num_compartments"] = eqx.static_field() # cm^2

  # Shared across compartments
  specific_membrane_capacitance: Scalar = eqx.static_field() # millifarads / cm^2
  leak_reversal_potential: Scalar = eqx.static_field() # millivolts
  ion_reversal_potentials: Dict[Ion, Scalar] = eqx.static_field() # millivolts

  log_leak_conductance_density: Scalar # seimens / cm^2

  # Per-compartment
  # seimens / cm^2
  log_max_channel_conductance_densities: Float[Array, "num_compartments num_channels"]
  log_ca_decay_rate: Float[Array, " num_compartments"]  # millisecond
  logit_free_ca_perc: Float[Array, " num_compartments"]  # unitless

  def __init__(self,
               num_compartments: int,
               channels: ChannelGroup,
               surface_area: Float[Array, " num_compartments"],
               temp_celsius: float,
               specific_membrane_capacitance: Scalar,
               leak_conductance_density: Scalar,
               leak_reversal_potential: Scalar,
               ion_reversal_potentials: Dict[Ion, Scalar],
               max_channel_conductance_densities: Float[Array, "num_compartments num_channels"],
               cao: float,
               cai_min: float,
               ca_buffer_depth: float,
               ca_decay_rate: float,
               free_ca_perc: float):
    """Create a compartment group with calcium dynamics.

    Args:
      num_compartments: The number of compartments in the group.
      channels: A ChannelGroup containing voltage- and calcium-gated ion channels.
      surface_area: The surface area of each compartment in cm^2, a [num_compartments] array.
      temp_celsius: The temperature in celsius.
      specific_membrane_capacitance: The specific membrane capacitance in millifarads / cm^2,
        shared across all compartments.
      leak_conductance_density: The density of the leak conductance channel in seimens / cm^2,
        shared across all compartments.
      leak_reversal_potential: The reversal potential in millivolts, shared across all
        compartments.
      ion_reversal_potentials: The reversal potentials of each ion in millivolts, shared
        across all compartments.
      max_channel_conductance_densities: The conductance densities of each channel in each
        compartment in seimens / cm^2, an array of shape [num_compartments, num_channels].
      cao: The extracellular calcium concentration in millimolar, shared across all compartments.
      cai_min: The minimum intracellular calcium concentration in millimolar, shared
        across all compartments.
      ca_buffer_depth: The depth of the calcium buffer, in micrometers, shared across
        all compartments.
      ca_decay_rate: The decay rate of calcium in milliseconds.
      free_ca_perc: The percent of free calcium.
    """
    self.num_compartments = num_compartments
    self.temp_celsius = jnp.array(temp_celsius)
    self.surface_area = surface_area
    self.channels = channels
    self.log_max_channel_conductance_densities = jnp.log(max_channel_conductance_densities)
    self.specific_membrane_capacitance = specific_membrane_capacitance
    self.log_leak_conductance_density = jnp.log(leak_conductance_density)
    self.leak_reversal_potential = leak_reversal_potential
    self.ion_reversal_potentials = ion_reversal_potentials
    # Calcium params
    self.cao = jnp.array(cao)
    self.cai_min = jnp.array(cai_min)
    self.ca_buffer_depth = jnp.array(ca_buffer_depth)
    self.log_ca_decay_rate = jnp.log(jnp.full([self.num_compartments], ca_decay_rate))
    self.logit_free_ca_perc = jscipy.special.logit(
            jnp.full([self.num_compartments], free_ca_perc))

  def init_state(
          self,
          v: Union[Scalar, float]
          ) -> Tuple[Float[Array, " num_compartments"], CaGroupState]:
    """Creates a resting state for the compartment group.

    Args:
      v: The resting voltage, in millivolts
    Returns:
      init_vs: The initial voltage of each compartment, an array of shape [num_compartments].
      init_state: The initial state of each compartment, a CaGroupState.
    """
    vs = jnp.full([self.num_compartments], v)
    cais = jnp.full([self.num_compartments], self.cai_min)
    channel_state = self.channels.resting_state(v, self.cai_min)
    channel_state = jnp.tile(channel_state[jnp.newaxis, :], [self.num_compartments, 1])
    return vs, CaGroupState(channel_state=channel_state, cai=cais)

  def step(
          self,
          dt: Union[float, Scalar],
          t: Scalar,
          ext_current: Float[Array, " num_compartments"],
          prev_vs: Float[Array, " num_compartments"],
          prev_state: CaGroupState
          ) -> Tuple[Float[Array, " num_compartments"], CaGroupState]:
    """Integrate the state of the compartment group for one step of size dt.

    Args:
      dt: The stepsize in milliseconds.
      t: The current time in milliseconds.
      ext_current: The external current applied to each compartment in milliamps, an array of
        size num_compartments.
      prev_vs: The voltage in millivolts of each compartment at the previous timestep,
        an array of size num_compartments.
      prev_state: The state of the compartment group at the previous timestep.
    Returns:
      new_voltage: The voltage of each compartment at time t + dt.
      new_state: The compartment group state at time t + dt.
    """
    del t
    # Do a voltage/calcium half step
    E_ca = nernst(self.temp_celsius, prev_state.cai, self.cao)
    v_and_cai_As, v_and_cai_bs = self.voltage_and_cai_dynamics(
            prev_state.channel_state, E_ca, ext_current)
    v_and_cai = jnp.stack([prev_vs, prev_state.cai], axis=1)
    assert v_and_cai.shape == (self.num_compartments, 2)
    new_v_and_cai = jax.vmap(exp_euler_2x2_ltA, in_axes=(None, 0, 0, 0))(
            dt / 2., v_and_cai_As, v_and_cai_bs, v_and_cai)
    new_v, new_cai = new_v_and_cai.T

    # Now do a channel state step
    # (num_compartments, subunit_dim), (num_compartments, subunit_dim)
    channel_state_A_diags, channel_state_bs = jax.vmap(
            self.channels.state_dynamics)(new_v, new_cai)
    new_channel_state = jax.vmap(exp_euler, in_axes=(None, 0, 0, 0))(
            dt, channel_state_A_diags, channel_state_bs, prev_state.channel_state)

    # Now another voltage/calcium step
    E_ca = nernst(self.temp_celsius, new_cai, self.cao)
    v_and_cai_As, v_and_cai_bs =  self.voltage_and_cai_dynamics(
      new_channel_state, E_ca, ext_current)
    new_v_and_cai = jax.vmap(exp_euler_2x2_ltA, in_axes=(None, 0, 0, 0))(
            dt / 2., v_and_cai_As, v_and_cai_bs, new_v_and_cai)
    new_v, new_cai = new_v_and_cai.T
    new_state = CaGroupState(channel_state=new_channel_state, cai=new_cai)
    return new_v, new_state

  def voltage_and_cai_dynamics(
      self,
      channel_state: Float[Array, "num_compartments channel_state_dim"],
      E_ca: Float[Array, " num_compartments"],
      ext_current: Float[Array, " num_compartments"],
      ) -> Tuple[Float[Array, "num_compartments 2 2"], Float[Array, "num_compartments 2"]]:
    """Compute the conditionally linear voltage dynamics for each compartment.

    Args:
      channel_state: The state of the ion channels in each compartment.
      E_ca: The calcium reversal potential in millivolts for each compartment.
      ext_current: The external current applied to each compartment in milliamps.
    Returns:
      A: The [num_compartments, 2, 2] matrix in the system of linear ODEs.
      b: The [num_compartments, 2] drift vector in the system of linear ODEs.
    """
    return jax.vmap(
            voltage_and_cai_dynamics,
            in_axes=(None, None, None, 0, 0, None, 0, 0, None, 0, 0, 0, None, None))(
                    self.leak_reversal_potential,
                    jnp.exp(self.log_leak_conductance_density),
                    self.specific_membrane_capacitance,
                    ext_current,
                    self.surface_area,
                    self.channels,
                    jnp.exp(self.log_max_channel_conductance_densities),
                    channel_state,
                    self.ion_reversal_potentials,
                    E_ca,
                    jax.nn.sigmoid(self.logit_free_ca_perc),
                    jnp.exp(self.log_ca_decay_rate),
                    self.ca_buffer_depth,
                    self.cai_min)
