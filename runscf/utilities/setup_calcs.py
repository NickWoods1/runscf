import os
import shutil
from runscf.utilities.method import algorithm

"""
Functions whose utility is to set up directory structures, param files, etc.
Primarily called in the 'initilise' task
"""

"""
Allows the user to safely define a method (returned as a string)
"""
def user_define_method():

    # Read in the list of allowed methods defined by methods.csv
    allowed_methods_file = open('methods.csv', 'r')
    allowed_methods_list = allowed_methods_file.readlines()
    allowed_methods_list = [x.strip() for x in allowed_methods_list]

    # User inputs the name of the method they are using
    # If this method is not allowed, the user is forced to enter a new method
    while True:
        try:
            method_str = input('Enter name of method: ')
            if method_str not in allowed_methods_list:
                raise ValueError
        except ValueError:
            print("The method selected is not an allowed method, please re-enter a valid method.")
            continue
        else:
            break

    return method_str

"""
Allows user to safely define the head directory for the set of computations
that runscf will execute
"""
def user_define_head_dir(task):

    # User defines the location of the script output, and which method is being used.
    head_directory = input('Enter name of head directory: ')

    # Perform check for whether the user-specified directory already exists
    # If it does, give the user the option to replace the old directory
    if task == 'initilise':
        if os.path.isdir(head_directory) == True:
            while True:
                try:
                    # Directory exists, user gets option to replace or exit script
                    replace_dir = input("The directory {0} already exists, replace? (y/n) ".format(head_directory))
                    if replace_dir != "y" and replace_dir != "n":
                        raise ValueError
                except ValueError:
                    print("Invalid response, respond with y/n.")
                    continue
                else:
                    break

            if replace_dir == "y":
                # User wants to replace the directory
                shutil.rmtree(head_directory)
                os.mkdir(head_directory)
            else:
                # User doesn't want to replace the directory, exit
                print("Directory not replaced, exiting.")
                exit()

        else:
            # If it doesn't exist, make it and continue
            os.mkdir(head_directory)

    return head_directory

"""
Creates the directory structure. 
"""
def generate_directories(head_directory):

    # Check the test suite directory is present
    if os.path.isdir("test_suite") == False:
        print("Error: test_suite directory not present. Exiting.")
        exit()

    # Generate the subdirectory tree
    os.mkdir('{0}/convergence_data'.format(head_directory))
    os.mkdir('{0}/convergence_data/systems'.format(head_directory))
    os.mknod('{0}/runscf.out'.format(head_directory))


"""
Allows user to choose the the parameters that the method will have for the benchmark.
Initilises the method as an instance of the algorithm class.

Returns the method as an object with its associated parameters
"""
def specify_parameters(method_str):

    print()
    print('You have chosen the method: {0}.'.format(method_str))
    print('Please specify the parameters for this method that will be used in the benchmark')
    print('Enter "done" when you are finished setting parameters')


    # Create an instance of the algorithm class with default parameters
    method_object = algorithm(method_str)

    # Dictionary of possible modifiable parameters (attributes of the algorithm class)
    all_method_params = method_object.__dict__

    # Empty (so far) dictionary of user-specified method parameters
    # appended and passed as kwargs to the method class.
    method_params = {}

    # Let the user specify parameters, and type 'done' when finished.
    done=False
    while done==False:
        while True:
            try:
                print()
                param_name = str(input('Enter parameter name: '))

                if param_name == "done":
                    done=True
                    print()
                    print('Finished setting parameters.')
                    break

                if param_name not in all_method_params:
                    raise ValueError

            except ValueError:
                print('Not a valid parameter, please re-enter a valid parameter.')
                continue

            else:
                param_value = float(input('Enter value of parameter: '))
                method_params[param_name] = param_value
                break

    # Output from the above is the set of parameters that the user specified.
    # Now create an instance of the algorithm class with these parameters (any left undefined by the
    # user will take the default value
    method_object = algorithm(method_str,**method_params)

    return method_object

"""
Modifies the param files across the test suite to replace the parameters
specified by the user, and if no parameter is specified, the defaults 
determined in the algorithm class (method.py). 
"""
def update_param_files(cwd,head_directory,method_object):

#    print("Warning mix history is 10")

    test_suite_seednames = os.listdir('/{0}/{1}/systems/'.format(cwd,head_directory))

    # Make a dictionary out of the method specified and associated attributes (parameter values)
    method_params = method_object.__dict__

    # Cycle through all directories in the test suite
    for i in test_suite_seednames:

        # Open the .param in the current directory, and a temporary param used for writing the new .param file
        seedname_param = open('/{0}/{1}/systems/{2}/{2}.param'.format(cwd,head_directory,i),'r')
        seedname_param_tmp = open('/{0}/{1}/systems/{2}/{2}.param_tmp'.format(cwd,head_directory,i),'w')

        # Cycle through lines in the param file
        for line in seedname_param:

            # Initially, the line has not been rewritten verbatim to ..._tmp or overridden and written to ..._tmp
            rewrote_old_param = False
            param_overridden = False

            # If the line in the param file is an attribute of the algorithm class, replace it with the
            # value specified for this computation (default or user specified)
            for param in method_params:
                if param in line:
                    seedname_param_tmp.writelines('{0} {1} \n'.format(param,method_params[param]))
                    param_overridden = True       


            # Hacky Code for replacing strings (need to update this)
            if "scalar_precondition" in line:
                seedname_param_tmp.writelines('kerker_precondition \n')
                param_overridden = True  
           # if "MSB2" in line:
           #     seedname_param_tmp.writelines('MSB1 \n')
           #     param_overridden = True  


            # If the line in the param file is not an attribute of the algorithm class, leave it as is
            for param in method_params:
                if param_overridden==False and rewrote_old_param==False and param not in line:
                    seedname_param_tmp.writelines(line)
                    rewrote_old_param = True

        # Replace the old .param with the _tmp.param
        shutil.move('/{0}/{1}/systems/{2}/{2}.param_tmp'.format(cwd,head_directory,i),'/{0}/{1}/systems/{2}/{2}.param'.format(cwd,head_directory,i))




