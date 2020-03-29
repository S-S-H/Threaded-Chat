##################
# Server Side.
##################
import _thread
import socket

HOST = '0.0.0.0'
PORT = 65432
BUFFER_SIZE=1024 #used for packets

#accepts clients connections and creates a thread for each login session
def session_receiver():
    while(True):
        conn, addr = multi_server.s.accept()
        conn.send(("Welcome To The Sevrer!").encode())
        conn.send(("Enter Your Nickname: ").encode())
        _thread.start_new_thread(connect_client, (conn,addr))#used in order to be able to receive nicknames and connect users parallely

#receives a packet from any client and broadcasts to all of the online clients
def receive_and_send(conn,nickname):
    while(True):
        try:
            packet=conn.recv(BUFFER_SIZE)
            message = nickname+(": ").encode() + b' ' + packet #to be broadcasted format.
            print(message.decode())
            if(packet.decode()=="/online"): #checks if the user inserted the known command
                online_usr='Current Online Users:'+'\n'
                for client in multi_server.clients:
                    if(client[2]!=nickname): #present all of the users but the requesting one.
                        online_usr += client[2].decode() +'\n'
                conn.send(online_usr.encode())
                continue #since it wasnt a message that should be broadcasted, skip this phase and keep running.

            for client in multi_server.clients:
                if (client[2] != nickname):  # we dont want to return the message to its sender...
                    client[0].send(message)

        except socket.error:#in case someone disconnected
            ####close the socket of the disconnecting client and remove them from the DB.####
            idx=get_client_place(nickname)
            temp=multi_server.clients[idx]
            temp[0].close()
            multi_server.clients.remove(temp)
            for client in multi_server.clients:
                    client[0].send(nickname+(" Has Disconnected.").encode())

            return #terminate this client's receiver thread

#get the client's to be disconnected index (we dont use the username to identify the index since the list is dynamic)
def get_client_place(nickname):
    for client in multi_server.clients:
        if(nickname==client[2]):
            return multi_server.clients.index(client)
    return -1

#recieves every session's nickname and then logs them in and adds them to the server's database
def connect_client(conn,addr):
    nickname = conn.recv(BUFFER_SIZE) #used to recognize the messages sender
    conn.send(("Note: to check who else is online, type /online").encode())
    message = nickname.decode() + " Has Connected."
    print(message)
    for client in multi_server.clients:
        if (client[2] != nickname):  # letting all the connected users know who just logged in
            client[0].send(message.encode())

    multi_server.clients.append([conn, addr, nickname])  # adding the client to the server's database
    _thread.start_new_thread(receive_and_send, (conn, nickname))

class Server:
    def __init__(self):
        self.clients=[]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen()
        print("Server Is Up, Waiting For Clients To Connect...")
        _thread.start_new_thread(session_receiver,())#start handling users join

multi_server=Server() #inits the server object
while True:#busy wait
    pass