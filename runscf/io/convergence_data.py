"""
Module dedicated to parsing and writing convergence data
to .conv files
"""

import io


"""
Finds the seedname.conv_residual and moves it to the appropriate directory
"""
def generate_residual_conv():

    #read list of seednames
    #move conv_res from systems to conv_data/seedname/...

"""
Goes in to each .castep, finds the scf vs. energy convergence block,
writes scf # vs |energy| in a seedname.conv_energy file,
moves this to appropriate directory
"""
def generate_energy_conv():

    #read seednames list
    #move to dir, open seedname.castep
    #search for 1st SCF line
    #search for final scf line (in each case, fail, fail due to hpc, success)
    #write all lines in between to a file (modding energy)
    #move to conv_data/seedname/...


    #given a .cell and .param in a directory
    #extract scf vs |energy| to seedname.conv_energy



