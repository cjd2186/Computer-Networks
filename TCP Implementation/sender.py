# -*- coding: utf-8 -*-
#client (sender) for TCP lite implementation
#@author: Christopher Demirjian
#@uni: cjd2186

import socket
import sys
import time

# #take in file name
if len(sys.argv)==3:
    destIP= (sys.argv[1])
    filename= str(sys.argv[2])
else:
    print("usage: <destination IP> <filename>")
    sys.exit()

#create UDP connection
servPort= 8080
servIp= destIP

#create client socket to send data over
clientSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    
#open and read from file
file = open(filename, "r") 

#send SYN, seq=0, ackseq=0
SYNdata=makeHeader(0,0,0,1,0)
clientSock.sendto(SYNdata, (servIp, servPort))

#receive SYN ACK from receiver
servData, servAddr= clientSock.recvfrom(1044)
SYN, ACK, FIN= parseHeaders(servData)
if (not(SYN==1 and ACK==1)):
    clientSock.sendto(SYNdata, (servIp, servPort))

#send ACK after receiving SYN ACK
ACKdata= makeHeader(0, 1, 1, 0, 0)
clientSock.sendto(ACKdata, (servIp, servPort))

#send data to receiver
seqNum=1
ackNum=1

windowSize=4
window=[]
while(True):
    x=file.read(1024)
    toSend=makeHeader(seqNum, ackNum, 0, 0, 0)
    toSend+=x.encode()
    clientSock.sendto(toSend, (servIp, servPort))
    seqNum+=1024
    if (x==''):
        break

#all data has been sent to receiver, close file
file.close()

#send FIN to receiver
FINdata= makeHeader(seqNum, 0, 0, 0, 1)
clientSock.sendto(FINdata, (servIp, servPort))

#resend FIN if didnt get FIN ACK
servFINACK, servAddr= clientSock.recvfrom(1044)
SYN, ACK, FIN= parseHeaders(servData)
if (not(FIN==1 and ACK==1)):
    clientSock.sendto(FINdata, (servIp, servPort))

#send ACK and close connection
fACKdata= makeHeader(0, ackNum, ACK, SYN, FIN)
clientSock.sendto(fACKdata, (servIp, servPort))
clientSock.close()