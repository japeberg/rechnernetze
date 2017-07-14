###CLIENT-Teil Taschenrechner###

import socket
user_input = ""
user_input = input("Bitte URL eingeben, z. B. http//mein.grosser.rechner.de:7829/add/12/3\n")
print user_input

list_input = user_input.split('/')
#for item in range(len(list_input)):
#	print list_input[item]
#	print "\n"

FQDN_port = list_input[2]
FQDN = FQDN_port.split(':')[0]
port = FQDN_port.split(':')[1]

print "FQDN:" + FQDN
print "port:" + port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP-Protokoll, nicht UDP
#client_socket.connect((FQDN,int(port))) #1337 = server socket
client_socket.connect(("",8091)) #1337 = server socket
client_socket.send("GET /"+list_input[3]+"/"+list_input[4]+"/"+list_input[5]+" HTTP/1.0\r\n\r\n")
data = client_socket.recv(1024)
print data
client_socket.close()
