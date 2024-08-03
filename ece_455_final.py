import argparse
import csv
import math
from fractions import Fraction
from functools import reduce

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

def simulate_RM(tasks):
    if(tasks): #sorting data
        executions = []
        periods = []
        deadlines = []
        for task in tasks:
            executions.append(task[0])
            periods.append(task[1])
            deadlines.append(task[2])
        
        if not isUniSchedulable(executions, periods):
            return [False, None]

        hyperperiod = find_hyperperiod(periods)
    else:
        return [False, None]

def output_results(isSchedulable, preemptions):
    if isSchedulable:
        print(1)
        print(preemptions)
    else:
        print(0)

def main():
    parser = argparse.ArgumentParser(description="Parse the inputs txt file") #Instantiating parser object
    parser.add_argument('file', type=str, help="Path to the txt file to be processed") #Adding argument to parser
    
    args = parser.parse_args() #Assigning args from cmd to args var
    tasks = read_inputs(args.file) #Passing arg associated with inputs txt filepath for processing

    results = simulate_RM(tasks)
    #output_results(results[0], results[1])

if __name__ == "__main__":
    main()