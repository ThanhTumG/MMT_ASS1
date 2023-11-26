import socket as sk
import os
import threading
import shutil
import time

# Enter the server's IP
# SERVER_IP = input("Enter Server's IP: ")
# SERVER_PORT = 4869

SIZE = 1024
REPOSITORY_PATH = 'repository/'
FORMAT = 'utf-8'

#SERVER_IP = sk.gethostbyname(sk.gethostname())
#SERVER_PORT = 4869

def get_local_ip():
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    try:
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class Client:
    def __init__(self, IP, port, hostname):
        self.client_socket = None
        self.server_IP = IP
        self.server_Port = port
        self.hostname = hostname
        self.isConnected = False

        self.peer_socket = None


    ##### START CONNECT TO SERVER #####
    def start(self):
        # Create local repository
        if not os.path.exists(REPOSITORY_PATH):
            os.makedirs(REPOSITORY_PATH)

        # Connect to the server
        self.client_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_IP, self.server_Port))
        except:
            print(f"Failed to connect to server: {self.server_IP}:{self.server_Port}")
            return
        self.isConnected = True
        self.client_socket.send(self.hostname.encode(FORMAT))
        _ = self.client_socket.recv(SIZE).decode(FORMAT)
        print(f"Connected to server: {self.server_IP}:{self.server_Port}")
        self.publish_all()
        self.request_thread = threading.Thread(target=self.start_request)
        self.request_thread.start()
        time.sleep(0.2)

        # Listen to other peers
        self.client_server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.client_server.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.client_server.bind((get_local_ip(), 6969))
        self.client_server.listen()
        
        self.listen_thread = threading.Thread(target=self.listening)
        self.listen_thread.start()



    def getfile_from_target_peer(self, target_IP = '127.0.0.1', target_Port = 6969, fileName = ''):
        self.peer_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        try:
            self.peer_socket.connect((target_IP, target_Port))
        except:
            print(f'Failed to connect to peer: {target_IP}:{target_Port}')
        print(f'Connected to peer: {target_IP}:{target_Port}')

        request = 'FETCH@' + fileName
        self.peer_socket.send(request.encode(FORMAT))


        #data = self.peer_socket.recv(SIZE)
        
        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        filePath += fileName
        file = open(filePath, 'wb')
        while True:
            data = self.peer_socket.recv(SIZE)
            if not data or data == 'DONE'.encode(FORMAT):
                break
            file.write(data)
            self.peer_socket.send('OK'.encode(FORMAT))
        file.close()
        print('Received ' + fileName + f' from {target_IP}')
        self.peer_socket.close()


    ##### Start send request #####
    def start_request(self):
        while self.isConnected:
            self.choosing_option()


    ##### Client choose option #####
    def choosing_option(self):

        print('Enter your command:\n> publish `lname` `fname`: Add a file named `fname` from `lname` to repository and convey to the server\n> fetch `fname`: Find some copy of the file named `fname` and add it to repository\n> quit: Disconnect from server')
        
        option = input('Your command: ')
        if option.startswith('publish'):
            lname = option.split(' ')[1]
            fname = option.split(' ')[2]
            self.publish(lname, fname)
        elif option.startswith('fetch'):
            fname = option.split(' ')[1]
            self.fetch(fname)
        elif option == 'quit':
            self.disconnect(self.client_socket, self.server_IP, self.server_Port)
            self.isConnected = False
            self.client_server.close()
            exit(0)
        else:
            print('Invalid Command')

    def quitCli(self):
        self.disconnect(self.client_socket, self.server_IP, self.server_Port)
        self.isConnected = False
        self.client_server.close()
        # exit(0)
    ####### Disconnect from server ########
    def disconnect(self, my_socket = sk.socket, other_IP = '127.0.0.1', other_Port = 4869):

        msg = f'DISCONNECT@Disconnected from server {other_IP}:{other_Port}'

        my_socket.send(msg.encode(FORMAT))
        print(msg.split('@')[1])
        my_socket.close()


    ##### Publish all file in repository when connect to server #####
    def publish_all(self):

        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        fileList = ''
        
        for file in os.listdir(filePath):
            fileList += file + ' '
        
        if fileList != '':
            msg = 'PUBLISH@' + fileList
            self.client_socket.send(msg.encode(FORMAT))
            server_respond = self.client_socket.recv(SIZE).decode(FORMAT)
            _ = server_respond.split('@')
            print('Published all file to the server.')


    def publish(self, lname = '', fname = ''):
        
        filePath = os.path.join(lname, fname)
        if not os.path.exists(filePath):
            print('This file does not exist on your system.')
        else:
            shutil.copy(filePath, os.path.join(os.getcwd(), REPOSITORY_PATH))

        msg = 'PUBLISH@' + fname
        self.client_socket.send(msg.encode(FORMAT))
        
        server_respond = self.client_socket.recv(SIZE).decode(FORMAT)
        _, server_message = server_respond.split('@')
        print(server_message)


    def fetch(self, fname = ''):

        filePath = os.path.join(REPOSITORY_PATH, fname)
        if not os.path.exists(filePath):
            msg = 'FETCH@' + fname
            self.client_socket.send(msg.encode(FORMAT))
            
            server_respond = self.client_socket.recv(SIZE).decode(FORMAT)
            server_command, server_message = server_respond.split('@')
            if server_command == 'OK':
                clientList = []
                while True:
                    clients = self.client_socket.recv(SIZE).decode(FORMAT)
                    if clients.startswith('DONE'):
                        break
                    else:
                        clientList.append(clients)
                    self.client_socket.send('Received'.encode(FORMAT))
                if (clientList):
                    print(server_message, clientList)
                    target_IP = clientList[0].split(':')[0]
                    self.getfile_from_target_peer(target_IP, 6969, fname)
                else:
                    print('File not found on the server')
                    return server_message
            else:
                print(server_message)
                return server_message

        else:
            msg = 'ERROR@File existed in repository.'
            print(msg.split('@')[1])
            return msg


    def listening(self):
        while self.isConnected:
            self.sending_to_peers()


    def sending_to_peers(self):
        try:
            other_socket, other_address = self.client_server.accept()
            print(f"Peer {other_address} connected.")
            try:
                request = other_socket.recv(SIZE).decode(FORMAT)
            except:
                print('Waiting for request...')

            #request = other_socket.recv(SIZE).decode(FORMAT)
            fileName = request.split('@')[1]
            self.transfer_file(other_socket, other_address[0], fileName)
        except:
            if not self.isConnected:
                print('CLOSE')
                exit(0)  

        
    def transfer_file(self, receiver = sk.socket, receiver_IP = '127.0.0.1', fileName = ''):
        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        filePath += fileName
        file = open(filePath, 'rb')
        while True:
            data = file.read(SIZE)
            if not data:
                receiver.send('DONE'.encode(FORMAT))
                break
            receiver.send(data)
            _ = receiver.recv(SIZE).decode(FORMAT)
        file.close()
        print('Sent ' + fileName + f' to peer: {receiver_IP}')
        receiver.close()

    def deleteFile(self, fname):
        filePath = os.path.join(REPOSITORY_PATH, fname)
        os.remove(filePath)
        msg = 'DELETE@' + fname
        self.client_socket.send(msg.encode(FORMAT))

