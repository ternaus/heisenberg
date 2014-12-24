from __future__ import division
__author__ = 'vladimir'
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re

class Parser_ed:
  '''
  Class is used to parse xml files generated by ALPS
  '''
  def __init__(self, **kwargs):
    self.data_file = kwargs['data_file']
    self.data = ET.parse(self.data_file)
    self.root = self.data.getroot()
    self.fName = kwargs['fName']

    self.energy = None #total energy
    self.J = None # Coupling in the plane
    self.T = None # temperature
    self.num_sites = None #number of sites
    self.nx = None #number of sites in x direction
    self.ny = None #number of sites in y direction

  def get_nx(self):
    if self.nx == None:
      self.nx = int(re.search('(?<=Nx_)\d+', self.fName).group(0))

    return self.nx

  def get_ny(self):
    if self.ny == None:
      self.ny = int(re.search('(?<=Ny_)\d+', self.fName).group(0))
    return self.ny


  def get_num_sites(self):
    if self.num_sites == None:
      self.num_sites = self.root.find("Number_of_Sites")
      self.num_sites = int(float(self.num_sites.attrib["value"]))
    return self.num_sites

  def get_energy(self):
    if self.energy == None:
      self.energy = self.root.find("Energy_Density")
      self.energy = eval(self.energy.attrib['t_list']), eval(self.energy.attrib['y_list'])
    return self.energy

  def get_J(self):
    if self.J == None:
      self.J = float(self.root.find("J").attrib["value"])
    return self.J

  def get_T(self):
    if self.T == None:
      self.T = float(self.root.find("T").attrib["value"])
    return  self.T
