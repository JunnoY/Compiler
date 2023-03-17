import argparse
import os.path
import re

# read the input file name and the output file name from terminal using a parser
# the parser gives information of the format of the commands the user should type at terminal
parser = argparse.ArgumentParser(description ='Input format')
parser.add_argument('input',  help = 'Path of the input file.')
parser.add_argument('output', help = 'Path of the output file.')
args = parser.parse_args()
if not os.path.exists(args.input):
    print("There is no valid input file, or the input file does not exist.")
    quit()
else:
    input_file = args.input
    output_file = args.output
    # create a list of upper case letters of the alphabets
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # create a constraint set which stores all the inference nodes of a given node
    constraint_set = {}

    # crate a colour set which stores the colour of each node
    colour_set = {}

    # error state
    error = False

    # regex
    regex = re.compile(r'^\d+(?: +\d+)*$')
    '''
          ^\d_: Starts with one or more digit (a value with one or more digits)
          (?: \d+)*: Zero or more occurrences of (one or more) space followed by one or more digit (non-capturing group)
          $: Ends at the last digit
    '''

   # read the input file and check if the format of the input file matches the regex defined above
    with open(input_file, 'r') as fp:
        file_line = fp.read().splitlines()
        sentence = ''
        for i in range(len(file_line)):
            if i < len(file_line) - 1 and file_line[i] != '':
                sentence += file_line[i] + ' '
            elif i == len(file_line) - 1 and file_line[i] != '':
                sentence += file_line[i]
            elif file_line[i] == '':
                print("Empty line existed, cannot process.")
                quit()
        fp.close()
    # read the input file line by line,
    # for each line, store the first number as a key in the constraint set and the remaining numbers in a list as the value
    # initialise the colour set which for each line store the first number as a key and set its value to None
    if regex.fullmatch(sentence) is not None:
        with open(input_file, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                if line != "\n":
                    line = line.split()
                    constraint_set[line[0]] = []
                    colour_set[line[0]] = None
                    for i in range(1, len(line)):
                            constraint_set[line[0]].append(line[i])
            fp.close()

        # Rank the nodes according to the number of neighbours in descending order
        constraint_set = dict(sorted(constraint_set.items(), key=lambda item: len(item[1]), reverse=True))

        # For each node, loop through the alphabet list which finds the first alphabet that does not match with any colour
        # the taken_colour list, and set the alphabet to the value of the node in colour set
        for node in constraint_set:
            taken_colour = []
            for item in constraint_set[node]:
                if colour_set[item] is not None:
                    taken_colour.append(colour_set[item])
            for i in alphabet:
                match = False
                for j in taken_colour:
                    if i == j:
                        match = True
                if not match:
                    colour_set[node] = i
                    break
            # error = True if none of the 26 colours can be used for this specific node
            if colour_set[node] is None:
                error = True
                break
        # if there is no error, which we can assign a colour to each node using the existing 26 colours,
        # create the output file which writes the key value pair in colour set line by line
        if not error:
            with open(output_file, 'w') as fp:
                for i in range(len(colour_set)):
                    node = list(colour_set.keys())[i]
                    if i == len(colour_set) - 1:
                        line = node + colour_set[node]
                    else:
                        line = node + colour_set[node]+'\n'
                    fp.write(line)
                fp.close()
        # output a message and quit the program if we cannot use a colour to each node using the existing 26 colours
        else:
            print("Cannot produce a result with 26 colours or less.")
            quit()
    # output a message and quit the program if the format of the input file is invalid
    else:
        print("Input file has invalid format.")
        quit()
