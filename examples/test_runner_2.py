#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import utest_calc

calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(utest_calc.CalcTest))
calcTestSuite.addTest(unittest.makeSuite(utest_calc.CalcExTests))
print("count of tests: " + str(calcTestSuite.countTestCases()) + "\n")

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)
