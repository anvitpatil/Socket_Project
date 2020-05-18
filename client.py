import socket
import threading
import time

tEv = threading.Event()
tShutdown = threading.Event()

def receving(name, sock):
    shutdown = False
    while not shutdown:
        try:
            
	    data,addr = sock.recvfrom(1024)
	    print(str(data))
            if '?' in data:
                tEv.set()
	    if "Game Over" in data :  # message from server to stop
                tShutdown.set()
                shutdown = True
	except:
            pass
        finally:
            pass

host = '127.0.0.1'
port = 0
server = (host, 7777)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))


# Start listener
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

# Join the game
print("Lets get started!!!\n")
alias = raw_input("Enter your Name: ")
s.sendto(alias,server)


running = True
while running:
    if tEv.is_set():
        tEv.clear()
        message = raw_input()
        if message != '':
            s.sendto(alias + ": " + message, server)
    if tShutdown.is_set():
        running = False

rT.join()
s.close()
