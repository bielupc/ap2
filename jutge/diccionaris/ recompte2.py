from yogi import read, scan, tokens


def main() -> None:
  paraules: dict[str, int] = dict()

  for word in tokens(str):
    word = word.lower()
    if word not in paraules:
      paraules[word] = 1
    else:
      paraules[word] += 1

  for paraula, comptador in sorted(paraules.items(), key=lambda x: (x[1], x[0])):
      print(comptador, paraula)


if __name__ == "__main__":
  main()