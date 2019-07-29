import os
import shutil
import subprocess

class slurm_setup(object):

    def __init__(self,seedname,method_str,**kwargs):

        self.numnodes = kwargs.pop('',3)
        self.numcores = kwargs.pop('',96)
        self.time_allocated = kwargs.pop('','06:00:00')
        self.seedname = str('"{0}"'.format(seedname))
        self.castep_ver = '"/home/nw361/CASTEP/CASTEP-18.1-{0}/obj/linux_x86_64_ifort17/castep.mpi"'.format(method_str)

"""
Generates slurm submission scripts and places them
in the relevant directories
"""
def generate_submission_scripts(method_str,head_directory,cwd):

    # List of system names
    test_suite_seednames = os.listdir('/{0}/{1}/systems/'.format(cwd,head_directory))

    # Cycle through inputs
    # Copy slurm.submit file to each and modify it
    for seedname in test_suite_seednames:
        shutil.copyfile('{0}/slurm.submit'.format(cwd),'{0}/{1}/systems/{2}/slurm.submit'.format(cwd,head_directory,seedname))


    for seedname in test_suite_seednames:

        # Open the slurm.submit file in each dir, and a tmp to write to
        seedname_submit = open('/{0}/{1}/systems/{2}/slurm.submit'.format(cwd,head_directory,seedname),'r')
        seedname_submit_tmp = open('/{0}/{1}/systems/{2}/slurm.submit_tmp'.format(cwd,head_directory,seedname),'w')

        # Generate slurm script object for each seedname, and dictionary its tags/values
        # for writing to ..._tmp
        slurm_script = slurm_setup(seedname,method_str)

        slurm_tags = {'#SBATCH --nodes=': slurm_script.numnodes,
                      '#SBATCH --ntasks=': slurm_script.numcores,
                      '#SBATCH --time=': slurm_script.time_allocated,
                      '#SBATCH -J': slurm_script.seedname,
                      'application=': slurm_script.castep_ver,
                      'options=': slurm_script.seedname}

        # Cycle through lines in the slurm.submit file
        for line in seedname_submit:

            # Initially, the line has not been rewritten verbatim to ..._tmp or overridden and written to ..._tmp
            rewrote_old_line = False
            line_overridden = False

            # If the line has is an attribute of the slurm.script object
            # replace it with the specified value
            for tag in slurm_tags:
                if tag in line:
                        seedname_submit_tmp.writelines('{0}{1}\n'.format(tag,slurm_tags[tag]))
                        line_overridden = True

            # If not, leave the line as is
            for tag in slurm_tags:
                if line_overridden == False and rewrote_old_line == False and tag not in line:
                    seedname_submit_tmp.writelines(line)
                    rewrote_old_line = True

        # Replace the old slurm.submit with slurm.submit_tmp
        shutil.move('/{0}/{1}/systems/{2}/slurm.submit_tmp'.format(cwd,head_directory,seedname),
                    '/{0}/{1}/systems/{2}/slurm.submit'.format(cwd,head_directory,seedname))

    return test_suite_seednames

def submit_jobs(test_suite_seednames,head_directory,cwd):

    for seedname in test_suite_seednames:
        subprocess.call('sbatch slurm.submit',
                        cwd='{0}/{1}/systems/{2}/'.format(cwd,head_directory,seedname),shell=True)
