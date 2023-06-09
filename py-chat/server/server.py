from socket import *
import socket
import threading
import time
import sys
import json
import logging
import os
from chat import Chat

from session import Manager, Session
from handler import AuthHandler, CoreHandler

SERVER_IP=os.getenv('SERVER_IP') or "0.0.0.0"
SERVER_PORT=os.getenv('SERVER_PORT') or "8889"

chatserver = Chat()

class ProcessTheClient(threading.Thread):
     def __init__(self, connection, address):
          self.connection = connection
          self.address = address
          self.current = None
          self.next = None
          self.session = Session()
          self.session.connect(self.connection)
          threading.Thread.__init__(self)

     def push_back(self, handle):
          if self.current is None:
               self.current = handler
               self.next = handler
          else:
               self.next.handle_next(handler)
               self.next = handler

     def run(self):
          #rcv=""
          while True:
               try:
                    data = self.connection.recv(1024)
                    request = json.loads(data.decode())
                    print(request)
                    if self.current is not None:
                         self.current.handle(self.session, request)
               except BaseException as e:
                    try:
                         self.session.send({
                              'To': None,
                              'status': 'ERROR',
                              'message': 'Internal Server Error'
                         })
                    except:
                         Manager.del_sesion(self.session)
                         self.connection.close()

               '''
               if data:
                    d = data.decode()
                    rcv=rcv+d
                    if rcv[-2:]=='\r\n':
                         #end of command, proses string
                         logging.warning("data dari client: {}" . format(rcv))
                         hasil = json.dumps(chatserver.proses(rcv))
                         hasil=hasil+"\r\n\r\n"
                         logging.warning("balas ke  client: {}" . format(hasil))
                         self.connection.sendall(hasil.encode())
                         rcv=""
               else:
                    break
               '''

class Server(threading.Thread):
     def __init__(self):
          self.the_clients = []
          self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          threading.Thread.__init__(self)

     def run(self):
        self.my_socket.bind((SERVER_IP,int(SERVER_PORT)))
        self.my_socket.listen(1)
        while True:
               self.connection, self.client_address = self.my_socket.accept()
               logging.warning("Incoming client > {}" . format(self.client_address))
               
               clt = ProcessTheClient(self.connection, self.client_address)
               clt.push_back(AuthHandler.get_instance())
               clt.push_back(CoreHandler.get_instance())
               clt.start()
               self.the_clients.append(clt)
     

def main():
     svr = Server()
     svr.start()

if __name__=="__main__":
     print("Server is running.....")
     main()

