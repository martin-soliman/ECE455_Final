import argparse
import csv

def read_inputs(fin):
    try:
        with open(fin, 'r') as inputs: #file opened
            reader = csv.reader(inputs, delimiter=',')
            rows = []
            for row in reader: #row contains string data for current row
                rows.append([int(num) for num in row]) #list comprehension which converts each row to int values, and appends it to rows 2D sarray
        print(rows)
    except FileNotFoundError: #filepath does not exist
        print("File not found :(")
    except Exception as e: #other unexpected errors
        print(f"Error: {e}")

def ouput_results(isSchedulable, preemptions):
    if isSchedulable:
        print(1)
        print(preemptions)
    else:
        print(0)

def main():
    parser = argparse.ArgumentParser(description="Parse the inputs txt file") #Instantiating parser object
    parser.add_argument('file', type=str, help="Path to the txt file to be processed") #Adding argument to parser
    
    args = parser.parse_args() #Assigning args from cmd to args var
    read_inputs(args.file) #Passing arg associated with inputs txt filepath for processing

if __name__ == "__main__":
    main()