from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from math import ceil
from jaxtyping import Float
import numpy as np
from typing import Callable, Union, Tuple, List, Dict
from janus.morphology import Morphology, Neurite, Soma, MorphologyTreeNode


@dataclass
class CompartmentSpec:

  layout_id: int
  neurite: MorphologyTreeNode
  start_arclen: float
  end_arclen: float

  def resistance(self,
                 from_arclen: float,
                 to_arclen: float,
                 resistivity: float) -> float:
    a = self.start_arclen + (self.end_arclen - self.start_arclen) * from_arclen
    b = self.start_arclen + (self.end_arclen - self.start_arclen) * to_arclen
    return self.neurite.resistance(a, b, resistivity)

  @cached_property
  def center(self) -> Float[np.ndarray, " 3"]:
    if isinstance(self.neurite, Neurite):
      pts, rads = self.neurite.slice(self.start_arclen, self.end_arclen)
      return Neurite(pts, rads).center()
    elif isinstance(self.neurite, Soma):
      return self.neurite.center()
    else:
      assert False, f"Weird neurite type ({self.neurite.__class__}) for compartment."

  @cached_property
  def surface_area(self) -> float:
    if isinstance(self.neurite, Neurite):
      pts, rads = self.neurite.slice(self.start_arclen, self.end_arclen)
      return Neurite(pts, rads).surface_area()
    elif isinstance(self.neurite, Soma):
      return self.neurite.surface_area()
    else:
      assert False, f"Weird neurite type ({self.neurite.__class__}) for compartment."


Node = Union[CompartmentSpec, int]


@dataclass
class Edge:

  src: Node
  dst: Node

  def __post_init__(self):
    assert isinstance(self.src, CompartmentSpec) or isinstance(self.dst, CompartmentSpec), \
            "Cannot have edge between two junction nodes (int values)."

  def resistance(self, resistivity_map: Dict[str, float]) -> float:
    r = 0.
    if isinstance(self.src, CompartmentSpec) and self.src.neurite.group_name is not None:
      r += self.src.resistance(0.5, 1., resistivity_map[self.src.neurite.group_name])
    if isinstance(self.dst, CompartmentSpec) and self.dst.neurite.group_name is not None:
      r += self.dst.resistance(0., 0.5, resistivity_map[self.dst.neurite.group_name])
    return r


DiscretizationStrategy = Callable[[Neurite], Float[np.ndarray, " num_compartments"]]


def num_compartments_strategy(num_compartments: int) -> DiscretizationStrategy:
  if num_compartments <= 0:
    raise ValueError(f"num_compartments ({num_compartments}) must be at least 1.")
  return lambda _: np.linspace(0., 1., num=num_compartments + 1)[1:-1]


def max_length_strategy(max_length_mm: float) -> DiscretizationStrategy:

  def strat(neurite: Neurite) -> Float[np.ndarray, " num_compartments"]:
    num_comps = ceil(neurite.length() / max_length_mm)
    return num_compartments_strategy(num_comps)(neurite)

  return strat


@dataclass
class DiscretizedMorphology:

  morphology: Morphology
  compartments: List[CompartmentSpec]
  edges: List[Edge]
  num_junction_nodes: int
  group_compartments: Dict[str, List[CompartmentSpec]]
  neurite_compartments: Dict[MorphologyTreeNode, List[CompartmentSpec]]

  def __init__(self,
               morphology: Morphology,
               disc_strat: DiscretizationStrategy):
    self.morphology = morphology
    # Will store all compartments in a mapping from group name to list
    group_compartments: Dict[str, List[CompartmentSpec]] = {}
    edges: List[Edge] = []
    # The frontier will store unexpanded nodes.
    frontier: List[Tuple[Node, Neurite]] = []
    cur_junc_id = 0
    # First, generate the somal compartment. This is always a single compartment.
    soma_comp = CompartmentSpec(
            layout_id=-1, neurite=morphology.soma, start_arclen=0., end_arclen=1.)
    group_compartments["soma"] = [soma_comp]
    # Add all the soma's children to the frontier
    for neurite in morphology.soma.children:
      frontier.append((soma_comp, neurite))

    while len(frontier) > 0:
      (parent_comp, neurite) = frontier.pop()
      # Ensure the neurite group is in the component dictionary
      assert neurite.group_name is not None
      if neurite.group_name not in group_compartments:
        group_compartments[neurite.group_name] = []
      # Discretize
      partition = disc_strat(neurite)
      partition = np.concatenate([np.array([0.]), partition, np.array([1.])])
      for start_arclen, end_arclen in zip(partition[:-1], partition[1:]):
        new_comp = CompartmentSpec(
                layout_id=-1,
                neurite=neurite,
                start_arclen=start_arclen,
                end_arclen=end_arclen)
        group_compartments[neurite.group_name].append(new_comp)
        edges.append(Edge(parent_comp, new_comp))
        parent_comp = new_comp
      last_comp = parent_comp
      # If there is more than one child, add a junction node.
      if len(neurite.children) > 1:
        edges.append(Edge(last_comp, cur_junc_id))
        for child in neurite.children:
          frontier.append((cur_junc_id, child))
        cur_junc_id += 1
      # Otherwise, no junction node.
      elif len(neurite.children) == 1:
        frontier.append((last_comp, neurite.children[0]))

    # Layout the nodes so that nodes from the same group are contiguous.
    self.compartments: List[CompartmentSpec] = []
    self.edges = edges
    self.num_junction_nodes = cur_junc_id
    self.group_compartments = group_compartments
    self.neurite_compartments: Dict[MorphologyTreeNode, List[CompartmentSpec]] = {}

    for _, group_comps in self.group_compartments.items():
      for comp in group_comps:
        comp.layout_id = len(self.compartments)
        self.compartments.append(comp)
        if comp.neurite not in self.neurite_compartments:
          self.neurite_compartments[comp.neurite] = []
        self.neurite_compartments[comp.neurite].append(comp)

    # Check that things are laid out properly
    for i, comp in enumerate(self.compartments):
      assert i == comp.layout_id
      assert comp.neurite in self.neurite_compartments
      assert comp in self.neurite_compartments[comp.neurite]
      if isinstance(comp.neurite, Neurite):
        assert comp.neurite.group_name in self.group_compartments
        assert comp in self.group_compartments[comp.neurite.group_name]
    assert len(self.group_compartments["soma"]) == 1
    assert soma_comp in self.group_compartments["soma"]
    assert self.compartments[0] == soma_comp
    assert soma_comp.layout_id == 0
