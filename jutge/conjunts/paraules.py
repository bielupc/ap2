from yogi import read, scan, tokens


def main() -> None:
  paraules: set[str] = set()

  for word in tokens(str):
    paraules.add(word.lower())
  
  # print(*sorted(paraules), sep="\n")

  ordenat = sorted(paraules)
  for paraula in ordenat:
    print(paraula)


if __name__ == "__main__":
  main()