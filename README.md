# Arduino-GM-counter

Author: Mateusz Wolniewicz
Date: 06/06/2024
Version: 1.1.0
Licence: MIT Open Source 
OS and sotfware version: Windows 11 with Python 3.12.3 and Arduino IDE 2.3.2.

Update:  Poisson function fitting and displaying is added. Some minor correctios are made. 

Arduino program proceses the signal from Geiger-Muller counter board. 
Noumber of counts per given time interval is being send via USB using serial communication.
Histogram.py program reads the data form Arduino and creates the histogram.
Program fits the Poisson function based on the mean as the lambda parameter.  
Graph is acctualised with data every given time period (same as counting interval).
Saving data is possible. Data saved are number of counts per given time period and time period itself. Each record will be in new column. 
Variables such as time interval, conncection port, saving data to file and more can be determined using parameters.
To set the parameters of program run it with arguments as given below.

Command-line arguments:

* '-i', '--interval', type=int, default=1000,  'Interval period of reading the counts from Arduino in milliseconds'
* '-p', '--port', type=str, default='COM6',  'Port where Arduino is connected'
* '-min', '--min_counts', type=int, default=0,  'Lower bound of histogram'
* '-max', '--max_counts', type=int, default=20,  'Upper bound of histogram'
* '-r', '--records', type=int, default=1000,  'Number of records to be kept on the histogram'
* '-s', '--save_data', type=bool, default=False,  'Whether to save data to a file'
* '-fn', '--filename', type=str, default='./geiger_data.csv',  'CSV file name for saving data'

Example: 
python Histogram_v1.1.0.py -p COM6 -min 0 -max 20 -i 6000 -r 1000 -s True -f ./geiger_data.csv


Requirements: 
A) Hardware:
1. Arduino ESP32 board (or any Arduino-like board with digitalRead and Serial capablity)
2. RadiationD-v1.1(CAJOE) Geiger-Muller counter board.
3. PC device with USB serial communication and screen.
4. USB C to USB A cable (or proper USB cable to connct PC and Arduino). 

B) Software:
1. histogram.ino installed on the Arduino board.
2. Python verion 3.12.3 or above on PC device (not tested for back capability).
3. Histogram.py 

Hardware connections:
1.Connect the GND on Arduino to the GND on the Geiger counter board.
2.Connect the 5V on the Geiger counter to the 5V on Arduino OR connect the external power supply.
3.Connect the VIN on the Geiger counter to the D2 digital pin on the Arduino ESP32. 
4.Connect the Arduino via USB cable to the PC. 
5.Turn on the GM counter board. 

NOTE: 
If different Arduino board is used make sure that the propoer pin name is in the histogram.ino code.
One can change pin to any digital pin on board via changing the value of the GM_PIN variable and reuploading the code to the board. 



Acknowledgements:
This program was created as a project for Software in Physical Experiments course during Physics and Nuclear Technology subject on Warsaw Universtity of Technology.   
Many thanks to my teacher Marcin Slodkowski, PhD and my colleague inz. Piotr Hasiec for inspiration and help during this project. 
