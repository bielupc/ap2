from yogi import read, scan, tokens
from  dataclasses import dataclass
import math
from collections import deque



@dataclass(frozen=True)
class Roca:
  x: float 
  y: float 
  r: float
  _id: int

def explore(adj: dict[int, list[int]], v: int, cc: dict[int, int], ccnum: int) -> None:
    """
        Donat la llista d'adjacència d'un graf, coloca ccnum a les posicions de cc referents a nodes visitables desde v.
    """
    cc[v] = ccnum
    for u in adj[v]:
        if cc[u] == 0:
            explore(adj, u, cc, ccnum)


def connected_components(adj: dict[int, list[int]]) ->dict[int, int]:
    """Donada la llista d'adjacència d'un graf, retorna les seves components conectades en forma de diccionari (node, ccnum).""" 
    cc = {node: 0 for node in adj.keys()}
    ccnum = 1

    for node in adj.keys():
        if cc[node] == 0:
            explore(adj, node, cc, ccnum)
            ccnum+=1
    
    return cc

def distance(r1: Roca, r2: Roca) -> float:
  """Returns the distance between the arcs of two circumferences."""
  return math.sqrt((r2.x  - r1.x) ** 2 + (r2.y - r1.y) ** 2) - r1.r - r2.r

def create_graph(roques: list[Roca], d: float) -> dict[int, list[int]]:
  """Returns the adjacency list of the walkable graph."""
  adj: dict[int, list[int]] = {roca._id: list() for roca in roques}

  for v in roques:
    for u in roques:
      if v != u and distance(v, u) < d:

        adj[v._id].append(u._id)
  return adj

def bfs(adj: dict[int, list[int]], s: int, dist: dict[int, int]) -> dict[int, int]:
  dist[s] = 0
  Q: list[int] = [s]

  while len(Q) > 0:
    u = Q.pop(0)
    for v in adj[u]:
      if dist[v] == -1:
        dist[v] = dist[u] + 1
        Q.append(v)
  
  return dist


def find_path(roques: list[Roca], d: float) -> str | int:
  """Returns if it's possible to go from the first rock to the last one."""
  adj = create_graph(roques, d)
  # cc = connected_components(adj)

  # if cc[roques[0]._id] != cc[roques[-1]._id]:
    # return "Xof!"
  # else:
  dist = {node: -1 for node in adj.keys()}
  steps = bfs(adj,0, dist)[roques[-1]._id]
  return steps if steps != -1 else "Xof!"



  



def main() -> None:
  n = scan(int)
  roques: list[Roca] = list()

  while n is not None:
    d = read(float)
    for i in range(n):
      roques.append(Roca(read(float), read(float), read(float), i))
    print(find_path(roques, d))
    roques.clear()
    n = scan(int)






if __name__ == "__main__":
  main()