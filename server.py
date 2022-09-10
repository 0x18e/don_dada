import socket



recv = socket.socket()

ip = socket.gethostname()

recv.bind((ip, 44444))

recv.listen(2)

print("Your depression is getting worse....")

while True:

    conn, addr = recv.accept()

    print(f"{addr} has connected")
