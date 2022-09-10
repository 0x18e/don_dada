import socket


sock = socket.socket()

sock.connect((socket.gethostname(), 44444))

