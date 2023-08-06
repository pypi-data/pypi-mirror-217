from typing import Dict, List, Tuple, Set

Graph = Dict[int, List[int]]


def collapse_tree(tree: Graph, root_id: int) -> Tuple[List[List[int]], Graph]:
  """Transforms tree by combining unbranched chains of nodes.

  Args:
    tree: The tree to transform
    root_id: The id of the tree root node.

  Returns:
    chains: A list of nodes in the new tree. Each node is made up of a list of nodes in the
      previous tree. The id of each node is indicated by its position in the list.
    chain_tree: The new tree, with node ids as indicated in chains.
  """
  if len(tree) == 0:
    return [[root_id]], {}

  assert root_id in tree
  chains = [[root_id]]
  chain_tree = {}
  to_expand = [(int(0), x) for x in tree[root_id]]
  while len(to_expand) > 0:
    parent_chain_id, cur_chain_start_id = to_expand.pop()
    cur_chain_id = len(chains)
    cur_chain = [cur_chain_start_id]
    while cur_chain[-1] in tree and len(tree[cur_chain[-1]]) == 1:
      cur_chain.append(tree[cur_chain[-1]][0])
    chains.append(cur_chain)
    if parent_chain_id in chain_tree:
      chain_tree[parent_chain_id].append(cur_chain_id)
    else:
      chain_tree[parent_chain_id] = [cur_chain_id]
    if cur_chain[-1] in tree:
      to_expand.extend([(cur_chain_id, x) for x in tree[cur_chain[-1]]])
  return chains, chain_tree


def node_list(graph: Graph) -> Set[int]:
  """Get the set of all node ids in a graph."""
  nodes = set([])
  for p, cs in graph.items():
    nodes.add(p)
    nodes.update(cs)
  return nodes


def edge_list(graph: Graph) -> List[Tuple[int, int]]:
  """Get the list of all edges in a graph."""
  edges: List[Tuple[int, int]] = []
  for p, cs in graph.items():
    for c in cs:
      edges.append((p, c))
  return edges


def has_cycle_dfs(node: int, parent: int, graph: Graph, visited: Dict[int, bool]) -> bool:
  """Helper function for detecting whether a graph has a cycle using depth-first search."""
  visited[node] = True
  if node in graph: # Only visit neighbors if there are any
    for neighbor in graph[node]:
      if not visited[neighbor]:
        if has_cycle_dfs(neighbor, node, graph, visited):
          return True
      elif neighbor != parent:
        return True
  return False


def assert_is_connected_tree(graph: Graph, root_id: int):
  """Checks if a graph is a connected tree."""
  if len(graph) == 0:
    return
  nodes = node_list(graph)
  edges = edge_list(graph)
  assert len(edges) == len(nodes) - 1, \
          "Number of edges must equal number of nodes - 1 to be a connected tree."
  assert len(set(edges)) == len(edges), "Cannot have duplicate edges."

  visited = {i: False for i in nodes}
  has_cycle = has_cycle_dfs(root_id, -1, graph, visited)
  assert not has_cycle, "Graph has a cycle."
  assert all(visited.values()), "Graph is not connected."
