import re
import time



def func_split(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()  # Lire tout le contenu du fichier
            mots = re.findall(r'\b\w+\b', contenu)  # Utilisation d'une expression régulière pour trouver tous les mots
            return mots
    except FileNotFoundError:
        return "Le fichier n'a pas été trouvé."


def reduce_function(shuffle_list, reduce_dict):
    for element in shuffle_list:
        if element in reduce_dict:
            reduce_dict[element] += 1
        else:
            reduce_dict[element] = 1

def trier_dict(dict_entree):
    
    sorted_dict = dict(sorted(dict_entree.items(), key=lambda item: (-item[1], item[0])))

    return sorted_dict

reduce_dict = {} 
nom_fichier = 'file_to_split/fichier_a_traiter.txt'


start_time1 = time.time()
list_shuffle = func_split(nom_fichier)
end_time1 = time.time()

dure_map = end_time1 - start_time1
print(f'la durée du map est {round((dure_map),5)} ')

start_time2 = time.time()
reduce_function(list_shuffle,reduce_dict)
end_time2 = time.time()

dure_reduce = end_time2 - start_time2
print(f'la durée du reduce est {round((dure_reduce),5)} ')

start_time3 = time.time()
sorted_dict = trier_dict(reduce_dict)
end_time3 = time.time()

dure_tri = end_time3 - start_time3
print(f'la durée du tri est {round((dure_tri),5)} ')



print(f'le traitement séquentiel a duré {round((dure_map + dure_reduce + dure_tri),5)} ')

fichier_resultat = 'resultats_sequentiel/resultat_sequentiel_200MB' +  '.txt'
with open(fichier_resultat, 'w', encoding = 'utf-8') as file:
    file.write(f'le map a duré {str(round((dure_map),5))} secondes ' + '\n')
    file.write(f'le reduce a duré {str(round((dure_reduce),5))} secondes  ' + '\n')
    file.write(f'le tri a duré {round((dure_tri),5)} secondes  ' + '\n' )
    file.write(f'le traitement séquentiel a duré {round((dure_map + dure_reduce + dure_tri),5)} ' + '\n')  
    file.write(f'veuillez trouver le résultat final ci-dessous :' + '\n')  
    file.write('\n')   
# Écriture des éléments de la liste dans le fichier
    for key, value in sorted_dict.items():
        file.write(f"{key}: {value}\n")

    file.close()
