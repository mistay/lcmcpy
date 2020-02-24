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
import socketpair

class Singleton:
   __instance = None
   agentEvents = None

   @staticmethod 
   def getInstance():
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance
   def __init__(self):
      if Singleton.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self
         self.agentEvents = threading.Event()
         self.agentResponse = ''

class MyWebserver():
    def __init__(self):
        self.event = threading.Event()

    def run(self):
        print('starting server...')
        server_address = ('127.0.0.1', 8080)
        httpd = ThreadingHTTPServer(server_address, MyWebserver_RequestHandler)
        print('running server...')
        httpd.serve_forever()
        
class MyWebserver_RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # handle controller connection
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode('utf-8')
        print("path: %s body: %s " % (self.path, post_body))
        self.send_header('Content-type','text/html')
        message = ''
        if 'control' in self.path:
            Singleton.getInstance().agentResponse = post_body
            Singleton.getInstance().agentEvents.set()
            message = "control done."
        elif 'portforward' in self.path:

            socketpair.Socketpair.run(12000)

            Singleton.getInstance().agentResponse = post_body
            Singleton.getInstance().agentEvents.set()
            message = "portforward done."
        else:
            message = self.index()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        # handle agent connection
        self.send_response(200)

        if 'agent' in self.path:
            Singleton.getInstance().agentEvents.wait()
            Singleton.getInstance().agentEvents.clear()
            self.send_header('Content-type','application/json')
            message = Singleton.getInstance().agentResponse
            pass
        else:
            self.send_header('Content-type','text/html')
            message = self.index()

        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def index(self):
        message = ""
        message += "<!DOCTYPE html><html lang=\"de\"><head><title>Title goes here.</title>\n";
        message += "<meta charset=\"utf-8\">\n";
        message += "<script>\n";
        message += "function post(url, data) {\n";
        message += "    if (data=='') data='{\"portforward\": {\"12000\":\"localhost:3389\", \"12347\":\"localhost:3389\"}}' \n";
        message += "    var xhttp = new XMLHttpRequest();\n";
        message += "    xhttp.open('POST', url, true);\n";
        message += "    xhttp.send(data);\n";
        message += "}\n";
        message += "</script>\n";
        message += "</head>"
        message += "<body>"
        message += "<p><a href=\"#\" onclick=\"post('portforward', '');\">portforward</a></p>"
        message += "<p><a href=\"#\" onclick=\"post('control', '{&quot;cmd&quot;: &quot;putty&quot;}')\">rpc</a></p>"
        message += "</body>"
        return message
