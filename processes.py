from threading import Thread
import socket
import time
from datetime import datetime

REQUEST = "1"
GRANT = "2"
RELEASE = "3"

server = ("127.0.0.1", 8080)
buffer_size = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def process(prcss, content, k, r):
    for ri in range(r):
        UDPClientSocket.sendto(str.encode(f"{REQUEST}|{prcss}|{content}"), server)
        loop_rcv = True
        while loop_rcv:
            rcv = UDPClientSocket.recvfrom(buffer_size)
            message = rcv[0].decode()
            address = rcv[1]
            message = message.split("|")
            msg = message[0]
            prcss_rcv = message[1]
            if (msg == GRANT) and (prcss_rcv == prcss):
                with open('resultado.txt', 'a') as f:
                    f.write(f"{prcss} | {datetime.now().strftime('%H:%M:%S.%f')}\n")
                UDPClientSocket.sendto(str.encode(f"{RELEASE}|{prcss}|{content}"), server)
                loop_rcv = False
        time.sleep(k)

if __name__ == "__main__":
    n = int(input("n: "))
    r = int(input("r: "))
    k = int(input("k: "))

    for ni in range(n):
        Thread(target=process, args=(str(ni), "00000", k, r)).start()