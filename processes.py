from threading import Thread, Lock
import socket

server = ("127.0.0.1", 8080)
buffer_size = 1024