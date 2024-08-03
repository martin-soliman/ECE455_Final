import argparse

def read_inputs(fin):
    try:
        with open(fin, 'r') as inputs:
            content = inputs.read()
            print("File content:")
            print(content)
    except FileNotFoundError: 
        print("File not found :(")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse the inputs txt file") #Instantiating parser object
    parser.add_argument('file', type=str, help="Path to the txt file to be processed") #Adding argument to parser
    
    args = parser.parse_args() #Assigning args from cmd to args var
    read_inputs(args.file) #Passing arg associated with inputs txt filepath for processing

if __name__ == "__main__":
    main()