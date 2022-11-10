################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

from .time_operations import time_string_to_seconds, find_interval

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def create_logs_count_dict(time_intervals):
    """This function creates a dictionary to be used by count_logs()

    Args:
        time_intervals (dict): A dictionary created by time_operations.create_time_intervals_dict()

    Returns:
        dict: A dictionary which maps time intervals to the integer 0
    """
    logs_count = {}
    for key in time_intervals:
        logs_count[key] = 0
    return logs_count


def count_logs(logs_count, time_intervals, line):
    """This function adds a count to a time interval belonging to the logs_count dictionary if the time in the line fits in that interval.

    Args:
        logs_count (dict): A dictionary created with the create_logs_count_dict() function
        time_intervals (_type_): A dictionary created with the time_operations.create_time_intervals_dict() function
        line (str): a line belonging to a log file, containing the time when the log was read out
    """
    # Variables
    line                = line.split(" ")
    current_time        = time_string_to_seconds(line[1])

    # Operation
    interval = find_interval(time_intervals, current_time)
    if interval in logs_count:
        logs_count[interval] += 1



def create_logs_count_report(logs_count, report_name):
    """This function generates a report file based on the dictionary created with count_logs()

    Args:
        logs_count (dict): a dictionary created with the count_logs() function
        report_name (str): the name (and relative location) of the report file
    """
    with open(report_name, "w") as file:
        for key in logs_count:
            if logs_count[key] != 0:
                file.write(f"{key} {logs_count[key]}\n")
    
