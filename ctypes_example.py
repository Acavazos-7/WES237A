#!/usr/bin/env python
# coding: utf-8

# # ctypes
# The following imports ctypes interface for Python

# In[1]:


import ctypes


# Now we can import our shared library

# In[2]:


_libInC = ctypes.CDLL('./libMyLib.so')


# Let's calll our C function, myAdd(a, b).

# In[5]:


_libInC.myAdd(2, 5)


# This is cumbersome to write, so let's wrap this C function in a Python function for ease of use.

# In[7]:


def addC(a,b):
    return _libInC.myAdd(a,b)


# Usage example:

# In[8]:


addC(10, 202)


# # Multiply
# 
# Following the code for your add function, write a Python wrapper function to call your C multiply code

# In[10]:


def multiplyC(a,b):
    return _libInC.myMultiply(a,b)


# In[11]:


multiplyC(7,11)


# In[ ]:




