from treti_pokus import find_path
from vizualizace import Obrazek
from obstacles_generation import obstacle_gui
from time import perf_counter

obstacles, start_pos, end_pos = obstacle_gui(generate_random_obstacles=True)  # jmenuje se to obstacle gui,
# ale vystupem je i start a end pos

t = perf_counter()
finalstates = find_path(obstacles, start_pos, end_pos, break_at_first=True, random=True)  # break at first je true,
# protoze se stejne divame jenom na obrazek prvni vygenerovane cesty
pathfindingt = perf_counter() - t

t = perf_counter()
img = Obrazek(coef=4)

for j, row in enumerate(obstacles):  # vybarveni policek s prekazkami metodou obrazku
    for i, ele in enumerate(row):
        if ele:
            img.fill((i, j), color=(255, 0, 0))

print(finalstates)

for pos in finalstates[0][1]:
    img.addpoint(pos, color=(0, 255, 0))

img.addpoint(finalstates[0][0], color=(255, 0xa5, 0))

print(f"pathfinding {pathfindingt}")
print(f"obrazek {perf_counter()-t}")
img.show()
