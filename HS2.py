import socket
import sys
import time
import serial
import RPi.GPIO as GPIO
PORT_NUMBER = 5002
HOST_NAME = ""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_NAME,PORT_NUMBER))
server_socket.listen(5)
SIZE = 512

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
door = 4
big_light = 11
blue_light = 22
table_light = 17
solder_light = 10
door_state = False
big_light_state = False
table_light_state = False
solder_light_state = False
smart_plug1_state = False
GPIO.setup (door, GPIO.OUT)
GPIO.setup (big_light, GPIO.OUT)
GPIO.setup (blue_light, GPIO.OUT)
GPIO.setup (table_light, GPIO.OUT)
GPIO.setup (solder_light, GPIO.OUT)

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

def checkTemp():
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        return ser.readline()

def openDoor():
        GPIO.output(door,1)
        door_state = True

def closeDoor():
        GPIO.output(door, 0)
        door_state = False


def table_light_on():
        table_light_state = True
        GPIO.output(table_light, 1)

def table_light_off():
        table_light_state = False
        GPIO.output(table_light, 0)

        
def solder_light_on():
	solder_light_state = True
	GPIO.output(solder_light, 1)
 
def solder_light_off():
	solder_light_state = False
	GPIO.output(solder_light, 0)


def blue_light_on():
        GPIO.output(blue_light,1)
        
def blue_light_off():
        GPIO.output(blue_light,0)


def big_light_on():
        GPIO.output(big_light,1)
	big_light_state = True

def big_light_off():
        GPIO.output(big_light,0)
        big_light_state = False

def smart_plug1_change():
	global smart_plug1_state
		
        if (smart_plug1_state):
		send("light1_off", "10.0.1.37", 23)
        
        	print "smart plug1 off"
		smart_plug1_state = False
	else:
                send("light1_on", "10.0.1.37", 23)
        
		print "smart plug1 on"
		smart_plug1_state = True

def assign_var():
	smart_plug1_state = False



def send(message, address, port):
        s = socket.socket()
        host = address
        port = port
        s.connect((host,port))
        s.send(message)
        s.close()

def sendLog(String):
        message = 'HS1_______%s'% (String)
        send(message, "", 5007)


while True:
        client_socket, address = server_socket.accept()
        data = client_socket.recv(SIZE)
        #print data
        print "roger: ",
        print data
        sendLog(data)
        if (data == "temp"):
                client_socket.send(checkTemp())
        elif (data == "open_door5"):
                openDoor()
                time.sleep(5)
                closeDoor()
        elif (data == "close_door"):
                closeDoor()
        elif (data == "open_door"):
                openDoor()
        elif (data == "open_door_change"):
                if door_state :
                        closeDoor()
                else : openDoor()
        


        elif (data == "table_light_on"):
                table_light_on()
        elif (data == "table_light_off"):
                table_light_off()
	
        elif (data == "solder_light_on"):
                solder_light_on()
        elif (data == "solder_light_off"):
                solder_light_off()
        
        elif (data == "big_light_on"):
                big_light_on()
        elif (data == "big_light_off"):
                big_light_off()
        
        elif (data == "blue_light_on"):
                blue_light_on()
        elif (data == "blue_light_off"):
                blue_light_off()
        

	elif (data == "smart_plug1"):
		smart_plug1_change()
	elif (data == "start"):
		assign_var()
        elif (data == "table_light_change"):
                if table_light_state :
                        table_light_off()
                else : table_light_on()



        else :
                client_socket.send("whatever")

sys.ext()