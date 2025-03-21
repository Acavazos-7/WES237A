#!/usr/bin/env python
# coding: utf-8

# # Part A4.1

# In[1]:


import time
import socket
import pynq
import multiprocessing
from pynq.overlays.base import BaseOverlay
from pynq.lib.pmod import Pmod

# PYNQ setup for the buzzer and buttons using the base overlay
base = BaseOverlay("base.bit")  # Load the base bitstream to access the PMOD and buttons


# In[2]:


get_ipython().run_cell_magic('microblaze', 'base.PMODB', '\n#include "gpio.h"\n#include "pyprintf.h"\n\n//Function to turn on/off a selected pin of PMODB\nunsigned int write_gpio(unsigned int pin, unsigned int val)\n{\n    if (val > 1)\n    {\n        pyprintf("pin value must be 0 or 1");\n    }\n    gpio pin_out = gpio_open(pin);\n    gpio_set_direction(pin_out, GPIO_OUT);\n    gpio_write(pin_out, val);\n    return 0;\n}\n\n// Function to reset all GPIO pins on PMODB\nint reset_gpio()\n{\n    // Assuming PMODB has 8 pins, you might need to adjust this based on the actual pin count\n    for (unsigned int pin = 0; pin < 8; pin++)\n    {\n        gpio pin_out = gpio_open(pin);\n        gpio_set_direction(pin_out, GPIO_OUT);\n        gpio_write(pin_out, 0); // Resetting to low state\n    }\n    return 0;\n    pyprintf("All GPIO pins on PMODB have been reset to low state.");\n}\n')


# In[3]:


#Button setup
btns = base.btns_gpio
button0 = btns[0].read()  # BT0
button1 = btns[1].read()  # BT1
button2 = btns[2].read()  # BT2
button3 = btns[3].read()  # BT3


# In[4]:


# Function to control the buzzer based on frequency (to interact with MicroBlaze)
def buzzer(frequency):          
    time_on = 1 / (2 * frequency)
    time_off = time_on
    
    while True:
        write_gpio(0,1)  # Turn on buzzer
        time.sleep(time_on)  # Sleep for the calculated time
        write_gpio(0,0)  # Turn off buzzer
        time.sleep(time_off)  # Sleep for the calculated time

# Server process to listen for button presses and control buzzer
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))  # Binding to all IPs on port 12345
    server_socket.listen(1)  # Listening for incoming connections
    
    print("Server started. Waiting for client to connect...")
    client_socket, client_address = server_socket.accept()  # Accept a client connection
    print(f"Connection from {client_address} established.")
    
    while True:
        data = client_socket.recv(1024).decode('utf-8')  # Receive data from client
        
        if data == 'start':
            print("Button 0 pressed: Starting buzzer.")
            buzzer(1)  # Start buzzer with 1 Hz frequency
            time.sleep(1)
        
        if data == 'disconnect':
            print("Button 2 pressed: Disconnecting server.")
            break  # Disconnect and stop the server
            time.sleep(0.5)
    
    server_socket.close()  # Close the server socket

# Client process to control buzzer
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))  # Replace with the server's IP address
    
    while True:
        if button1 == 1:  # If button 1 is pressed
            print("Button 1 pressed: Emitting tone on buzzer.")
            client_socket.send('start'.encode('utf-8'))  # Send start command to server
            time.sleep(0.5)
        
        if button2 == 1:  # If button 3 is pressed
            print("Button 3 pressed: Disconnecting client.")
            client_socket.send('disconnect'.encode('utf-8'))  # Send disconnect command to server
            client_socket.close()  # Close the client connection
            break
        time.sleep(0.1)
        
def run_multiprocessing():
    #Function to run the server and client processes in parallel
    server_process = multiprocessing.Process(target=start_server)
    client_process = multiprocessing.Process(target=start_client)
    
    server_process.start()
    client_process.start()

    server_process.join()
    client_process.join()


# In[ ]:


# Start the server and client using multiprocessing
try:
    while True:
        # Check if Button 0 is pressed
        if button3 == 1:  # Button is pressed
            print("Button 3 pressed. Exiting program...")
            break
        start_server();
        start_client();
        run_multiprocessing();
        print("multiprocessing has begun")
        
finally:
        print("program has been teinated")


# In[ ]:




