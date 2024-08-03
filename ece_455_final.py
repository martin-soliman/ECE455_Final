import argparse
import csv
import math
from fractions import Fraction
from functools import reduce

TIME_STEP = 0.001 #global const for precision of up to 0.001 for time-based operations

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

        release_times = {} #dict to store release times, key is task#, value is array of release times
        for key in priorities:
            release_time = 0
            release_times[key] = []
            while release_time <= hyperperiod:
                release_times[key].append(release_time)
                release_time += periods[key]
        
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

    time_chart = [] #array used to store task executed at each time step of 0.001s

    for i in range(0, hyperperiod, TIME_STEP):
        curr_task = 


def output_results(results):
    if results:
        print(1)
        print(results)
    else:
        print(0)

def main():
    parser = argparse.ArgumentParser(description="Parse the inputs txt file") #Instantiating parser object
    parser.add_argument('file', type=str, help="Path to the txt file to be processed") #Adding argument to parser
    
    args = parser.parse_args() #Assigning args from cmd to args var
    tasks = read_inputs(args.file) #Passing arg associated with inputs txt filepath for processing

    RM_params = prep_RM(tasks)
    if RM_params:
        results = simulate_RM(RM_params)
    else:
        results = None
    #output_results(results)

if __name__ == "__main__":
    main()