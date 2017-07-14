import socket
import time

HOST = ''
PORT = 8088

woerter = {}

s_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_pop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

# Funktion um einen Informationsblock (endet auf '.') auszulesen
def read_pop(conn):
    liste = []
    while 1:
        liste.append(recvline(conn))
        if liste[-1] == '.':
            break
    return liste

def pop_pull():
    s_pop.connect(("dem.informatik.tu-chemnitz.de",110))
    liste = []
#    liste.append(recvline(s_pop))
    s_pop.send("USER rot\r\n")

    s_pop.send("PASS rot\r\n")
    s_pop.send("LIST \r\n")
#    print type(s_pop)
    liste = read_pop(s_pop)
    temp_counter = liste[-2].split()
    counter = temp_counter[0]
    counter = int(counter)
    print counter
    print liste
    temp = counter*(-1)-2
# Es wird die letzte Zeile mit Inhalt betrachtet und die ID der letzten Email genutzt um ein For-schleife zu schreiben, die von der ersten bis zur letzten Email durchiteriert
# Dafuer wird counter negiert und -2 gerechnet. -2 da wir an der zweit letzten Position der Liste enden wollen (Listenende ist -1)
    for e in range(counter):
       temp= temp+1
       print liste[temp]

    mails = []
    for e in range(counter):
        # .send Methode kann nur strings aufnehmen
        temp = str(e+1)
        s_pop.send("RETR "+temp+"\r\n")
        # Man braucht einen String fuer join daher ""
        mails.append("".join(read_pop(s_pop)))
    print mails
    s_pop.close()
    return mails

def http_response(conn, content):
    # Antwort an den Browser
    conn.send("HTTP/1.1 200 OK\r\nDate: Wed, 11 Apr 2012 21:29:04 GMT\r\nServer: Python/6.6.6 (custom)\r\nContent-Length:1024\r\nContent-Type: text/html\r\n\r\n")
    conn.send("<html><head></head><body>")
    conn.send(content)
    conn.send("</body></html>\r\n\r\n")
    

mails = pop_pull()

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
   
    if path == '/':
        output = "<h1>Emails</h1><br>"
        for e in range(len(mails)):
            output = output+'<a href="/'+str(e)+'">Email '+str(e+1)+'</a><br>'
        http_response(conn,output)
    else:
        output = '<h1>Emails '+path[1:]+'</h1><br>'
        output = output+mails[int(path[1:])]

        http_response(conn,output)
        
        

    conn.close()
s_http.close()
