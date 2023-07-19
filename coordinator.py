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
    while True:
        in_terminal = input("Input terminal: ")
        if in_terminal == "1":
            with queue_lock:
                print("Fila de pedidos atual:")
                for item in queue:
                    print(item)

        elif in_terminal == "2":
            with processes_lock:
                print("Quantas vezes cada processo foi atendido:")
                for processo, contador in processes.items():
                    print(f"Processo {processo}: {contador} vezes")
        elif in_terminal == "3":
            break

def coordinatorListener():
    while True:
        rcv = UDPServerSocket.recvfrom(buffer_size)
        message = rcv[0].decode()
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
        with queue_lock:
            if queue:
                msg, prcss, content, address = queue.pop(0)
            else:
                continue

        file_lock.acquire()
        
        with processes_lock:
            if prcss not in processes:
                processes[prcss] = 1
            else:
                processes[prcss] += 1

        UDPServerSocket.sendto(f"{GRANT}|{prcss}|{content}".encode(), address)


if __name__ == "__main__":
    Thread(target=terminalThread).start()
    Thread(target=coordinatorListener).start()
    Thread(target=coordinatorManager).start()
