from __future__ import division
import argparse

__author__ = 'vladimir'

'''
This script takes as an input
nx - number of sites in x direction
ny - number of sites in y direction
J - interaction strength
Ti - initial temperature
Tf - final temperature
Ts - step in temperature
f - dilution.
  f = 0 corresponds to square lattice
  f = 1 corresponds to PAM


  As an output xml files with all possible measurements
'''

import pyalps
import sys
import os

parser = argparse.ArgumentParser()

parser.add_argument('-J', default = -1, type=float, help="coupling constant")
parser.add_argument('-Ti', type=float, help="initial temperature")
parser.add_argument('-Tf', type=float, help="final temperature")
parser.add_argument('-Ts', type=float, help="step in temperature")
parser.add_argument('-f', default = 0, type=float, help="dilution")
parser.add_argument('-nx', type=int, help="sites in x direction")
parser.add_argument('-ny', type=int, help="sites in y direction")
parser.add_argument('-variable', type=str, help='type of the variable to plot')
args = parser.parse_args(sys.argv[1:])

J = args.J
nx = args.nx
ny = args.ny
f = args.f

#prepare the input parameters
parms = [{
          'LATTICE'                   : "square lattice",
          'MODEL'                     : "spin",
          'local_S'                   : 1/2,
          'J'                         : J,
          'L'                         : nx,
          'W'                         : ny,
          'CONSERVED_QUANTUMNUMBERS'  : 'Sz',
          'MEASURE_STRUCTURE_FACTOR[Structure Factor S]'        : 'Sz',
          'MEASURE_CORRELATIONS[Diagonal spin correlations]='   : 'Sz',
          'MEASURE_CORRELATIONS[Offdiagonal spin correlations]' : 'Splus:Sminus',
          'MEASURE_CORRELATIONS[SzSz]' : 'Sz:Sz',
          'TRANSLATION_SYMMETRY' : True,
          'MEASURE_ENERGY' : True,
        }]

#write the input file and run the simulation
input_file = pyalps.writeInputFiles('parm1a',parms)
res = pyalps.runApplication('fulldiag',input_file)

#load all measurements for all states
# data = pyalps.loadEigenstateMeasurements(pyalps.getResultFiles(prefix='parm1a'))
result_name = 'nx{nx}_ny{ny}_J{J}_f{f}'.format(nx=nx, ny=ny, J=J, f=f)
data = pyalps.evaluateFulldiagVersusT(pyalps.getResultFiles(prefix='parm1a'),DELTA_T=0.1, T_MIN=0.1, T_MAX=10.0)

print data

