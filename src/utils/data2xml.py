from __future__ import division
__author__ = 'vladimir'
from xml.etree import ElementTree
from xml.dom import minidom

class DataToXML:
  '''
  This class takes data generated by ALPS loop or exact diagonalization algorithm and saves it as an xml file
  '''
  def __init__(self, **kwargs):
    self.data = kwargs['data']
    self.result = ElementTree.Element("root")
    if 'ed' in kwargs:
      for item in self.data[0]:
        ElementTree.SubElement(self.result, item.props["observable"].replace(" ", "_").replace("^", "_X"), attrib={"y_list": str(list(item.y)), 't_list': str(list(item.x))})
    elif 'looper' in kwargs:
      for item in self.data[0]:
        ElementTree.SubElement(self.result, item.props["observable"].replace(" ", "_").replace("^", "_X"), attrib={"value": str(item.y[0].mean), 'error': str(item.y[0].error)})

      for key, value in self.data[0][0].props.iteritems():
        ElementTree.SubElement(self.result, key , attrib={"value": str(value)})
    else:
      raise Exception('algorithm is not defined')


  def __str__(self):
    return ElementTree.tostring(self.result)


  def pretty(self):
    a = ElementTree.tostring(self.result).replace("^", "**").replace("|", "").replace("&", "")
    reparsed = minidom.parseString(a)
    return reparsed.toprettyxml(indent="  ")

  def tofile(self, file_name):
    f = open(file_name, "w")
    print >> f, self.pretty()
    f.close()