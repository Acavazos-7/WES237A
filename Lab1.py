asyncio example
import asyncio

cond = False  # Initial state is stopped

async def flash_leds():
    global cond
    while True:
        if cond:  # Only run the LED sequence if cond is True
            led4.write(0x1)
            led5.write(0x7)
            await asyncio.sleep(0.1)
            led4.write(0x0)
            led5.write(0x0)
            await asyncio.sleep(0.05)
            led4.write(0x1)
            led5.write(0x7)
            await asyncio.sleep(0.1)
            led4.write(0x0)
            led5.write(0x0)
            await asyncio.sleep(0.05)

            led4.write(0x7)
            led5.write(0x4)
            await asyncio.sleep(0.1)
            led4.write(0x0)
            led5.write(0x0)
            await asyncio.sleep(0.05)
            led4.write(0x7)
            led5.write(0x4)
            await asyncio.sleep(0.1)
            led4.write(0x0)
            led5.write(0x0)
            await asyncio.sleep(0.05)
        else:
            await asyncio.sleep(0.1)  # Short delay to avoid busy waiting

async def get_btns(_loop):
    global cond
    while True:
        await asyncio.sleep(0.01)
        button = btns.read()
        if button == 0:  # Button 0 pressed
            cond = False
        elif button == 1:  # Button 1 pressed
            cond = True

loop = asyncio.new_event_loop()
loop.create_task(flash_leds())
loop.create_task(get_btns(loop))
loop.run_forever()
loop.close()
led4.write(0x0)
led5.write(0x0)
print("Done.")


GPIO example
from pynq.overlays.base import BaseOverlay
import time
from datetime import datetime
base = BaseOverlay("base.bit")
%%microblaze base.PMODB

#include "gpio.h"
#include "pyprintf.h"

// Function to turn on/off a selected pin of PMODB
void write_gpio(unsigned int pin, unsigned int val) 
{
    gpio pin_out = gpio_open(pin);
    gpio_set_direction(pin_out, GPIO_OUT);
    gpio_write(pin_out, val);
}

// Function to read the value of a selected pin of PMODB
unsigned int read_gpio(unsigned int pin) 
{
    gpio pin_in = gpio_open(pin);
    gpio_set_direction(pin_in, GPIO_IN);
    return gpio_read(pin_in);
}

write_gpio(0, 1);
write_gpio(1, 0);
read_gpio(2)
read_gpio(3)
