################
### METADATA ###
################
# Author: Lander Wuyts

###############
### IMPORTS ###
###############

from random import randint

######################
### INITIALIZATION ###
######################

#################
### FUNCTIONS ###
#################

def create_sample(file_name, one_in_number, line):
    """This function is meant to create a sample of a huge file.
    Every line that is entered will be assigned a random number between 1 and one_in_number.
    If the random number is 1, the line will be added to the sample file.

    Args:
        file_name (str): The name of the sample file
        one_in_number (int): Sets the size of the sample. For example, "100" means that 1/100th of the file will be used to create a sample
        line (str): The line of the file that is being read
    Output:
        All lines that are randomly selected, are added to file_name.
    """
    with open(file_name, "a") as file:
        randnumber = randint(1,one_in_number)
        if randnumber == 1:
            file.write(f"{line}\n")

    