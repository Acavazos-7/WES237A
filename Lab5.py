#!/usr/bin/env python
# coding: utf-8

# # Using PYNQ library for PMOD_ADC
# 
# This just uses the built in Pmod_ADC library to read the value on the PMOD_AD2 peripheral.

# In[1]:


from pynq.overlays.base import BaseOverlay
from pynq.lib import Pmod_ADC
base = BaseOverlay("base.bit")


# In[2]:


adc = Pmod_ADC(base.PMODA)


# Read the raw value and the 12 bit values from channel 1.
# 
# Refer to docs: https://pynq.readthedocs.io/en/v2.1/pynq_package/pynq.lib/pynq.lib.pmod.html#pynq-lib-pmod

# In[12]:


adc.read_raw(ch1=1, ch2=0, ch3=0)


# In[11]:


adc.read(ch1=1, ch2=0, ch3=0)


# # Using MicroblazeLibrary
# 
# Here we're going down a level and using the microblaze library to write I2C commands directly to the PMOD_AD2 peripheral
# 
# Use the documentation on the PMOD_AD2 to answer lab questions

# In[13]:


from pynq.overlays.base import BaseOverlay
from pynq.lib import MicroblazeLibrary
base = BaseOverlay("base.bit")


# In[14]:


liba = MicroblazeLibrary(base.PMODA, ['i2c'])


# In[15]:


dir(liba) # list the available commands for the liba object


# In the cell below, open a new i2c device. Check the resources for the i2c_open parameters

# In[41]:


device = liba.i2c_open(3, 2 ) # TODO open a device


# In[42]:


dir(device) # list the commands for the device class


# Below we write a command to the I2C channel and then read from the I2C channel. Change the buf[0] value to select different channels. See the AD spec sheet Configuration Register. https://www.analog.com/media/en/technical-documentation/data-sheets/AD7991_7995_7999.pdf
# 
# Changing the number of channels to read from will require a 2 byte read for each channel!

# In[68]:


buf = bytearray(2)
buf[0] = int('00000000', 2)
device.write(0x28, buf, 1)
device.read(0x28, buf, 2)
print(format(int(((buf[0] << 8) | buf[1])), '#018b'))


# Compare the binary output given by ((buf[0]<<8) | buf[1]) to the AD7991 spec sheet. You can select the data only using the following command

# In[69]:


result_12bit = (((buf[0] & 0x0F) << 8) | buf[1])
print(result_12bit)


# # Using MicroBlaze

# In[73]:


base = BaseOverlay("base.bit")


# In[83]:


get_ipython().run_cell_magic('microblaze', 'base.PMODA', '\n#include "i2c.h"\n\nint read_adc(){\n    i2c i2c_device = i2c_open(3, 2);\n    unsigned char buf[2];\n    buf[0] = 0;\n    i2c_write(i2c_device, 0x28, buf, 1);\n    i2c_read(i2c_device, 0x28, buf, 2);\n    return ((buf[0] & 0x0F) << 8) | buf[1];\n}\n')


# In[85]:


read_adc()


# In[ ]:


S

