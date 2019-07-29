"""
Module containing functions whose primary purpose is to
write the runscf output file
"""

import os
import shutil as shutil
import re

"""
Write the generic initial data in the output file

Returns output file
"""
def init_runscf_io(cwd,head_directory,method_str):

    runscf_out = open('{0}/{1}/runscf.out'.format(cwd,head_directory), 'w')

    runscf_out.writelines('========================================================\n')
    runscf_out.writelines('======             runscf output file             ======\n')
    runscf_out.writelines('========================================================\n')
    runscf_out.writelines('\n')

    runscf_out.writelines('The method used for this instance is: {0}\n'.format(method_str))
    runscf_out.writelines('Data is stored in: {0}/{1}\n'.format(cwd,head_directory))
    runscf_out.writelines('\n')

    return runscf_out


"""
Writes parameters of the calculations in the header of runscf.out
"""
def write_calc_params(cwd, head_directory, runscf_out):

    # List of system names
    test_suite_seednames = os.listdir('/{0}/{1}/systems/'.format(cwd,head_directory))

    # Open the first parameter file that we can find
    param_file =  open('/{0}/{1}/systems/{2}/{2}.param'.format(cwd,head_directory,test_suite_seednames[1]),'r')

    runscf_out.writelines('\n')
    runscf_out.writelines('======    Parameters used in the calculations     ======\n')
    runscf_out.writelines('\n')

    # Loop that writes the relevant parameters from the .param file
    # into runscf.out
    start_printing_to_output_file = False
    for line in param_file:
        if start_printing_to_output_file:
            runscf_out.writelines(line)

        if 'SCF Params' in line:
            start_printing_to_output_file = True

    runscf_out.writelines('\n')
    runscf_out.writelines('========================================================\n')
    runscf_out.writelines('\n')


""""
Function that writes the SCF cycles taken to converge for each
system in the test suite
"""
def write_scf_to_conv(cwd, head_directory, runscf_out):

    # List of system names
    test_suite_seednames = os.listdir('/{0}/{1}/systems/'.format(cwd,head_directory))


    # Dictionaries of whereby the key are the input seednames
    # the values will be convergence data e.g. SCF to convergence, wall clock time, success/fail, ...
    seedname_conv_status = {}
    seedname_iteration_to_conv = {}
    seedname_wall_clock_to_conv = {}


    # Give warning message if nextra_bands required in some inputs
    for seedname in test_suite_seednames:

        seedname_castep_out = open('/{0}/{1}/systems/{2}/{2}.castep'.format(cwd,head_directory,seedname),'r')

        # If nextra_bands exists in the output file, print a warning
        for line in seedname_castep_out:
            if 'nextra_bands' in line:
                print('Warning: {0} requires nextra_bands'.format(seedname))

    # Populate convergence status dictionary (Did the calculation succeed or not?)
    for seedname in test_suite_seednames:

        # Opens the output castep file of the system we're looking at
        seedname_castep_out = open('/{0}/{1}/systems/{2}/{2}.castep'.format(cwd,head_directory,seedname),'r')

        # Loops over all lines in the file to check whether the singlepoint calculation
        # failed or succeeded, and appends the result to a dictionary
        for line in seedname_castep_out:
            if 'Final energy, E' in line:
                seedname_conv_status[seedname] = 'Success'
                break
            elif 'Current total energy, E' in line:
                seedname_conv_status[seedname] = 'Fail due to SCF limit'
                break
            else:
                seedname_conv_status[seedname] = 'Fail due to timeout'

        seedname_castep_out.close()

    # Populate iterations to converge dictionary (How many iterations did seedname take to converge?)
    for seedname in test_suite_seednames:

        seedname_castep_out = open('/{0}/{1}/systems/{2}/{2}.castep'.format(cwd,head_directory,seedname),'r')

        # Start at -4 because 4 redundant lines in .castep containing <-- SCF
        iteration_counter = -4
        for line in seedname_castep_out:
            if seedname_conv_status[seedname] == 'Success':
                if '<-- SCF' in line:
                   iteration_counter = iteration_counter + 1
            else:
                iteration_counter = 1000

        seedname_iteration_to_conv[seedname] = str(iteration_counter)

        seedname_castep_out.close()

    # Populate wall clock time to converge dictionary (How much wall clock time did seedname take to converge?)
    for seedname in test_suite_seednames:

        seedname_castep_out = open('/{0}/{1}/systems/{2}/{2}.castep'.format(cwd, head_directory, seedname), 'r')

        # Record wallclock time
        for line in seedname_castep_out:
            if seedname_conv_status[seedname] == 'Success':
                if 'Total time' in line:
                    seedname_wall_clock_to_conv[seedname] = re.sub("\D","",str(line))[:-2]
            else:
                # Replace with whatever was used as default max time
                seedname_wall_clock_to_conv[seedname] = str(14400)

        seedname_castep_out.close()

    runscf_out.writelines('\n')
    runscf_out.writelines('======             Convergence data               ======\n')
    runscf_out.writelines('\n')

    # Output to runscf.out
    for seedname in test_suite_seednames:
        runscf_out.writelines('Input:                        ' + seedname + '\n')
        runscf_out.writelines('Convergence Status:           ' + seedname_conv_status[seedname] + '\n')
        runscf_out.writelines('Iterations to Convergence:    ' + seedname_iteration_to_conv[seedname] + '\n')
        runscf_out.writelines('Wall Clock to Convergence:    ' + seedname_wall_clock_to_conv[seedname] + '\n')
        runscf_out.writelines('\n')


    runscf_out.writelines('========================================================\n')
    runscf_out.writelines('\n')


    # Compute the total efficiency and robustness

    number_converged = 0
    for seedname in test_suite_seednames:
        if seedname_conv_status[seedname] == 'Success':
            number_converged = number_converged + 1

    robustness = number_converged / len(seedname_conv_status)


    # Wall clock efficiency
    total_time = 0
    for seedname in test_suite_seednames:
        if seedname_conv_status[seedname] == 'Success':
            total_time = total_time + int(seedname_wall_clock_to_conv[seedname])

    eff_wall_clock = number_converged / total_time

    # Iteration efficiency
    total_iterations = 0
    for seedname in test_suite_seednames:
        if seedname_conv_status[seedname] == 'Success':
            total_iterations = total_iterations + int(seedname_iteration_to_conv[seedname])

    eff_iterations = number_converged / total_iterations

    runscf_out.writelines('\n')
    runscf_out.writelines('========            Final Scores            =======')
    runscf_out.writelines('\n')
    runscf_out.writelines('\n')
    runscf_out.writelines('Efficiency (wall clock):      {0} \n'.format(eff_wall_clock))
    runscf_out.writelines('Efficiency (iterations):      {0} \n'.format(eff_iterations))
    runscf_out.writelines('Robustness:                   {0} \n'.format(robustness))
    runscf_out.writelines('\n')
    runscf_out.writelines('===================================================')

# Generates the iteration vs residual data files
def generate_residual_conv(cwd,head_directory):

    # List of system names
    test_suite_seednames = os.listdir('/{0}/{1}/systems/'.format(cwd,head_directory))

    # Copy residual_conv files
    for seedname in test_suite_seednames:
        shutil.copyfile('/{0}/{1}/systems/{2}/{2}.conv_residual'.format(cwd,head_directory,seedname),
                        '{0}/{1}/convergence_data/{2}.conv_residual'.format(cwd,head_directory,seedname))



