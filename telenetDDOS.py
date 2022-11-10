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
from helpers import count_logs
from helpers import log_count_outliers  as outliers
from helpers import time_operations
from helpers import create_sample       as sample
from helpers import file_iteration      as iterate
from helpers import analyze_report      as analyze
from helpers import graph
from helpers import flag

######################
### INITIALIZATION ###
######################

def initiate_name(folder, sample_rand_number, mode_use_sample, interval_start=0, interval_end=86400, mode_use_specific_time=False):
    name = folder + "\\"
    if mode_use_sample:
        name += f"sample{sample_rand_number}_"
    if mode_use_specific_time:
        name += (time_operations.seconds_to_time_string(interval_start)).replace(":","")
        name += "-"
        name += (time_operations.seconds_to_time_string(interval_end)).replace(":","")
        name += "_"
    return name
    

#################
### VARIABLES ###
#################

# Modes
mode_testing                = False

mode_create_sample          = False
mode_use_sample             = False

mode_count_logs             = False
mode_log_count_outliers     = False
mode_analyze_report         = False
mode_plot_log_count_graph   = False

mode_use_specific_time      = False
mode_filter_specific_time   = False  # Requires mode_use_specific_time to be true

mode_flag                   = True

# Time interval
## How many seconds are in each interval
log_interval_size       = 3

## Custom interval start and end times
custom_interval_start   = time_operations.time_string_to_seconds("21:55:36")
custom_interval_end     = time_operations.time_string_to_seconds("21:55:52")

## Create a dictionary with all time intervals
if mode_use_specific_time:
    time_intervals = time_operations.create_time_intervals_dict(log_interval_size, custom_interval_start, custom_interval_end)
else:
    time_intervals = time_operations.create_time_intervals_dict(log_interval_size)

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
    sample_rand_number  = "_n" + str(randint(10000,99999))
else:
    sample_rand_number  = ""  # Choose which sample file you want to analyze

sample_file_name        = sample_folder_name + "\\" + f"sample_1_in_{sample_size}{sample_rand_number}.txt" 
sample_file_path        = current_directory + "\\" + sample_file_name


if mode_use_sample and os.path.exists(sample_file_name):
    log_file_name       = sample_file_name
    log_file_path       = sample_file_path

## Report files
output_folder_name     = "reports"
output_folder_path     = current_directory + "\\" + output_folder_name

output_name_base            = initiate_name(output_folder_name, sample_rand_number, mode_use_sample, custom_interval_start, custom_interval_end, mode_use_specific_time)
output_file_name            = output_name_base
report_to_analyze_file_name = output_name_base


if mode_count_logs or mode_plot_log_count_graph:
    output_file_name            += f"logs_count_{log_interval_size}_sec_intervals.txt"

elif mode_log_count_outliers:
    output_file_name            += f"outlier_logs_by_count_{log_interval_size}.txt"
    report_to_analyze_file_name += f"logs_count_{log_interval_size}_sec_intervals.txt"

elif mode_analyze_report:
    if mode_use_specific_time:
        output_file_name            += "analysis_filtered_logs.txt"
        report_to_analyze_file_name += "filtered_logs.txt"
    else:
        output_file_name            += f"analysis_outlier_logs_{log_interval_size}.txt"
        report_to_analyze_file_name += f"outlier_logs_by_count_{log_interval_size}.txt"

elif mode_filter_specific_time:
    report_to_analyze_file_name += f"logs_count_{log_interval_size}_sec_intervals.txt"
    output_file_name            += "filtered_logs.txt"

elif mode_flag:
    output_file_name            = "FLAG.txt"
    if mode_use_specific_time:
        report_to_analyze_file_name += "analysis_filtered_logs.txt"
    else:
        report_to_analyze_file_name += f"analysis_outlier_logs_{log_interval_size}.txt"
else:
    output_file_name            += "REPORT_ERROR.txt"

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
        iterate.iterate_over_file(
            log_file_name,
            sample.create_sample,
            sample_file_name,
            sample_size
            )

        execution_output = f"File {sample_file_name} created"

    # Mode: count the amount of logs in a certain timeframe
    elif mode_count_logs:      
        # Create a dictionary which will hold the amount of logs in all time intervals
        log_count = count_logs.create_logs_count_dict(time_intervals)
        print("Empty log count dictionary created")
        
        # Fill the log count dictionary by iterating over the file
        iterate.iterate_over_file(
            log_file_name,
            count_logs.count_logs,
            log_count,
            time_intervals
        )
        print(f"File {log_file_name} read, logs counted")

        # Create a report which shows the intervals and the amount of logs in them
        count_logs.create_logs_count_report(log_count, output_file_name)

        execution_output = f"Report file {output_file_name} created successfully"

    # Mode: find outliers in the log count report
    elif mode_log_count_outliers:
        # Make a list with all the amounts of logs generated in the mode_count_logs.
        count_log_report_numbers = []
        iterate.iterate_over_file(
            report_to_analyze_file_name,
            outliers.gather_results,
            count_log_report_numbers
        )
        print("Created a list with all the amount of logs during the selected intervals")
        
        # Calculate the mean, median, mode, min, max, max (top_size), ... of the list
        top_size = 10
        count_logs_statistical_numbers = outliers.get_statistically_relevant_numbers(count_log_report_numbers, top_size)

        # Find the intervals which have among the top (top_size) amounts of logs
        intervals_in_top = []
        iterate.iterate_over_file(
            report_to_analyze_file_name,
            outliers.get_intervals_within_top_5_logs,
            intervals_in_top,
            count_logs_statistical_numbers["top"]
        )
        print("Found the intervals whith the largest amount of logs")

        # Create a new report file containing the logs that fall within the previously selected intervals
        iterate.iterate_over_file(
            log_file_name,
            outliers.filter_logs,
            output_file_name,
            intervals_in_top
        )
        execution_output = f"Logs analyzed, report created at {output_file_name}"

    # Mode: analyze the report with the outliers and create a new report based on the biggest outliers
    elif mode_analyze_report:
        # Analyze the log report made in mode_log_count_outliers and count how many times each IP and port appear
        outlier_source_ip_port_count    = {}
        outlier_source_ip_count         = {}
        iterate.iterate_over_file(
            report_to_analyze_file_name,
            analyze.analyze_log,
            outlier_source_ip_port_count,
            outlier_source_ip_count
        )
        print("Gathered IP and port combinations which appear most frequently")
        
        # Find the top x (see top_size) IP-port combinations
        top_size = -1
        outlier_source_ip_port_count_top  = dict(sorted(outlier_source_ip_port_count.items(), key=lambda x : x[1], reverse=True)[:top_size])
        outlier_source_ip_count_top       = dict(sorted(outlier_source_ip_count.items(), key=lambda x : x[1]['total'], reverse=True)[:top_size])

        # Create a report with the top IP-port combinations
        analyze.create_analysis_report(outlier_source_ip_port_count_top, output_file_name)

        execution_output = f"Biggest outliers analyzed, report created at {output_file_name}"

    # Mode: plot a graph from the log file to give an overview
    elif mode_plot_log_count_graph:
        x_axis_data = []
        y_axis_data = []

        iterate.iterate_over_file(
            output_file_name,
            graph.get_data,
            x_axis_data,
            y_axis_data
        )

        graph.plot_data(
            x_data      = x_axis_data, 
            x_axis_name = "time", 
            y_data      = y_axis_data, 
            y_axis_name = "amount of requests", 
            title       = f"Requests in {log_interval_size} second intervals"
        )
    
        execution_output = f"Plotting of {output_file_name} done"

    # Mode: create a log file containing only lines from a specific time
    elif mode_filter_specific_time:
        # Create a log containing only the lines from the selected time
        iterate.iterate_over_file(
            log_file_name,
            outliers.filter_logs,
            output_file_name,
            time_intervals            
        )

        execution_output = f"Filtering done, created {output_file_name}"
    
    # Mode: create a flag
    elif mode_flag:
        # Create the flag based on the top 5 ip:port combinations
        flag_content = flag.create_flag(report_to_analyze_file_name)
        # Write the flag to an output file
        flag.write_flag_doc(output_file_name, flag_content)

        execution_output = f"Flag '{flag_content}' written to {output_file_name}"
    # Descriptive text
    print(execution_output)
    print(">>> Script complete")

###############
### TESTING ###
###############
else:
    print(output_file_name)
    print(report_to_analyze_file_name)

    # Interesting time: 21u52- 21u58
    print("Test complete")
