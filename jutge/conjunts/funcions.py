from typing import Optional

def average(s: set[float]) -> float: return sum(s) / len(s)

def different_elements(l1: list[int], l2: list[int]): return len(set(l1 + l2))

def has_duplicates(L: list[int]) -> bool: return len(L) != len(set(L))

def extraneous_maybe(l1: list[str], l2: list[str]) -> Optional[str]: return None if len(set(l2) - set(l1)) == 0 else (set(l2) - set(l1)).pop() 

def extraneous(l1: list[str], l2: list[str]) -> str: return (set(l2) - set(l1)).pop()

def different_words(s: str) -> int: return len(set([w.lower() for w in s.split()]))