from yogi import read, scan, tokens


def main() -> None:
  paraules: dict[str, int] = dict()

  for word in tokens(str):
    word = word.lower()
    if word not in paraules:
      paraules[word] = 1
    else:
      paraules[word] += 1

  resultat = sorted(paraules.keys()), 
  print(resultat)


if __name__ == "__main__":
  main()