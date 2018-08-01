
import paho.mqtt.client as mqtt
import time, datetime
import socket

#first line we are declaring variable to control the connection state
#second line assgin the variable to connect to ip address of mqtt server
#third line obviously for port and the other two lines for creating a user and password

# sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# result = sock.connect_ex(('174.19.0.20',1883))#
	
# if result ==0:
# 	print "The following ports have been scanned"

# else:
# 	print "Ports are closed"

ports = [1883,8883,8884]
openPorts=[]
for i in ports:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = sock.connect_ex(('174.19.0.20',i))

    if result==0:
	print "Port " +str(i)+"  is open"
	openPorts.append(i)
    else: 
        print "Port " +str(i)+ " is closed"

userSelection = int(raw_input("Which port do you wish to connect to? make sure choose an open port."))

if userSelection not in openPorts:
	raise ValueError('You must use an existing and open port number.') 
	exit() 

port = userSelection

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

    
 
Connected = False   #global variable for the state of the connection


mydict = {}
topics= {}
info= {}


	
def on_message(client, userdata, message):
    #print("received message = %s - %s"%(message.topic,str(message.payload)))
    #mydict[message.topic]=message.payload	

    
    
    parts=message.topic.split("/")
    #print (parts)
    if parts[0]=="$SYS":
        if parts[2] == "clients" and parts[3] == "connected":
	    info["connected"]=int(message.payload)
        elif parts[2] == "clients" and parts[3] == "maximum": 
	    info["maximum"]=int(message.payload)
        elif parts[2] == "clients" and parts[3] == "active":
	    info["active"]=int(message.payload)
        elif parts[2] == "version":
	    info["version"]=message.payload

    if message.topic in topics:
        topics[message.topic]+=1
    else:
        topics[message.topic]=1
    
#Ask user for address to connect to BEFORE port selection
server_selection = int(raw_input("Please type the server you wish to connect to "))
mqttServer_address = server_selection
mqttServer_address= "174.19.0.20"
cl_name="Monitor"
client = mqtt.Client(cl_name)   #creating a client
client.on_connect= on_connect  #callback funcation
print("connecting to server ",mqttServer_address)
client.connect(mqttServer_address, port=port)
client.on_message=on_message
print("subscribing")
client.subscribe("$SYS/#")  
#client.subscribe([("$SYS/broker/messages/stored/#", 0), ("$SYS/broker/clients/connected/#", 0)])
client.subscribe("#")




#info= ("$SYS/broker/clients/connected ")


client.loop_start()         #starting the loop


while True:
    print " -----x INFO x----"
    for item in info:
	print item,info[item]    

    print " ----x TOPICS x----"
    dolltops=0
    for t in topics:
        if t.startswith("$"):
            dolltops+=topics[t]
        else:
            print "%s \t : %d"%(t,topics[t])
    print "Dollar topics \t :",dolltops
    time.sleep(3)
    print "------------------"\
    #Show only the current number of connected clients
    #Show the number of stored messages
    #Show the actual stored messages - how?
    #Add a second dictionary of all messages (subscribe to #)
    

client.disconnect()
client.loop_stop()
