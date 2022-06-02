#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import inv_student;

class CalcBasicTests(unittest.TestCase):
    def test_inv_student_load(self):
        self.assertTrue(inv_student.student_load("inv_1.db"))
    
if __name__ == '__main__':
    unittest.main()
