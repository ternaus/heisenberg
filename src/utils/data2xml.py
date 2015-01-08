from __future__ import division
__author__ = 'vladimir'
from xml.etree import ElementTree
from xml.dom import minidom
import pyalps
import sys

class DataToXML:
  '''
  This class takes data generated by ALPS loop or exact diagonalization algorithm and saves it as an xml file
  '''
  def __init__(self, **kwargs):
    self.data = kwargs['data'];
    self.lattice = kwargs['lattice']

    self.result = ElementTree.Element("root")
    if 'ed' in kwargs:
      for item in self.data[0]:
        ElementTree.SubElement(self.result, item.props["observable"].replace(" ", "_").replace("^", "_X"), attrib={"y_list": str(list(item.y)), 't_list': str(list(item.x))})
    elif 'looper' in kwargs:
      for item in self.data[0]:
        if "Diagonal spin correlations" in item.props["observable"]:
          ElementTree.SubElement(self.result, item.props["observable"].replace(" ", "_").replace("^", "_X"), attrib={"value": str(correlations2dict(item.x, item.y))})
        elif item.props["observable"] == "Offdiagonal spin correlations":
          ElementTree.SubElement(self.result, item.props["observable"].replace(" ", "_").replace("^", "_X"), attrib={"value": str(correlations2dict(item.x, item.y))})
        else:
          ElementTree.SubElement(self.result, item.props["observable"].replace(" ", "_").replace("^", "_X"), attrib={"value": str(item.y[0].mean), 'error': str(item.y[0].error)})

      for key, value in self.data[0][0].props.iteritems():
        ElementTree.SubElement(self.result, key , attrib={"value": str(value)})

      ElementTree.SubElement(self.result, "vertices", attrib={"value": str(lattice2vertices(self.lattice))})
    else:
      raise Exception('algorithm is not defined')


  def __str__(self):
    return ElementTree.tostring(self.result)


  def pretty(self):
    a = ElementTree.tostring(self.result).replace("^", "**").replace("|", "").replace("&", "").replace("[", "_").replace("]", "").replace("Winding Number", "Winding_Number").replace(" spin correlations", "_spin_correlations")

    reparsed = minidom.parseString(a)
    return reparsed.toprettyxml(indent="  ")

  def tofile(self, file_name):
    f = open(file_name, "w")
    print >> f, self.pretty()
    f.close()

def correlations2dict(x, y):
  '''

  :param data: ALPS output about spin-spin correlation functions
  :return: dictionary: key - site value that is correlated with site 0, value - tuple with (value, error)
  '''

  result = dict(zip(x, y))

  for x in result:
    temp = str(result[x]).replace("+/-", "").strip(). split()
    result[x] = (float(temp[0]), float(temp[1]))

  return result

def lattice2vertices(lattice):
  '''

  :param lattice: lattice in xml format
  :return: dictionary - key site value, value - type, coordinates
  '''
  result = {}
  data = ElementTree.parse(lattice)
  root = data.getroot()
  for vertex in root.iter("VERTEX"):
    id = int(vertex.attrib["id"])
    tp = int(vertex.attrib["type"])
    coordinates = vertex.find("COORDINATE").text
    temp = coordinates.strip().split()
    result[id] = (tp, float(temp[0]), float(temp[1]), float(temp[2]))

  return result