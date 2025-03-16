import os





def create_splits(file_path, num_splits, output_folder):
    with open(file_path, 'r') as file:
        content = file.read()

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunk_size = len(content) // num_splits
    remainder = len(content) % num_splits

    start = 0
    for i in range(num_splits):
        end = start + chunk_size + (1 if i < remainder else 0)
        split_file_name = f"S{i}.txt"
        split_file_path = os.path.join(output_folder, split_file_name)
        with open(split_file_path, 'w') as split_file:
            split_file.write(content[start:end])
        print(f"Fichier '{split_file_path}' créé avec les données correspondantes.")
        start = end

# Création des splits à partir du fichier donné
create_splits('file_to_split/nom_du_fichier.txt', 8, 'splits')  # 3 splits dans un dossier 'splits_folder'
