import numpy as np
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

# === 1. Create the adjacency matrix ===
# Correct Zachary Karate Club Adjacency Matrix (0-based indexing)
A = np.zeros((34, 34), dtype=int)

# Add all edges (converted to 0-based indexing)
edges = [
    (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),(0,12),(0,13),(0,17),(0,19),(0,21),(0,31),
    (1,2),(1,3),(1,7),(1,13),(1,17),(1,19),(1,21),(1,30),
    (2,3),(2,7),(2,8),(2,9),(2,13),(2,27),(2,28),(2,32),
    (3,7),(3,12),(3,13),
    (4,6),(4,10),
    (5,6),(5,10),(5,16),
    (6,16),
    (8,30),(8,32),(8,33),
    (9,33),
    (13,33),
    (14,32),(14,33),
    (15,32),(15,33),
    (18,32),(18,33),
    (19,33),
    (20,32),(20,33),
    (22,32),(22,33),
    (23,25),(23,27),(23,29),(23,32),(23,33),
    (24,25),(24,27),(24,31),
    (25,31),
    (26,29),(26,33),
    (27,33),
    (28,31),(28,33),
    (29,32),(29,33),
    (30,32),(30,33),
    (31,32),(31,33),
    (32,33)
]

# Fill the adjacency matrix
for i, j in edges:
    A[i, j] = 1
    A[j, i] = 1  # Make it symmetric


print("Correct Zachary Karate Club Adjacency Matrix Shape:", A.shape)
print("Total edges:", np.sum(A) // 2)  # Should be 78
print("Matrix is symmetric:", np.array_equal(A, A.T))

print("Matrice d'adjacence créée avec succès!")
print(f"Dimensions: {A.shape}")
print(f"Nombre total d'arêtes: {np.sum(A) // 2}")

# === 2. Create the graph ===
G = nx.from_numpy_array(A)

# === 3. Graph order and size ===
order = G.number_of_nodes()
size = G.number_of_edges()

print("Graph order (number of nodes):", order)
print("Graph size (number of edges):", size)

# === 4. Degree distribution ===
degrees = [deg for _, deg in G.degree()]
degree_count = Counter(degrees)

print("\nDegree distribution:")
for deg, count in sorted(degree_count.items()):
    print(f"Degree {deg}: {count} nodes")

plt.figure(figsize=(10, 6))
sns.barplot(x=list(degree_count.keys()), y=list(degree_count.values()))
plt.xlabel("Degree")
plt.ylabel("Number of nodes")
plt.title("Degree distribution")
plt.show()

# === 5. Clustering coefficients ===
clustering_coeffs = nx.clustering(G)
avg_clustering = nx.average_clustering(G)
print("\nAverage clustering coefficient:", round(avg_clustering, 3))

# === 6. Frequent motifs (triangles) ===
triangles_per_node = nx.triangles(G)
total_triangles = sum(triangles_per_node.values()) / 3  # each triangle counted 3 times
print("\nTotal number of triangles:", int(total_triangles))

# === 7. Cliques ===
cliques = list(nx.find_cliques(G))
max_clique = max(len(c) for c in cliques)
print("\nNumber of cliques found:", len(cliques))
print("Maximum clique size:", max_clique)

# === 8. k-cores ===
core_numbers = nx.core_number(G)
max_kcore = max(core_numbers.values())
print("\nMaximum k-core:", max_kcore)

# Extract and visualize a specific k-core
k = max_kcore
kcore_subgraph = nx.k_core(G, k)
plt.figure(figsize=(10, 8))
nx.draw(kcore_subgraph, with_labels=True, node_color="lightblue", node_size=500)
plt.title(f"{k}-core of the graph")
plt.show()

# === 9. Centrality measures ===
deg_centrality = nx.degree_centrality(G)
bet_centrality = nx.betweenness_centrality(G)
close_centrality = nx.closeness_centrality(G)
eig_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Find the most central nodes
def top_nodes(centrality_dict, n=5):
    return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:n]

print("\nTop 5 nodes by degree centrality:")
print(top_nodes(deg_centrality))

print("\nTop 5 nodes by betweenness centrality:")
print(top_nodes(bet_centrality))

print("\nTop 5 nodes by closeness centrality:")
print(top_nodes(close_centrality))

print("\nTop 5 nodes by eigenvector centrality:")
print(top_nodes(eig_centrality))

# Gather all top nodes for visualization
centrality_data = []

for name, cent_dict in [
    ("Degree", deg_centrality),
    ("Betweenness", bet_centrality),
    ("Closeness", close_centrality),
    ("Eigenvector", eig_centrality)
]:
    for node, value in top_nodes(cent_dict, n=5):
        centrality_data.append({
            "Node": str(node),
            "Centrality Type": name,
            "Centrality Value": value
        })

# Create DataFrame and plot
df_centrality = pd.DataFrame(centrality_data)

plt.figure(figsize=(14, 7))
sns.barplot(
    data=df_centrality,
    x="Centrality Type",
    y="Centrality Value",
    hue="Node",
    palette="Set2"
)
plt.title("Top 5 Most Central Nodes per Centrality Measure", fontsize=14, fontweight='bold')
plt.xlabel("Centrality Measure", fontsize=12, fontweight='bold')
plt.ylabel("Centrality Value", fontsize=12, fontweight='bold')
plt.legend(title="Node", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# Build graph
G = nx.from_numpy_array(A)

# Define groups
group_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 17, 19, 21]
group_2 = [9, 14, 15, 16, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]

# Centralities
deg_centrality = nx.degree_centrality(G)
bet_centrality = nx.betweenness_centrality(G)

# Top nodes
def top_nodes(cent_dict, n=5):
    return sorted(cent_dict.items(), key=lambda x: x[1], reverse=True)[:n]

top_deg = top_nodes(deg_centrality)
top_bet = top_nodes(bet_centrality)

print("Top 5 by Degree Centrality:", top_deg)
print("Top 5 by Betweenness Centrality:", top_bet)

# Create dataframe for plotting
df = pd.DataFrame({
    "Node": [n for n, _ in top_deg + top_bet],
    "Centrality Value": [v for _, v in top_deg + top_bet],
    "Type": ["Degree"] * 5 + ["Betweenness"] * 5
})

# Barplot
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Type", y="Centrality Value", hue="Node", palette="Set2")
plt.title("Top 5 Nodes by Centrality", fontsize=13, fontweight='bold')
plt.xlabel("Centrality Type")
plt.ylabel("Centrality Value")
plt.legend(title="Node", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Bridge nodes
bridge_nodes = [
    n for n in G.nodes() if
    (n in group_1 and any(nb in group_2 for nb in G.neighbors(n))) or
    (n in group_2 and any(nb in group_1 for nb in G.neighbors(n)))
]

print("\nBridge nodes connecting both groups:", sorted(bridge_nodes))
