# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 01:01:50 2022
@author: Christopher Demirjian
@uni: cjd2186
"""

LOGIC:
This program follows the structure and logic as presented in the DNS RFC 1035.


ITERATIVE QUERY PROCESS:
First, this program takes in a port number as a command line argument, in which
  this DNS resolver will run on. 
This DNS server then makes a connection with the DIG user program, and takes in 
  the user's DNS query.
This DNS query is then relayed to the ICANN DNS root server.
The root server sends a response back to this DNS resolver, which is parsed for its 
  type A record (most likely stored under additional RRs), containing the IP address of the 
  TLD server to relay the user query to.
The TLD server is then queried, and its response is once again parsed to find the type
  A record for the IP address of the authoritative server to relay the user query to.
The authoritative server is finally queiried, and its response contains a type A
  RR under its answer, which contains the ip of the user's query.
This ip is then wrapped into a response header format that is sent back to the user client.
The ip and ttl (time to live) are then cached in a dictionary with the ip as the key,
  and the cache is later checked before each query, deleting any records that are expired
  before checking if a domain ip is cached. If a domain ip is not in the cache, the query
  process begins, and the DNS resolver queries the root server and iteratively finds
  the domain ip.

TOOLS:
Wireshark was used along with dig and localhost to figure out the byte order and structure
  for which bytes correspond to which flag and component of the DNS header.

DNS PROXY STRUCTURE:

                 Local Host                        |  Foreign
                                                   |
    +---------+               +----------+         |  +--------+
    |         | user queries  |          |queries  |  |        |
    |  User   |-------------->|          |---------|->|Foreign |
    | Program |               | Resolver |         |  |  Name  |
    |         |<--------------|          |<--------|--| Server |
    |         | user responses|          |responses|  |        |
    +---------+               +----------+         |  +--------+
                                |     A            |
                cache additions |     | references |
                                V     |            |
                              +----------+         |
                              |  cache   |         |
                              +----------+         |
                              

DNS QUERY/RESPONSE HEADER STRUCTURE:

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    
    go past 12 byte header
    
server testing: python main.py <port number>
client testing: dig -p <port number> <domain> @localhost