import socket
import sys
import time
#from time import gmtime, strftime


PORT_NUMBER = 5007
HOST_NAME = ""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_NAME,PORT_NUMBER))
server_socket.listen(5)
SIZE = 512
#strftime("%Y-%m-%d %H:%M:%S", gmtime())

def log(_s):

    logfile = open('logs/[%s].log' % (time.strftime("%Y-%m-%d")), 'a')
    s = '[%s] %s' % (time.strftime("%Y-%m-%d %H:%M:%S"), _s)
    logfile.write(s + '\n')
    logfile.flush()
    print s


while True:
        client_socket, address = server_socket.accept()
        data = client_socket.recv(SIZE)
        #print strftime("%Y-%m-%d %H:%M:%S", gmtime()) ,
        log(data)
sys.ext()
