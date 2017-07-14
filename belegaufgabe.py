import socket

HOST = ''
PORT = 8088

s_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_pop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Socket created"

# Muss Werte als Tupel uebergeben bekommen
s_http.bind((HOST,PORT ))


s_http.listen(10)

# vorgegebene Funktion
def recvline(conn) :
    data = ''
    while 1:
        # Empfaengt genau ein Byte
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
        if liste[-1] == '.':    # Wenn bei Pop in einer Zeile nur ein Punkt steht, dann ist es das Ende der E-Mail
            break
    return liste

def pop_pull():
    s_pop.connect(("dem.informatik.tu-chemnitz.de",110))
    liste = []
    s_pop.send("USER rot\r\n")
    s_pop.send("PASS rot\r\n")
    s_pop.send("LIST \r\n")
    liste = read_pop(s_pop)
    temp_counter = liste[-2].split() 
    counter = temp_counter[0]   # Hier steht dann die 3 drin
    counter = int(counter)
    print counter
    print liste
    temp = counter*(-1)-2
    # Es wird die letzte Zeile mit Inhalt betrachtet und die ID der letzten Email genutzt um ein For-schleife zu schreiben, die von der ersten bis zur letzten Email durchiteriert
    # Dafuer wird counter negiert und -2 gerechnet. -2 da wir an der zweit letzten Position der Liste enden wollen (Listenende ist -1)
    for e in range(counter):
       temp= temp+1 # temp startet bei -5
       print liste[temp]
    mails = []
    for e in range(counter):
        # .send Methode kann nur strings aufnehmen
        temp = str(e+1)
        s_pop.send("RETR "+temp+"\r\n") # RETR <id> liefert den Head und Body einer Email 
        # Man braucht einen String fuer join daher ""
        mails.append("".join(read_pop(s_pop)))
    s_pop.close()
    return mails

# Antwort an den Browser
def http_response(conn, content):
    # HTTP-Status Code uns Beispielheader. Header sind optional (Date, Server, etc.)
    conn.send("HTTP/1.1 200 OK\r\nDate: Wed, 11 Apr 2012 21:29:04 GMT\r\nServer: Python/6.6.6 (custom)\r\nContent-Length:1024\r\nContent-Type: text/html\r\n\r\n")
    conn.send("<html><head></head><body>")
    conn.send(content)
    conn.send("</body></html>\r\n\r\n")
    # \r\n wird doppelt benutzt, da zur Terminierung eine Leerzeile notwendig ist
    
# Beginn unseres Programms
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
    path = temp[1] # [1] beinhaltet die /<file>-Angabe
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
