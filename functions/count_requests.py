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

def create_requests_count_dict(time_intervals):
    """This function creates a dictionary to be used by count_requests()

    Args:
        time_intervals (dict): A dictionary created by time_operations.create_time_intervals_dict()

    Returns:
        dict: A dictionary which maps time intervals to the integer 0
    """
    requests_count = {}
    for key in time_intervals:
        requests_count[key] = 0
    return requests_count


def count_requests(requests_count, time_intervals, line):
    """This function adds a count to a time interval belonging to the requests_count dictionary if the time in the line fits in that interval.

    Args:
        requests_count (dict): A dictionary created with the create_requests_count_dict() function
        time_intervals (_type_): A dictionary created with the time_operations.create_time_intervals_dict() function
        line (str): a line belonging to a log file, containing the time when the log was read out
    """
    # Variables
    line                = line.split(" ")
    current_time        = time_string_to_seconds(line[1])

    # Operation
    interval = find_interval(time_intervals, current_time)
    requests_count[interval] += 1



def create_requests_count_report(requests_count, report_name):
    """This function generates a report file based on the dictionary created with count_requests()

    Args:
        requests_count (dict): a dictionary created with the count_requests() function
        report_name (str): the name (and relative location) of the report file
    """
    with open(report_name, "w") as file:
        for key in requests_count:
            file.write(f"{key} {requests_count[key]}\n")
    
