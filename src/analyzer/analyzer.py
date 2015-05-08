#!/usr/bin/env python
import sys
import os
import Parser
from pylab import *
import pandas as pd
import seaborn as sns

sns.set_context(context='poster')
__author__ = 'vladimir'

'''
This script is used to plot data that is generated for the heisenberg model
'''
import numpy
import argparse
parser = argparse.ArgumentParser()


parser.add_argument('-dilution', type=float, help="dilution. f = 0 => 2D, f = 1 => PAM")
parser.add_argument('-beta', type=float, help="inverse temperature")
parser.add_argument('-J', type=float, default=1, help="coupling strength")
parser.add_argument('-J1', type=float, help="coupling in the z direction")
parser.add_argument('-m', type=str, default="heisenberg", help="name of the model")
parser.add_argument('-x_variable', type=str, help="""variable along x axis
T - temperature
J1
""")

parser.add_argument('--errors', dest='errors', action='store_true', help="Do we plot errorbars or not")
parser.add_argument('--no-errors', dest='errors', action='store_false')
parser.set_defaults(errors=True)

parser.add_argument('-y_variable', type=str, help="""variable along y axis
energy - total energy
C - specific heat
binder_staggered - Binder ratio of the staggered magnetization
""")
args = parser.parse_args(sys.argv[1:])

grid(True)
y_variable_list = ['energy', 'C', 'binder_staggered']
x_variable_list = ['T', 'beta', 'J1']

if args.y_variable not in y_variable_list:
  raise Exception("y_variable = {y_variable} should be in y_variable list = {y_list}".format(y_variable=args.y_variable, y_list=y_variable_list))

if args.x_variable not in x_variable_list:
  raise Exception("x_variable = {x_variable} should be in y_variable list = {x_list}".format(x_variable=args.x_variable, x_list=x_variable_list))

execfile('settings.py')

path = os.path.join(folder_with_different_models, args.m)
data_list = (Parser.Parser(data_file=os.path.join(path, item)) for item in os.listdir(path))

nx_ny_list = {}

if args.x_variable == 'T':
  xlabel("$T$")
  #filter J
  data_list = (item for item in data_list if (item.get_J() == args.J))

  #filter nx
  data_list = (item for item in data_list if (item.get_nx() == args.nx))
  #filetr ny
  data_list = (item for item in data_list if (item.get_ny() == args.ny))
  #filter J1
  data_list = (item for item in data_list if (item.get_J1() == args.J1))
  #filter dilution
  data_list = (item for item in data_list if (item.get_dilution() == args.dilution))
  if args.y_variable == "energy":
    ylabel("energy")
    result = [(item.get_T(), item.get_energy()[0], item.get_energy()[1]) for item in data_list]
  elif args.y_variable == 'C':
    ylabel("$C$")
    result = [(item.get_T(), item.get_C()[0], item.get_C()[1]) for item in data_list]


elif args.x_variable == 'J1':
  xlabel("$J'$")
  #filter J
  data_list = (item for item in data_list if (item.get_J() == args.J))

  #filter beta
  data_list = (item for item in data_list if (item.get_beta() == args.beta))

  #filter dilution
  data_list = (item for item in data_list if (item.get_dilution() == args.dilution))

  #create nx_ny_list

  for item in data_list:
    nx = item.get_nx()
    ny = item.get_ny()
    if (nx, ny) not in nx_ny_list:
      nx_ny_list[(nx, ny)] = [item]
    else:
      nx_ny_list[(nx, ny)] += [item]

  #This is list over spearate nx, ny, but beta can be the same, so I need to divide with respect to J1
  for (nx, ny) in nx_ny_list:
    print "nx = ", nx
    print 'ny = ', ny
    J1_dict = {}
    for item in nx_ny_list[(nx, ny)]:
      if item.get_J1() not in J1_dict:
        J1_dict[item.get_J1()] = [item]
      else:
        J1_dict[item.get_J1()] += [item]


    result = []
    for J1 in J1_dict:
      if args.y_variable == "energy":
        ylabel("energy")
        result += [(J1, numpy.mean([tx.get_energy()[0] for tx in J1_dict[J1]]), numpy.sqrt(sum([tx.get_energy()[1]**2 for tx in J1_dict[J1]])) / len(J1_dict[J1]))]
      elif args.y_variable == 'C':
        ylabel("$C$")
        result += [(J1, numpy.mean([tx.get_C()[0] for tx in J1_dict[J1]]), numpy.sqrt(sum([tx.get_C()[1]**2 for tx in J1_dict[J1]])) / len(J1_dict[J1]))]
      elif args.y_variable == 'binder_staggered':
        ylabel("$Binder$")
        temp = [tx.get_binder_staggered()[0] for tx in J1_dict[J1]]
        result += [(J1, numpy.mean(temp), 2 * numpy.std(temp) / math.sqrt(len(temp)))]


    temp1 = []
    for key in J1_dict:
      for x in J1_dict[key]:
        temp1 += [[key, x.get_binder_staggered()[0]]]
    df = pd.DataFrame(temp1)

    df.columns = ['J1', 'binder']
    df.to_csv('temp{N}_{dilution}.csv'.format(N=nx, dilution=args.dilution), index=False)
    # sns.regplot('J1', 'binder', df, lowess=True, label=r'${nx} \times {ny}$'.format(nx=nx, ny=ny), scatter=True)




    result.sort()

    x_list = [item[0] for item in result]
    y_list = [item[1] for item in result]
    y_err = [item[2] for item in result]

    print args.errors
    print 'x_list = ', x_list
    print 'y_list = ', y_list
    print 'y_err = ',   y_err

    if args.errors:
      errorbar(x_list, y_list, yerr=y_err, label=r'${nx} \times {ny}$'.format(nx=nx, ny=ny), linewidth=2)
    elif not args.errors:
      errorbar(x_list, y_list, label=r'${nx} \times {ny}$'.format(nx=nx, ny=ny), linewidth=2)

title('dilution = ${x}$'.format(x=(1-args.dilution)))
legend()
show()


