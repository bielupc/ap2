from yogi import read, scan, tokens
import heapq
from typing import Union

def h(node, target):
  return 1


def astar(G: dict[int, dict[int, int]], s: int, t: int) -> list[int] | None:
  Q: list[Union[tuple[int, int]]] = [(0, s)]
  prev: dict[int, int] = dict()
  g = {node: float('inf') for node in G}
  g[s] = 0
  f = {node: float('inf') for node in G}
  f[s] = h(s, t)

  while Q:
      current_fscore, current_node = heapq.heappop(Q)

      if current_node == t:
          return reconstruct_path(prev, current_node)

      for neighbor, weight in G[current_node].items():
        tentative_gscore = g[current_node] + weight

        if tentative_gscore < g[neighbor]:
          prev[neighbor] = current_node
          print(current_node)
          g[neighbor] = tentative_gscore
          f[neighbor] = tentative_gscore + h(neighbor, t)
          heapq.heappush(Q, (f[neighbor], neighbor))

  return None 

def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)

    path.reverse()
    return path


def main() -> None:
  n = scan(int)
  while n is not None:
    G: dict[int, dict[int, int]] = {node: dict() for node in range(n)}
    m = read(int)
    for _ in range(m):
      i = read(int)
      j = read(int)
      G[i][j] = read(int)
    x = read(int)
    y = read(int)

    path = astar(G, x, y)
    print(*path) if path is not None else print(f"no path from {x} to {y}")
    G.clear()
    n = scan(int)


if __name__ == "__main__":
  main()