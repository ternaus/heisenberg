#!/usr/bin/env python
from __future__ import division

import time
import pyalps
import matplotlib.pyplot as plt
import pyalps.plot

#prepare the input parameters
import sys
import os
# from src import DilutedLattice
sys.path += [os.path.join(os.getcwd(), '..', '..')]
sys.path += [os.path.join(os.getcwd(), '..')]

import DilutedLattice
import data2xml

parms = []


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-nx', type=int, help="number of sites in x direction")
parser.add_argument('-ny', type=int, help="number of sites in y direction")
parser.add_argument('-dilution', type=float, help="dilution. f = 0 => 2D, f = 1 => PAM")
parser.add_argument('-beta', type=float, help="inverse temperature")
parser.add_argument('-J', type=float, default = 1, help="coupling strength")
parser.add_argument('-J1', type=float, default = 1, help="coupling in the z direction")

args = parser.parse_args(sys.argv[1:])

Nx = args.nx
Ny = args.ny
dilution = args.dilution
J = args.J
J1 = args.J1
beta = args.beta

timestamp = str(time.time()).replace(".", "")

#Save lattice to file
ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)

lattice_name = 'lattice_Nx_{Nx}_Ny_{Ny}_dilution_{dilution}_{timestamp}'.format(Nx=Nx, Ny=Ny, dilution=dilution, timestamp=timestamp)
f = open(lattice_name + ".xml", 'w')
print >> f, ds
f.close()

parms.append(
    {
      'LATTICE'        : "diluted {Nx} x {Ny}, dilution = {dilution}".format(Nx=Nx, Ny=Ny, dilution=dilution),
      'LATTICE_LIBRARY' : lattice_name + ".xml",      
      'MODEL_LIBRARY' : os.path.join(os.getcwd(), "..", "..", "heisenberg.xml"),      
      'MODEL'          : "heisenberg",
      'local_S'        : 0.5,
      'T'              : 1 / beta,
      'J'              : J,
      'J1'             : J1,
      'THERMALIZATION' : 5000,
      'SWEEPS'         : 50000,
      # 'L'              : 60,
      'ALGORITHM'      : "loop"
    }
)

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

input_file = pyalps.writeInputFiles(os.path.join(os.getcwd(), temp, timestamp, lattice_name), parms)
# input_file = pyalps.writeInputFiles(lattice_name, parms)

pyalps.runApplication('loop', input_file, writexml=True)

#load the susceptibility and collect it as function of temperature T
data = pyalps.loadMeasurements(pyalps.getResultFiles(prefix=lattice_name))

print "data = ", data
d_xml = data2xml.DataToXML(data=data)
results = 'results'

try:
  os.mkdir(results)
except:
  pass

file_name = os.path.join(results, lattice_name + "_beta_{beta}_Nx_{Nx}_Ny_{Ny}_J_{J}_J1_{J1}.xml".format(beta=beta, Nx=Nx, Ny=Ny, J=J, J1=J1))
d_xml.tofile(file_name)

