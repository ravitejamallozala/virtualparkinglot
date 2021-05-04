# Virtual Parking Lot 

## Problem statement:
We own a parking lot that can hold up to ‘n’ cars. 
slots is given numbers starting at 1 increasing with increasing distance from the entry point.
Implement automated ticketing system that allows our customers to use our parking lot.

Inputs are given in a file where all the commands along with parking slot size will be provided.
Input filepath is given as user input when program is run.

## Project Setup & Installation:

### For Ubuntu Users:

- Installations required to run the project can be installed by running the shell script provided.
- open terminal, navigate to the project directory.

Command:-
***sh ubuntu_install.sh

### For Mac Users:
- Installations required to run the project can be installed by running the shell script provided.
- open terminal, navigate to the project directory.

Command:-
***sh mac_install.sh


### Running the project: (Both Mac and Ubuntu Users)
- open terminal, navigate to the project directory.
Command:-
***sh run.sh
  
- We can also pass the file name as command line arguments
for example:

Command:
  ***sh run.sh test_files/inp.txt

- We can also run the program directly using python 

Command:
  ***python3 virtual_parking.py
  
- can also pass filename as command line argument
  
Command:
  ***python3 virtual_parking.py
  
### Running the Unittests cases: (Both Mac and Ubuntu Users)
- open terminal, navigate to the project directory.

Command:-
***sh run_unittest.sh 

### Project Code details:
- it is a python project with no additional packages used.  
- Assuming all the commands in the given input file are in correct format. Min validations on commands are done.
- Indian registration number format is accepted.
https://en.wikipedia.org/wiki/Vehicle_registration_plate#India
- You can input the file name as command line arguments given as per instructions or type it as user input.
- Basic unittests are written to check the code correctness, we can run them using the instructions given above. 
- Sample input files are present in the "test_files" Directory. 
