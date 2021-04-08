import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

import random_map
import search_algorithm

plt.figure(figsize=(5, 5))

map = random_map.RandomMap(size=30)

ax = plt.gca()
ax.set_xlim([0, map.size])
ax.set_ylim([0, map.size])

for i in range(map.size):
    for j in range(map.size):
        if map.IsObstacle(i,j):
            rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
        else:
            rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
            ax.add_patch(rec)

rec = Rectangle((0, 0), width = 1, height = 1, facecolor='b')
ax.add_patch(rec)

rec = Rectangle((map.size-1, map.size-1), width = 1, height = 1, facecolor='r')
ax.add_patch(rec)

plt.axis('equal')
plt.axis('off')
plt.tight_layout()
# plt.show()

plt.ion()

a_star = search_algorithm.AStar(map)
a_star.RunAndSaveImage(ax, plt)
plt.ioff()
plt.show()