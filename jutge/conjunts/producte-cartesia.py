from yogi import read, scan, tokens

def cartesian_product(a: set[int], b: set[int]) -> set[tuple[int, int]]:
  if len(a) < len(b): a, b = b, a
  result: set[tuple[int, int]] = set()

  for x in a:
    for y in b:
      result.add((x, y))
  return result

