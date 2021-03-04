
import unittest
import numpy as np
from flutter_utilities import *

class TestComplex2RealNotation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_values(self):
        
        fd_complex = {"c_aa":{"values":[2.4-0.36j, 8/np.pi*(2.8-0.63j)],"k":[0.5, np.pi/10]},
            "c_ah":{"values":[0.0071+1.2j, 4/np.pi*(0.19+1.7j)],"k":[0.5, np.pi/10]},
            "c_ha":{"values":[-3.6-0.45j, 4/np.pi*(-9.0+0.68j)],"k":[0.5, np.pi/10]},
            "c_hh":{"values":[0.063-1.6j, 2/np.pi*(-1.2-5.1j)],"k":[0.5, np.pi/10]}}

        fd_real = {"H1":{"values":[-1.6*np.pi/2, -5.1],"U_red":[np.pi/0.5, 10]},
            "H2":{"values":[-0.45*np.pi/4, 0.68],"U_red":[np.pi/0.5, 10]},
            "H3":{"values":[-3.6*np.pi/4, -9.0],"U_red":[np.pi/0.5, 10]},
            "H4":{"values":[0.063*np.pi/2, -1.2],"U_red":[np.pi/0.5, 10]},
            "A1":{"values":[1.2*np.pi/4, 1.7],"U_red":[np.pi/0.5, 10]},
            "A2":{"values":[-0.36*np.pi/8, -0.63],"U_red":[np.pi/0.5, 10]},
            "A3":{"values":[2.4*np.pi/8, 2.8],"U_red":[np.pi/0.5, 10]},
            "A4":{"values":[0.0071*np.pi/4, 0.19],"U_red":[np.pi/0.5, 10]}}

        self.assertDictEqual(fd_real, complex2real_notation(fd_complex))