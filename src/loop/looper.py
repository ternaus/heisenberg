#!/usr/bin/env python
from __future__ import division

'''
Main file for sse algorithm for heisenberg model.
'''

import time
import pyalps

#prepare the input parameters
import sys
import os
# from src import DilutedLattice


sys.path += [os.path.join(os.getcwd(), '..', '..')]
sys.path += [os.path.join(os.getcwd(), '..')]
sys.path += [os.path.join(os.getcwd(), '..', 'utils')]
sys.path += [os.path.join(os.getcwd(), '..', '..', 'utils')]



import DilutedLattice
import data2xml

parms = []

try:
  import argparse
except:
  Nx = int(sys.argv[sys.argv.index("-nx") + 1])
  Ny = int(sys.argv[sys.argv.index("-ny") + 1])
  dilution = float(sys.argv[sys.argv.index("-dilution") + 1])
  beta = float(sys.argv[sys.argv.index("-beta") + 1])
  J = float(sys.argv[sys.argv.index("-J") + 1])
  J1 = float(sys.argv[sys.argv.index("-J1") + 1])
else:
  parser = argparse.ArgumentParser()
  parser.add_argument('-nx', type=int, help="number of sites in x direction")
  parser.add_argument('-ny', type=int, help="number of sites in y direction")
  parser.add_argument('-dilution', type=float, help="dilution. f = 0 => 2D, f = 1 => PAM")
  parser.add_argument('-beta', type=float, help="inverse temperature")
  parser.add_argument('-J', type=float, default=1, help="coupling strength")
  parser.add_argument('-J1', type=float, default=1, help="coupling in the z direction")

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


LATTICE_LIBRARY = os.path.join(temp, lattice_name + ".xml")
parms.append(
    {
      'LATTICE'        : "diluted {Nx} x {Ny}, dilution = {dilution}".format(Nx=Nx, Ny=Ny, dilution=dilution),
      'LATTICE_LIBRARY': LATTICE_LIBRARY,
      'MODEL_LIBRARY': os.path.join(os.getcwd(), "..", "heisenberg.xml"),
      'MODEL'          : "heisenberg",
      'local_S'        : 0.5,
      'T'              : 1 / beta,
      'J'              : J,
      'J1'             : J1,
      'THERMALIZATION': 5000,
      'SWEEPS'         : 50000,
      'ALGORITHM'      : "loop",
      # 'MEASURE[Winding Number]': 1,
      # 'MEASURE_CORRELATIONS[Diagonal spin correlations]':"Sz",
    }
)


#write the input file and run the simulation

input_file = pyalps.writeInputFiles(os.path.join(os.getcwd(), temp, timestamp, lattice_name), parms)

pyalps.runApplication('loop', input_file, writexml=True)

data = pyalps.loadMeasurements(pyalps.getResultFiles(prefix=lattice_name))

results = 'results'

try:
  os.mkdir(results)
except:
  pass

file_name = os.path.join(results, lattice_name + "_beta_{beta}_Nx_{Nx}_Ny_{Ny}_J_{J}_J1_{J1}.xml".format(beta=beta,
                                                                                                         Nx=Nx,
                                                                                                         Ny=Ny,
                                                                                                         J=J,
                                                                                                         J1=J1))

d_xml = data2xml.DataToXML(data=data, looper=True, lattice=LATTICE_LIBRARY)

d_xml.tofile(file_name)

