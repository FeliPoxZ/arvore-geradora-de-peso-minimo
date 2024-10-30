import networkx as nx
import random
import matplotlib.pyplot as plt
import time
import kruskal as k
import prim as p
import mplcursors as mplc
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Criar um grafo vazio
G = nx.Graph()

# Definir número de nós e arestas
num_nos = 10  # Ajuste conforme necessário
num_arestas = 14  # Total de arestas desejadas

# Adicionar nós ao grafo
for i in range(num_nos):
    G.add_node(i)

# Criar uma árvore geradora para garantir que todos os vértices estejam conectados
for i in range(1, num_nos):
    u = random.randint(0, i - 1)
    peso = random.randint(1, 10)
    G.add_edge(i, u, weight=peso)

# Adicionar arestas aleatórias até atingir o número total desejado
while len(G.edges) < num_arestas:
    u = random.randint(0, num_nos - 1)
    v = random.randint(0, num_nos - 1)
    if u != v and not G.has_edge(u, v):  # Evitar laços e arestas duplicadas
        peso = random.randint(1, 10)
        G.add_edge(u, v, weight=peso)

# Calcular a árvore geradora mínima usando Kruskal
start_time = time.perf_counter()
kruskal = nx.minimum_spanning_tree(G)
end_time = time.perf_counter()
soma_pesos_kruskal = kruskal.size(weight='weight')
tempo_kruskal = end_time - start_time

# Calcular a árvore geradora mínima usando Prim
start_time = time.perf_counter()
prim = nx.minimum_spanning_tree(G, algorithm="prim")
end_time = time.perf_counter()
soma_pesos_prim = prim.size(weight='weight')
tempo_prim = end_time - start_time

# Usando o meu Kruskal
#print("Usando o meu Kruskal")
arestas = [k.Aresta(u, v, d['weight']) for u, v, d in G.edges(data=True)]
n = G.number_of_nodes()

tempo_inicial_meu_kruskal = time.perf_counter()
agpm = k.kruskalFUnction(arestas, n)
tempo_final_meu_kruskal = time.perf_counter()
tempo_utilizado_meu_kruskal = tempo_final_meu_kruskal - tempo_inicial_meu_kruskal
soma_pesos_meu_kruskal = sum(aresta.peso for aresta in agpm)

#print(f"Soma dos pesos das arestas da Árvore Geradora Mínima: {soma_pesos_meu_kruskal} e tempo utilizado {round(tempo_utilizado_meu_kruskal, 8)}")
#print("Tempo utilizado meu Kruskal: {:.10f} segundos".format(tempo_utilizado_meu_kruskal))

# ----------------------------------------------------

grafo_prim = [[] for _ in range(num_nos)]

# transformando em uma tabela de adjacencia
for (u, v, data) in G.edges(data=True):
    peso = data['weight']
    grafo_prim[u].append((v, peso))
    grafo_prim[v].append((u, peso))

start_time = time.perf_counter()
agpm_prim = p.prim(grafo_prim, num_nos)
end_time = time.perf_counter()
tempo_utilizado_meu_prim = end_time - start_time

soma_pesos_meu_prim = sum(peso for _, _, peso in agpm_prim)
#print(soma_pesos_meu_prim)

resultado_prim = p.gerar_grafoNetworx(agpm_prim, num_nos)

#print(agpm_prim)

"""

fig, axs = plt.subplots(3, 2, figsize=(18, 25))
plt.subplots_adjust(hspace=0.8, wspace=0.4)

# Desenhar o grafo original
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, ax=axs[0, 0], node_color='lightblue', edge_color='gray')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=axs[0, 0])
axs[0, 0].set_title("Grafo Original")

# Desenhar a árvore geradora mínima (Kruskal do NetworkX)
pos = nx.spring_layout(kruskal)
nx.draw(kruskal, pos, with_labels=True, ax=axs[0, 1], node_color='lightgreen')
mst_labels_kruskal = nx.get_edge_attributes(kruskal, 'weight')
nx.draw_networkx_edge_labels(kruskal, pos, edge_labels=mst_labels_kruskal, ax=axs[0, 1])
axs[0, 1].set_title("Kruskal - NetworkX")
axs[0, 1].text(0.5, -0.3, f'Tempo: {round(tempo_kruskal, 8)} s\nPeso Total: {soma_pesos_kruskal}', 
                ha='center', va='top', transform=axs[0, 1].transAxes)

# Desenhar a árvore geradora mínima (Prim do NetworkX)
pos = nx.spring_layout(prim)
nx.draw(prim, pos, with_labels=True, ax=axs[1, 0], node_color='lightgreen')
mst_labels_prim = nx.get_edge_attributes(prim, 'weight')
nx.draw_networkx_edge_labels(prim, pos, edge_labels=mst_labels_prim, ax=axs[1, 0])
axs[1, 0].set_title("Prim - NetworkX")
axs[1, 0].text(0.5, -0.3, f'Tempo: {round(tempo_prim, 8)} s\nPeso Total: {soma_pesos_prim}', 
                ha='center', va='top', transform=axs[1, 0].transAxes)

# Desenhar a árvore geradora mínima (Kruskal do seu algoritmo)
G_agpm = nx.Graph()
for aresta in agpm:
    G_agpm.add_edge(aresta.origem, aresta.destino, weight=aresta.peso)

pos = nx.spring_layout(G_agpm)
nx.draw(G_agpm, pos, with_labels=True, ax=axs[1, 1], node_color='lightgreen')
mst_labels_meu_kruskal = nx.get_edge_attributes(G_agpm, 'weight')
nx.draw_networkx_edge_labels(G_agpm, pos, edge_labels=mst_labels_meu_kruskal, ax=axs[1, 1])
axs[1, 1].set_title("Meu Kruskal")
axs[1, 1].text(0.5, -0.3, f'Tempo: {tempo_utilizado_meu_kruskal:.10f} s\nPeso Total: {soma_pesos_meu_kruskal}', 
                ha='center', va='top', transform=axs[1, 1].transAxes)

# Desenhar a árvore geradora mínima (Prim do seu algoritmo)
grafo_prim = [[] for _ in range(num_nos)]
for (u, v, data) in G.edges(data=True):
    peso = data['weight']
    grafo_prim[u].append((v, peso))
    grafo_prim[v].append((u, peso))

start_time = time.perf_counter()
agpm_prim = p.prim(grafo_prim, num_nos)
end_time = time.perf_counter()
tempo_utilizado_meu_prim = end_time - start_time

soma_pesos_meu_prim = sum(peso for _, _, peso in agpm_prim)
resultado_prim = p.gerar_grafoNetworx(agpm_prim, num_nos)

# Desenhar a árvore geradora mínima (Prim do seu algoritmo)
pos = nx.spring_layout(resultado_prim)
nx.draw(resultado_prim, pos, with_labels=True, ax=axs[2, 0], node_color='lightblue')
mst_labels_meu_prim = nx.get_edge_attributes(resultado_prim, 'weight')
nx.draw_networkx_edge_labels(resultado_prim, pos, edge_labels=mst_labels_meu_prim, ax=axs[2, 0])
axs[2, 0].set_title("Meu Prim")
axs[2, 0].text(0.5, -0.3, f'Tempo: {tempo_utilizado_meu_prim:.10f} s\nPeso Total: {soma_pesos_meu_prim}', 
                ha='center', va='top', transform=axs[2, 0].transAxes)

# Gráfico de comparação de tempos de execução
algoritmos = ['Kruskal (NetworkX)', 'Prim (NetworkX)', 'Meu Kruskal', 'Meu Prim']
tempos = [tempo_kruskal, tempo_prim, tempo_utilizado_meu_kruskal, tempo_utilizado_meu_prim]

axs[2, 1].bar(algoritmos, tempos, color=['lightblue', 'lightgreen', 'orange', 'red'])
axs[2, 1].set_title("Comparação de Tempos de Execução")
axs[2, 1].set_xlabel("Algoritmos")
axs[2, 1].set_ylabel("Tempo (segundos)")
axs[2, 1].grid(axis='y', linestyle='--', alpha=0.7)
axs[2, 1].set_ylim(0, max(tempos) * 1.2)  # Aumenta o limite superior em 20%

for i, tempo in enumerate(tempos):
    axs[2, 1].text(i, tempo, f'{tempo:.10f}', ha='center', va='bottom')  

# Ajustar layout
mplc.cursor(hover=True)

"""



algoritmos = ['Kruskal (NetworkX)', 'Prim (NetworkX)', 'Meu Kruskal', 'Meu Prim']
tempos = [tempo_kruskal, tempo_prim, tempo_utilizado_meu_kruskal, tempo_utilizado_meu_prim]


# Criar uma nova figura para o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(algoritmos, tempos, color=['lightblue', 'lightgreen', 'orange', 'red'])

# Configurar título e rótulos
plt.title("Comparação de Tempos de Execução com 10 vertices e 14 arestas")
plt.xlabel("Algoritmos")
plt.ylabel("Tempo (segundos)")

# Adicionar grade
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Ajustar limites do eixo y
plt.ylim(0, max(tempos) * 1.2)  # Aumenta o limite superior em 20%

# Adicionar rótulos em cima das barras
for i, tempo in enumerate(tempos):
    plt.text(i, tempo, f'{tempo:.6f}', ha='center', va='bottom')
    
    

print(f"Kruskal networx -> tempo {tempo_kruskal} peso: {soma_pesos_kruskal}")
print(f"prim networx -> tempo {tempo_prim} peso: {soma_pesos_prim}")
print(f"Kruskal minha implementação -> tempo {tempo_utilizado_meu_kruskal} peso: {soma_pesos_meu_kruskal}")
print(f"PRIM minha implementação -> tempo {tempo_utilizado_meu_prim} peso: {soma_pesos_meu_prim}")




# Mostrar o gráfico de barras
plt.tight_layout()
plt.show()
