import shutil
import argparse
import os
from runscf.utilities.setup_calcs import generate_directories, specify_parameters, update_param_files,user_define_method,user_define_head_dir
from runscf.utilities.slurm import generate_submission_scripts, submit_jobs
from runscf.io.runscf_output_file import init_runscf_io, write_calc_params, write_scf_to_conv, generate_residual_conv


"""
runscf main function that structures the code
"""
def main():

    # Current version of runscf and test suite
    # Find a way to set this automatically from git...
    __version__=0.1

    # Parser class for runscf
    parser = argparse.ArgumentParser(
        prog='runscf',
        description='runscf executes a specified castep binary on a suite of input systems and scrapes output for convergence data',
        epilog='written by Nick Woods')

    # Specify arguments that runscf can take
    parser.add_argument('--version', action='version', version='This is version {0} of runscf.'.format(__version__))
    parser.add_argument('task', help='what do you want runscf to do: initilise, submit, parse')

    args = parser.parse_args()

    # Execute what the user has specified
    if args.task == 'initilise':
        print('=================================================')
        print('===== Initilising the directories and files =====')
        print('=================================================')
        print()

        # Define the present working directory
        cwd = os.getcwd()

        # User defined what method they are using (e.g. Pulay) stored as a string
        method_str = user_define_method()

        # User defines the head directory for the runscf computations
        head_directory = user_define_head_dir(args.task)

        # Generate the directory/file structure
        generate_directories(head_directory)

        # Copy test suite into the newly generated directory
        shutil.copytree('test_suite', head_directory + '/systems')

        # Specify parameters of the method
        method_object = specify_parameters(method_str)

        # Update the .param files with these parameters
        update_param_files(cwd, head_directory, method_object)

        print()
        print('Finished generating directory and file structure')

    elif args.task == 'submit':
        print('===========================================================')
        print('===== Creating submission scripts and submitting jobs =====')
        print('===========================================================')
        print()

        # Define the present working directory
        cwd = os.getcwd()

        # User defined what method they are using (e.g. Pulay) stored as a string
        method_str = user_define_method()

        # User defines the head directory for the runscf computations
        head_directory = user_define_head_dir(args.task)

        # Generate the slurm submission scripts and place them in each directory
        test_suite_seednames = generate_submission_scripts(method_str,head_directory,cwd)

        # Submit the jobs via slurm
        submit_jobs(test_suite_seednames,head_directory,cwd)

        # End
        print()
        print('Jobs successfully submitted')

    elif args.task == 'parse':
        print('===============================================================')
        print('===== Parsing output for SCF data and writing output file =====')
        print('===============================================================')
        print()

        # Define the present working directory
        cwd = os.getcwd()

        # User defined what method they are using (e.g. Pulay) stored as a string
        method_str = user_define_method()

        # User defines the head directory for the runscf computations
        head_directory = user_define_head_dir(args.task)

        # Begin writing to runscf.out (return the file)
        runscf_out = init_runscf_io(cwd, head_directory,method_str)

        # Write the parameters of the method to runscf.out
        write_calc_params(cwd, head_directory, runscf_out)

        # Writes convergence data to output file, including final robustness and efficiency
        write_scf_to_conv(cwd, head_directory, runscf_out)

        # Moves the iteration vs residual to the correct location
        generate_residual_conv(cwd,head_directory)

    else:
        print('Enter a valid task for runscf')
        print('Exiting...')