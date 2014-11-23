import random

__author__ = 'vladimir'


'''
This class describes diluted square lattice withe periodic boundary conditions.
'''

import sys
import traceback



from xml.etree import ElementTree

f = 1
Nx = 2
Ny = 2



class DilutedSquare:
  def __init__(self, **kwargs):
    self.Nx = kwargs['Nx']
    if not isinstance(self.Nx, int):
      try:
        raise Exception("number of sites in x direction is not integer")
      except:
        traceback.print_exc(file=sys.stdout)
        exit(3)

    if self.Nx < 1:
      try:
        raise Exception("number of sites in x direction should be bigger than 1")
      except:
        traceback.print_exc(file=sys.stdout)
        exit(3)

    self.Ny = kwargs['Ny']
    if not isinstance(self.Ny, int):
      try:
        raise Exception("number of sites in y direction is not integer")
      except:
        traceback.print_exc(file=sys.stdout)
        exit(3)

    if self.Ny < 1:
      try:
        raise Exception("number of sites in y direction should be bigger than 1")
      except:
        traceback.print_exc(file=sys.stdout)
        exit(3)

    self.dilution = kwargs['dilution']

    if not (isinstance(self.dilution, float) or self.dilution == 0 or self.dilution ==1):
      try:
        raise Exception("dilution should be float or 0 or 1")
      except:
        traceback.print_exc(file=sys.stdout)
        exit(3)

    if not 0 <= self.dilution <= 1:
      try:
        raise Exception("dilution should be in [0, 1]")
      except:
        traceback.print_exc(file=sys.stdout)
        exit(3)


    self.root = ElementTree.Element("GRAPH")

    edge_ind = 1
    for nx in range(self.Nx):
      for ny in range(self.Ny):
        i = self.xy2i(nx, ny, self.Nx)
        v = ElementTree.SubElement(self.root, "VERTEX", attrib={"id": str(i), 'type': "0"})
        c = ElementTree.SubElement(v, "COORDINATE")
        c.text = "{nx} {ny}".format(nx=nx, ny=ny)

        n1_tx, n1_ty = nx + 1, ny

        if n1_tx >= Nx:
          n1_tx = 0

        n1_i = self.xy2i(n1_tx, n1_ty, Nx)

        n2_tx, n2_ty = nx, ny + 1

        if n2_ty >= Ny:
          n2_ty = 0

        n2_i = self.xy2i(n2_tx, n2_ty, Nx)


        ElementTree.SubElement(self.root, "EDGE", attrib={"id": str(edge_ind), 'type': "0", "source": str(i), "target": str(n1_i)})

        ElementTree.SubElement(self.root, "EDGE", attrib={"id": str(edge_ind), 'type': "0", "source": str(i), "target": str(n2_i)})

        edge_ind += 1

    vertex_ind = Nx * Ny

    # edges that stick out of the square lattice
    for nx in range(Nx):
      for ny in range(Ny):
        i = self.xy2i(nx, ny, Nx)
        if random.random() <= self.dilution:
          v = ElementTree.SubElement(self.root, "VERTEX", attrib={"id": str(i), 'type': "1"})
          c = ElementTree.SubElement(v, "COORDINATE")
          c.text = "{nx} {ny}".format(nx=nx, ny=ny)
          vertex_ind += 1

          ElementTree.SubElement(self.root, "EDGE", attrib={"id": str(edge_ind), 'type': "0", "source": str(i), "target": str(vertex_ind)})
          edge_ind += 1

  def __str__(self):
    return str(ElementTree.dump(self.root))

  def xy2i(self, x, y, Nx):
    return y * Nx + x + 1
  
  def num_edges(self, tp=None):
    result = 0
    for item in self.root:
      if item.tag == "EDGE":
        if tp==None:
          result += 1
        elif tp!= None:
          if int(item.attrib["type"]) == tp:
            result += 1
    return result

  def num_vertices(self, tp=None):
    num_vertices = 0
    for item in self.root:
      if item.tag == "VERTEX":
        if tp==None:
           num_vertices += 1
        elif tp!= None:
          if int(item.attrib["type"]) == tp:
            num_vertices += 1
    return num_vertices
  def __len__(self):
    '''

    :return: sum of edges and vertices.
    '''
    return len(self.root)
#