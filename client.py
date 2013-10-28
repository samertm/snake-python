import socket
import sys

HOST, PORT = "samertm.com", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.connect((HOST, PORT))



                 
