import igraph as ig
import pandas as pd
import matplotlib.pyplot as plt
import sys

VERTICES_CSV = "Vertices-projeto.csv"
GRAPHML_OUT = "grafo_ponderado.graphml"
BARRAS_INTERMEDIACAO_OUT = "centralidade_intermediacao_ponderada_barras.png"
BARRAS_AUTOVALOR_OUT = "centralidade_autovalor_barras.png"
BARRAS_GRAU_OUT = "centralidade_grau_barras.png"
GRAFO_OUT = "grafo_direcionado_ponderado.png"

try:
    df_vertices = pd.read_csv(VERTICES_CSV)
except FileNotFoundError:
    raise SystemExit(f"Arquivo '{VERTICES_CSV}' não encontrado.")

if "Id" not in df_vertices.columns:
    raise SystemExit("Coluna 'Id' não encontrada no CSV.")

n_vertices = 84
if len(df_vertices) != n_vertices:
    print(f"Atenção: CSV tem {len(df_vertices)} vértices, mas será usado {n_vertices}.")

g = ig.Graph(directed=True)
g.add_vertices(n_vertices)
g.vs["name"] = df_vertices["Id"].astype(str).tolist()

arestas_1based = [
    (1,25), (2,25), (3,9), (3,25), (4,25), (5,8), (6,25), (7,8), (7,15), (7,26), (7,25),
    (8,9), (8,24), (9,7), (9,25), (10,25), (11,25), (12,68), (13,58), (13,68), (13,75),
    (13,64), (13,73), (14,12), (14,13), (14,68), (14,58), (14,51), (15,25), (16,2), (16,3),
    (16,7), (16,8), (16,10), (16,15), (16,24), (16,26), (16,27), (16,50), (16,52), (16,61),
    (16,25), (17,64), (17,73), (17,53), (18,22), (19,66), (19,68), (19,51), (19,12), (19,73),
    (20,25), (21,22), (21,68), (21,73), (21,58), (21,64), (21,66), (21,48), (22,68), (23,27),
    (23,25), (24,2), (24,60), (26,7), (26,24), (26,25), (27,25), (28,55), (28,25), (29,3),
    (30,38), (31,30), (32,9), (32,42), (32,24), (32,15), (33,56), (33,11), (33,1), (34,3),
    (34,7), (34,15), (34,25), (35,1), (36,10), (36,15), (36,60), (36,2), (36,5), (36,7),
    (36,3), (36,4), (36,61), (36,25), (36,81), (37,2), (37,25), (39,20), (39,60), (40,52),
    (41,44), (42,55), (43,3), (43,41), (45,56), (46,21), (46,68), (47,20), (47,52), (47,25),
    (48,66), (48,68), (48,75), (49,1), (49,2), (49,3), (49,7), (49,8), (49,9), (49,10),
    (49,15), (49,25), (49,26), (49,28), (49,38), (49,47), (49,50), (49,52), (49,54), (49,55),
    (49,60), (49,61), (50,7), (50,24), (51,68), (51,25), (52,25), (53,68), (54,3), (54,55),
    (54,25), (55,25), (56,25), (57,26), (57,50), (57,80), (58,68), (58,75), (58,51), (59,58),
    (59,68), (59,51), (59,73), (59,75), (60,25), (61,25), (62,68), (62,63), (63,51), (63,68),
    (63,58), (68,12), (64,73), (64,77), (65,46), (65,48), (65,68), (65,58), (65,73), (65,66),
    (66,48), (66,19), (66,68), (66,17), (66,73), (66,77), (66,62), (66,76), (66,58), (66,51),
    (66,12), (67,3), (67,25), (68,25), (69,25), (70,68), (70,69), (70,75), (70,63), (70,58),
    (70,51), (70,12), (70,73), (71,17), (72,68), (73,64), (73,68), (74,51), (74,68), (75,68),
    (75,51), (76,58), (77,68), (77,73), (78,61), (79,10), (79,25), (79,60), (80,25), (81,25),
    (82,81), (82,25), (83,38), (83,25), (84,45), (84,25)
]

arestas_corrigidas = [(a-1, b-1) for a,b in arestas_1based]
g.add_edges(arestas_corrigidas)

pesos = [
    3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 2, 3, 3, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 2, 2, 2, 2, 2,
    1, 3, 3, 3, 3, 2, 3, 3, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 3, 3, 2, 1, 2, 3, 1, 3, 2, 1, 3, 3, 3, 2, 3, 1, 3, 1,
    2, 1, 1, 3, 3, 2, 1, 1, 2, 3, 1, 2, 3, 2, 2, 1, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 3, 2, 3, 1, 2, 2,
    2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 3, 1, 2, 2, 2, 2, 2, 3,
    2, 2, 1, 3, 2, 1, 3, 3, 1, 3, 3
]
g.es["weight"] = pesos

betweenness = g.betweenness(weights=g.es["weight"])
df_bet = pd.DataFrame({
    "Vértice": g.vs["name"],
    "Centralidade de Intermediação": betweenness
}).sort_values(by="Centralidade de Intermediação", ascending=False)

plt.figure(figsize=(14,6))
plt.bar(df_bet["Vértice"], df_bet["Centralidade de Intermediação"], color="darkorange")
plt.title("Centralidade de Intermediação Ponderada dos Vértices", fontsize=14)
plt.xlabel("Vértices")
plt.ylabel("Centralidade de Intermediação")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(BARRAS_INTERMEDIACAO_OUT, dpi=300)
plt.show()

eigen = g.eigenvector_centrality(weights=g.es["weight"])
df_eigen = pd.DataFrame({
    "Vértice": g.vs["name"],
    "Centralidade de Autovalor": eigen
}).sort_values(by="Centralidade de Autovalor", ascending=False)

plt.figure(figsize=(14,6))
plt.bar(df_eigen["Vértice"], df_eigen["Centralidade de Autovalor"], color="lightsalmon")
plt.title("Centralidade de Autovalor Ponderada dos Vértices", fontsize=14)
plt.xlabel("Vértices")
plt.ylabel("Centralidade de Autovalor")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(BARRAS_AUTOVALOR_OUT, dpi=300)
plt.show()

degree = g.degree()
df_degree = pd.DataFrame({
    "Vértice": g.vs["name"],
    "Centralidade de Grau": degree
}).sort_values(by="Centralidade de Grau", ascending=False)

plt.figure(figsize=(14,6))
plt.bar(df_degree["Vértice"], df_degree["Centralidade de Grau"], color="skyblue")
plt.title("Centralidade de Grau dos Vértices", fontsize=14)
plt.xlabel("Vértices")
plt.ylabel("Centralidade de Grau")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(BARRAS_GRAU_OUT, dpi=300)
plt.show()

layout = g.layout("fr")
cores_arestas = []
for e in g.es:
    w = e["weight"]
    if w == 1:
        cores_arestas.append("gray")
    elif w == 2:
        cores_arestas.append("orange")
    else:
        cores_arestas.append("red")

ig.plot(
    g,
    layout=layout,
    vertex_label=g.vs["name"],
    vertex_color="skyblue",
    vertex_size=25,
    edge_color=cores_arestas,
    edge_arrow_size=0.5,
    edge_width=1,
    bbox=(1200,1200),
    margin=50,
    target=GRAFO_OUT
)

g.es["color"] = cores_arestas
g.write_graphml(GRAPHML_OUT)

print(f"\nGráfico intermediação: {BARRAS_INTERMEDIACAO_OUT}")
print(f"Gráfico autovalor: {BARRAS_AUTOVALOR_OUT}")
print(f"Gráfico grau: {BARRAS_GRAU_OUT}")
print(f"Imagem do grafo: {GRAFO_OUT}")
print(f"Arquívo Gephi: {GRAPHML_OUT}")










