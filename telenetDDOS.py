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
from helpers import count_logs, log_count_outliers, time_operations, create_sample, file_iteration, analyze_report

######################
### INITIALIZATION ###
######################

def initiate_name(folder, sample_rand_number, mode_use_sample):
    name = folder + "\\"
    if mode_use_sample:
        name += f"sample{sample_rand_number}_"
    return name
    

#################
### VARIABLES ###
#################

# Modes
mode_testing                = False
mode_create_sample          = False
mode_use_sample             = False
mode_count_requests         = False
mode_request_count_outliers = False
mode_analyze_report         = True

# How many seconds are in each interval
request_interval_size_seconds   = 3

# Files and folders
current_directory       = os.getcwd()

## Log file
log_file_name           = "2019-10-17.accept.txt"  # 437 461 lines
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
reports_folder_name             = "reports"
reports_folder_path             = current_directory + "\\" + reports_folder_name

report_file_name                = initiate_name(reports_folder_name, sample_rand_number, mode_use_sample)

if mode_count_requests:
    report_file_name            += f"requests_count_{request_interval_size_seconds}_sec_intervals.txt"
elif mode_request_count_outliers:
    report_to_analyze_file_name = report_file_name + f"requests_count_{request_interval_size_seconds}_sec_intervals.txt"
    report_file_name            += f"outlier_logs_by_count_{request_interval_size_seconds}.txt"
elif mode_analyze_report:
    report_to_analyze_file_name = report_file_name + f"outlier_logs_by_count_{request_interval_size_seconds}.txt"
else:
    report_file_name            += "REPORT_ERROR.txt"

## Find outliers in the request count
analysis_request_count_file_name        = initiate_name(reports_folder_name, sample_rand_number, mode_use_sample) \
                                        + f"analysis_outlier_logs_{request_interval_size_seconds}.txt"



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
    # Initial message
    print(description)

    # Mode: Create a representative sample from the larger logset
    if mode_create_sample:
        print(f"Selecting 1 in every {sample_size}th line at random to create a sample...")
        file_iteration.iterate_over_file(
            log_file_name,
            create_sample.create_sample,
            sample_file_name,
            sample_size
            )

        execution_output = f"File {sample_file_name} created"

    # Mode: count the amount of requests in a certain timeframe
    elif mode_count_requests:
        # Create a dictionary with all time intervals
        time_intervals = time_operations.create_time_intervals_dict(request_interval_size_seconds)
        print("Time intervals created for counting the amount of requests")
        
        # Create a dictionary which will hold the amount of requests in all time intervals
        requests_count = count_logs.create_requests_count_dict(time_intervals)
        print("Empty request count dictionary created")
        
        # Fill the request count dictionary by iterating over the file
        file_iteration.iterate_over_file(
            log_file_name,
            count_logs.count_requests,
            requests_count,
            time_intervals
        )
        print(f"File {log_file_name} read, requests counted")

        # Create a report which shows the intervals and the amount of requests in them
        count_logs.create_requests_count_report(requests_count, report_file_name)

        execution_output = f"Report file {report_file_name} created successfully"

    # Mode: find outliers in the request count report
    elif mode_request_count_outliers:
        # Make a list with all the amounts of requests generated in the mode_count_requests.
        count_request_report_numbers = []
        file_iteration.iterate_over_file(
            report_to_analyze_file_name,
            log_count_outliers.gather_results,
            count_request_report_numbers
        )
        print("Created a list with all the amount of logs during the selected intervals")
        
        # Calculate the mean, median, mode, min, max, max (top_size), ... of the list
        top_size = 10
        count_request_statistical_numbers = log_count_outliers.get_statistically_relevant_numbers(count_request_report_numbers, top_size)

        # Find the intervals which have among the top (top_size) amounts of requests
        intervals_in_top = []
        file_iteration.iterate_over_file(
            report_to_analyze_file_name,
            log_count_outliers.get_intervals_within_top_5_requests,
            intervals_in_top,
            count_request_statistical_numbers["top"]
        )
        print("Found the intervals whith the largest amount of logs")

        # Create a new report file containing the logs that fall within the previously selected intervals
        file_iteration.iterate_over_file(
            log_file_name,
            log_count_outliers.create_analysis,
            report_file_name,
            intervals_in_top
        )
        execution_output = f"Logs analyzed, report created at {report_file_name}"

    # Mode: analyze the report with the outliers and create a new report based on the biggest outliers
    elif mode_analyze_report:
        # Analyze the log report made in mode_request_count_outliers and count how many times each IP and port appear
        outlier_source_ip_port_count    = {}
        outlier_source_ip_count         = {}
        file_iteration.iterate_over_file(
            report_to_analyze_file_name,
            analyze_report.analyze_log,
            outlier_source_ip_port_count,
            outlier_source_ip_count
        )
        print("Gathered IP and port combinations which appear most frequently")
        
        # Find the top x (see top_size) IP-port combinations
        top_size = -1
        outlier_source_ip_port_count_top  = dict(sorted(outlier_source_ip_port_count.items(), key=lambda x : x[1], reverse=True)[:top_size])
        outlier_source_ip_count_top       = dict(sorted(outlier_source_ip_count.items(), key=lambda x : x[1]['total'], reverse=True)[:top_size])

        # Create a report with the top IP-port combinations
        analyze_report.create_analysis_report(outlier_source_ip_port_count_top, analysis_request_count_file_name)

        execution_output = f"Biggest outliers analyzed, report created at {analysis_request_count_file_name}"

    # Descriptive text
    print(execution_output)
    print(">>> Script complete")

###############
### TESTING ###
###############
else:
    
    print("Test complete")
