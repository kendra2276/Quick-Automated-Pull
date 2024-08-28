## Quick-Automated-Pull

## Python
This repository contains the Python script used to create a program that monitors physician signatures on all orders. After extracting the data using SQL, the data is formatted in Python to set up the script for weekly execution. This overview includes only the Python script for simplicity.

## Project Overview
This project was initiated during a Kaizen Event. Orders arriving at the lab without physician signatures cause significant rework for accessioning and client relations, leading to delays in patient testing.

## Data Sources
The SQL script pulls data from the following tables:

Order Table: Contains information on orders, including whether a signature is missing based on boolean values.


## Automation
Once approved by the program manager, the program is automated using a batch file and Task Scheduler, running on a weekly basis. 
