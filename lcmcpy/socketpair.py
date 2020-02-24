from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import http.server
import atexit
import datetime
import os
import signal
import sys
import time
import socket
import threading
import socket
from threading import Thread, Lock
from queue import Queue
import time

class Sockethandler(threading.Thread):
    def run(self, c):
        while True: 
            data = c.recv(1024) 
            if not data: 
                print('Bye') 
                #self.print_lock.release() 
                break
            data = data[::-1] 
            c.send(data) 
        c.close()

class Socketpair (threading.Thread):
    def run(port):
        #self.print_lock = threading.Lock()
        host = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        print("socket bound to port", port)
  
        s.listen(5)
        print("socket is listening")

        while True: 
            c, addr = s.accept()
            #self.print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])
            Sockethandler().run(c)
        s.close() 
