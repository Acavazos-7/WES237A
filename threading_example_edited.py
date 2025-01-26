#!/usr/bin/env python
# coding: utf-8

# # threading
# importing required libraries and programing our board

# In[1]:


import threading
import time
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")


# # Two threads, single resource
# 
# Here we will define two threads, each responsible for blinking a different LED light. Additionally, we define a single resource to be shared between them. 
# 
# When thread0 has the resource, led0 will blink for a specified amount of time. Here, the total time is 50 x 0.02 seconds = 1 second. After 1 second, thread0 will release the resource and will proceed to wait for the resource to become available again.
# 
# The same scenario happens with thread1 and led1.

# In[2]:


def blink(t, d, n):
    '''
    Function to blink the LEDs
    Params:
      t: number of times to blink the LED
      d: duration (in seconds) for the LED to be on/off
      n: index of the LED (0 to 3)
    '''
    for i in range(t):
        base.leds[n].toggle()
        time.sleep(d)
    base.leds[n].off()

def worker_t(_l, num):
    '''
    Worker function to try and acquire resource and blink the LED
    _l: threading lock (resource)
    num: index representing the LED and thread number.
    '''
    for i in range(4):
        using_resource = _l.acquire(True)    
        print("Worker {} has the lock".format(num))
        blink(50, 0.02, num)
        _l.release()
        time.sleep(0) # yeild
    print("Worker {} is done.".format(num))
        
# Initialize and launch the threads
threads = []
fork = threading.Lock()
for i in range(2):
    t = threading.Thread(target=worker_t, args=(fork, i))
    threads.append(t)
    t.start()

for t in threads:
    name = t.getName()
    t.join()
    print('{} joined'.format(name))


# # Two threads, two resource
# 
# Here we examine what happens with two threads and two resources trying to be shared between them.
# 
# The order of operations is as follows.
# 
# The thread attempts to acquire resource0. If it's successful, it blinks 50 times x 0.02 seconds = 1 second, then attemps to get resource1. If the thread is successful in acquiring resource1, it releases resource0 and procedes to blink 5 times for 0.1 second = 1 second. 

# In[4]:


def worker_t(_l0, _l1, num):
    '''
    Worker function to try and acquire resource and blink the LED
    _l0: threading lock0 (resource0)
    _l1: threading lock1 (resource1)
    num: index representing the LED and thread number.
    init: which resource this thread starts with (0 or 1)
    '''
    using_resource0 = False
    using_resource1 = False
        
    for i in range(4):
        
        #worker aquires lock1 then lock2
        using_resource0 = _l0.acquire(True)
        print("Worker {} has lock0".format(num))
        blink(50, 0.02, num)
        using_resource1 = _l1.acquire(True)
        print("Worker {} has lock1".format(num))
        blink(5, 0.1, num)
        
        #worker releases lock1 then lock2
        _l0.release()
        print("Worker {} has released lock0".format(num)) #print to confirm
        _l1.release()
        print("Worker {} has released lock1".format(num)) #print to confirm
        
        time.sleep(0) # yeild
    print("Worker {} is done.".format(num))
        
# Initialize and launch the threads
threads = []
fork = threading.Lock()
fork1 = threading.Lock()
for i in range(2):
    t = threading.Thread(target=worker_t, args=(fork, fork1, i))
    threads.append(t)
    t.start()

for t in threads:
    name = t.getName()
    t.join()
    print('{} joined'.format(name))


# You may have notied (even before running the code) that there's a problem! What happens when thread0 has resource1 and thread1 has resource0! Each is waiting for the other to release their resource in order to continue.
# 
# This is a **deadlock**. Adjust the code above to prevent a deadlock.

# # Non-blocking Acquire
# 
# In the above code, when _l.acquire(True)_ was used, the thread stopped executing code and waited for the resource to be acquired. This is called **blocking**: stopping the execution of code and waiting for something to happen. Another example of **blocking** is if you use _input()_ in Python. This will stop the code and wait for user input.
# 
# What if we don't want to stop the code execution? We can use non-blocking version of the acquire() function. In the code below, _resource_available_ will be True if the thread currently has the resource and False if it does not. 
# 
# Complete the code to and print and toggle LED when lock is not available.

# In[12]:


def blink(t, d, n):
    for i in range(t):
        base.leds[n].toggle()
        time.sleep(d)
        
    base.leds[n].off()

def worker_t(_l, num):
    for i in range(10):
        resource_available = _l.acquire(False) # this is non-blocking acquire
        if resource_available:
            # write code to:
            # print message for having the key
            print('Worker {} has the key'.format(num))
            
            # blink for a while
            blink(50, 0.02, num)
            
            # release the key
            _l.release()
            
            # give enough time to the other thread to grab the key
            time.sleep(0.5) #5 millisecond delay
        else:
            # write code to:
            # print message for waiting for the key
            print('Worker {} is waiting for the key'.format(num))
            
            # blink for a while with a different rate
            blink(5, 0.1, num)
            
            # the timing between having the key + yield and waiting for the key should be adjusted so no thread get stuck in waiting
            time.sleep(0.1) #one millisecond delay
            
    print('worker {} is done.'.format(num))
        
threads = []
fork = threading.Lock()
for i in range(2):
    t = threading.Thread(target=worker_t, args=(fork, i))
    threads.append(t)
    t.start()

for t in threads:
    name = t.getName()
    t.join()
    print('{} joined'.format(name))


# In[ ]:




