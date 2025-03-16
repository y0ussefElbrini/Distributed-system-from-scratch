import matplotlib.pyplot as plt
import numpy as np

# Durées des phases Map, Reduce et Tri pour les nouvelles données

map_times_all = np.array(
    [13.15332, 6.52735, 4.44495, 3.34484, 2.10028, 1.02353])

reduce_times_all = np.array(
    [15.03636, 4.51524, 1.98434, 1.7329, 0.91023, 0.57782])

tri_times_all = np.array(
    [8.89239, 8.97049, 9.01607, 9.09961, 9.24734, 9.15523])

reduce2_times_all = np.array(
    [61.2742635, 46.95163, 40.617673, 40.2886, 37.39993, 30.85782])  # reduce en comptant le merge
num_processors = np.array([4, 8, 12, 16, 32, 64])

# Durées séquentielles des phases Map, Reduce et Tri pour les nouvelles données

sequential_map_time = 50.99696

sequential_reduce_time = 28.50489
# Remplacez cette valeur par la durée séquentielle de la phase Tri
sequential_tri_time = 19.43527

# Calcul des durées totales de Map + Reduce, Map + Reduce + Tri et Map + Reduce + Reduce2 pour les nouvelles données
total_time_map_reduce = map_times_all + reduce_times_all
total_time_map_reduce_tri = map_times_all + reduce_times_all + tri_times_all
total_time_map_reduce_reduce2 = map_times_all + reduce2_times_all
total_time_map_reduce_reduce2_tri = map_times_all + \
    reduce2_times_all + tri_times_all

# Calcul des speedups pour les nouvelles données
sequential_time_map_reduce = sequential_map_time + sequential_reduce_time
sequential_time_map_reduce_tri = sequential_map_time + \
    sequential_reduce_time + sequential_tri_time
sequential_time_map_reduce_reduce2 = sequential_map_time + \
    sequential_reduce_time
sequential_time_map_reduce_reduce2_tri = sequential_map_time + \
    sequential_reduce_time + sequential_tri_time


total_speedup_map_reduce = sequential_time_map_reduce / total_time_map_reduce
total_speedup_map_reduce_tri = sequential_time_map_reduce_tri / \
    total_time_map_reduce_tri

total_speedup_map_reduce2_tri = sequential_time_map_reduce_reduce2 / \
    total_time_map_reduce_reduce2_tri
# Tracé des courbes pour les nouvelles données avec Reduce2
plt.figure(figsize=(8, 6))

plt.plot(num_processors, total_speedup_map_reduce,
         marker='o', label='Map + Reduce (99% portion parallèle)')
plt.plot(num_processors, total_speedup_map_reduce_tri,
         marker='o', label='Map + Reduce + Tri (90% portion parallèle)')

plt.plot(num_processors, total_speedup_map_reduce2_tri,
         marker='o', label='Map + (Reduce + Merge) + tri (50% portion parallèle)')

plt.xlabel('Nombre de machines')
plt.ylabel('Speedup')
plt.title(
    'Comparaison de la loi d \'Amdahl Law pour les différents cas (fichier 670MB)')
plt.legend()
plt.grid(True)
plt.yticks([0, 2, 4, 10, 15, 20, 25, 30])
plt.show()
