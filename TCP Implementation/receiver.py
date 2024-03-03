# -*- coding: utf-8 -*-
#server (receiver) for TCP lite implementation
#@author: Christopher Demirjian
#@uni: cjd2186

import socket
import sys
import time

#create UDP connection

servPort=8080
servIp= '10.0.0.1'

#take in file name
if len(sys.argv)==2:
    filename= str(sys.argv[1])
else:
    print("usage: <filename>")
    sys.exit()

#make header to send
#given seqNum, ackNum and ACK, SYN, FIN bits,
# returns header with flags set
def makeHeader(seqNum, ackNum, ACK, SYN, FIN):
    srcport= (0).to_bytes(2, byteorder='big')
    destport= (0).to_bytes(2, byteorder='big')
    
    seqNum= (seqNum).to_bytes(4, byteorder='big')
    
    ackNum= (ackNum).to_bytes(4, byteorder='big')
    
    headLenNotUsed= (5).to_bytes(1, byteorder='big')
    C='0'
    E='0'
    U='0'
    A= str(ACK)
    P='0'
    R='0'
    S= str(SYN)
    F= str(FIN)
    flags= headLenNotUsed + int(C+E+U+A+P+R+S+F,2).to_bytes(1, byteorder='big')
    rwdn= (0).to_bytes(2, byteorder='big')
    
    checksum= (0).to_bytes(2, byteorder='big')
    urg= (0).to_bytes(2, byteorder='big')
    
    return bytes(srcport+destport+seqNum+ackNum+flags+rwdn+checksum+urg)

#interprets header given data received
#returns if header has a SYN, ACK, or FIN bit on
def parseHeaders(data):
    header=data[0:20]
    seqNum=header[4:8]
    ackNum=header[8:12]
    flags=header[13:14]
    if (int.from_bytes(flags, 'big') & (1<<1)):
        SYN=1
    else:
        SYN=0
    if (int.from_bytes(flags, 'big') & (1<<4)):
        ACK=1
    else:
        ACK=0
    if (int.from_bytes(flags, 'big') & (1<<0)):
        FIN=1
    else:
        FIN=0
    return (SYN, ACK, FIN)

#create listening socket
#while loop to keep server running
while 1:
    servSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servSock.bind((servIp, servPort))
    state=None
    seqNum=0
    ackNum=1
    
    #receive SYN from sender
    clientSYN, clientAddr= servSock.recvfrom(1044)
    SYN, ACK, FIN= parseHeaders(clientSYN)
    
    #send SYN ACK to sender
    if (SYN==1):
        SYNACKdata= makeHeader(seqNum, ackNum, 1, 1, 0)
        servSock.sendto(SYNACKdata, clientAddr)
    
    #recieve ACK of SYN ACK from sender
    clientData, clientAddr= servSock.recvfrom(1044)
    SYN, ACK, FIN= parseHeaders(clientData)
    if (ACK==1):
        state='estab'
    
    windowSize=4
    window=[]
    #time in file name to ensure that a new file is created with each transfer
    transferfile= str(time.time())+'transfer.txt'
    f = open(transferfile, mode = "a")
    #receive data from sender
    while(True):
        servData, servAddr= servSock.recvfrom(1044)
        #transfers file to new file named "transfer.txt"
        
        f.write(servData[20:].decode())
        
        #send an ACK after each packet
        ACK= makeHeader(1, ackNum,1, 0, 0)
        servSock.sendto(ACK, clientAddr)
        ackNum+=1024
        SYN, ACK, FIN= parseHeaders(servData)
        if (FIN==1):
            FINACK= makeHeader(seqNum, ackNum, 1, 0, 1)
            servSock.sendto(FINACK, clientAddr)
            break
    f.close()