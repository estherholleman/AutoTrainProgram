# AutoTrainProgram
This repository contains the Python code for the automated program to run the expriment described in the journal article An incremental training method with automated, extendable maze for training spatial behavioral tasks in rodents (published here: https://rdcu.be/bPO0l). 

## Getting Started
Clone this repository using either the green 'clone or download' button or using the following command:
```
git clone https://github.com/estherholleman/AutoTrainProgram.git
```

Run main.py, this will bring up the graphical interface of the program. 

Extra functions used in main.py are located in the 'secondary' folder. 

The Arduino folder contains the .ino files for the micro-controllers (feeder, master, and slave). It also includes several files for testing purposes (for instance test_I2C to test the I2C connection). 

An (initially empty) folder labeled 'experiments' should also be present in the same folder as main.py. This is where the results/outcomes of the training sessions will be saved. 

