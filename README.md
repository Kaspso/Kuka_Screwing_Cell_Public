# KUKA Screwing Cell

This repository contains the python code that has been developed for AAU's newer screwing cell, which is based on the KUKA ... robot and the ... screwdriver. The repository also contains the sampled data files to make them accessible for post processing.

The python file `main_program.py` starts a GUI wherefrom the cell can be controlled together with the HMI.
The robot and screwdriver can be controlled from the GUI. As an example the fixture can be controlled to be either open or closed. The screwing program and the screwing process can also be started from the GUI. Also, labels can be edited and deleted from the GUI.

The PLC and PC is connected over ethernet and use the python snap7 module.

The Robot and PC for the streaming of data is connected by UDP/IP. The robot sends the tool center point position, forces and moments.

For commanding the robot from the PC a TCP/IP connection is used. This connection send what state the robot should go to.

Robot ip 192.168.1.50
Data collection Pc ip 192.168.1.100
PLC ip 192.168.1.1

gateway ip: 192.168.1.5

To prepare and run the cell, see the README file in _Guide_ folder