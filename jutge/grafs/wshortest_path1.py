from yogi import read, scan, tokens
import heapq


def dijkstra(G: dict[int, dict[int, int]], s: int) -> dict[int, int]:
  dist: dict[int, int] = {node: 1000000 for node in G.keys()}
  prev: dict[int, int] = {node: 0 for node in G.keys()}

  dist[s] = 0

  Q = [(0, s)]

  while Q:
    current_dist, current_node = heapq.heappop(Q)

    if current_dist > dist[current_node]:
      continue

    for neighbor, weight in G[current_node].items():
      distance = current_dist + weight

      if distance < dist[neighbor]:
        dist[neighbor] = distance
        heapq.heappush(Q, (distance, neighbor))
  return dist




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

    dist = dijkstra(G, x)[y]
    print(dist) if dist != 1000000 else print(f"no path from {x} to {y}")


    n = scan(int)


if __name__ == "__main__":
  main()