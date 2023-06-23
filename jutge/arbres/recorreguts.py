from yogi import tokens
from typing import TypeAlias

Bintree: TypeAlias = tuple[int, tuple[int, Bintree, Bintree]]

def draw_postorder(t: list[int], d: int) -> None:
  pass



def main() -> None:
  tree = [i for i in tokens(int)]

  print(f"pos: {draw_postorder(tree, 0)}")
  print(f"ino: {draw_inorder(tree, 0)}")



if __name__ == "__main__":
  main()