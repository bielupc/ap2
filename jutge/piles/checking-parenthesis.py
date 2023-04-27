import yogi as yg


def familia(par: str) -> int:
  """"Retorna el tipus de parèntesi"""
  if par == "(" or par == ")":
    return 1
  else:
    return 2


def es_correcta(paraula: str) -> bool:
  """Ens diu si la paraula té una paranterització correcta."""
  pila: list[str] = list()
  for p in paraula:
    if p == "(" or p == "[":
      pila.append(p)
    elif p == ")" or p == "]":
      ultim = pila[-1]
      pila.pop()
      if familia(p) != familia(ultim):
        return False
  return len(pila) == 0


def main() -> None:
  for paraula in yg.tokens(str):
    if es_correcta(paraula):
      print(paraula, "is correct")
    else:
      print(paraula, "is incorrect")


if __name__ == "__main__":
  main()