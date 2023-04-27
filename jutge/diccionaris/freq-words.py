from yogi import read, scan, tokens


def main() -> None:
  n = scan(int)
  while n is not None:
    k = read(int)

    vegades: dict[str, int] = dict()

    for _ in range(n):
      word = read(str)
      if word not in vegades:
        vegades[word] = 1
      else:
        vegades[word] += 1

    ordenat = sorted(vegades.items(), key=lambda x: (-x[1], x[0]))
    for i in range(k):
        print(ordenat[i][0])

    print("----------")
    n = scan(int)





if __name__ == "__main__":
  main()