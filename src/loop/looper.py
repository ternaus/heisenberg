from __future__ import division


import pyalps
import matplotlib.pyplot as plt
import pyalps.plot

#prepare the input parameters
import sys
import os
# from src import DilutedLattice

sys.path += [os.path.join(os.getcwd(), '..')]

import DilutedLattice
import data2xml

parms = []

Nx = 4
Ny = 4
dilution = 1

#Save lattice to file
ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)

lattice_name = 'lattice_Nx_{Nx}_Ny_{Ny}_dilution_{dilution}'.format(Nx=Nx, Ny=Ny, dilution=1)
f = open(lattice_name + ".xml", 'w')
print >> f, ds
f.close()

# beta_list = [2**tx for tx in range(10)]
beta_list = [1]
J = -1
J1 = -1
beta = 1

parms.append(
    {
      'LATTICE'        : "diluted {Nx} x {Ny}, dilution = {dilution}".format(Nx=Nx, Ny=Ny, dilution=dilution),
      'LATTICE_LIBRARY' : lattice_name + ".xml",
      'MODEL_LIBRARY' : os.path.join("..", "heisenberg.xml"),
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


input_file = pyalps.writeInputFiles(os.path.join(temp, lattice_name), parms)
pyalps.runApplication('loop', input_file, writexml=True)

#load the susceptibility and collect it as function of temperature T
data = pyalps.loadMeasurements(pyalps.getResultFiles(prefix=lattice_name))
d_xml = data2xml.DataToXML(data=data)
results = 'results'

try:
  os.mkdir(results)
except:
  pass

file_name = os.path.join(results, lattice_name + "_beta_{beta}_Nx_{Nx}_Ny_{Ny}_J_{J}_J1_{J1}.xml".format(beta=beta, Nx=Nx, Ny=Ny, J=J, J1=J1))
d_xml.tofile(file_name)

