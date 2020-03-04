import unittest
from kicommand.kicommand import kc

class TestIsTests(unittest.TestCase):
    def test_isfloat(self):
        self.assertFalse(kc('1.5 isfloat'))
        self.assertFalse(kc('1.5 int isfloat'))
        self.assertTrue(kc('1.5 float isfloat'))
        self.assertFalse(kc('1.5,3.5 float isfloat'))
        
    def test_isint(self):
        self.assertFalse(kc('1.5 isint'))
        self.assertTrue(kc('1.5 int isint'))
        self.assertFalse(kc('1.5 float isint'))
        self.assertFalse(kc('1.5,3.5 int isint'))
        
    def test_isiter(self):
        self.assertFalse(kc('1.5 isiter'))
        self.assertFalse(kc('1.5 int isiter'))
        self.assertFalse(kc('1.5 float isiter'))
        self.assertTrue(kc('1.5,3.5 int isiter'))
        self.assertTrue(kc('1.5,3.5 split isiter'))

    def test_isstring(self):
        self.assertTrue(kc('1.5 isstring'))
        self.assertFalse(kc('1.5 int isstring'))
        self.assertFalse(kc('1.5 float isstring'))
        self.assertFalse(kc('1.5,3.5 int isstring'))
    # def test_callfilter(self):
    # def test_callnotfilter(self):
    # def test_calllist(self):
    # def test_fcall(self):
    

if __name__ == '__main__':
    unittest.main()
   