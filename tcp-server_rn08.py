import socket, sys
from _thread import *

# Funktion um Daten in einer Verbindung aufzunehmen
def clientthread(conn):
    data = conn.recv(1024)
    mitarbeiter.append(data.decode("utf-8"))
    ausgabe = ''.join(str(e) for e in mitarbeiter)
    print (ausgabe)
    conn.sendall(data)
    conn.close()


HOST = ''
PORT = 51235

mitarbeiter=[]

# Erstellt ein Socketobjekt
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

try:
    # bindet das Socketobjekt an einen Socket (IP+PORT)
    s.bind((HOST, PORT))
# Falls Bindung nicht funktioniert
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

# Bestimmt die Warteschlange des Sockets
s.listen(10)
print ('Socket now listening')

while 1:
    # .accept() wartet bis eine Verindung aufgebaut wurde
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    # startet den clientthread in einem getrennten Thread
    start_new_thread(clientthread ,(conn,))

s.close()
