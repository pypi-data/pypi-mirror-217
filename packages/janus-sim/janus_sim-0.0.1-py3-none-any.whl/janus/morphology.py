from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Optional, List, Tuple, Dict
from functools import cached_property, cache
from jaxtyping import Float
import numpy as np

from janus.graph_util import Graph, collapse_tree, assert_is_connected_tree
from janus.graphics_util import circle


class MorphologyTreeNode(ABC):

  def __init__(self,
               group_name: str,
               children: Optional[List[Neurite]] = None):
    self.group_name = group_name
    if children is not None:
      self._children = children
    else:
      self._children: List[Neurite] = []

  @property
  def children(self) -> List[Neurite]:
    return self._children

  @abstractmethod
  def surface_area(self) -> float:
    raise NotImplementedError

  @abstractmethod
  def center(self) -> Float[np.ndarray, "3"]:
    raise NotImplementedError

  @abstractmethod
  def bounding_box(self) -> Tuple[Float[np.ndarray, " 3"], Float[np.ndarray, " 3"]]:
    raise NotImplementedError

  @abstractmethod
  def resistance(self, a: float, b: float, resistivity: float) -> float:
    raise NotImplementedError

  @abstractmethod
  def __hash__(self) -> int:
    raise NotImplementedError

  @abstractmethod
  def __eq__(self, other) -> bool:
    raise NotImplementedError

  def connect(self, other: Neurite):
    if other in self.children:
      raise ValueError("Cannot connect a child to a parent multiple times.")
    if other == self:
      raise ValueError("Cannot connect a neurite to itself.")
    self.children.append(other)
    other.parent = self

  def disconnect(self, child: Neurite):
    if child not in self.children:
      raise ValueError("Cannot disconnect sections that aren't connected.")
    self.children.remove(child)
    child.parent = None

  def sections(self) -> Iterator[MorphologyTreeNode]:
    for child in self.children:
      yield from child.sections()
    yield self


DEFAULT_GROUP_NAME = "neurite"


class Neurite(MorphologyTreeNode):

  cached_attrs = ["pts", "rads", "normals", "arclens", "length",
                  "surface_area", "bounding_box", "center"]

  def __init__(self,
               pts: Float[np.ndarray, " num_points, 3"],
               rads: Float[np.ndarray, " num_points"],
               group_name: Optional[str] = None):
    if pts.shape[0] != rads.shape[0]:
      raise ValueError("Points and radii must have same leading shape.")
    self._inner_pts: Float[np.ndarray, " num_points 3"] = pts
    self._inner_pts.flags.writeable = False
    self._inner_rads: Float[np.ndarray, " num_points"] = rads
    self._inner_rads.flags.writeable = False
    self._parent: Optional[MorphologyTreeNode] = None
    if group_name is None:
      group_name = DEFAULT_GROUP_NAME
    super().__init__(group_name, children=None)

  @cached_property
  def pts(self) -> Float[np.ndarray, " num_points 3"]:
    if self.parent is not None and isinstance(self.parent, Neurite):
      return np.concatenate([self.parent.pts[-1][np.newaxis], self._inner_pts])
    return self._inner_pts

  @cached_property
  def rads(self) -> Float[np.ndarray, " num_points"]:
    if self.parent is not None and isinstance(self.parent, Neurite):
      return np.concatenate([self.parent.rads[-1][np.newaxis], self._inner_rads])
    return self._inner_rads

  @property
  def parent(self) -> Optional[MorphologyTreeNode]:
    return self._parent

  @parent.setter
  def parent(self, parent: Optional[MorphologyTreeNode]):
    self._parent = parent
    self._expire_pts_cache()

  def _expire_pts_cache(self):
    for attr in Neurite.cached_attrs:
      if attr in self.__dict__:
        delattr(self, attr)

  @cache
  def surface_area(self) -> float:
    """The total surface area of cable in this section, in micrometers^2."""
    sa = 0.
    for ((pt1, pt2), (r1, r2)) in zip(zip(self.pts[:-1], self.pts[1:]),
                                      zip(self.rads[:-1], self.rads[1:])):
      h = np.linalg.norm(pt2 - pt1)
      c1 = 2 * np.pi * r1
      c2 = 2 * np.pi * r2
      l = np.sqrt(np.square(r2 - r1) + np.square(h))
      sa += 0.5 * (c1 + c2) * l
    return sa

  @cache
  def center(self) -> Float[np.ndarray, "3"]:
    return self.at(0.5)[0]

  @cache
  def normals(self) -> List[Float[np.ndarray, " 3"]]:
    if self.pts.shape[0] == 1:
      raise ValueError("normals are undefined for neurite with only one point.")
    res = []
    for beg, end in zip(self.pts[:-1], self.pts[:1]):
      vec = end - beg
      res.append(vec / np.linalg.norm(vec))
    # The last entry is duplicated
    res.append(res[-1])
    return res

  @cache
  def bounding_box(self) -> Tuple[Float[np.ndarray, " 3"], Float[np.ndarray, " 3"]]:
    if self.pts.shape[0] == 1:
      raise ValueError("bounding_box is undefined for neurite with only one point.")
    resolution = 10
    pts = []
    for center, normal, rad in zip(self.pts, self.normals(), self.rads):
      pts.append(circle(center, normal, rad, resolution))
    pts = np.concatenate(pts, axis=0)
    min_pt = np.min(pts, axis=0)
    max_pt = np.max(pts, axis=0)
    return min_pt, max_pt

  @cache
  def arclens(self) -> Float[np.ndarray, "num_points"]:
    """Return the arclength of each point in the cable."""
    if self.pts.shape[0] == 1:
      raise ValueError("arclens is undefined for neurite with only one point.")
    norms = np.linalg.norm(self.pts[1:] - self.pts[:-1], axis=1)
    tot_norm = np.sum(norms)
    norms = np.pad(norms, (1, 0))
    arclens = np.cumsum(norms) / tot_norm
    return arclens

  @cache
  def length(self) -> float:
    """The total length of cable in this section, in micrometers."""
    norms = np.linalg.norm(self.pts[1:] - self.pts[:-1], axis=1)
    tot_norm = np.sum(norms)
    return tot_norm

  def at(self, arclen: float) -> Tuple[Float[np.ndarray, "3"], Float[np.ndarray, ""]]:
    if self.pts.shape[0] == 1:
      raise ValueError("Cannot index into neurite with only one point.")
    if arclen < 0. or arclen > 1.:
        raise IndexError(f"Arclength {arclen} must be in interval [0, 1]")
    x = np.interp(arclen, self.arclens(), self.pts[:,0])
    y = np.interp(arclen, self.arclens(), self.pts[:,1])
    z = np.interp(arclen, self.arclens(), self.pts[:,2])
    r = np.interp(arclen, self.arclens(), self.rads)
    return np.array([x, y, z]), r

  def slice(
        self,
        from_arclen: float,
        to_arclen: float,
        include_from: bool = True,
        include_to: bool = True,
        ) -> Tuple[Float[np.ndarray, "num_compartments 3"],
                   Float[np.ndarray, " num_compartments"]]:
    if self.pts.shape[0] == 1:
      raise ValueError("Cannot slice neurite with only one point.")
    if from_arclen < 0. or from_arclen > 1.:
      raise IndexError(f"Starting arclen ({from_arclen}) must be in interval [0, 1].")
    if to_arclen < 0. or to_arclen > 1.:
      raise IndexError(f"Stop arclen ({to_arclen}) must be in interval [0, 1]")
    if from_arclen >= to_arclen:
      raise IndexError(
              f"Start arclen ({from_arclen}) must be less than stop arclen ({to_arclen}).")

    pts_list = []
    rad_list = []

    if include_from:
      start_pt, start_rad = self.at(from_arclen)
      pts_list.append(start_pt)
      rad_list.append(start_rad)

    # np.where returns a tuple of length 1
    mid_inds = np.where(
            np.logical_and(self.arclens() > from_arclen, self.arclens() < to_arclen))[0]
    if len(mid_inds) > 0:
      pts_list.extend(self.pts[ind] for ind in mid_inds)
      rad_list.extend(self.rads[ind] for ind in mid_inds)

    if include_to:
      end_pt, end_rad = self.at(to_arclen)
      pts_list.append(end_pt)
      rad_list.append(end_rad)

    if len(pts_list) == 0 and len(rad_list) == 0:
      return np.empty([0, 3]), np.empty([0])
    else:
      return np.array(pts_list), np.array(rad_list)

  def resistance(self, from_arclen: float, to_arclen: float, resistivity: float) -> float:
    """The resistance between two arclengths in TODO: units."""
    if self.pts.shape[0] == 1:
      raise ValueError("Cannot compute resistance of neurite with only one point.")
    pts, rs = self.slice(from_arclen, to_arclen, include_from=True, include_to=True)
    resistance = 0.
    for i in range(len(pts) - 1):
      l = np.linalg.norm(pts[i + 1] - pts[i])
      resistance += resistivity * (l / (np.pi * rs[i] * rs[i + 1]))
    return resistance

  def __hash__(self) -> int:
    return hash((self._inner_pts.tobytes(),
                 self._inner_rads.tobytes(),
                 self.group_name))

  def __eq__(self, other) -> bool:
    if (isinstance(other, self.__class__) and
        np.array_equal(self._inner_pts, other._inner_pts) and
        np.array_equal(self._inner_rads, other._inner_rads) and
        self.group_name == other.group_name):
      return True
    return False

  def sections(self) -> Iterator[Neurite]:
    yield self
    for child in self.children:
      yield from child.sections()

  def split(self, at_arclen: float) -> Tuple[Neurite, Neurite]:
    if at_arclen <= 0. or at_arclen >= 1.:
      raise ValueError(f"Split location ({at_arclen}) must be > 0 and < 1.")
    if self.parent is None:
      pts1, rs1 = self.slice(0., at_arclen, include_from=True, include_to=True)
    else:
      pts1, rs1 = self.slice(0., at_arclen, include_from=False, include_to=True)

    pts2, rs2 = self.slice(at_arclen, 1., include_from=False, include_to=True)
    n1 = Neurite(pts=pts1, rads=rs1, group_name=self.group_name)
    n2 = Neurite(pts=pts2, rads=rs2, group_name=self.group_name)
    n1.connect(n2)

    if self.parent is not None:
      self.parent.connect(n1)
      self.parent.disconnect(self)

    for child in self.children:
      n2.connect(child)

    self._children = []
    return n1, n2

  def merge(self) -> Neurite:
    if len(self.children) > 1:
      raise ValueError("Cannot merge section with more than one child.")
    elif len(self.children) == 0:
      raise ValueError("Cannot merge section with no children.")

    child = self.children[0]
    new_pts = np.concatenate([self._inner_pts, child._inner_pts])
    new_rs = np.concatenate([self._inner_rads, child._inner_rads])
    new_neurite = Neurite(pts=new_pts, rads=new_rs, group_name=self.group_name)

    if self.parent is not None:
      self.parent.connect(new_neurite)
      self.parent.disconnect(self)

    self.disconnect(child)

    for c in child.children:
      new_neurite.connect(c)

    self._children = []
    child._children = []
    return new_neurite

  def neurites(self) -> Iterator[Neurite]:
    for child in self.children:
      yield from child.neurites()
    yield self


class Soma(MorphologyTreeNode):

  def __init__(self,
               center: Float[np.ndarray, " 3"],
               radius: float):
    if center.shape != (3,):
      raise ValueError("Center must be array of shape (3,).")
    self._center = center
    self._center.flags.writeable = False
    self._radius = radius
    super().__init__("soma", children=None)

  def surface_area(self) -> float:
    """Surface area of the cylinder representing the soma, in micrometers squared."""
    return 4 * np.pi * np.square(self._radius)

  def center(self) -> Float[np.ndarray, " 3"]:
    return self._center

  def radius(self) -> float:
    return self._radius

  def resistance(self, from_arclen: float, to_arclen: float, resistivity: float) -> float:
    length = np.abs(from_arclen - to_arclen) * self._radius
    area = np.pi * np.square(self._radius)
    return resistivity * (length / area)

  def bounding_box(self) -> Tuple[Float[np.ndarray, " 3"], Float[np.ndarray, " 3"]]:
    return self._center - self._radius, self._center + self._radius

  def __hash__(self) -> int:
    return hash((self._center.tobytes(), self._radius))

  def __eq__(self, other) -> bool:
    if (isinstance(other, self.__class__) and
        np.array_equal(self._center, other._center) and
        self._radius == other._radius):
      return True
    return False

  def neurites(self) -> Iterator[Neurite]:
    for child in self.children:
      yield from child.neurites()


STANDARD_GROUP_NAMES = {
    1: "soma",
    2: "axon",
    3: "basal_dendrite",
    4: "apical_dendrite"
}


def get_group_name(ind: int) -> str:
  if ind in STANDARD_GROUP_NAMES:
    return STANDARD_GROUP_NAMES[ind]
  else:
    return f"group_{ind}"


def parse_swc(filename: str
              ) -> Tuple[Dict[int, Tuple[int, float, float, float, float]], Graph, int]:
  nodes = {}
  tree = {}
  soma_id = None
  with open(filename, "r") as f:
    for line in f.readlines():
      l = line.strip()
      # Comment
      if l[0] == "#": continue
      id_, struct_id, x, y, z, r, parent_id = l.split()
      id_ = int(id_)
      struct_id = int(struct_id)
      x = float(x)
      y = float(y)
      z = float(z)
      r = float(r)
      parent_id = int(parent_id)
      assert id_ not in nodes
      nodes[id_] = (struct_id, x, y, z, r)
      if struct_id == 1: # We found the soma
        assert soma_id is None, "Multiple soma entries found."
        soma_id = id_
      else:
        assert parent_id in nodes
        if parent_id not in tree:
          tree[parent_id] = [id_]
        else:
          tree[parent_id].append(id_)
  assert soma_id is not None, "Soma not found"
  assert_is_connected_tree(tree, soma_id)
  return nodes, tree, soma_id


class Morphology:

  def __init__(self, soma: Soma):
    self.soma = soma

  @classmethod
  def from_swc(cls, filename: str) -> Morphology:
    nodes, tree, soma_id = parse_swc(filename)
    chains, chain_graph = collapse_tree(tree, soma_id)
    # Check that all chains have the same structure id
    for chain in chains:
      struct_ids = [nodes[x][0] for x in chain]
      si = struct_ids[0]
      assert all([x == si for x in struct_ids])
    # Construct the compartment tree
    soma_center = np.array(nodes[soma_id][1:4])
    soma_rad = nodes[soma_id][4]
    soma = Soma(soma_center, soma_rad)
    morphology = Morphology(soma)
    assert [soma_id] in chains
    if len(chains) == 1:
      return morphology
    soma_chain_id = chains.index([soma_id])
    frontier: List[Tuple[MorphologyTreeNode, List[int]]] = []
    frontier.extend((soma, chains[i]) for i in chain_graph[soma_chain_id])
    while len(frontier) > 0:
      parent, child_chain = frontier.pop()
      # Construct the new section
      pts = np.array([nodes[i][1:4] for i in child_chain])
      rads = np.array([nodes[i][4] for i in child_chain])
      group_name = get_group_name(nodes[child_chain[0]][0])
      child = Neurite(pts=pts, rads=rads, group_name=group_name)
      parent.connect(child)
      child_chain_ind = chains.index(child_chain)
      if child_chain_ind in chain_graph:
        frontier.extend((child, chains[i]) for i in chain_graph[child_chain_ind])
    return morphology

  def bounding_box(self) -> Tuple[Float[np.ndarray, " 3"], Float[np.ndarray, " 3"]]:
    min_pt = np.full([3], np.inf)
    max_pt = np.full([3], -np.inf)
    for sec in self.soma.sections():
      bb_min, bb_max = sec.bounding_box()
      min_pt = np.minimum(min_pt, bb_min)
      max_pt = np.maximum(max_pt, bb_max)
    return min_pt, max_pt

  def total_length(self) -> float:
    length = 0.
    for n in self.soma.neurites():
      length += n.length()
    return length

  def total_surface_area(self) -> float:
    sa = 0.
    for sec in self.soma.sections():
      sa += sec.surface_area()
    return sa

  def num_sections(self) -> int:
    num_sections = 0
    for _ in self.soma.sections():
      num_sections += 1
    return num_sections

  def num_points(self) -> int:
    num_points = 1
    for sec in self.soma.neurites():
      num_points += sec._inner_pts.shape[0]
    return num_points

  def check(self):
    pass
