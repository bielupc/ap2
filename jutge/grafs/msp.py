from yogi import read, scan, tokens
import heapq


def mst(G: dict[int, dict[int, int]], s: int) -> None:

  visited: dict[int, bool] = {node: False for node in G.keys()}
  visited[s] = True
  prev: dict[int, int] = dict()
  Q: list[tuple[int, int, int]] = list()

  for u in G[s]:
    heapq.heappush(Q, (G[s][u],s, u))

  while Q:
    weight, u, v = heapq.heappop(Q)
    if not visited[v]:
      visited[v] = True
      prev[v] = u
      
      for node in G[v]:
        if not visited[node]: 
          heapq.heappush(Q, (G[v][node], v, node))

  return prev 




def main() -> None:
  n = scan(int)

  while n is not None:
    m = read(int)
    G: dict[int, dict[int, int]] = {i: {} for i in range(1, m+1)}
    for _ in range(1, m+1):
      u = read(int)
      v = read(int)
      G[u][v] = read(int)
    print(mst(G, v))
    n = scan(int)


if __name__ == "__main__":
  main()