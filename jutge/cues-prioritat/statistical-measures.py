import yogi as yg
import heapq

def processa_comanda(comanda: str, data: list[int], max_: int, sum_: int, count_: int) -> tuple[bool, int, int, int, int]:
  if comanda == "delete":
    if len(data) != 0:
      least = data[0]
      heapq.heappop(data)
      min_ = data[0] if len(data) > 0 else 0
      return len(data) == 0, min_, max_, sum_ - least, count_ - 1
    else:
      return False, 0, 0, 0, 0
  else:
    n = yg.read(int)
    if len(data) == 0:
      max_ = n

    heapq.heappush(data, n)
    max_ = max_ if max_ > n else n
    return False, data[0], max_, sum_ + n, count_ + 1
   

def main() -> None:
  data: list[int] = list()
  sum_ = 0
  count_ = 0
  max_ = 0
  for comanda in yg.tokens(str):
    buida, min_, max_, sum_, count_ = processa_comanda(comanda, data, max_, sum_, count_)
    if not buida:
      print(f'minimum: {min_}, maximum: {max_}, average: {sum_ / count_:.4f}')
    else:
      print("no elements")


if __name__ == "__main__":
  main()