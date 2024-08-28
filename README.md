## Quick-Automated-Pull

## Python
This repository contains  the Python script used to create the program that monitored the physician signatures on all orders. Once the data is extracted using SQL, it was then formated in Python. The  formating in Python was to set up the script to run on a weeklly basis.  To keep this a high level overview, jsut the Python script will be included.

## Project Overview
The need for this project came from a Kaizen Event.  When orders arrive at the lab without a physician signatures this causes a lot of re-work for accessioning and client relations. This then ultimately leads to a  delay in  patient testing.

## Data Sources
The SQL script pulls data from the following tables:

Order Table: Contains information on orders placed  such as if an order is missing a signature based on boolean values. 


## Automation
Finally, once the data has been approved by the program manager the program is then automated using a batch file along with Task Scheduler. The program runs on a weekly basis. 
