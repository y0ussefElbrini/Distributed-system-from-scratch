import matplotlib.pyplot as plt

# Données du traitement séquentiel
seq_duration = {
    "map": 50.99696,
    "reduce": 28.50489,
    "tri": 19.43527
}

# Calcul du temps total de traitement pour le système séquentiel
seq_total_duration = sum(seq_duration.values())

# Données du traitement distribué
num_machines = [4, 8, 12, 16, 32, 64]
map_values = [13.15332, 6.52735, 4.44495, 3.34484, 2.10028, 1.02353]
shuffle_values = [99.48, 51.75489, 36.46802, 27.79048, 17.68784, 9.87813]
reduce_values = [15.03636, 4.51524, 1.98434, 1.7329, 0.91023, 0.57782]
tri_values = [8.89239, 8.97049, 9.01607, 9.09961, 9.24734, 9.15523]
merge_values = [46.2379, 42.43639, 38.6333, 38.5557, 36.4897, 30.28]

# Calcul du temps total de traitement pour chaque configuration du système distribué
total_duration = [sum(x) for x in zip(
    map_values, shuffle_values, reduce_values, tri_values, merge_values)]

# Tracer les courbes
plt.figure(figsize=(8, 6))

# Courbe du système séquentiel (temps constant)
plt.axhline(y=seq_total_duration, color='r',
            linestyle='--', label='Système séquentiel')

# Courbe du système distribué (temps en fonction du nombre de machines)
plt.plot(num_machines, total_duration, marker='o', label='Système distribué')

plt.xlabel('Nombre de machines')
plt.ylabel('Temps total de traitement ')
plt.title('Comparaison du temps de traitement entre séquentiel et distribué (fichier de 670MB)')
plt.legend()
plt.grid(True)
plt.show()
