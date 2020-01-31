import unittest
from kicommand import run as kc
import pcbnew

class TestProgramming(unittest.TestCase):
# conversion: mils fromsvg dict mil string list ilist index. len delist float mm pairwise int iset bool split 
# remaining:  fromsvg string ilist index. pairwise iset split 

    def test_builtins_sindex_fcallargs(self):
        self.assertEqual(kc('builtins pow sindex list 2,3 float list fcallargs'),[8.0])

    def test_len(self):
        self.assertEqual(kc('1,2,3,4,5,6 int len'),6)
        self.assertEqual(kc('12345 len'),5)
		
    def test_list_delist(self):
        self.assertEqual(kc('1,2,3,4,5 int list'),[[1,2,3,4,5]])
        self.assertEqual(kc('1,2,3,4,5 int delist'),1)
		
    def test_index(self):
        self.assertEqual(kc('987654 1 index int'),8)
        self.assertEqual(kc('9,8,7,6,5 int 3 index'),6)

    def test_mils_mil_mm(self):
        self.assertEqual(kc('10 mm'),10*pcbnew.IU_PER_MM)
        self.assertEqual(kc('10 mils'),10*pcbnew.IU_PER_MILS)
        self.assertEqual(kc('10 mil'),10*pcbnew.IU_PER_MILS)            

    def test_plus(self):
        self.assertEqual(kc('0 1 +'),1)
        self.assertEqual(kc('5.3 6.2 +'),11.5)
    
    def test_sum(self):
        self.assertEqual(kc('0,1,2,3.1,4,5 float sum'),15.1)
        self.assertEqual(kc('5.3 float list 6.2 float list concat sum'),11.5)
        
    def test_plusdot(self):
        self.assertEqual(kc('3,7 float 5.3,6.2 float +.'),[8.3,13.2])
        
    def test_minus(self):
        self.assertEqual(kc('0 1 -'),-1)
        self.assertEqual(kc('1 0 -'),1)
        self.assertAlmostEqual(kc('5.3 6.2 -'),-0.9,15) # this comes back as -0.9000000000000004
        self.assertAlmostEqual(kc('6.2 5.3 -'),0.9,15) # this comes back as 0.9000000000000004

    def test_divide(self):
        self.assertEqual(kc('12 1 /'),12)
        self.assertEqual(kc('1 2 /'),0.5)
    
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

    def test_bool(self):
        self.assertTrue(kc('0 bool'))
        self.assertEqual(kc('0 float bool'),[False])
        self.assertEqual(kc('0 int bool'),[False])
        self.assertFalse(kc("' bool"))
        self.assertTrue(kc('1 bool'))
        self.assertEqual(kc('1 float bool'),[True])
        self.assertEqual(kc('1 int bool'),[True])
        self.assertTrue(kc('Hello bool'))
        self.assertTrue(kc('2 bool'))
        self.assertEqual(kc('2 float bool'),[True])
        self.assertEqual(kc('2 int bool'),[True])
    def test_multiply(self):
        self.assertEqual(kc('0 1 *'),0.0)
        self.assertEqual(kc('1 1 *'),1.0)
        self.assertEqual(kc('2 3 *'),6.0)

    def test_dict(self):
        self.assertEqual(kc('1,2,3,4,5 int 5,4,3,2,1 int dict'), {1: 5, 2: 4, 3: 3, 4: 2, 5: 1})

if __name__ == '__main__':
    unittest.main()
   