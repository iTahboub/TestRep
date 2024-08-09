# First Come First Served

def FCFS(process_dict):
    t = 0  # to keep track of time and calculate processing times
    gantt = []
    temp_dict = process_dict.copy()
    processes = {}  # to store each process initialized by it PID and storing times as values
    idle_counter = 0

    while temp_dict:
        first_in = min(temp_dict,
                       key=lambda k: process_dict[k][1])  # Checking which process has the earliest arrival time
        arrive_time = temp_dict[first_in][1]
        burst_time = temp_dict[first_in][0]

        while t < arrive_time:  # Cheking if the earliest arrival time is less than 0 i.e. whether the CPU should act idle or not
            t += 1
            idle_counter += 1
            gantt.append('_')

        gantt.append(first_in)  # Appending in the gantt chart each process by according to its arrival time
        start_time = t
        t += burst_time
        finish_time = t

        response_time = start_time - arrive_time
        turnaround_time = finish_time - arrive_time
        waiting_time = turnaround_time - burst_time

        processes[first_in] = [response_time, turnaround_time, waiting_time]

        del temp_dict[first_in]

    waiting_times = [p[2] for p in processes.values()]
    turnaround_times = [p[1] for p in processes.values()]
    response_times = [p[0] for p in processes.values()]

    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
    avg_response_time = sum(response_times) / len(response_times)

    overview = [avg_waiting_time, avg_turnaround_time, avg_response_time, idle_counter]

    return gantt, processes, overview


def FCFS_Report():

    print("\n##################################### FIRST COME FIRST SERVED ALGORITHM ######################################\n")
    process_dict = {"P1": (3, 3), "P2": (7, 2), "P3": (1, 6), "P4": (5, 4)}

    gantt, procs, results = FCFS(process_dict)

    print(gantt, "\n------------------------------------------------------\n")

    for process, times in procs.items():
        print(f"Process {process}: Response Time: {times[0]}, Turnaround Time: {times[1]}, Waiting Time: {times[2]}")

    print("\n------------------------------------------------------\n")

    print(
        f"TU: Time Unit \n\nAverage waiting time : {results[0]} TU \nAverage Turnaround time : {results[1]} TU\nAverage Response time : {results[2]} TU\nCPU was idle for {results[3]} TU")

    print("\n**************************************************************************************************************\n")



###########################################################################################################################################
###########################################################################################################################################

# SJF NON-PRE EMPTIVE

def sjf_nonpreemptive(process_list):
    t = 0
    gantt = []
    completed_process = {}

    def get_burst_time(process):
        return process[0]

    while process_list:
        available_processes = []
        for p in process_list:
            if p[1] <= t:
                available_processes.append(p)
        if available_processes:
            available_processes.sort(key=get_burst_time)
            selected_process = available_processes[0]
            burst_time = selected_process[0]
            arrival_time = selected_process[1]
            pid = selected_process[2]

            if t < arrival_time:
                t = arrival_time
            start_time = t
            response_time = start_time - arrival_time
            t = start_time + burst_time
            gantt.append(pid)
            completion_time = t
            turnaround_time = completion_time - arrival_time
            waiting_time = turnaround_time - burst_time

            completed_process[pid] = [completion_time, turnaround_time, waiting_time, response_time]

            process_list.remove(selected_process)
        else:
            t += 1
            gantt.append("Idle")

    return gantt, completed_process


def sjf_Report():
    # First element for Burst Time, Second for Arrival time,and Third the name of the process
    process_list = [[3, 3, "p1"], [7, 2, "p2"], [1, 6, "p3"], [5, 4, "p4"]]
    gantt, completed_process = sjf_nonpreemptive(process_list)

    print("\n######################################### SORTEST JOB FIRST ALGORITHM ########################################\n")


    print("\nGantt Chart:", gantt, '\n')

    for process, value in completed_process.items():
        print("Process ", process)
        print("  Completion Time: ", value[0])
        print("  Turnaround Time: ", value[1])
        print("  Waiting Time: ", value[2])
        print("  Response Time: ", value[3])
        print('\n')

    turnaround = [value[1] for value in completed_process.values()]
    waiting_time = [value[2] for value in completed_process.values()]
    response_time = [value[3] for value in completed_process.values()]

    avg_waiting_time = sum(waiting_time) / len(waiting_time)
    print("The average waiting time:", avg_waiting_time)

    avg_turnaround_time = sum(turnaround) / len(turnaround)
    print("The average turnaround time:", avg_turnaround_time)

    avg_response_time = sum(response_time) / len(response_time)
    print("The average response time:", avg_response_time)

    print("\n**************************************************************************************************************\n")



###########################################################################################################################################
###########################################################################################################################################

# Priority First

# global variables for Priority algorithm

waitingTimes = {}
turnaroundTimes = {}
waitingTimesSum = 0.0
turnaroundTimeSum = 0.0


def availables(time, processes):  # function to determine the available processes
    availableProcesses = []
    for process in processes:
        arrivalTime = process[1]
        if arrivalTime <= time:
            availableProcesses.append(process)
    return availableProcesses


def find_completion_time(ganttChart, name):
    for i in range(len(ganttChart) - 1, -1, -1):  # iterate through the ganttChart in reverse
        if ganttChart[i] == name:
            return i + 1  # Return the time at which the process finishes


def calculateAverages(processes, ganttChart):  # a function that calculates the average of waiting and turnAround time
    responseTimesSum = 0
    turnaroundTimeSum=0
    waitingTimes=0
    responseTimes = {}
    for process in processes:
        name = process[0]
        arrivalTime = process[1]

        startTime = ganttChart.index(name)
        completionTime = find_completion_time(ganttChart, name)

        turnaroundTimes[name] = completionTime - arrivalTime
        responseTimes[name] = startTime - arrivalTime

        turnaroundTimeSum += turnaroundTimes[name]
        responseTimesSum += responseTimes[name]

    averageTurnaroundTime = turnaroundTimeSum / len(processes)
    averageResponseTime = responseTimesSum / len(processes)
    averageWaitingTime = averageResponseTime
    waitingTimes = responseTimes

    return averageTurnaroundTime, averageResponseTime, averageWaitingTime


def priorityScheduling(processes):
    time = 0
    ganttChart = []
    while processes:
        availableProcesses = availables(time, processes)  # determine what are the available processes

        if not availableProcesses:  # if no processes are available, increment time
            ganttChart.append("idle")
            time += 1
            continue

        currentProcess = min(availableProcesses,
                             key=lambda x: x[2])  # select process with the highest priority (smallest number)

        burstTime = currentProcess[3]
        name = currentProcess[0]
        while burstTime:  # simulate the burst time
            ganttChart.append(name)
            time += 1
            burstTime -= 1

        processes.remove(currentProcess)  # remove the process after completion

    return ganttChart


def priority_first_report():
    # process = [name, arrival time, priority, burst time]
    original_processes = [
        ["p4", 4.0, 3, 5],
        ["p1", 3.0, 4, 3],  # Change priority to see comprehend the difference between sjf and pfs
        ["p2", 2.0, 3, 7],
        ["p3", 6.0, 1, 1],
    ]

    ganttChart = priorityScheduling(original_processes.copy())
    avgTurnaroundTime, avgWaitingTime, avg_res_time = calculateAverages(original_processes, ganttChart)

    print("\n##################################### PRIORITY FIRST SCHEDULING ALGORITHM ####################################\n")
    print("Gantt Chart:", ganttChart)
    print("Average Turnaround Time:", avgTurnaroundTime)
    print("Average Waiting Time:", avgWaitingTime)
    print("Average Response Time: ", avgWaitingTime)

    print("\n\n//Note that response time = waiting time, and that it due to non-preemptive feature of the priority first scheduling//")
    print("\n**************************************************************************************************************\n")


###########################################################################################################################################
###########################################################################################################################################

# Compariosn Analysis

import matplotlib.pyplot as plt
import numpy as np
import mplcursors

# Use this dictionary for inserting the values of FCFS
process_dict = {"P1": (3, 3), "P2": (7, 2), "P3": (1, 6), "P4": (5, 4)}
gantt, procs, results = FCFS(process_dict)

#########################################################################################
#The following is the data needed for inserting SJF data in the bar char

# Use this array for inserting the values of SJF Non-Pre emptive
process_list = [[3, 3, "p1"], [7, 2, "p2"], [1, 6, "p3"], [5, 4, "p4"]]
gantt2, completed_process = sjf_nonpreemptive(process_list)  #
#
turnaround = [value[1] for value in completed_process.values()]  #
waiting_time = [value[2] for value in completed_process.values()]  #
response_time = [value[3] for value in completed_process.values()]  #
#  This block of code is only for SJF use
avg_waiting_time_sjf = sum(waiting_time) / len(waiting_time)  #
#
avg_turnaround_time_sjf = sum(turnaround) / len(turnaround)  #
#
avg_response_time_sjf = sum(response_time) / len(response_time)  #

##########################################################################################
#The following is the data needed for inserting PFS data in the bar char
# process = [name, arrival time, priority, burst time]

original_processes = [
        ["p4", 4.0, 3, 5],
        ["p1", 3.0, 4, 3],     #Change priority to see comprehend the difference between sjf and pfs
        ["p2", 2.0, 3, 7],
        ["p3", 6.0, 1, 1],
    ]

ganttChart = priorityScheduling(original_processes.copy())
avgTurnaroundTime, avgWaitingTime, avg_res_time_pf = calculateAverages(original_processes, ganttChart)

# Data
algorithms = ['FCFS', 'SJF Non-pre emptive', 'Priority first']
avg_wait_time = [results[0], avg_waiting_time_sjf, avgWaitingTime]
avg_res_time = [results[2], avg_response_time_sjf, avgWaitingTime]
avg_turnaround_time = [results[1], avg_turnaround_time_sjf, avgTurnaroundTime]

# Bar chart parameters
bar_width = 0.25
indices = np.arange(len(algorithms))

# Plotting the bar chart
fig, ax = plt.subplots()

# Creating bars for each attribute
bar1 = ax.bar(indices, avg_wait_time, bar_width, label='AVG Waiting time')
bar2 = ax.bar(indices + bar_width, avg_res_time, bar_width, label='AVG Response time')
bar3 = ax.bar(indices + 2 * bar_width, avg_turnaround_time, bar_width, label='AVG Turnaround time')

# Adding labels, title, and legend
ax.set_xlabel('Algorithms')
ax.set_ylabel('Time Unit')
ax.set_title('Comparison of CPU Scheduling algorithms')
ax.set_xticks(indices + bar_width)
ax.set_xticklabels(algorithms, rotation=0, ha='right')
ax.legend()

ax.set_yticks(np.arange(0, max(max(avg_wait_time), max(avg_res_time), max(avg_turnaround_time)) + 3.25, 1))


# Adding tooltips using mplcursors
def hover_annotation(bar_container):
    mplcursors.cursor(bar_container, hover=True).connect("add", lambda sel: sel.annotation.set_text(
        f'{sel.artist.get_label()}\nValue: {sel.target[1]:.1f}'
    ))


hover_annotation(bar1)
hover_annotation(bar2)
hover_annotation(bar3)

# Displaying the chart
plt.tight_layout()
plt.show()

######################################################################################
# Reporting the algorithms

FCFS_Report()
sjf_Report()
priority_first_report()
