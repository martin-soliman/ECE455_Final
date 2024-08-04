import argparse
import csv
import math
from fractions import Fraction
from functools import reduce

TIME_STEP = 0.001 #global const for precision of up to 0.001 for time-based operations
INDEX_TO_TIME = 1000 #global constant to convert time_chart index to corresponding time 

def read_inputs(fin):
    try:
        with open(fin, 'r') as inputs: #file opened
            reader = csv.reader(inputs, delimiter=',')
            rows = []
            for row in reader: #row contains string data for current row
                rows.append([float(num) for num in row]) #list comprehension which converts each row to int values, and appends it to rows 2D sarray
        return rows
    except FileNotFoundError: #filepath does not exist
        print("File not found :(")
    except Exception as e: #other unexpected errors
        print(f"Error: {e}")

def isUniSchedulable(executions, periods):
    #ensuring that set of tasks can be scheduled on UNIprocessor system

    tot_util = 0
    for i in range(0,len(executions)):
        tot_util += executions[i]/periods[i]

    if tot_util > 1:
        return False
    else:
        return True

def gcd(a, b):
    return math.gcd(a, b) #returning gcd of a and b

def lcm(a, b):
    return abs(a * b) // gcd(a, b) #using gcd to find lcd of a and b

def find_hyperperiod(periods):
    #since periods can be decimal up to 0.001 precision, we need to use fractions to find LCM 

    fracs = [Fraction(period).limit_denominator() for period in periods] #list comprehension to convert each float into a fraction

    nums = [frac.numerator for frac in fracs] #list comprehension for numerators
    lcm_num = reduce(lcm, nums) #iteratively finding lcm of ALL numerators

    denoms = [frac.denominator for frac in fracs] #list comprehension for denominators 
    gcd_denom = reduce(gcd, denoms) #iteratively finding gcd of ALL denominators

    hyperperiod = Fraction(lcm_num, gcd_denom) #the hyperperiod (lcm of all periods) is the fraction lcd_num/gcd_denom
    return float(hyperperiod)

def prep_RM(tasks):
    #block needed to prepare data BEFORE simulation
    if(tasks):
        executions = []
        periods = []
        deadlines = []
        for task in tasks:
            executions.append(task[0])
            periods.append(task[1])
            deadlines.append(task[2])
        
        if not isUniSchedulable(executions, periods):
            return 

        hyperperiod = find_hyperperiod(periods)
        priorities = {} #priorities dict, key is task #, value is task period
        for i in range(0, len(periods)):
            priorities[i] = periods[i]
        priorities = dict(sorted(priorities.items(), key=lambda item: item[1])) #sorting based on values of priorities dict
        
        count = 1
        for key in priorities:
            priorities[key] = count
            count += 1
        #print(f"Priorities: {priorities}")

        release_times = {} #dict to store release times, key is release time, value is array of tasks
        for key in priorities:
            release_time = periods[key]
            while release_time <= hyperperiod:
                if release_time not in release_times.keys():
                    release_times[release_time] = []
                release_times[release_time].append(key)
                release_time += periods[key]
        
        #print(f"Release times: {release_times}")
        
        return {'executions': executions,
                'periods': periods,
                'deadlines': deadlines,
                'hyperperiod': hyperperiod,
                'priorities': priorities,
                'release_times': release_times
                }
    else:
        return 

def simulate_RM(RM_params):
    executions = RM_params['executions']
    periods = RM_params['periods']
    deadlines = RM_params['deadlines']
    hyperperiod = RM_params['hyperperiod']
    priorities = RM_params['priorities']
    release_times = RM_params['release_times']

    time_chart = [] #array to store task executed at each time step of 0.001s
    preemptions = {} #dict to store preemptions, key is task #, value is num preemptions
    release_queue = [] #initializing queue of tasks at t = 0 based on task priorities, queue contains task # and remaining exec time
    for key in priorities:
        preemptions[key] = 0
        release_queue.append([key, executions[key]/TIME_STEP])
    
    released = release_queue.pop(0)
    curr_task = released[0]
    t_exec = released[1]
    start_time = 0

    for i in range(0, int((hyperperiod/TIME_STEP)+1)): #simulating up until hyperperiod
        time_chart.append(curr_task)
        if (i + 1)/INDEX_TO_TIME not in release_times.keys() and (curr_task == -1 or i < (start_time + t_exec - 1)): #no task(s) released AND (no task currently OR curr task is not finished execution)
            continue

        elif (i + 1)/INDEX_TO_TIME in release_times.keys(): #new task(s) released
            for task in release_times[(i + 1)/INDEX_TO_TIME]:
                if(curr_task == -1 or priorities[task] < priorities[curr_task] or i >= (start_time + t_exec - 1)): #processor is idle, new task is higher priority than curr task, or curr task JUST finished
                    if curr_task != -1 and i < (start_time + t_exec - 1): #if processor isn't idle and curr_task isn't already finished
                        release_queue.insert(0, [curr_task, executions[curr_task]*INDEX_TO_TIME - (i + 1 - start_time)]) #placing curr task and remaining exec time back on queue
                        preemptions[curr_task] += 1 #incrementing preemption count of curr task
                    curr_task = task #updating curr task
                    t_exec = executions[task]*INDEX_TO_TIME #updating remaining exec time
                    start_time = i + 1 #updating start_time
                else: #place task in queue according to priority
                    count = 0
                    for n in release_queue:
                        if priorities[task] >= priorities[n]:
                            count += 1
                        else:
                            break
                    release_queue.insert(count, [task, executions[task]*INDEX_TO_TIME])
                        
        elif i >= (start_time + t_exec - 1): #curr task finished execution
            if release_queue:
                released = release_queue.pop(0) #releasing next task
                curr_task = released[0]
                t_exec = released[1]
                start_time = i + 1 #storing start time of release
            else:
                curr_task = -1; #no tasks to release (idle processor)
        
    output = []
    for i in range(0, len(periods)):
        if i in preemptions.keys():
            output.append(preemptions[i])
        else:
            output.append(0)
    #print(f"Output: {output}")
    return output

def output_results(results):
    if results:
        print(1)
        for i in range(0, len(results)):
            if i == len(results) - 1:
                print(results[i])
            else:
                print(f"{results[i]}", end=', ')

def main():
    parser = argparse.ArgumentParser(description="Parse the inputs txt file") #Instantiating parser object
    parser.add_argument('file', type=str, help="Path to the txt file to be processed") #Adding argument to parser
    
    args = parser.parse_args() #Assigning args from cmd to args var
    tasks = read_inputs(args.file) #Passing arg associated with inputs txt filepath for processing

    #tasks = [[1,3,3],[2,4,5]]

    RM_params = prep_RM(tasks)
    if RM_params:
        results = simulate_RM(RM_params)
    else:
        results = None
    output_results(results)

if __name__ == "__main__":
    main()