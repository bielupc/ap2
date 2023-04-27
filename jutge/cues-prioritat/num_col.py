import yogi as yg
import heapq
import fileinput


def procesar_comanda(comanda: str, data: list[int]) -> None:
  """
  Donada una linia de comandes, S(store), A(ask for greatest), R(remove greatest), I(increase greatest) o D(decrease greatest), les executa i imprimeix l'element màxim. Si no es possible, imprimeix un error.
  """

  heapq._heapify_max(data)

  if comanda == "S":
    n = yg.read(int)
    heapq.heappush(data, n)

  elif comanda == "A":
    if len(data) == 0:
      print("error!")
    else:
      print(heapq.nlargest(1,data)[0])

  elif comanda == "R":
    if len(data) == 0:
      print("error!")
    else:
      heapq.heappop(data)
  
  elif comanda == "I":
    if len(data) == 0:
      print("error!")
    else:
      n = yg.read(int)
      max_heap = heapq.nlargest(1,data)[0]
      heapq.heappop(data)
      heapq.heappush(data, max_heap+n)

  elif comanda == "D":
    if len(data) == 0:
      print("error!")
    else:
      n = yg.read(int)
      max_heap = heapq.nlargest(1,data)[0]
      heapq.heappop(data)
      heapq.heappush(data, max_heap-n)


def main() -> None:
  data: list[int] = list()

  for comanda in yg.tokens(str):
    procesar_comanda(comanda, data)

if __name__ == "__main__":
  main()