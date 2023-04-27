import fileinput
from yogi import scan, read

def main() -> None:
  n = read(int)
  log: dict[str, list[int]] = dict()

  for aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa in range(n):
    nom = read(str)
    log[nom] = [0, 0, 0]

  j1 = scan(str)
  while j1 is not None:
    j2 = read(str)
    resultat = read(str)

    if resultat[0] == "1" and resultat[1] == "/":
      log[j1][1] += 1
      log[j2][1] += 1

    elif resultat[0] == "1":
      log[j1][0] += 1
      log[j2][2] += 1

    else: 
      log[j1][2] += 1
      log[j2][0] += 1

    j1 = scan(str)
    

  for jugador, wins in sorted(log.items(), key=lambda x: x[0]):
    print(jugador, *wins)


if __name__ == "__main__":
  main()