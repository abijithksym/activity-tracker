#!/usr/bin/env python
import socket
 

TCP_IP = '127.0.0.1'
TCP_PORT = 9090
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Starting Server::::::")
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)
conn, addr = s.accept()
print('Connection address:', addr)
while True:
	data = conn.recv(BUFFER_SIZE)
	print("received data:", data.decode())
	reply=(b'msg received')
	conn.send(reply)  # echo
# conn.close()