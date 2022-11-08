################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def analyze_log(ip_port_dict, ip_dict, line):
    """This function is used to analyze logs that were deemed interesting by earlier functions, such as count_requests.\n
    It modifies the given dictionaries to count how many times certain values appear.

    Args:
        ip_port_dict (dict): An empty dictionary, which will get the following structure:\n
        - key: "<ip> <port>"
        - value: amount of times the ip-port combination appears
        ip_dict (dict): An empty dictionary, which will get the following structure:\n
        - key: "<ip>"
        - value: a dictionary, which will get the following structure: {"total" : amount, "<port>" : amount, ... }
        line (str): The line of the log which should be read out
    """
    line    = line.split(" ")
    ip      = line[3]
    port    = line[4]
    ip_port = f"{ip} {port}"

    # add as "ip port" : amount
    if ip_port in ip_port_dict:
        ip_port_dict[ip_port] += 1
    else:
        ip_port_dict[ip_port] = 1

    # add as "ip" : {"port" : amount}
    if ip in ip_dict:
        if port in ip_dict[ip]:
            ip_dict[ip][port] += 1
        else:
            ip_dict[ip][port] = 1
        ip_dict[ip]["total"] += 1
    else:
        ip_dict[ip] = {"total" : 1, port : 1}


def create_analysis_report(ip_port_top, report_name):
    """This function creates a report based on the dictionary created with analyze_log()

    Args:
        ip_port_top (dict): A dictionary containing the ip-port combinations with the largest occurence, created in analyze_log()
        report_name (str): The name of the output file
    """
    with open(report_name, "w") as file:
        for ip_port in ip_port_top:
            file.write(f"{ip_port} {ip_port_top[ip_port]}\n")
