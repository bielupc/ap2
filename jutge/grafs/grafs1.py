from yogi import read, scan

def explore(adj: dict[int, list[int]], v: int, cc: dict[int, int], ccnum: int) -> None:
    """
        Donat la llista d'adjacència d'un graf, coloca ccnum a les posicions de cc referents a nodes visitables desde v.
    """
    cc[v] = ccnum
    for u in adj[v]:
        if cc[u] == 0:
            explore(adj, u, cc, ccnum)


def connected_components(adj: dict[int, list[int]]) ->dict[int, int]:
    """Donada la llista d'adjacència d'un graf, retorna les seves components conectades en forma de diccionari (node, ccnum).""" 
    cc = {node: 0 for node in adj.keys()}
    ccnum = 1

    for node in adj.keys():
        if cc[node] == 0:
            explore(adj, node, cc, ccnum)
            ccnum+=1
    
    return cc


def trobar_cami(x: int, y: int, adj: dict[int, list[int]]) -> bool:
    """Donats dos vèrtex i una llista d'adjacència, retorna si es accessible."""
    cc = connected_components(adj)
    return cc[x] == cc[y]
    


def main() -> None:
    n = read(int)
    m = read(int)
    
    #Creem les llistes d'adjacència en un diccionari
    adj: dict[int, list[int]] = dict()
    for _ in range(m):
        u = read(int)
        v = read(int)
        if u in adj:
            adj[u].append(v)
        else:
            adj[u] = [v]
        
        if v not in adj:
            adj[v] = list()
    
    x, y = read(int), read(int)
    print("yes") if trobar_cami(x, y, adj) else print("no")


if __name__ == "__main__":
    main()
