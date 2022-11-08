################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

import statistics
from .time_operations import is_in_interval

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def gather_results(result_list, line):
    """This function adds the number of requests per timeframe in a requests_count log to a list

    Args:
        result_list (list): the list to which the number of requests should be added
        line (str): the line of the requests_count log that is being analyzed
    """
    line = line.split(" ")
    result_list.append(int(line[2]))


def get_statistically_relevant_numbers(result_list, top_size):
    """This function analyses a list of integers and returns the median, mean and mode in a dictionary

    Args:
        result_list (list): a list of integers

    Returns:
        dict: a dictionary containing three elements:\n
        - "median"\t: The value in the middle of the list if it is sorted\n
        - "mean"\t: The sum of all values, divided by the number of values\n
        - "mode"\t: The value that occurs the most
        - "min"\t: The smallest value in the list
        - "max"\t: The largest value in the list
        - "top 5"\t: The 5 largest values in the list
    """
    result_list.sort()
    return {
        "median"    : statistics.median(result_list), 
        "mean"      : statistics.mean(result_list), 
        "mode"      : statistics.mode(result_list),
        "min"       : min(result_list),
        "max"       : max(result_list),
        "top"     : [result_list[(-1*i)] for i in range(1,top_size)]
        }


def get_intervals_within_top_5_requests(intervals, top_5, line):
    """This function checks if the number of requests in an interval is within the top 5 number of requests per interval

    Args:
        intervals (list): A list which will contain all the intervals that have a number of requests within the top 5
        top_5 (list): The 5 highest request counts found with get_statistically_relevant_numbers
        line (str): the line of the requests_count log that is being analyzed
    """
    line = line.split(" ")
    if int(line[2]) in top_5:
        intervals.append(f"{line[0]} {line[1]}")


def create_analysis(file_name, intervals, line):
    """This function creates a log file containing all lines that fall within a given interval

    Args:
        file_name (str): The name of the report file to write to
        intervals (list): A list of intervals created with get_intervals_within_top_5_requests()
        line (str): A line of the log file that is being analyzed
    """
    line_list = line.split(" ")
    with open(file_name, 'a') as file:
        for interval in intervals:
            if is_in_interval(line_list[1], interval):
                file.write(f"{line}\n")
