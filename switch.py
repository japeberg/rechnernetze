
keys = range(256) #Empfaenger
values = [0] * 256  #Ausgangsports, alle noch unbekannt
# zip() fuegt zwei Listen im reißverschlussverfahren zu einem dict zusammen
address_table = dict(zip(keys, values)) #{Empfaenger:Ausgangsport}

program = 1
port_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}

while(program == 1):
    user_input = input("Bitte Eingangsportnummer (1..N), Absenderadresse (1..255) und Zieladresse (1..255) eingeben, z. B. '1 2 3'\n")
    if user_input == 'a': #Abbruch des Programms
        print ("hallo", address_table.items())
        for receiver, port in address_table.items():
            if port > 0:
                port_dict[port].append(receiver)

        for key in port_dict:
            print(key, ':', port_dict[key])

        #for key in address_table.keys():
        #    if
        #    print(key, ":", address_table[key])
        #    program = 0 #verhindert neuen Prompt/beendet Programm

    else:

        list_input = user_input.split(' ')

        port_in = int(list_input[0])
        sender = int(list_input[1])
        empfaenger = int(list_input[2])

        if (address_table[empfaenger] == 0) or (address_table[empfaenger] == 255): #broadcasting oder Ausgangsport unbekannt
                print("Ausgabe auf allen Ports")

        else:
            print("Ausgabe auf Port", address_table[empfaenger])

        address_table[sender] = port_in #sich den Port merken, von dem der Sender in den Switch kam, damit man spaeter dorthin senden kann

