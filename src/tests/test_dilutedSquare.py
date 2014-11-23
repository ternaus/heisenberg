from unittest import TestCase
from src import DilutedLattice

__author__ = 'vladimir'

class TestDilutedSquare(TestCase):
  def test_1site_d0(self):
    Nx = 1
    Ny = 1
    dilution = 0
    ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)
    print ds
    self.assertEqual(3, len(ds))
    num_edges = 0
    num_vertices = 0
    self.assertEquals(2, ds.num_edges())
    self.assertEquals(2, ds.num_edges(0))
    self.assertEquals(1, ds.num_vertices(0))
