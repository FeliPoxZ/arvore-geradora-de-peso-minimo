import heapq
import networkx as nx

def prim(grafo, n):
    inicio = 0  # Começamos com o primeiro vértice (vértice 0)
    
    agpm = []  # Lista que vai armazenar as arestas da árvore geradora mínima
    distancias = [float('inf')] * n  # Inicializa distâncias como infinito
    distancias[inicio] = 0  # Distância do vértice inicial para ele mesmo é 0
    
    heap = [(0, inicio)]  # Heap com o vértice inicial e seu peso
    pai = [-1] * n  # Inicializa a lista de pais como -1
    incluídos = set()  # Conjunto para rastrear quais vértices foram incluídos na AGM

    while heap:
        peso, u = heapq.heappop(heap)  # Remove o vértice com menor peso

        if u in incluídos:
            continue  # Se já foi incluído, ignora

        incluídos.add(u)  # Marca o vértice como incluído na AGM

        # Adiciona as arestas do vértice u à AGM
        if pai[u] != -1:  # Ignora a aresta do vértice inicial
            agpm.append((pai[u], u, peso))  # Adiciona a aresta (pai[u], u, peso)

        for v, peso_ in grafo[u]:
            if v not in incluídos and peso_ < distancias[v]:
                distancias[v] = peso_  # Atualiza a distância para v
                pai[v] = u  # Armazena quem é o pai de v
                heapq.heappush(heap, (peso_, v))  # Adiciona v à heap com seu peso

    return agpm  # Retorna a lista de arestas da AGM



def gerar_grafo(arestas, n):
    grafo = {i: [] for i in range(n)}  # Inicializa o grafo com n vértices

    for (u, v, peso) in arestas:
        grafo[u].append((v, peso))  # Adiciona aresta de u para v
        grafo[v].append((u, peso))  # Adiciona aresta de v para u (grafo não direcionado)

    return grafo


def gerar_grafoNetworx(arestas, n):
    grafo = nx.Graph()  # Cria um grafo não direcionado

    for (u, v, peso) in arestas:
        grafo.add_edge(u, v, weight=peso)  # Adiciona a aresta com peso

    return grafo
