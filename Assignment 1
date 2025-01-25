from pynq.overlays.base import BaseOverlay
from pynq.lib.pmod import Pmod_PWM
import time
from datetime import datetime
from pynq.lib import LED, Switch, Button
base = BaseOverlay("base.bit")

%%microblaze base.PMODB

#include "gpio.h"
#include "pyprintf.h"

//Function to turn on/off a selected pin of PMODB
unsigned int write_gpio(unsigned int pin, unsigned int val)
{
    if (val > 1)
    {
        pyprintf("pin value must be 0 or 1");
    }
    gpio pin_out = gpio_open(pin);
    gpio_set_direction(pin_out, GPIO_OUT);
    gpio_write(pin_out, val);
    return 0;
}

// Function to reset all GPIO pins on PMODB
int reset_gpio()
{
    // Assuming PMODB has 8 pins, you might need to adjust this based on the actual pin count
    for (unsigned int pin = 0; pin < 8; pin++)
    {
        gpio pin_out = gpio_open(pin);
        gpio_set_direction(pin_out, GPIO_OUT);
        gpio_write(pin_out, 0); // Resetting to low state
    }
    return 0;
    pyprintf("All GPIO pins on PMODB have been reset to low state.");
}

print("Testing each gpio and Color...")
write_gpio(1, 1)
write_gpio(2, 0)
write_gpio(3, 0)
time.sleep(1)

write_gpio(1, 0)
write_gpio(2, 1)
write_gpio(3, 0)
time.sleep(1)
    
write_gpio(1, 0)
write_gpio(2, 0)
write_gpio(3, 1)
time.sleep(1)
print("Testing complete!")

reset_gpio()
print("GPIOs have been reset")

#Use this to test individual PWM for each color
#Duty Cycle equals 0-100
#PWM LED
def pwmRED(frequency, duty_cycle):
    period = 1 / frequency
    on_time = duty_cycle*period
    off_time = (100-duty_cycle)*period
    start=time.time()
    
    while time.time()-start<5:
        write_gpio(1, 0) #Blue LED
        write_gpio(2, 0) #Green LED
        write_gpio(3, 1) #Red LED
        time.sleep(on_time)
        write_gpio(1, 0)
        write_gpio(2, 0)
        write_gpio(3, 0)
        time.sleep(off_time)  
        
#Duty Cycle equals 0-100
#PWM LED
def pwmGREEN(frequency, duty_cycle):
    period = 1 / frequency
    on_time = duty_cycle*period
    off_time = (100-duty_cycle)*period
    start=time.time()
    
    while time.time()-start<5:
        write_gpio(1, 0) #Blue LED
        write_gpio(2, 1) #Green LED
        write_gpio(3, 0) #Red LED
        time.sleep(on_time)
        write_gpio(1, 0)
        write_gpio(2, 0)
        write_gpio(3, 0)
        time.sleep(off_time)  
        
#Duty Cycle equals 0-100
#PWM LED
def pwmBLUE(frequency, duty_cycle):
    period = 1 / frequency
    on_time = duty_cycle*period
    off_time = (100-duty_cycle)*period
    start=time.time()
    
    while time.time()-start<1:
        write_gpio(1, 1) #Blue LED
        write_gpio(2, 0) #Green LED
        write_gpio(3, 0) #Red LED
        time.sleep(on_time)
        write_gpio(1, 0)
        write_gpio(2, 0)
        write_gpio(3, 0)
        time.sleep(off_time)   
        
#Testing PWM for whichever color you want
#example: Green LED, 100 Hz, 50%
print("staring loop")
pwmRED(500, 50)
print("Loop has finished")

#Testing PWM for whichever color you want
#example: Green LED, 100 Hz, 50%
print("staring loop")
pwmGREEN(500, 50)
print("Loop has finished")

#Testing PWM for whichever color you want
#example: Green LED, 100 Hz, 50%
start_time=time.time()
while time.time()-start_time<5:
    print("staring loop")
    pwmBLUE(500, 50)
print("Loop has finished")

#Testing PWM for whichever color you want
#example: Green LED, 100 Hz, 50%
print("staring loop")
pwmRED(500, 50)
pwmRED(1000, 50)
pwmRED(2000, 50)
pwmRED(5000, 50)
pwmRED(10000, 50)
print("Loop has finished")

#Testing PWM for whichever color you want
#example: Green LED, 100 Hz, 50%
print("staring loop")
pwmBLUE(10000, 5)
pwmBLUE(10000, 25)
pwmBLUE(10000, 50)
pwmBLUE(10000, 75)
pwmBLUE(10000, 100)
pwmBLUE(10000, 75)
pwmBLUE(10000, 50)
pwmBLUE(10000, 25)
pwmBLUE(10000, 5)
print("Loop has finished")

import asyncio
import time

btns = base.btns_gpio

#My conditions for activating each colors PWM
#Start off False, PWM is off
red=False
green=False
blue=False
off=False

async def pwm():
    global red, green, blue, off
    period = 1 / 50 #frequency = 50Hz
    on_time = 50*period #duty cycle = 50%
    off_time = (100-50)*period
    #This will cause the LED to be on for 1 second and off for 1 second
    while True:
        if red: #Red LED ON
            write_gpio(1, 0) #Blue LED
            write_gpio(2, 0) #Green LED
            write_gpio(3, 1) #Red LED
            await asyncio.sleep(on_time)
            write_gpio(1, 0)
            write_gpio(2, 0)
            write_gpio(3, 0)
            await asyncio.sleep(off_time)
            print("Red LED is Blinking") #Debug statement to reflect which color is blinkng
        elif green: #Green LED ON
            write_gpio(1, 0) #Blue LED
            write_gpio(2, 1) #Green LED
            write_gpio(3, 0) #Red LED
            await asyncio.sleep(on_time)
            write_gpio(1, 0)
            write_gpio(2, 0)
            write_gpio(3, 0)
            await asyncio.sleep(off_time)
            print("Green LED is Blinking") #Debug statement to reflect which color is blinkng
        elif blue: #Blue LED ON
            write_gpio(1, 1) #Blue LED
            write_gpio(2, 0) #Green LED
            write_gpio(3, 0) #Red LED
            await asyncio.sleep(on_time)
            write_gpio(1, 0)
            write_gpio(2, 0)
            write_gpio(3, 0)
            await asyncio.sleep(off_time)
            print("Blue LED is Blinking") #Debug statement to reflect which color is blinkng
        elif off: #LEDS are off
            write_gpio(1, 0) #Blue LED
            write_gpio(2, 0) #Green LED
            write_gpio(3, 0) #Red LED
            await asyncio.sleep(on_time)
            write_gpio(1, 0)
            write_gpio(2, 0)
            write_gpio(3, 0)
            await asyncio.sleep(off_time)
            print("LEDs are off") #Debug statement to reflect which color is blinkng
        else:
            await asyncio.sleep(0.1)  # Short delay to avoid busy waiting

    
#Implementing Button Presses using ASYNCIO    
async def get_btns(_loop):
    global red, green, blue, off
    while True:
        await asyncio.sleep(0.01)
        button = btns.read()
        button0 = btns[0].read()
        button1 = btns[1].read()
        button2 = btns[2].read()
        button3 = btns[3].read()
        if button0 == 1:  # Button 0 pressed, Using ==1 (button is high) to test button input
            red=True
            green=False
            blue=False
            off=False
            print("Button 0 was pressed") #Debug statement to determine button was pressed
        elif button1 == 1:  # Button 1 pressed
            red=False
            green=True
            blue=False
            off=False
            print("Button 1 was pressed") #Debug statement to determine button was pressed
        elif button2 != 0:  # Button 2 pressed, Using !=0 (button is not low) to test button input
            red=False
            green=False
            blue=True
            off=False
            print("Button 2 was pressed") #Debug statement to determine button was pressed
        elif button3 != 0:  # Button 3 pressed
            red=False
            green=False
            blue=False
            off=True
            print("button 3 was pressed") #Debug statement to determine button was pressed
        else:
            await asyncio.sleep(0.1)  # Short delay to avoid busy waiting
            
loop = asyncio.new_event_loop()
loop.create_task(pwm())
loop.create_task(get_btns(loop))
loop.run_forever()
loop.close()
print("Done.")
