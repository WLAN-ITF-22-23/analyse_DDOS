################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############
import math

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def time_string_to_seconds(string):
    """This function converts a string that represents a time of day to the number of seconds that have passed since 00:00:00.
    

    Args:
        string (str): This string must be formatted as "HH:MM:SS".
    > H: hour
    > M: minute
    > S: second

    Returns:
        int: The number of seconds passed from 00:00:00 to the input string
    """
    string_list = list(map(int, string.split(":")))
    seconds = string_list[0] * 60 * 60 + string_list[1] * 60 + string_list[2]

    return seconds


def seconds_to_time_string(int):
    """This function converts a number of seconds into a string representing the time of day.

    Args:
        int (int): the number of seconds that have passed, preferrably less than 86400

    Returns:
        str: A string representing the time of day, formatted as "HH:MM:SS".
    """
    hours = math.trunc(int / 3600)
    seconds = int - hours * 3600
    minutes = math.trunc(seconds / 60)
    seconds -= minutes * 60

    return "{}:{:02d}:{:02d}".format(hours, minutes, seconds)


def time_interval_calculator(current_time_str, time_difference_int):
    """This string calculates the time after a number of seconds will have passed.

    Args:
        current_time_str (str): A string representing the current time, formatted as "HH:MM:SS"
        time_difference_int (int): An integer representing the amount of seconds that will pass after the current_time_str

    Returns:
        str: A string representing the time after current_time_str when time_difference_int seconds have passed.
    """
    current_time_int = time_string_to_seconds(current_time_str)
    new_time_int = current_time_int + time_difference_int
    new_time_str = seconds_to_time_string(new_time_int)

    return new_time_str


def create_time_intervals_dict(interval_size):
    """This function creates a dictionary of different time intervals, 
    which can be searched to check in which interval a given time in seconds (between 0 and 86400) falls.

    Args:
        interval_size (int): the size of the intervals in seconds

    Returns:
        dict: a dictionary with the following structure:
        > key (str): the time interval in human readable format (ex: "00:00:00 00:30:00")\n
        > value (list): a list with the following structure (ex: [0, 1800]):\n
        >> interval_start (int): the start of the interval in seconds\n
        >> interval_end (int): the end of the interval in seconds
    """
    time_difference_start   = 0
    time_max_int            = 86400
    time_intervals_dict     = {}

    while time_difference_start < time_max_int:
        time_difference_end = time_difference_start + interval_size
        time_intervals_dict[f"{seconds_to_time_string(time_difference_start)} {seconds_to_time_string(time_difference_end)}"] = \
            [time_difference_start, time_difference_end]
        
        time_difference_start = time_difference_end + 1
    
    return time_intervals_dict


def find_interval(dict, current_time):
    """This function searches which interval a given time in seconds belongs in.

    Args:
        dict (dict): A dictioniary created with the create_time_intervals_dict() function
        current_time (int): The time in seconds for which you want to know it's interval

    Returns:
        str: a string representing the time interval in human readable format (ex: "00:00:00 00:30:00")
    """
    for key in dict:
        if current_time >= dict[key][0] and current_time <= dict[key][1]:
            return key
        
    return False

