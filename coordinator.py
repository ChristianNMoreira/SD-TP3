from threading import Thread, Lock
import socket
from datetime import datetime

REQUEST = "1"
GRANT = "2"
RELEASE = "3"

IP = "127.0.0.1"
Port = 8080
buffer_size = 1024

queue_lock = Lock()
file_lock = Lock()
log_lock = Lock()
processes_lock = Lock()

queue = []
processes = {}

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((IP, Port))

def terminalThread():
    while True:
        in_terminal = input("Input terminal: ")
        if in_terminal == "1":

            queue_lock.acquire()
            print("Fila de pedidos atual:")
            for item in queue:
                print(item)
            queue_lock.release()

        elif in_terminal == "2":
            processes_lock.acquire()
            print("Quantas vezes cada processo foi atendido:")
            for processo, contador in processes.items():
                print(f"Processo {processo}: {contador} vezes")
            processes_lock.release()
        elif in_terminal == "3":
            break

def coordinatorListener():
    while True:
        rcv = UDPServerSocket.recvfrom(buffer_size)
        message = rcv[0].decode()
        address = rcv[1]
        msg, prcss, content = message.split("|")
        if msg == REQUEST:
            queue_lock.acquire()
            queue.append((msg, prcss, content, address))
            queue_lock.release()
            log_lock.acquire()
            with open('log.txt', 'a') as f:
                f.write(f"[R] REQUEST | {prcss} | {datetime.now().strftime('%H:%M:%S.%f')}\n")
            log_lock.release()
        elif msg == RELEASE:
            file_lock.release()
            log_lock.acquire()
            with open('log.txt', 'a') as f:
                f.write(f"[R] RELEASE | {prcss} | {datetime.now().strftime('%H:%M:%S.%f')}\n")
            log_lock.release()

def coordinatorManager():
    while True:
        queue_lock.acquire()
        if queue:
            msg, prcss, content, address = queue.pop(0)
        else:
            queue_lock.release()
            continue
        queue_lock.release()
        
        processes_lock.acquire()
        if prcss not in processes:
            processes[prcss] = 1
        else:
            processes[prcss] += 1
        processes_lock.release()

        log_lock.acquire()
        with open('log.txt', 'a') as f:
            f.write(f"[S] GRANT | {prcss} | {datetime.now().strftime('%H:%M:%S.%f')}\n")
        log_lock.release()

        file_lock.acquire()
        UDPServerSocket.sendto(f"{GRANT}|{prcss}|{content}".encode(), address)


if __name__ == "__main__":
    Thread(target=terminalThread).start()
    Thread(target=coordinatorListener).start()
    Thread(target=coordinatorManager).start()