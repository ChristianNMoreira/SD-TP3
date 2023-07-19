from threading import Thread, Lock
import socket

REQUEST = "1"
GRANT = "2"
RELEASE = "3"

IP = "127.0.0.1"
Port = 8080
buffer_size = 1024

queue_lock = Lock()
file_lock = Lock()
processes_lock = Lock()

queue = []
processes = {}

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((IP, Port))

def terminalThread():
    loop_terminal = True
    while loop_terminal:
        in_terminal = input("Input terminal: ")
        if in_terminal == "1":
            print("fila de pedidos atual")
        if in_terminal == "2":
            print("quantas vezes cada processo foi atendido")
        if in_terminal == "3":
            loop_terminal = False

def coordinatorListener():
    while True:
        rcv = UDPServerSocket.recvfrom(buffer_size)
        message = rcv[0]
        address = rcv[1]
        message = message.split("|")
        msg = message[0]
        prcss = message[1]
        content = message[2]
        if msg == REQUEST:
            queue_lock.acquire()
            queue.append((msg, prcss, content, address))
            queue_lock.release()
        if msg == RELEASE:
            file_lock.release()

def coordinatorManager():
    while True:
        queue_lock.acquire()
        queue_first = queue.pop(0)
        queue_lock.release()
        msg, prcss, content, address = queue_first
        file_lock.acquire()
        processes_lock.acquire()
        if not prcss in processes:
            processes[prcss] = 1
        else:
            processes[prcss] += 1
        processes_lock.release()
        UDPServerSocket.sendto(f"2|{prcss}|{content}", address)


if __name__ == "__main__":
    Thread(target=terminalThread).start()
    Thread(target=coordinatorListener).start()
    Thread(target=coordinatorManager).start()