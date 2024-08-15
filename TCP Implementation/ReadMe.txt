# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 01:01:50 2022
@author: Christopher Demirjian
@uni: cjd2186
"""

LOGIC:
This program follows the structure and logic as presented in TCP Lite,
  implementing a simiplified version of TCP on top of UDP.

Transfer Process:
Upon loading up the server receiver and the client sender, the client sends a SYN
  segment to the server, in which case the server responds to the client with
    a SYN ACK, and the client finishes this handshake with an ACK.
After this handshake, the client is able to send over its data in segments of size
  1024, which are taken in and appened to a file by the server.
Finally, after an EOF is read from the client's file to be sent, the client 
  sends a FIN segment to initiate a closed connection. The server responds with
    a FIN ACK, and the client sends an ACK before closing its TCP connection.
    The server persists its connection as well, as it is a server.

TOOLS:
Wireshark was used along RFC 793 to find out how to construct the TCP headers,
  and the protocol that is used to send data over TCP.
  
TCP header:

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |       |C|E|U|A|P|R|S|F|                               |
   | Offset| Rsrvd |W|C|R|C|S|S|Y|I|            Window             |
   |       |       |R|E|G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |         Urgent Pointer        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                           [Options]                           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                                                               :
   :                             Data                              :
   :                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    
client testing: 
python sender.py <destination-ip> <filename>

server testing:
python receiver.py <filename>
