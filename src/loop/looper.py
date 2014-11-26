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

parms = []

Nx = 8
Ny = 8
dilution = 1

#Save lattice to file
ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)

lattice_name = 'lattice_Nx_{Nx}_Ny_{Ny}_dilution_{dilution}'.format(Nx=Nx, Ny=Ny, dilution=1)
f = open(lattice_name + ".xml", 'w')
print >> f, ds
f.close()

# beta_list = [2**tx for tx in range(10)]
beta_list = [1]
for beta in beta_list:
    parms.append(
        { 
          'LATTICE'        : "diluted {Nx} x {Ny}, dilution = {dilution}".format(Nx=Nx, Ny=Ny, dilution=dilution),
          'LATTICE_LIBRARY' : lattice_name + ".xml",
          'MODEL'          : "spin",
          'local_S'        : 0.5,
          'T'              : 1 / beta,
          'J'              : -1,
          'J1'             : -1,
          'THERMALIZATION' : 5000,
          'SWEEPS'         : 50000,
          # 'L'              : 60,
          'ALGORITHM'      : "loop"
        }
    )

#write the input file and run the simulation
results = "results"
try:
  os.mkdir(results)
except:
  pass


input_file = pyalps.writeInputFiles(os.path.join(results, lattice_name), parms)
pyalps.runApplication('loop', input_file, writexml=True)

#load the susceptibility and collect it as function of temperature T
data = pyalps.loadMeasurements(pyalps.getResultFiles(prefix=lattice_name))
print data
susceptibility = pyalps.collectXY(data,x='T',y='Susceptibility')
print susceptibility
# #make plot
# plt.figure()
# pyalps.plot.plot(susceptibility)
# plt.xlabel('Temperature $T/J$')
# plt.ylabel('Susceptibility $\chi J$')
# plt.ylim(0,0.22)
# plt.title('Quantum Heisenberg chain')
# plt.show()
