#!/usr/bin/env python
'''
This script creates start scripts for the ALPS heisenberg looper simulation
'''

from __future__ import division
import os
import sys
import time

execfile("simulation_parameters_heisenberg.py")

try:
  os.symlink(os.path.join("loop", "looper.py"), "looper.py")
except:
  pass

jobs = "jobs"

try:
  os.mkdir(jobs)
except:
  pass
scriptFile = open(os.path.join(jobs, "startScript.sh"), 'w')

for J in j_list:
  for J1 in j1_list:
    for dilution in dilution_list:
      for nx, ny in shape_list:
        for beta in beta_list:
          time.sleep(0.01)
          timestamp = time.time()
          if '-home' in sys.argv:
            jobScript = r'''
#!/bin/bash
/usr/bin/time -v {path}/looper.py -J {J} -J1 {J1} -beta {beta} -nx {nx} -ny {ny} -dilution {dilution} > {timestamp}.log
        '''.format(J=J, J1=J1, beta=beta, nx=nx, ny=ny, dilution=dilution, path=os.getcwd(), timestamp=timestamp)
          elif '-cluster' in sys.argv:
            jobScript = r'''
#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -pe orte 1
#cd $SGE_O_WORKER
source /home/viglovik/intel/bin/compilervars.sh intel64
/usr/bin/time -v {path}/looper.py -J {J} -J1 {J1} -beta {beta} -nx {nx} -ny {ny} -dilution {dilution} > {timestamp}.log
        '''.format(J=J, J1=J1, beta=beta, nx=nx, ny=ny, dilution=dilution, path=os.getcwd(), timestamp=timestamp)
          jobFile = "v_{J}_{J1}_nx{nx}_ny{ny}_beta{beta}_dilution{dilution}_{timestamp}.sh".format(J=J, J1=J1, nx=nx, ny=ny, beta=beta, dilution=dilution, timestamp=timestamp)
          resultFile = open(os.path.join(jobs, jobFile), 'w')
          print >> resultFile, jobScript.lstrip()
          resultFile.close()

          if '-home' in sys.argv:
            print >> scriptFile, "{jobFile}".format(jobFile=jobFile)
          elif '-cluster' in sys.argv:
            print >> scriptFile, "qsub {jobFile}".format(jobFile=jobFile)
scriptFile.close()

