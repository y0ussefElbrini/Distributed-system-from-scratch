import socket
import os
import struct
import traceback
import time
import pickle




global final_list
final_list =[] 


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

def trier_dict(dict_entree):
    
    sorted_dict = dict(sorted(dict_entree.items(), key=lambda item: (-item[1], item[0])))

    return sorted_dict



def main():

    hosts = open_file ('machines.txt')
    port = 60002 # replace with the server port number
    sockets =[] 

    for i, h in enumerate(hosts):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((h, port))
            sockets.append(client_socket)

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

      
    for i, h in enumerate(hosts):
        try:

            # send file
            filename = 'machines.txt'
            filesize = os.path.getsize(filename)
            message = 'listmachines'
            send_one_message(sockets[i],message.encode())
            send_one_message(sockets[i],filename.encode())
            send_one_message(sockets[i],str(filesize).encode())
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    send_one_message(sockets[i],data)
                    data = f.read(1024)
            response = recv_one_message(sockets[i]).decode()
            print(f'Received response: {response}')


        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    start_time1 = time.time()  
    for i, h in enumerate(hosts):
        try:

            message = 'Map'
            send_one_message(sockets[i],message.encode())

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    for i, h in enumerate(hosts):
        try:

            message_map = recv_one_message(sockets[i]).decode()
            print(f'Received response from machine {i} : {message_map}')            

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    end_time1 = time.time()
    print(f'le map a duré {round((end_time1 - start_time1),5)} secondes  ')


    start_time2 = time.time()
    for i, h in enumerate(hosts):
        try:

            message = 'Shuffle'
            send_one_message(sockets[i],message.encode())

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    for i, h in enumerate(hosts):
        try:

            message_shuffle = recv_one_message(sockets[i]).decode()
            print(f'Received response from machine {i} : {message_shuffle}')            

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    end_time2 = time.time()
    print(f'le shuffle a duré {round((end_time2 - start_time2),5)} secondes  ')

    start_time3 = time.time()
    for i, h in enumerate(hosts):
        try:

            message = 'Reduce'
            send_one_message(sockets[i],message.encode())

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    for i, h in enumerate(hosts):
        try:

            message_reduce = recv_one_message(sockets[i]).decode()
            print(f'Received response from machine {i} : {message_reduce}')            

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    end_time3 = time.time()
    print(f'le reduce a duré {round((end_time3 - start_time3),5)} secondes  ')

    print(f'le temps global de traitement sans tri est a {round((end_time3 + end_time2 + end_time1 - start_time3 - start_time2 - start_time1),5)} secondes  ')
    
    start_time5 = time.time()
    for i, h in enumerate(hosts):
        try:


            message = 'final_result'
            send_one_message(sockets[i],message.encode())
    

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()


    for i, h in enumerate(hosts):
        try:

            response1 = recv_one_message(sockets[i]).decode()
            resultat = eval(response1)
            for val in resultat:
                final_list.append(val)
            print(f'Received response from machine {i} : {len(response1)}') 
              

        except Exception as e:
            print(f'Error : {e}')
            traceback.print_exc()

    end_time5 = time.time()
    print(f'la réception du résultat de reduce de la part des machines a duré {round((end_time5 - start_time5),5)} secondes  ')
    
    final_dict = dict(final_list)

    start_time4 = time.time()
    final_dict_sorted = trier_dict(final_dict)
    end_time4 = time.time()

    print(f'le tri a duré {round((end_time4 - start_time4),5)} secondes  ')
    
    print(f'la longueur du résultat final est {len(final_dict_sorted)} ')

    fichier_resultat = 'resultats_reparti/resultat ' + str(len(hosts)) + '_machines_' + 'xxxMB' + '.txt'
    with open(fichier_resultat, 'w', encoding = 'utf-8') as file:
        file.write(f'le map a duré {str(round((end_time1 - start_time1),5))} secondes ' + '\n')
        file.write(f'le shuffle a duré {str(round((end_time2 - start_time2),5))} secondes  ' + '\n')
        file.write(f'le reduce a duré {str(round((end_time3 - start_time3),5))} secondes  ' + '\n')
        file.write(f'le tri a duré {round((end_time4 - start_time4),5)} secondes  ' + '\n' ) 
        file.write(f'le temps du merge est {end_time5 - start_time5} ' + '\n')
        file.write(f'la longeur du résultat final est{len(final_dict)} ' + '\n')
        file.write('\n')          
        file.write(f'veuillez trouver le résultat final ci-dessous :' + '\n')  
        file.write('\n')   
    # Écriture des éléments de la liste dans le fichier
        for key, value in final_dict_sorted.items():
            file.write(f"{key}: {value}\n")

        file.close()
if __name__ == '__main__':
    main()