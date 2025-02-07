#!/usr/bin/env python
# coding: utf-8

# # Part A2.1

# In[ ]:


import threading
import pynq.lib.rgbled as rgbled
import time
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")


# In[ ]:


btns = base.btns_gpio
On = True
leds = [base.leds[index] for index in range (4)]
led4 = rgbled.RGBLED(4)
forks = [threading.Lock() for i in range(5)]


# In[ ]:


# Define philosopher states
EATING = "EATING"
NAPPING = "NAPPING"
STARVING = "STARVING"

#Utilize LEDS 0-3
def blink(led, times, duration):
    for i in range(times):
        led.toggle()
        time.sleep(duration)
    led.off()

#Utilize LED 4
def led_4(times, duration):
    for i in range (times):
        led4.write(0x2)
        led4.write(0x0)
        time.sleep(duration)
    led4.write(0x0)
    
#Define Philosophers routine
def philosopher(index, left_fork, right_fork):
    while On:
        # Check for On button to exit the loop
        end_Loop()

        # Philosopher is starving (waiting for both forks)
        print(f"Philosopher {index} is STARVING")
        set_led_state(index, STARVING)
        
        left_fork.acquire() #acquire left fork
        right_fork.acquire() #acquire right fork
        
        # Philosopher is eating
        print(f"Philosopher {index} is EATING")
        set_led_state(index, EATING)
        time.sleep(2)  # Eating duration
        
        left_fork.release() #release left fork
        right_fork.release() #release right fork

        # Philosopher is napping
        print(f"Philosopher {index} is NAPPING")
        set_led_state(index, NAPPING)
        time.sleep(2.1)  # Napping duration

#Define State of Philosopher and LEDs
def set_led_state(index, state):
    if state == EATING:
        # Blink LED at a higher rate to indicate eating
        if index == 4:
            led_4(20, 0.1)
        else:
            blink(leds[index], 20, 0.1)
    elif state == NAPPING:
        # Blink LED at a lower rate to indicate napping
        if index == 4:
            led_4(10, 0.4)
        else:
            blink(leds[index], 10, 0.2)
    elif state == STARVING:
        # Turn off LED to indicate starving
        if index == 4:
            led4.write(0x0)
        else:
            leds[index].off()

#End loop using any button
def end_Loop():
    global On
    button = btns.read()
    if button != 0:
        print("Button pressed, Setting On to False")
        On = False


# In[ ]:


# Create and start philosopher threads
On = True
while On:
    threads = []
    for i in range(5):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % 5]
        t = threading.Thread(target=philosopher, args=(i, left_fork, right_fork))
        threads.append(t)
        t.start()

    # Join threads to ensure they complete
    for t in threads:
        name = t.getName()
        t.join()
        print('{} joined'.format(name))
    end_Loop()
print("loop has ended")


# # Part A2.2

# In[1]:


import threading
import pynq.lib.rgbled as rgbled
import time
import random
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")


# In[2]:


btns = base.btns_gpio
On = True
leds = [base.leds[index] for index in range(4)]
led4 = rgbled.RGBLED(4)
forks = [threading.Lock() for i in range(5)]


# In[3]:


# Define philosopher states
EATING = "EATING"
NAPPING = "NAPPING"
STARVING = "STARVING"

#Utilize LEDS 0-3
def blink(led, times, duration):
    for i in range(times):
        led.toggle()
        time.sleep(duration)
    led.off()

#Utilize LED 4
def led_4(times, duration):
    for i in range (times):
        led4.write(0x2)
        led4.write(0x0)
        time.sleep(duration)
    led4.write(0x0)
    
#Use Random number generator to set eating and napping times
def random_eating_time():
    return random.randint(5, 10) / 10 #eating time is from 0.5 to 1 second

def random_napping_time():
    return random.randint(1, 5) / 10 #napping time is from 0.1 to 0.5 seconds
    
#Define Philosophers routine
def philosopher(index, left_fork, right_fork):
    while On:
        # Check for On button to exit the loop
        end_Loop()

        # Philosopher is starving (waiting for forks)
        print(f"Philosopher {index} is STARVING")
        set_led_state(index, STARVING)
        
        left_fork.acquire() #acquire left fork
        right_fork.acquire() #acquire right fork
        
        # Philosopher is eating
        print(f"Philosopher {index} is EATING")
        set_led_state(index, EATING)
        eating_time = random_eating_time()
        time.sleep(eating_time)  # Eating duration
        print(f"Eating Time is {eating_time} seconds")
        
        left_fork.release() #release left fork
        right_fork.release() #release right fork

        # Philosopher is napping
        print(f"Philosopher {index} is NAPPING")
        set_led_state(index, NAPPING)
        napping_time = random_napping_time()
        time.sleep(napping_time)  # Napping duration
        print(f"Napping Time is {napping_time} seconds")

#Define State of Philosopher and LEDs
def set_led_state(index, state):
    if state == EATING:
        # Blink LED at a higher rate to indicate eating
        if index == 4:
            led_4(10, 0.3)
        else:
            blink(leds[index], 10, 0.1)
    elif state == NAPPING:
        # Blink LED at a lower rate to indicate napping
        if index == 4:
            led_4(5, 0.4)
        else:
            blink(leds[index], 5, 0.2)
    elif state == STARVING:
        # Turn off LED to indicate starving
        if index == 4:
            led4.write(0x0)
        else:
            leds[index].off()

#End loop using any button
def end_Loop():
    global On
    button = btns.read()
    if button != 0:
        print("Button pressed, Setting On to False")
        On = False


# In[5]:


# Create and start philosopher threads
On = True
while On:
    threads = []
    for i in range(5):
        left_fork = forks[i] # i number of forks
        right_fork = forks[(i + 1) % 5] #i number fork +1 to determine right side, and added mod 5 to always circle 5 spots
        t = threading.Thread(target=philosopher, args=(i, left_fork, right_fork))
        threads.append(t)
        t.start()

    # Join threads to ensure they complete
    for t in threads:
        name = t.getName()
        t.join()
        print('{} joined'.format(name))
    end_Loop()
print("loop has ended")


# In[ ]:




