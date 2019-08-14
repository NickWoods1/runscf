
**********************
# `runscf`
**********************

## How to Install
python setup.py install

## Commands
`runscf --help`

`runscf --version`

`runscf initilise` takes a test suite of input geometries (.cell), and generates a 
directory structure that sets up the calculations for other
commands. This includes specifing the parameters, the `castep` binary, etc.

`runscf submit` deals with generating the slurm submission scripts, and submitting
the jobs. 

`runscf parse` parses the output of the calculations for SCF convergence data, and
collates the data in various directories. 

`runscf plot` deals with plotting the SCF convergence data.

## Description

`runscf` is a python package that takes as input a set of `castep` input files, and executes
a specified `castep` binary across these input files, either on a local machine, 
or via slurm. `runscf` then has the capability to scrape the output files for SCF
convergence data.
