#Part A3.1: Access PMU from Python
import ctypes
# Load the shared library
_libInC = ctypes.CDLL('./libMyLib.so')
# Initialize counters (reset and disable divider)
_libInC.init_counters(1, 1)

# Get start cycle count
start_cycles = _libInC.get_cyclecount()

# Code to measure (example: a loop)
for _ in range(20):
    pass​
# Get end cycle count
end_cycles = _libInC.get_cyclecount()

# Calculate and print elapsed cycles
elapsed_cycles = end_cycles - start_cycles
print(f"Elapsed cycles: {elapsed_cycles}")

#PART A3.2:Comparing and Gathering Data
import time
import os
import sys
import ctypes
import pylab as pl
from IPython import display
import psutil
import matplotlib.pyplot as plt
import numpy as np
psutil.cpu_percent(percpu=True)
[7.8, 0.0]
%matplotlib inline

while True:
    def recur_fibo(n):     
        if n <= 1:
            return n
        else:
            return recur_fibo(n - 1) + recur_fibo(n - 2)​
    tic = time.time()

    try:
        nterms = int(input("Enter the number of Fibonacci terms to calculate: "))
        command = f"taskset -c 1 {nterms}"
        os.system(command)​
    print(f"Error executing command: {command}. Exit code: {exit_code}")

        if nterms <= 0:
            print("Please enter a positive integer.")
        else:
            recur_fibo(nterms)​
    except ValueError:
        print("Invalid input. Please enter an integer.")

    tac = time.time()
    print('time spent: {}'.format(tac - tic))​

    X = np.arange(1)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    for i in range(10):
        data = psutil.cpu_percent(percpu=True)
        ax.cla()
        ax.bar(X + 0.0, data[0]/100, color = 'b', width = 0.5)
        ax.bar(X + 1.0, data[1]/100, color = 'g', width = 0.5)
        display.clear_output(wait=True)
        display.display(plt.gcf())
    plt.clf()
    print('time spent: {}'.format(tac - tic))