################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

import os
from .time_operations import seconds_to_time_string, time_string_to_seconds

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def iterate_over_file(file_name, func, *arguments):
    """This function is used to read over a file line by line and execute a given function

    Args:
        file_name (str): The name (and path) of the file that needs to be read
        func (function): The function that has to be executed on every line of the file. 
        A string containing the current line will always be passed as the last argument.
    """
    line        = True
    counter     = 0
    intervals   = create_print_triggers(3600 * 5)
    
    with open(file_name, 'r') as file:
        while line:
            line = file.readline().rstrip()
            if not line:
                break
            # Counter 
            counter = get_iteration_feedback(line, intervals, counter)

            # Actions
            action = func(*arguments, line)



def iterate_over_file_test(file_name, counter_max, func, *arguments):
    """This function is used to read over a file line by line and execute a given function, until a number of lines is reached.

    Args:
        file_name (str): The name (and path) of the file that needs to be read
        counter_max (int): The maximum number of lines that need to be read.
        func (function): The function that has to be executed on every line of the file. 
        A string containing the current line will always be passed as the last argument.
    """
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


            # Actions
            action = func(*arguments, line)

            counter += 1


def create_print_triggers(interval_size):
    """This function creates a list of integers representing seconds, which can be used by get_iteration_feedback()

    Args:
        interval_size (int): The amount of seconds which will be used as the size of the interval

    Returns:
        list: A list with integers, which represent an amount of seconds. Each item is interval_size bigger than the last.
        The final item is 86400, representing 24 hours.
    """
    intervals = []
    time = 0
    while time < 86400:
        intervals.append(time)
        time += interval_size

    intervals.append(86400)

    return sorted(intervals)


def get_iteration_feedback(line, intervals, counter):
    """This function checks if the time in a line has passed a certain treshhold. 
    If so, it prints the time to inform the user of the location in the script.

    Args:
        line (str): A line from a log that is being read
        intervals (list): A list created with create_print_triggers()
        counter (int): A number representing the current position on the list. Must start at 0.

    Returns:
        _type_: _description_
    """
    line = line.split(" ")
    time = time_string_to_seconds(line[1])
    if time > intervals[counter]:
        print(f">>> {line[1]} reached")
        counter += 1
    return counter

