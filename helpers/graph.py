################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

import matplotlib.pyplot as plt

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def get_data(x_data, y_data, log_count_line):
    log_count_line = log_count_line.split(" ")
    x_data.append(log_count_line[0])
    y_data.append(log_count_line[2])


def plot_data(x_data, x_axis_name, y_data, y_axis_name, title):
    plt.plot(x_data, y_data)
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.title(title)

    plt.show()
