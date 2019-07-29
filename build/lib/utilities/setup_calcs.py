import os

# Sets up the calculation: directory structure, scf method used, and init files.

def setup():

    # User defines the location of the script output, and which method is being used.
    head_directory = input('Enter name of head directory: ')
    method = input('Enter name of method: ')

    # Check for whether that directory already exists
    path = os.getcwd()

    print(path)