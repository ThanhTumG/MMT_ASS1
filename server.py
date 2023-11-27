import socket as sk
import threading
import time

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
 
SERVER_IP = get_local_ip()
SERVER_PORT = 4004
#SERVER_IP = sk.gethostbyname(sk.gethostname())

SIZE = 1024
FORMAT = 'utf-8'

class Server:
    def __init__(self, ip, port):
        self.server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.server.bind((ip, port))
        self.server.listen()
        self.onlineClient = dict()
        self.connectedClient = dict()
        self.clientFileList = dict()

    def start(self):
        print(f"Server is listening on {self.server_ip}:{self.server_port}")
        while True:
            threading.Thread(target=self.start_request).start()
            
            client_socket, client_address = self.server.accept()
            client_name = client_socket.recv(SIZE).decode(FORMAT)
            print('\nClient ' + client_name + f' (IP Address: {client_address}) connected.')
            self.connectedClient[client_name] = client_address
            client_socket.send('_'.encode(FORMAT))
            self.onlineClient[client_name] = client_address

            threading.Thread(target=self.handle_client, args=(client_socket, client_address, client_name)).start()
            time.sleep(1)
            

    def start_request(self):
        while True:
            self.server_option()


    def server_option(self):
        print('\nEnter your command:\n> discover `hostname`: discover the list of local files of hostname\n> ping `hostname`: live check hostname')
        option = input('\nYour command: ')
        if option.startswith('discover'):
            print(self.discover(option.split(' ')[1]))
        elif option.startswith('ping'):
            print(self.ping(option.split(' ')[1]))


    def handle_client(self, client_socket, client_address, client_name):
        while True:
            
            # Receive client's requests
            try:
                client_request = client_socket.recv(SIZE).decode(FORMAT)
            except:
                print('Waiting for a request...')

            client_command, client_message = client_request.split('@')         # Client request in format `cmd@msg`
            
            if client_command != 'DISCONNECT':
                print(f"\n[{client_address}]Client's request: [{client_command}]", client_message)

            if client_command == 'PUBLISH':
                fileName = client_message.split(' ')
                if client_address in self.clientFileList:
                    fileName = fileName[0]
                    if (fileName not in self.clientFileList[client_address]):
                        self.clientFileList[client_address].append(fileName)
                        cmd = 'OK'
                        msg = 'Uploaded successfully!'
                    else:
                        cmd = 'ERROR'
                        msg = 'FileName existed in repository'
                else:
                    self.clientFileList[client_address] = fileName[:-1]
                    cmd = 'OK'
                    msg = 'Uploaded successfully!'
                
                self.send_message(client_socket, cmd, msg)
                print(msg)
                
            elif client_command == 'FETCH':
                fileName = client_message
                curClientList = list()
                for cli in self.clientFileList:
                    if fileName in self.clientFileList[cli] and cli in self.onlineClient.values():
                        curClientList.append(cli)
                if curClientList:
                    self.send_message(client_socket, 'OK', 'These are clients having the file:')
                    for client in curClientList:
                        client = client[0] + ':' + str(client[1])
                        client_socket.send(client.encode(FORMAT))
                        _ = client_socket.recv(SIZE).decode(FORMAT)
                    
                    self.send_message(client_socket, 'DONE', 'All clients are sent.')
                    self.clientFileList[client_address].append(fileName)
                    print(f'All clients are sent to [{client_address}]')
                else:
                    self.send_message(client_socket, 'ERROR', 'Filename does not exist on server.')
                    print('Filename does not exist.')

            elif client_command == 'ERROR':
                print(client_message)
            elif client_command == 'DELETE':
                fileName = client_message
                self.clientFileList[client_address].remove(fileName)

            else:
                print(f'Client {client_address} disconnected.')
                self.onlineClient.pop(client_name)
                client_socket.close()
                break
    
    def send_message(self, client_socket, cmd, msg):
        respond = cmd + '@' + msg
        client_socket.send(respond.encode(FORMAT))

    def ping(self, hostname = ''):
        if hostname not in self.connectedClient:
            return 'This host have not connected to server yet.'
        else:
            if hostname in self.onlineClient:
                output = 'Online'
            else:
                output = 'Offline'
            return output

    def discover(self, hostname = ''):
        if hostname in self.connectedClient:
            return self.clientFileList[self.connectedClient[hostname]]
        else:
            return hostname + " have not connected to server yet."

def main():
    server = Server(SERVER_IP, SERVER_PORT)
    server.start()

if __name__ == '__main__':
    main()