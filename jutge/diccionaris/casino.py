import yogi as yg

def gestionar_comanda(nom: str, comanda: str, data: dict[str, int]) -> None:
  """
  A partir d'un nom i una instrucció, executa l'instrucció si pot
  i guarda els canvis en el diccionari data.
  """

  if comanda == "enters":
    if nom not in data:
      data[nom] = 0
    else:
      print(f"{nom} is already in the casino") 
  
  
  if comanda == "leaves":
    if nom in data:
      print(f"{nom} has won {data[nom]}")
      del data[nom]
    else:
      print(f"{nom} is not in the casino")
  
  if comanda == "wins":
    quantitat = yg.read(int)
    if nom in data:
      data[nom] += quantitat
    else:
      print(f"{nom} is not in the casino")
  

def main() -> None:
  data: dict[str, int] = dict()

  for nom in yg.tokens(str):
    comanda = yg.read(str)
    gestionar_comanda(nom, comanda, data)
  
  print("----------")
  for nom, guanys in sorted(data.items()):
    print(f"{nom} is winning {guanys}")


if __name__ == "__main__":
  main()