# -*- coding: utf-8 -*-
#@author: Christopher Demirjian
#@uni: cjd2186

import socket
import sys
import time

servPort=53
servIp=  '127.0.0.1'

#take in listening port number (default 53)
if len(sys.argv)==2:
    servPort= int(sys.argv[1])
else:
    print("usage: <port number>")
    sys.exit()

#create listening socket
#while loop to keep server running
servSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSock.bind((servIp, servPort))
cache={}

#get each flag from data to put in header
def getFlags(flags):
    
    #extract first and last bytes from flags
    #bits 0-7
    byte1= bytes(flags[:1])
    #bits 8-15
    QR='1'
    Opcode= ''
    for bit in range(1,5):
        #add bit onto Opcode
        #check if each bit is a 1 or a 0
        #bit is incremented with each iteration of for loop
        Opcode+= str(ord(byte1)&(1<<bit))
    #authorative answer flag, not a third party server
    AA= '1'
    #truncation, will not have a truncated answer
    TC= '0'
    #recursion desired; iterative proxy server
    RD = '0'
    #recursion availabile; not supported
    RA= '0'
    #free bits
    Z= '000'
    #response code
    RCODE='0000'
    #return codes together as two separate bytes, in big endian
    return int(QR+Opcode+AA+TC+RD, 2).to_bytes(1, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

#get domain from query header to put in response
def getQueryDomain(data):
    #have we hit the bit that shows the length of the domain
    lbit=False
    expectedLength=0
    domainStr=''
    domainsplit=[]
    bytecounter=0
    domainEndIdx=0
    #iterate through each byte in domain name (bytes after 12)
    #want to stop appending bytes to string when 00 it reached
    #want to ignore character iterpreted as . in domain suffix
    for byte in data:
        if (lbit==True):
            if (byte!=0):
                domainStr += chr(byte)
            bytecounter+=1
            #if we have reached end of domain machine name
            if (bytecounter==expectedLength):
                domainsplit.append(domainStr)
                #reset domain string to empty
                domainStr=''
                #reset lbit, going to find suffix lbit next
                lbit=False
                #reset to reach the next part of domain
                bytecounter=0
                
            #if we are at end of domain name
            if (byte==0):
                domainsplit.append(domainStr)
                #reached end of domain
                break
        else:
            lbit=True
            #first byte of string is length of domain
            expectedLength=byte
        #increment the byte,
        domainEndIdx+=1
    
    #return the array of the domain machine and domain suffix
    return domainsplit

#function used to find the IP for the next Nameserver to query
def findRecordIP(data, lastrec):
    
    #already past the header (first 12 bytes)
    #want to go to the first AAAA record (will be additional RR)
    #after hitting the AAAA record, go back to previous record
    typeA=False
    classIN=False
    foundQuery=False
    #iterate through each byte in domain name (bytes after 12)
    #want to stop appending bytes to string when 00 it reached
    #want to ignore character iterpreted as . in domain suffix
    NS_ip=''
    ttl=''
    for byte in range(0, len(data)):
        #identify the type A and class IN within query
        if ((data[byte].to_bytes(1, byteorder='big'))== b'\x00' and 
            (data[byte+1].to_bytes(1, byteorder='big')) == b'\x01'):
            typeA=True
           
        if (typeA==True and 
            (data[byte+2].to_bytes(1, byteorder='big'))== b'\x00' and 
            (data[byte+3].to_bytes(1, byteorder='big'))== b'\x01'):
            classIN=True
        if (typeA==True and classIN==True):
            foundQuery=True
            bytecounter=byte
            break
        typeA=False
        classIN=False
    #now that byte counter shows where the first query ends, the next
    #  type A record will have the NS ip in its data field from answers
    if (foundQuery==True):
        for byte in range(bytecounter+1, len(data)):
            #passed query type A record, next type A record will contain the target ip
            if (lastrec==False):
                if ((data[byte].to_bytes(1, byteorder='big'))== b'\x00' and 
                    (data[byte+1].to_bytes(1, byteorder='big'))== b'\x01' and 
                    (data[byte+2].to_bytes(1, byteorder='big'))== b'\x00' and 
                    (data[byte+3].to_bytes(1, byteorder='big'))== b'\x01'):
                    #only want the RR of the answer
                    data=data[byte-2: byte+14]
                    ttl=data[6:10]
                    ttl_int=int.from_bytes(ttl, 'big')
                    #this array of bytes will have the ip address
                    #must bring byte (index) to start of ip, have 4 parts of ip address
                    NS_ip=data[12:16]
                    x1=(data[12])
                    x2=(data[13])
                    x3=(data[14])
                    x4=(data[15])
                    NS_ip= (str(x1) + '.' + str(x2) +'.'+ str(x3)+'.' + str(x4))
                    return (NS_ip, ttl_int)
            else: #check additional records
                for byte in range(bytecounter, len(data)):
                    #passed query type A record, next type A record will contain the target ip
                    if ((data[byte].to_bytes(1, byteorder='big'))== b'\xc0' and 
                        (data[byte+1].to_bytes(1, byteorder='big'))== b'\x0c' and 
                        (data[byte+2].to_bytes(1, byteorder='big'))== b'\x00' and 
                        (data[byte+3].to_bytes(1, byteorder='big'))== b'\x01' and
                        (data[byte+4].to_bytes(1, byteorder='big'))== b'\x00' and 
                        (data[byte+5].to_bytes(1, byteorder='big'))== b'\x01'):
                        #only want the RR of the answer
                        data=data[byte: byte+16]
                        ttl=data[6:10]
                        ttl_int=int.from_bytes(ttl, 'big')
                        #this array of bytes will have the ip address
                        #must bring byte (index) to start of ip, have 4 parts of ip address
                        NS_ip=data[12:16]
                        x1=(data[12])
                        x2=(data[13])
                        x3=(data[14])
                        x4=(data[15])
                        NS_ip= (str(x1) + '.' + str(x2) +'.'+ str(x3)+'.' + str(x4))
                        return (NS_ip, ttl_int)
                
#construct Response headers for query
def constructResp(data, authip, ttl):
    #get first two bytes of DNS query for transactionID
    TID= data[:2]
    #retrieve the flags of DNS query (bytes 3 and 4)
    flags=getFlags(data[2:4])
    
    #question count, set to 1
    QDCOUNT=b'\x00\x01'
    ANCOUNT=b'\x00\x01'
    NSCOUNT=b'\x00\x00'
    ARCOUNT=b'\x00\x00'
    
    #use domain from getQueryDomain to get domain and query type
    qd=getQueryDomain(data[12:])
    qdlen=0
    for i in range(0,len(qd)):
        qdlen+=len(qd[i])
    #construct name and len before each part of name
    NAME=bytearray('', 'utf-8')
    for part in range (0, len(qd)-1):
        NAME+= len(qd[part]).to_bytes(1, 'big')
        for char in qd[part]:
            NAME+= ord(char).to_bytes(1, 'big')
    #first x00 is to show end of name

    QUERIES= NAME+ b'\x00\x00\x01\x00\x01'
    
    strip= authip.split('.')
    ip=bytearray('', 'utf-8')
    for part in strip:
        ip+=(int(part).to_bytes(1, 'big'))
    ttl= ttl.to_bytes(4, 'big')
    ANSWERS=b'\xc0\x0c\x00\x01\x00\x01'+ ttl+ b'\x00\x04' +ip
    
    #concatinate parts of result and return response
    #int(QR+Opcode+AA+TC+RD, 2).to_bytes(1, byteorder='big')
    
    response= TID + flags+ QDCOUNT+ ANCOUNT+ NSCOUNT + ARCOUNT + QUERIES + ANSWERS
    return response

#iteriatively query servers to find ip for domain
def query(domain):
    
    #first DNS server to query
    rootIp= '199.7.83.42'
    rootPort= 53
    #make socket to send to root, get next IP address
    rootSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rootSock.sendto(data, (rootIp, rootPort))
    rootdata, rootAddr= rootSock.recvfrom(2048)
    NSip, NSttl= findRecordIP(rootdata, False)
    rootSock.close()
    
    #make socket to send to TLD server, get next IP address    
    TLDSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    TLDSock.sendto(data, (NSip, rootPort))
    TLDdata, TLDAddr= TLDSock.recvfrom(2048)
    TLDip, TLDttl= findRecordIP(TLDdata,False)
    TLDSock.close()
    
    authSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    authSock.sendto(data, (TLDip, rootPort))
    authdata, authAddr= authSock.recvfrom(2048)
    lastrec=True
    authip,ttl= findRecordIP(authdata, lastrec)
    #cache response before sending the authip and ttl
    expire=time.time() + ttl
    cache[domain]= (authip, ttl, expire)
    authSock.close()
    return (authip, ttl)

while 1:
    #use udp for size of 512 or less
    data, clAddr = servSock.recvfrom(512)
    
    #find website to query
    qd=getQueryDomain(data[12:])
    domain=''
    for i in range(0, len(qd)):
        domain+=qd[i]
        if (i< len(qd)-1):
            domain+='.'
    
    if (domain in cache):
        authip=cache[domain][0]
        ttl=cache[domain][1]
        expire=cache[domain][2]
        #if time is past experation time, delete from cache
        if(time.time()>= expire):
            #remove from cache
            cache.pop(domain)
            authip, ttl=query(domain)
        response= constructResp(data, authip, ttl)
        #send to client
        servSock.sendto(response, clAddr)
        
    else:
        authip, ttl= query(domain)
        response= constructResp(data, authip, ttl)
        servSock.sendto(response, clAddr)