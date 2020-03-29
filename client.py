##################
# Client Side.
##################
import _thread
import socket
import tkinter

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE=1024 #used for packets

#the chat_log has its deafault size so we need to multiply it everytime its close to the maximum
#in both recv and send threads (creating a function that both will use).

###
#root=tkinter.Tk()
#text=tkinter.Entry(root,)
#text.place(x=100,y=100)
#chat_log=tkinter.Listbox(root,)
#chat_log.place=(x=210,y=210)
#text.bind("<Enter>",)##
###



#connecting section
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting To The Server...")
s.connect((HOST, PORT))
print("Logged In!")

#receives other users' messages from the server
def client_recv():
    while(True):
        message = s.recv(BUFFER_SIZE).decode()
        #to do: change the presenting way duo to the new gui format
        print(message)

#sends the client's packet
def client_sender():
    while(True):
        #to do: scan the message via the textbox and not the regular input function.
        s.send(input().encode())

#both actions run parallely
_thread.start_new_thread(client_recv,())
_thread.start_new_thread(client_sender,())

while(True): #busy wait.
    pass
