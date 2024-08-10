This program is built on external python libraries, so make sure that you install primarily Python 3.10 and any compatible IDE, and install the following external libraries, either from your terminal or, if you use PyCharm download them from

Settings > Project > Python interpreter > +, the libraries you will need:

matplotlib
numpy
mplcursors 

for installing from terminal just type

pip install (Library name)
--------------------------------------------------------------------------------------------------------------------------

For firing the program, simply plug in your values of (Arrival Time, Burst Time, Priority) in 2 places in the script.

1. Entering data in this part is purposed to produce detailed report for each algorithm you wish to examine. It is in the report function of each algorithm. 

e.g. in FCFS_report(), you have a dictionary consisting of ("Process Name", Burst time, Arrival time), the places might be filled, but you can easily remove the values and plug in your values. 

-------------------------------------------------------------------------------------------------------------------------

2. Entering data in the section is used to draw a visual graph of the 3 scheduling algorithms and each having 3 Bars, Response time, waiting time, and turnaround time, respectively, the operation happens in the main (main section), starting from line 259.

As developers we copied the exact procedures used in the reports, your task as user to plug in any values you want, different from the report or the same ones, your choice, and the program will do the rest in terms of designing and drawing.

e.g.: Entering data for visualization in the Priority first algorithm, only replace the asterisks with your values

# process = [name, arrival time, priority, burst time]
original_processes = [
        ["*", *, *, *],
        ["*", *, *, *],     #Change priority to see comprehend the difference between sjf and pfs
        ["*", *, *, *],
        ["*", *, *, *],
    ]


#########################################################################################################################

                                             HAVE A HAPPY EXPERIENCE :)


