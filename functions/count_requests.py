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


# def logfile_activity_report(dict):
#     # Variables
#     global time_difference_seconds
#     global reports_folder_path

#     # Writing the report
#     report_name     = f"requests_count_{time_difference_seconds}_seconds_intervals.txt"
#     report_path_rel = f"{reports_folder_name}\\{report_name}"
#     report_path_abs = f"{reports_folder_path}\\{report_name}"

#     with open(report_path_rel, "w") as file:
#         file.write("interval_start interval_end amound_of_requests")
#         for interval in dict:
#             file.write(f"\n{dict[interval][0]} {interval} {dict[interval][1]}")

#     return f"File {report_path_rel} created"

    

# def time_interval_calculator(current_time_str, time_difference_int):
#     current_time_int = time_string_to_seconds(current_time_str)
#     new_time_int = current_time_int + time_difference_int
#     new_time_str = seconds_to_time_string(new_time_int)

#     return new_time_str
