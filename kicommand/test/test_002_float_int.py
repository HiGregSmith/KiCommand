import unittest
from kicommand import run as kc

class TestFloatInt(unittest.TestCase):
# conversion: mils fromsvg dict mil string list ilist index. len delist float mm pairwise int iset bool split 
# remaining:  fromsvg string ilist index. pairwise iset split 

    
    def test_int(self):
        self.assertEqual(kc('0 int'),0)
        self.assertEqual(kc('12.7 int'),12)
        self.assertEqual(kc('0,1 int'),[0,1])
        self.assertEqual(kc('2,1 int'),[2,1])
        self.assertEqual(kc('2.2,6.6 float int'),[2,6])

    def test_float(self):
        self.assertEqual(kc('0 float'),0)
        self.assertEqual(kc('0,1 float'),[0,1])
        self.assertEqual(kc('2,1 float'),[2,1])
        self.assertEqual(kc('2.4,1.6 float'),[2.4,1.6])


if __name__ == '__main__':
    unittest.main()
   