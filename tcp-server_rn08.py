import socket, sys
from _thread import *


HOST = ''
PORT = 51235

mitarbeiter=[]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

s.listen(10)
print ('Socket now listening')

def clientthread(conn):
    
    data = conn.recv(1024)
    mitarbeiter.append(data.decode("utf-8"))

    ausgabe = ''.join(str(e) for e in mitarbeiter)
    print (ausgabe)
    conn.sendall(data)

    conn.close()

while 1:
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(clientthread ,(conn,))

s.close()
