# Author: Mateusz Wolniewicz
# Date: 06/06/2024
# Version: 1.1.0
# Licence: Open Source
# Pyhon version: 3.12.3

# Update: Poisson function fitting and displaying is added. Some minor correctios are made. 

# This program reads the data form Arduio board via serial port. 
# Data are being displayed on the histogram. 
# Poisson function is fitted to the data with mean as a lambda parameter.
# Graph is acctualized wih given time interval.
# Variables such as time interval, conncection port, saving data to file 
# and more can be determined using flags. For more informations see "readme.md"

# Import libraries
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv
import os
import atexit
import argparse
from scipy.stats import poisson


# Command-line arguments
parser = argparse.ArgumentParser(description='Geiger-Muller Counter Histogram')
parser.add_argument('-i', '--interval', type=int, default=1000, help='Interval period of reading the counts from Arduino in milliseconds')
parser.add_argument('-p', '--port', type=str, default='COM6', help='Port where Arduino is connected')
parser.add_argument('-min', '--min_counts', type=int, default=0, help='Lower bound of histogram')
parser.add_argument('-max', '--max_counts', type=int, default=20, help='Upper bound of histogram')
parser.add_argument('-r', '--records', type=int, default=1000, help='Number of records to be kept on the histogram')
parser.add_argument('-s', '--save_data', type=bool, default=True, help='Whether to save data to a file')
parser.add_argument('-fn', '--filename', type=str, default='./geiger_data.csv', help='CSV file name for saving data')
args = parser.parse_args()

# Assign arguments to variables
Arduino_port = args.port
min_counts = args.min_counts
max_counts = args.max_counts
interval = args.interval
records = args.records
save_data = args.save_data
csv_filename = args.filename

args = parser.parse_args()

# Configure the serial port
ser = serial.Serial(Arduino_port, 115200)  

# Function for setting countig period
def set_counting_period(period):
    ser.write(f"{period}".encode('utf-8'))

# Initialize data storage
data = []
limits = [l for l in range(min_counts, max_counts, 1)]

# Setup the plot
fig, ax = plt.subplots()
bin_labels = [f"{limits[i]}" for i in range(len(limits))]+[(f"{max_counts}+")]
bars = ax.bar(bin_labels, [0]*len(bin_labels))

# Check if it is required to save data
if (save_data == True):
    # Initialize CSV file and open it
    file_exists = os.path.exists(csv_filename)
    csv_file = open(csv_filename, mode='a', newline='')
    csv_writer = csv.writer(csv_file)

    # Write header if the file is new
    if not file_exists:
        csv_writer.writerow(['Counts per', interval, 'ms'])

    # Ensure the file is closed on exit
    def close_file():
        csv_file.close()
    atexit.register(close_file)

    # Function to save data to CSV
    def save_to_csv(count):
        csv_writer.writerow([count])
        csv_file.flush()  # Ensure data is written to the file

# Function to update the histogram
def update_histogram(frame):
    global data

    # Read data from the serial port
    if ser.in_waiting:
        count = int(ser.readline().decode('utf-8').strip())
        data.append(count)
        
        # Save data (if required)
        if (save_data == True):
            save_to_csv(count)
    
        # Delete the oldest reocord when limit of records achived
        if len(data) > records:
            data.pop(0)
        
        # Initiate histogram bins
        bins = ([0]*(len(limits)+1))

        # Add points to the histogram bins
        for d in data:
            for k in range(0, len(limits)):
                if d <= limits[k]:
                    bins[k] += 1
                    break
            if d > limits[-1]:
                bins[-1] += 1   

        # Generate Poisson distribution based on the mean
        mean_counts = np.mean(data)
        poisson_dist = [poisson.pmf(k, mean_counts) * len(data)
                         for k in range(min_counts, len(limits)+1)]

        # Update the bars
        for bar, bin_count in zip(bars, bins):
            bar.set_height(bin_count)
        
        # Clear and plot Poisson fit
        ax.clear()
        ax.bar(bin_labels, bins, alpha=0.7, label='Observed')
        ax.plot(bin_labels, poisson_dist, 'r-', marker='o', label='Poisson fit')

        # Add descriptions to graph and update the Y sacle
        ax.set_ylim(0, max(max(bins)+1, max(poisson_dist)+1))
        ax.set_xlabel(f'Counts per {interval}ms range')
        ax.set_ylabel('Counts')
        ax.set_title('Geiger-Muller Counter Histogram')
        ax.legend()

    return bars

# Set up the counting period
set_counting_period(interval) 

# Set up the animation
ani = animation.FuncAnimation(fig, update_histogram, interval)

# Plot the graph
plt.xlabel('Counts per %dms range' % (interval))
plt.ylabel('Counts')
plt.title('Geiger-Muller Counter Histogram')
plt.show()
