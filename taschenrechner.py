####SERVER-Teil der Aufgabe####

import socket

HOST = ''
PORT = 8091

s_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket created"

s_http.bind((HOST,PORT ))
# 13333 ist ausgehender Port. Wahl beliebig ab) fuenfstellig

s_http.listen(10)

def recvline(conn) :
    data = ''
    while 1:
        d=conn.recv(1)
        if d == '\n':
            break
        if d != '\r':
            data = data + d
    return data

def http_response(conn, content):
    # Antwort an den Browser
    conn.send("HTTP/1.1 200 OK\r\nDate: Wed, 11 Apr 2012 21:29:04 GMT\r\nServer: Python/6.6.6 (custom)\r\nContent-Length:1024\r\nContent-Type: text/html\r\n\r\n")
    conn.send("<html><head></head><body>")
    conn.send(content)
    conn.send("</body></html>\r\n\r\n")
    
while 1:
    conn, addr = s_http.accept()
    request = []
    request.append(recvline(conn))
    while 1: 
        request.append(recvline(conn))
        if request[-1] == '':
            break
    temp = request[0].split()
    path = temp[1]
    #path = path[1:]
    print path
    parts = path.split("/")
    parts[2] = int(parts[2])
    parts[3] = int(parts[3])
    output = 0
    if parts[1] == "add":
        output = parts[2]+parts[3]
    elif parts[1] == "sub":
        output = parts[2]-parts[3]
    elif parts[1] == "mul":
        output = parts[2]*parts[3]

    http_response(conn, str(output))


    conn.close()
s_http.close()
