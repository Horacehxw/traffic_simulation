import unittest
from IDM import IDM, IDMAuto
from Constants import *


class MyTestCase(unittest.TestCase):

    def test_something(self):
        # using the initial value of Cars
        idm = IDM(112.65 / 3.6, 0.5, 3.0, 3.0, 1.5)
        self.assertAlmostEqual(idm.veq_table[4], 0.6543521725647148)
        self.assertAlmostEqual(idm.veq_table[20], 10.690092856310587)
        self.assertAlmostEqual(idm.veq_table[90], 28.89634917614212)


if __name__ == '__main__':
    unittest.main()
