from yogi import read, tokens, scan

def main() -> None:
  n = scan(int)
  while n is not None:
    k = read(int)
    base = {n for n in range(1, n+1)}
    rebut: set[int] = set()
    for _ in range(k):
      rebut.add(read(int))
    print((base-rebut).pop())
    n = scan(int)

if __name__ == "__main__":
  main()