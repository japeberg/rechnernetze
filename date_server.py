

import socket
import datetime

s_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#an Port...    binden, weil...
s_http.bind(('',8081 ))
#Parameter 10,weil...
s_http.listen(10)

#vorgegebene Funktion
def recvline(conn) :
    data = ''
    while 1:
        d=conn.recv(1)
        if d == '\n':
            break
        if d != '\r':
            data = data + d
    return data

#dynamischen html Inhalt erzeugen
def http_response_status(conn,status,content):
    conn.send("HTTP/1.1 " + status + "\r\n\r\n")
    conn.send("<html><head></head><body>")
    conn.send(content)
    conn.send("</body></html>\r\n\r\n")


while 1:
    conn, addr = s_http.accept()
    request = []
    request.append(recvline(conn))
    while 1: 
        request.append(recvline(conn))
        #Test auf Leerzeile
        if request[-1] == '':
            break
    #quasi GET Zeile spliten
    temp = request[0].split()
    path = temp[1]
    if path == '/index.html':
	   output = "Zeit\n" + str(datetime.datetime.now())
	   status = "200 OK"

    else:
	   output = "Not Found\nThe requested URL " + path + " was not found on this server."
	   status = "404 Not Found"
	
    http_response_status(conn,status,str(output))
    conn.close()
s_http.close()
