from threading import Thread, Lock
import socket
import time

REQUEST = "1"
GRANT = "2"
RELEASE = "3"

server = ("127.0.0.1", 8080)
buffer_size = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def process(prcss, content, k, r):
    UDPClientSocket.sendto(str.encode(f"{REQUEST}|{prcss}|{content}"), server)

    for ri in range(r):

        loop_rcv = True
        while loop_rcv:
            rcv = UDPClientSocket.recvfrom(buffer_size)
            message = rcv[0].decode()
            address = rcv[1]
            message = message.split("|")
            msg = message[0]
            prcss_rcv = message[1]
            print(msg, prcss_rcv, prcss, prcss_rcv == prcss)
            if (msg == GRANT) and (prcss_rcv == prcss):
                # escrever no arquivo
                UDPClientSocket.sendto(str.encode(f"{RELEASE}|{prcss}|{content}"), server)
                loop_rcv = False
        time.sleep(k)

if __name__ == "__main__":
    n = int(input("n: "))
    r = int(input("r: "))
    k = int(input("k: "))

    for ni in range(n):
        Thread(target=process, args=(ni, "00000", k, r)).start()