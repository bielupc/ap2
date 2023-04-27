import fileinput


def operate(pila: list[int], operator: str) -> None:
  """Modifica la pila segons l'operador adequat."""
  result = eval(f"pila[-2] {operator} pila[-1]")
  for _ in range(2):
    pila.pop()
  pila.append(result)



def main() -> None:
  for line in fileinput.input():
    pila: list[int] = list()
    for word in line.split():
      if word == "+" or word == "-" or word == "*":
        operate(pila, word)
      else:
        pila.append(int(word))
    print(pila[0])
      

if __name__ == "__main__":
  main()