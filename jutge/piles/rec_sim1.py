from yogi import tokens

def work(n: int) -> None:
  pila: list[tuple[int, str]] = list()
  resultat: list[int] = list()

  pila.append((n, "call"))

  while len(pila) > 0:
    num, action = pila.pop()
    if action == "call":
      if num == 1:
        resultat.append(num)
      else:
        pila.append((num, "end"))
        pila.append((num-1, "call"))
        pila.append((num-1, "call"))
    else:
      resultat.append(num)
  
  while len(resultat) > 0:
    print(" ", resultat[-1], end="", sep="")
    resultat.pop()

def main() -> None:
  for n in tokens(int):
    work(n)
    print()

main()