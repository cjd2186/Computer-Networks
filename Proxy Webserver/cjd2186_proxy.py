# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 22:53:34 2022

@author: cjd2186
"""


#format GET request with proper headers
#
# Echo server program
import socket
import time
import threading

class Proxy:
    def __init__(self):
        self.headers2= []
        self.headers3= {}
        
    #client to proxy
    def client_connection(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    seg_data=''
                    #establish tcp connection with client, as server
                    #accept GET requests from client
                    headers2=self.headers2
                    headers3=self.headers3
                    #data has the GET Request
                    print('200 OK')
                    #store the headers into a dictionary
                    seg_data=data.decode()
                    head= seg_data.split('\r\n')
                    for subString in head[1:len(head)-2]:
                        headers2.append(subString.split(': '))
                    headers3= {sub[0]: sub[1] for sub in headers2}
                    client= headers3['Host'].split(':')
                    client_machine= client[0]
                    client_port= int(client[1])
                    headers3['X-Forwarded-For']= host + client_machine
                    headers3['X-4119']= 'X-4119: cjd2186', time.time()
                    print(headers3)
                    #read GET request from client
                                
                    #parse the host header
                    req=''
                    for header in headers3:
                        header=str(header)
                        req+=(header)
                        req+=(': ')
                        req+=str((headers3[header]))
                        req+=('\r\n')
                        print(req)
                    #self.web_connection(client_machine, client_port, req)
                    data=self.web_connection(client_machine, client_port, req)
                    s.sendall(data)
        #cache if not already cached
        #check if cached file's get req is same as current
        cache_file = open("Cache.txt", "w+") 
        cache_file.write(str(time.time()))
        cache_file.write('\n')
        cache_file.write(req)
    
    #proxy to web server (proxy is the client)
    def web_connection(self, client_machine, client_port, req):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((client_machine, client_port))
            s.sendall(req.encode())
            data = s.recv(1024)
            print("here")
            print(data.decode())
        return data

    def run(self, host, port):
        #t = threading.Thread(target=self.client_connection, args=(conn,))
        #t.start()
        self.client_connection(host, port)
    
if __name__ == "__main__":
    proxy = Proxy()
    proxy.run("localhost", 8080)

#send request to the web server

#receive response from web server, take into proxy server

#send response from proxy server to web client
'''
# Echo client program
HOST = host_machine    # The remote host
PORT = host_port              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))
conn.sendall(data)
'''

#establish tcp connection with server
#send GET request to server
#take response from server
#
#send server response to client
#