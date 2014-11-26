from unittest import TestCase
from src import DilutedLattice


__author__ = 'vladimir'

class TestDilutedSquare(TestCase):

  def test_1site_d0(self):
    Nx = 1
    Ny = 1
    dilution = 0
    ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)
    self.assertEquals(2, ds.num_edges())
    self.assertEquals(2, ds.num_edges(0))
    self.assertEquals(1, ds.num_vertices(0))

  def test_4x4_square(self):
    Nx = 4
    Ny = 4
    dilution = 0
    ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)
    self.assertEquals(32, ds.num_edges())
    self.assertEquals(32, ds.num_edges(0))
    self.assertEquals(16, ds.num_vertices(0))

  def test_4x4_PAM(self):
    Nx = 4
    Ny = 4
    dilution = 1
    ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)
    self.assertEquals(Nx * Ny * 3, ds.num_edges())
    self.assertEquals(Nx * Ny * 2, ds.num_edges(0))
    self.assertEquals(Nx * Ny, ds.num_edges(1))
    self.assertEquals(Nx * Ny, ds.num_vertices(0))
    self.assertEquals(Nx * Ny, ds.num_vertices(1))

  def test_xy2i(self):
    Nx = 3
    Ny = 3

    dilution = 0
    ds = DilutedLattice.DilutedSquare(Nx=Nx, Ny=Ny, dilution=dilution)
    self.assertEquals(1, ds.xy2i(0, 0, Nx))
    self.assertEquals(2, ds.xy2i(1, 0, Nx))
    self.assertEquals(3, ds.xy2i(2, 0, Nx))
    self.assertEquals(4, ds.xy2i(0, 1, Nx))
