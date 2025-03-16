import socket
import threading
import struct
import traceback
import time
import os
import hashlib
import re
import pickle
from collections import defaultdict

global map_list
map_list =[] 

global shuffle_list
shuffle_list =[]

global reduce_dict
reduce_dict = {}

global list_machines_recu
list_machines_recu = []  

def divide_chunks(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def func_split(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()  # Lire tout le contenu du fichier
            mots = re.findall(r'\b\w+\b', contenu)  # Utilisation d'une expression régulière pour trouver tous les mots
            return mots
    except FileNotFoundError:
        return "Le fichier n'a pas été trouvé."

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def open_file(file):
    with open(file,'r',encoding='utf-8' ) as f:
        text_content = f.read()
        machine_list=text_content.split('\n')
        machine_list=[item.strip() for item in machine_list if item.strip()]
    return machine_list

def calculate_hash(value):
    return hash(value) % 3 + 1

def custom_hash(word, nombre_machines):
    hash_val = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16) % nombre_machines
    return hash_val

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    if lengthbuf is None:
        return b''  # Return an empty bytes-like object in case of error
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    fragments = []
    while count: 
        chunk = sock.recv(count)
        if not chunk: 
            return None
        fragments.append(chunk)
        count -=len(chunk)
    arr = b''.join(fragments)
    return arr

def map_function(input_file):
    with open(input_file, 'r') as file:
        words = file.read().split()
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        return list(word_count.items())
    
def reduce_function(shuffle_list, reduce_dict):
    for element in shuffle_list:
        if element in reduce_dict:
            reduce_dict[element] += 1
        else:
            reduce_dict[element] = 1
    
def handle_client(client_socket, address):
    global list_machines_recu
    print(f'{socket.gethostname()} New client connected: {address}')
    try:
        while True:

            data = recv_one_message(client_socket)
            if not data:
                break
            message = data.decode().strip().lower() # convert message to lowercase
            print(f'{socket.gethostname()} Received message from {address}: {message}')
            
            if message == 'hello':
                response = 'hello'
                send_one_message(client_socket,response.encode())

            elif message == 'listmachines':
                # receive filename
                filename = recv_one_message(client_socket).decode().strip()
                print(f'{socket.gethostname()} Received filename from {address}: {filename}')
            
                # receive filesize
                filesize = int(recv_one_message(client_socket).decode().strip())
                print(f'{socket.gethostname()} Received filesize from {address}: {filesize}')

                # receive file data
                with open(filename, 'wb') as f:
                    remaining_bytes = filesize
                    while remaining_bytes > 0:
                        data = recv_one_message(client_socket)
                        if not data:
                            break
                        f.write(data)
                        remaining_bytes -= len(data)

                list_machines_recu = open_file(filename)
                print(f'la liste des machines reçues est{list_machines_recu}' )
                print(f'{socket.gethostname()} Received the entire file from {address}: {filesize}')
                response = 'listmachines received'
                send_one_message(client_socket,response.encode())

            elif message == 'go':

                print("Traitement GO") 
                # Avoir le hostname local
                hostname = socket.gethostname()
                # Avoir l'adresse IP locale
                ip_address = socket.gethostbyname(hostname)
                machine_name, _, _ = socket.gethostbyaddr(ip_address)
                print(f"my hostname is {machine_name}")
                          
                for l in list_machines_recu: # Exclut l'adresse IP de la machine actuelle
                    if l != machine_name:    
                        client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket1.connect((l, port))
                        message = 'Bonjour'
                        send_one_message(client_socket1, message.encode())
                        print(f'{machine_name} Sent "Bonjour" to {l}')
                        time.sleep(2)
    
            elif message == 'map':

                hostname = socket.gethostname()
                # Get the local IP address
                ip_address = socket.gethostbyname(hostname)
                machine_name, _, _ = socket.gethostbyaddr(ip_address) 
                # Définition du chemin du dossier  
                path = '/tmp/yelbrini-23/adeployer/splits/'
                # affecter l'index du nom de la machine en question à idx_machine 
                idx_machine = list_machines_recu.index(machine_name) 
                # créer le nom du fichier à partir de l'index de la machine 
                nom_fichier = path + 'S' + str(idx_machine) + '.txt'
                # affecter la liste des mots splités à la list global de map déjà définie
                map_list = func_split(nom_fichier)
                # Envoie du message MAP OK au client afin qu'il entame la phase suivante                
                message_map = 'map fini sur machine' + str(idx_machine)
                send_one_message(client_socket,message_map.encode())

            elif message == 'bye':
                break

            elif message == 'pseudo_shuffle':
                response1 = recv_one_message(client_socket).decode()
                resultat = eval(response1)
                shuffle_list.extend(resultat)

            elif message == 'shuffle':

                print(f"Voici la liste sur laquelle sera basée l'étape de shuffle: {len(map_list)}")

                # Création d'un dictionnaire pour regrouper les mots selon le résultat de hash
                word_dict = defaultdict(list)
                for value in map_list:
                    server_number = custom_hash(value, len(list_machines_recu))
                    word_dict[server_number].append(value)
                
                # Envoi des groupes de mots aux serveurs concernés
                for server_number, words in word_dict.items():
                    server_address = list_machines_recu[int(server_number)]
                    client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket1.connect((server_address, port))
                    message = 'pseudo_shuffle'
                    send_one_message(client_socket1, message.encode())
                    # Envoi de tous les mots du groupe
                    send_one_message(client_socket1, str(words).encode())
                    
                # Envoyer un message global 'Shuffle OK' au client
                message_shuffle = 'Shuffle OK'
                send_one_message(client_socket, message_shuffle.encode())
                
                # Affichage de la liste shuffle pour ce serveur
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                machine_name, _, _ = socket.gethostbyaddr(ip_address) 
                print(f"La liste shuffle pour le serveur {machine_name} contient {len(map_list)} mots.")

            elif message == 'reduce':

                reduce_function(shuffle_list, reduce_dict)
                message_reduce = 'reduce OK'
                send_one_message(client_socket,message_reduce.encode())
                print(f"le calcul de reduce est{reduce_dict} ")

            elif message == 'final_result':
             
                list1 = list(reduce_dict.items())
                send_one_message(client_socket,str(list1).encode())


    except Exception as e:
        print(f'{socket.gethostname()} Error handling client {address}: {e}')
        traceback.print_exc()
    finally:
        client_socket.close()
        print(f'{socket.gethostname()} Client disconnected: {address}')

def start_server(port):
    # Initialize machine_ips as an empty list
    machine_ips = []    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()
        print(f'{socket.gethostname()} Server listening on port {port}')

        while True:
            client_socket, address = server_socket.accept()
            print(f'{socket.gethostname()} Accepted new connection from {address}')
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except Exception as e:
        print(f'{socket.gethostname()} Error starting server: {e}')
        traceback.print_exc()
    finally:
        server_socket.close()

if __name__ == '__main__':
    port = 60002 # pick any free port you wish that is not used by other students
    start_server(port)
