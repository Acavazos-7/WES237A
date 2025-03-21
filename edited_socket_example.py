#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
from pynq.overlays.base import BaseOverlay
import socket

base = BaseOverlay("base.bit")
btns = base.btns_gpio
leds = base.leds


# # Sockets
# 
# This notebook has both a client and a server functionality. One PYNQ board in the group will be the client and SENDS the message. Another PYNQ board will be the server and RECEIVES the message.

# ## Server
# 
# Here, we'll build the server code to LISTEN for a message from a specific PYNQ board.
# 
# When we send/receive messages, we need to pieces of information which will tell us where to send the information. First, we need the IP address of our friend. Second, we need to chose a port to listen on. For an analogy, Alice expects her friend, Bob, to deliver a package to our back door. With this information, ALICE (server ip address) can wait at the BACK DOOR (port) for BOB (client ip address) to deliver the package.
# 
# Format of the information
#  ipv4 address: ###.###.###.### (no need for leading zeros if the number is less than three digits)
#  port: ##### (it could be 4 or 5 digits long, but must be >1024)
#  
# Use the socket documentation (Section 18.1.3) to find the appropriate functions https://python.readthedocs.io/en/latest/library/socket.html
# 

# In[ ]:


# TODO:
# 1: Bind the socket to the pynq board <CLIENT-IP> at port <LISTENING-PORT>
# 2: Accept connections
# 3: Receive bytes from the connection
# 4: Print the received message
from socket import *
serverPort = 8080
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence)
    print(f'{capitalizedSentence}')
    print('closing socket')
    connectionSocket.close()


# ## Client
# 
# Now, we can implement the CLIENT code. 
# 
# Back to the analogy, now we're interested in delivering a package to our friend's back door. This means BOB (client ip address) is delivering a package to ALICE (server ip address) at her BACK DOOR (port)
# 
# **Remember to start the server before running the client code**

# In[8]:


# TODO: 
# 1: Connect the socket (sock) to the <SERVER-IP> and choosen port <LISTENING-PORT>
# 2: Send the message "Hello world!\n"
# 3: Close the socket
from socket import *
serverName = '100.81.33.120'
serverPort = 8080
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = raw_input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ('From Server:', modifiedSentence.decode())
clientSocket.close()


# On your server, you should see the message and then the server will shutdown! When we close a socket, both the client and the server are disconnected from the port.
# 
# Instead, change the function above to send 5 messages before closing.
# 
# The pseudocode looks like this
# 
# * connect the socket
# * for i in range(5)
#     * msg = input("Message to send: ")
#     * send the message (msg)
# * close the socket

# 
