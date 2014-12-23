#!/usr/bin/env python
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

sys.path += [os.path.join(os.getcwd(), '..', '..')]
sys.path += [os.path.join(os.getcwd(), '..')]
sys.path += [os.path.join(os.getcwd(), '..', 'utils')]

import time
import DilutedLattice
import data2xml

parser = argparse.ArgumentParser()

parser.add_argument('-J', default = 1, type=float, help="coupling constant")
parser.add_argument('-J1', default = 0, type=float, help="coupling constant in the perpendicular direction")
parser.add_argument('-Ti', type=float, help="initial temperature")
parser.add_argument('-Tf', type=float, help="final temperature")
parser.add_argument('-Ts', type=float, help="step in temperature")
parser.add_argument('-dilution', default = 0, type=float, help="dilution 0 - square, 1 - PAM")
parser.add_argument('-nx', type=int, help="sites in x direction")
parser.add_argument('-ny', type=int, help="sites in y direction")
parser.add_argument('-variable', type=str, help='type of the variable to plot')
args = parser.parse_args(sys.argv[1:])

J = args.J
J1 = args.J1
Nx = args.nx
Ny = args.ny
dilution = args.dilution

Ti = args.Ti
Ts = args.Ts
Tf = args.Tf
timestamp = str(time.time()).replace(".", "")

#Save lattice to file
ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)


temp = "temp"
try:
  os.mkdir(temp)
except:
  pass

try:
  os.mkdir(os.path.join(temp, timestamp))
except:
  pass


lattice_name = 'lattice_Nx_{Nx}_Ny_{Ny}_dilution_{dilution}_{timestamp}'.format(Nx=Nx, Ny=Ny, dilution=dilution, timestamp=timestamp)
f = open(os.path.join(temp, lattice_name + ".xml"), 'w')
print >> f, ds
f.close()

#prepare the input parameters
parms = [{
          'LATTICE'        : "diluted {Nx} x {Ny}, dilution = {dilution}".format(Nx=Nx, Ny=Ny, dilution=dilution),
          'LATTICE_LIBRARY' : os.path.join(temp, lattice_name + ".xml"),
          'MODEL'          : "heisenberg",
          'MODEL_LIBRARY'                     : os.path.join(os.getcwd(), "..", "heisenberg.xml"),
          'local_S'                   : 1/2,
          'J'                         : J,
          'J1'                        : J1,
          'L'                         : Nx,
          'W'                         : Ny,
          'CONSERVED_QUANTUMNUMBERS'  : 'Sz',
          'MEASURE_STRUCTURE_FACTOR[Structure Factor S]'        : 'Sz',
          'MEASURE_CORRELATIONS[Diagonal spin correlations]='   : 'Sz',
          'MEASURE_CORRELATIONS[Offdiagonal spin correlations]' : 'Splus:Sminus',
          'MEASURE_CORRELATIONS[SzSz]' : 'Sz:Sz',
          # 'TRANSLATION_SYMMETRY' : True,
          'MEASURE_ENERGY' : True,
        }]

#write the input file and run the simulation
temp = "temp"
try:
  os.mkdir(temp)
except:
  pass

try:
  os.mkdir(os.path.join(temp, timestamp))
except:
  pass

input_file = pyalps.writeInputFiles(os.path.join(os.getcwd(), temp, timestamp), parms)

#run the simulation

res = pyalps.runApplication('fulldiag',input_file, writexml=True)

print res
#load all measurements for all states
# data = pyalps.loadEigenstateMeasurements(pyalps.getResultFiles(prefix='parm1a'))
result_name = 'nx{nx}_ny{ny}_J{J}_J1{J1}_f{f}'.format(nx=Nx, ny=Ny, J=J, f=dilution, J1=J1)
data = pyalps.evaluateFulldiagVersusT(pyalps.getResultFiles(prefix=str(timestamp)),DELTA_T=args.Ts, T_MIN=args.Ti, T_MAX=args.Tf)

# print 'data = ', data

d_xml = data2xml.DataToXML(data=data, ed=True)
results = 'results'

try:
  os.mkdir(results)
except:
  pass

file_name = os.path.join(results, lattice_name + "Ti{Ti}_Tf{Tf}_Ts{Ts}_Nx_{Nx}_Ny_{Ny}_J_{J}_J1_{J1}.xml".format(Ti=Ti, Ts=Ts, Tf=Tf, Nx=Nx, Ny=Ny, J=J, J1=J1))
d_xml.tofile(file_name)
