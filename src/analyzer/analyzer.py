#!/usr/bin/env python
import sys
import os
import Parser
from pylab import *

__author__ = 'vladimir'

'''
This script is used to plot data that is generated for the heisenberg model
'''

import argparse
parser = argparse.ArgumentParser()


parser.add_argument('-dilution', type=float, help="dilution. f = 0 => 2D, f = 1 => PAM")
# parser.add_argument('-beta', type=float, help="inverse temperature")
parser.add_argument('-J', type=float, default = 1, help="coupling strength")
parser.add_argument('-J1', type=float, default = 0, help="coupling in the z direction")
parser.add_argument('-m', type=str, default = "heisenberg", help="name of the model")
parser.add_argument('-nx', type=int, help="number of  sites in x direction")
parser.add_argument('-ny', type=int, help="number of  sites in y direction")
parser.add_argument('-x_variable', type=str, help="""variable along x axis
T - temperature
""")

parser.add_argument('-y_variable', type=str, help="""variable along y axis
energy - total energy
""")
args = parser.parse_args(sys.argv[1:])

y_variable_list = ['energy']

if args.y_variable not in y_variable_list:
  raise Exception("y_variable = {y_variable} should be in y_variable list = {y_list}".format(y_variable=args.y_variable, y_list=y_variable_list))

execfile('settings.py')

path = os.path.join(folder_with_different_models, args.m)
data_list = (Parser.Parser(data_file=os.path.join(path, item)) for item in os.listdir(path))

#filter J
data_list = (item for item in data_list if (item.get_J() == args.J))

#filter nx
data_list = (item for item in data_list if (item.get_nx() == args.nx))
#filetr ny
data_list = (item for item in data_list if (item.get_ny() == args.ny))

result = []

if args.x_variable == "T":
  xlabel("$T$")
  if args.y_variable == "energy":
    ylabel("energy")
    result = [(item.get_T(), item.get_energy()[0], item.get_energy()[1]) for item in data_list]
  if args.y_variable == 'C':
    ylabel("$C$")
    result = [(item.get_T(), item.get_C()[0], item.get_C()[1]) for item in data_list]
result.sort()

x_list = [item[0] for item in result]
y_list = [item[1] for item in result]
y_err = [item[2] for item in result]

print 'x_list = ', x_list
print 'y_list = ', y_list
print 'y_err = ',   y_err
errorbar(x_list, y_list, yerr=y_err)
show()


