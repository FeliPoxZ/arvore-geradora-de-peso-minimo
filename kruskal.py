class Aresta:
    def __init__(self, origem, destino, peso):
        self.origem = origem
        self.destino = destino
        self.peso = peso
        
class ConjuntosDisJuntos:
    def __init__(self, n):
        self.pais = [i for i in range(n)]
        
    def encontrar(self, u):
        if u != self.pais[u]:
            self.pais[u] = self.encontrar(self.pais[u])  # Path compression
        return self.pais[u]
    
    def unir(self, u, v):
        pai_u = self.encontrar(u)
        pai_v = self.encontrar(v)
        if pai_u != pai_v:
            self.pais[pai_u] = pai_v  # Union

def kruskalFUnction(grafo, n):
    arestas = sorted(grafo, key=lambda aresta: aresta.peso)
    
    agpm = []
    
    conjuntos = ConjuntosDisJuntos(n)
    
    for aresta in arestas:
        u = aresta.origem
        v = aresta.destino
        
        if conjuntos.encontrar(u) != conjuntos.encontrar(v):
            agpm.append(aresta)
            conjuntos.unir(u, v)
    
    return agpm
