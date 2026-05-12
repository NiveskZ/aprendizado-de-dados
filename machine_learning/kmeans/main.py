import numpy as np

x = [4, 5, 10, 4, 3, 11, 14, 6, 10, 12]
y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]

pontos = np.array(list(zip(x, y)))

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

inercias = []

for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(pontos)
    inercias.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inercias,
         marker='o', color='steelblue', linewidth=2,
         markerfacecolor='white', markeredgewidth=2, markersize=8)
plt.title("Método do Cotovelo (Elbow Method)")
plt.xlabel("Número de Clusters (K)")
plt.ylabel("Inércia")
plt.xticks(range(1, 11))
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = km2.fit_predict(pontos)
centroides = km2.cluster_centers_

cores = ['steelblue', 'tomato']
nomes = ['Cluster 1', 'Cluster 2']

plt.figure(figsize=(8, 6))
for cluster_id in range(2):
    mask = labels == cluster_id
    plt.scatter(pontos[mask, 0], pontos[mask, 1],
                color=cores[cluster_id], label=nomes[cluster_id],
                s=100, edgecolors='white', linewidths=1.5, zorder=2)

plt.scatter(centroides[:, 0], centroides[:, 1],
            marker='X', s=200, color='black',
            edgecolors='white', linewidths=1,
            label='Centroides', zorder=3)

plt.title("Agrupamento K-Means com K=2")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()