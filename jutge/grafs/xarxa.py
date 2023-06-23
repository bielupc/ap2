from yogi import read, scan, tokens
import heapq
import collections


def bfs(G: dict[str, list[str]], s: str, k: int) -> int:

  counter = 0
  dst = 0

  visited = {node: False for node in G}

  Q = collections.deque([(s, 0)])
  visited[s] = True

  while Q:
    u, dist = Q.popleft()

    if dist == k:
      counter  += 1
    
    if dist > k:
      break

    for v in G[u]:
      if not visited[v]:
        visited[v] = True
        Q.append((v, dist+1))
  return counter


def main() -> None:
  n = read(int)
  m = read(int)

  G: dict[str, list[str]] = dict()

  for _ in range(n):
    G[read(str)] = list()

  for _ in range(m):
    u = read(str)
    v = read(str)
    G[u].append(v)
  
  for name in tokens(str):
    k = read(int)
    if k == 0:
      print(1)
    else:
      print(bfs(G, name, k))


if __name__ == "__main__":
  main()