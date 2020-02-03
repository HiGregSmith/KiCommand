import unittest
from kicommand import run as kc
import pcbnew

class TestProgramming(unittest.TestCase):
# conversion: mils fromsvg dict mil string list ilist index. len delist float mm pairwise int iset bool split 
# remaining:  fromsvg string ilist index. pairwise iset split 

    def test_istype(self):
        self.assertEqual(kc('board list BOARD istype'),[True])
        self.assertEqual(kc('board list MODULE istype'),[False])

    def test_filter_filtertype_board(self):
        self.assertEqual(kc('clear 1,2,3,4 int copy 3 int = filter'),[3])
        self.assertEqual(kc('clear board list copy BOARD filtertype delist ='),[True])
        self.assertEqual(kc('clear board list MODULE filtertype'),[])

    def test_ilist(self):
        self.assertEqual(kc('1,2,3,4 int ilist'),[1, 2, 3, 4])
        self.assertEqual(kc('asdf ilist'),[u'a', u's', u'd', u'f'])

    def test_builtins_sindex_fcallargs(self):
        self.assertEqual(kc('builtins pow sindex list 2,3 float list fcallargs'),[8.0])

    def test_len(self):
        self.assertEqual(kc('1,2,3,4,5,6 int len'),6)
        self.assertEqual(kc('12345 len'),5)
		
    def test_index(self):
        self.assertEqual(kc('987654 1 index int'),8)
        self.assertEqual(kc('9,8,7,6,5 int 3 index'),6)
		
    def test_indexdot(self):
        self.assertEqual(kc('1,2,3,4,5 int list 7,8,9,10,11 int append 3 index.'),[4, 10])

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

    def test_roundint(self):
        self.assertEqual(kc('12.56 roundint'),13)

    def test_roundn(self):
        self.assertEqual(kc('12.46 1 roundn'),12.5)
		
    def test_regex(self):
        self.assertEqual(kc('25,567,234,12,356,19,15,56 split 1.* regex bool'),[False, False, False, True, False, True, True, False] )

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
   