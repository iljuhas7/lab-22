#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import utest_calc

calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(utest_calc.CalcTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)
