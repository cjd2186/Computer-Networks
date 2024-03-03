@author: cjd2186
ReadMe: CSEE W4119 002 HW 2 HTTP Proxy Server
@file: cjd2186_proxy.py

------------------------------------------------------------------------------
HOW TO RUN CODE

In order to use the "cjd2186_proxy.py" file, run the python-file locally
  under port 8080 (hard-coded).
  
------------------------------------------------------------------------------
OUTPUT

Upon running this program, the proxy will make a connection with the web-browser
  and the proxy will take in, and parse the GET request from the browser.
The GET request will then be stored into a dictionary, and will be given a new
'X-Forwarded-For' heading, all of which will be sent to the web-server via a new
connection. 

------------------------------------------------------------------------------
LOGIC

Therefore, there will be a connection between the web browser, and the proxy, 
  as well as between the proxy and the web server.
  After sending the GET request to the web server, the proxy will receive
    the response from the web server, and send the response to the web browser.

------------------------------------------------------------------------------
THREADING AND CACHING ATTEMPT

This proxy stores the GET requests sent into a cache text file with the time stamp
  of the request-send.
  
------------------------------------------------------------------------------
LIMITATIONS

Although this is the intended design of my web-proxy, I had trouble properly
  implementing this, therefore the proxy hangs after sending the GET request from
    the proxy to the web-server.
Furthermore, the inability of the proxy to work inhibits my ability to send proper
  screenshots of the website that is accessed.