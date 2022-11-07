################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

import os

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def iterate_over_file(file_name, func, *arguments):
    with open(file_name, 'r') as file:
        line = True

        while line:
            line        = file.readline().rstrip()
            line_list   = line.split(" ")
            if not line:
                break
            if not line_list[0]:
                break

            # Counter
            print(f'Reading file - progress: {line_list[1]} / 23:59:59')
            os.system("cls")

            # Actions
            action = func(*arguments, line)



def iterate_over_file_test(file_name, counter_max, func, *arguments):
    counter = 1

    with open(file_name, 'r') as file:
        line = True

        while line and counter < counter_max:
            line        = file.readline().rstrip()
            line_list   = line.split(" ")
            if not line:
                break
            if not line_list[0]:
                break

            # Counter
            print(f'Reading file - progress: {line_list[1]} / 23:59:59')
            os.system("cls")

            # Actions
            action = func(*arguments, line)

            counter += 1

