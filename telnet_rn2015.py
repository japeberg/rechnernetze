import socket

HOST = ''
PORT = 8083

woerter = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket created"

s.bind((HOST, PORT))

s.listen(10)

def recvline(conn) :
    data = ''
    while 1:
        d=conn.recv(1)
        if d == '\n':
            break
        if d != '\r':
            data = data + d
    return data


while 1:
    conn, addr = s.accept()
#    wort = conn.recv(1024)
    wort = recvline(conn)
    print wort
    print woerter
    if woerter.has_key(wort):
        woerter[wort]+=1
	print "IF-ZWEIG"
    else:
        woerter[wort]=1
	print "Else-ZWEIG"
    print woerter
    output = str(woerter[wort])
    conn.send(output)
    conn.close()
s.close()
