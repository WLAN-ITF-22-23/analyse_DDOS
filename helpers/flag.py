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

def create_flag(file_name):
    counter = 0
    flag = "flag{"
    with open(file_name, 'r') as file:
        while counter < 5:
            line = file.readline().rstrip().split(" ")
            flag += line[0] + ":" + line[1] + ","
            counter += 1
    
    flag = flag[:-1] + "}"
    return flag


def write_flag_doc(file_name, flag):
    with open(file_name, 'w') as file:
        file.write(flag)

