from yogi import read, scan

def explore(adj: dict[str, list[str]], v: str, cc: dict[str, int], ccnum: int) -> None:
    """
        Donat la llista d'adjacència d'un graf, coloca ccnum a les posicions de cc referents a nodes visitables desde v.
    """
    cc[v] = ccnum
    for u in adj[v]:
        if cc[u] == 0:
            explore(adj, u, cc, ccnum)


def connected_components(adj: dict[str, list[str]]) ->dict[str, int]:
    """Donada la llista d'adjacència d'un graf, retorna les seves components conectades en forma de diccionari (node, ccnum).""" 
    cc = {node: 0 for node in adj.keys()}
    ccnum = 1

    for node in adj.keys():
        if cc[node] == 0:
            explore(adj, node, cc, ccnum)
            ccnum+=1
    
    return cc


def trobar_cami(x: str, y: str, adj: dict[str, list[str]]) -> bool:
    """Donats dos vèrtex i una llista d'adjacència, retorna si es accessible."""
    cc = connected_components(adj)
    return cc[x] == cc[y]


def main() -> None:
    adj: dict[str, list[str]] = dict()

    n = read(int)
    for _ in range(n):
        adj[read(str)] = list()

    m = read(int)
    for _ in range(m):
        adj[read(str)].append(read(str))
 
    
    x, y = read(str), read(str)
    print("yes") if trobar_cami(x, y, adj) else print("no")


if __name__ == "__main__":
    main()
