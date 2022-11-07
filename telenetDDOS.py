################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############
import os
from random import randint

# Custom functions
from functions import time_operations, create_sample, file_iteration, count_requests

######################
### INITIALIZATION ###
######################

#################
### VARIABLES ###
#################

# Modes
mode_testing            = True
mode_create_sample      = False
mode_use_sample         = True
mode_count_requests     = False
mode_analyze_report     = False

# Files and folders
current_directory       = os.getcwd()

## Log file
log_file_name           = "2019-10-17.accept.txt"  # 437461 lines
log_file_path           = current_directory + "\\" + log_file_name

## Sample file
sample_size = 1000

sample_folder_name      = "samples"
sample_folder_path      = current_directory + "\\" + sample_folder_name


if mode_create_sample:
    sample_rand_number  = "_" + str(randint(10000,99999))
else:
    sample_rand_number  = ""  # Choose which sample file you want to analyze

sample_file_name        = sample_folder_name + "\\" + f"sample_1_in_{sample_size}{sample_rand_number}.txt" 
sample_file_path        = current_directory + "\\" + sample_file_name


if mode_use_sample and os.path.exists(sample_file_name):
    log_file_name       = sample_file_name
    log_file_path       = sample_file_path

## Report file
reports_folder_name     = "reports"
reports_folder_path     = current_directory + "\\" + reports_folder_name

request_interval_size_seconds = 1800

report_file_name = reports_folder_name + "\\"

if mode_use_sample:
    report_file_name        += f"sample{sample_rand_number}_"
if mode_count_requests:
    report_file_name        += f"requests_count_{request_interval_size_seconds}_sec_intervals.txt"
else:
    report_file_name        += "REPORT_ERROR.txt"

# Output
description             = (f"""
Reading file: {log_file_path}
>>> Size: {format(os.stat(log_file_path).st_size / 1000, ".2f")} GB
""")

execution_output        = "ERROR"

# log_line_structure      = ["date", "time", "protocol", "source_IP", "source_port", "destination_IP", "destination_port"]

#################
### OPERATION ###
#################

if not(mode_testing):
    ## Mode: Create a sample
    if mode_create_sample:
        file_iteration.iterate_over_file(
            log_file_name,
            create_sample.create_sample,
            sample_file_name,
            sample_size
            )

        execution_output = f"File {sample_file_name} created"

    elif mode_count_requests:
        request_dict = time_operations.create_time_intervals_dict(request_interval_size_seconds)
        execution_output = "Error, this code isn't written yet"

    elif mode_analyze_report:
        execution_output = "Error: this code isn't written yet"

    # Descriptive text
    print(description)
    print(execution_output)
    print(">>> Script complete")

###############
### TESTING ###
###############
else:
    time_intervals = time_operations.create_time_intervals_dict(request_interval_size_seconds)
    requests_count = count_requests.create_requests_count_dict(time_intervals)
    
    file_iteration.iterate_over_file(
        log_file_name,
        count_requests.count_requests,
        requests_count,
        time_intervals
    )
    

    print("Test complete")
