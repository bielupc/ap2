from yogi import scan, read

def min_range(cities, s):
    if s == 0:
        return cities[-1] - cities[0]
    if len(cities) - 1 <= s:
        return 0
    mid = len(cities) // 2
    left_cities = cities[:mid+1]
    right_cities = cities[mid:]
    max_left = left_cities[-1]
    min_right = right_cities[0]
    for i in range(len(left_cities)-2, -1, -1):
        if max_left - left_cities[i] <= min_right - max_left:
            range_left = max_left - left_cities[i]
            range_right = min_range(right_cities, s-1)
            best_range = min(best_range, max(range_left, range_right))
        else:
            break
    for i in range(1, len(right_cities)):
        if right_cities[i] - min_right <= min_right - max_left:
            range_left = min_range(left_cities, s-1)
            range_right = right_cities[i] - min_right
            best_range = min(best_range, max(range_left, range_right))
        else:
            break
    range_left = min_range(left_cities, s)
    range_right = min_range(right_cities, s)
    best_range = min(best_range, max(range_left, range_right))
    return best_range




def main() -> None:
  n = scan(int)
  while n is not None:
    p = read(int)
    l = [read(int) for _ in range(n)]

    print(min_range(l, p))

    n = scan(int)


if __name__ == "__main__":
  main()