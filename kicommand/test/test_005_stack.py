import unittest
from kicommand import run as kc
import pcbnew

class TestProgramming(unittest.TestCase):

# zip2 zip 
    def test_swap(self):
        self.assertEqual(kc('1 2 3 4 int'),4)
        self.assertEqual(kc('1 2 3 4 swap int'),3)

    def test_pop(self):
        self.assertEqual(kc('1 2 3 pop int'),2)
    
    def test_pick(self):
        self.assertEqual(kc('34 67 234 789 2 pick int'),67)
		
		# swap, zip2, zip
    def test_zip2(self):
        self.assertEqual(kc('1,2,3,4 int 5,6,7,8 int zip2'),[(1, 5), (2, 6), (3, 7), (4, 8)] )
    def test_zip(self):
        self.assertEqual(kc('1,2,3,4 int list 5,6,7,8 int append zip'),[(1, 5), (2, 6), (3, 7), (4, 8)] )
		
    def test_clear(self):
        self.assertIsNone(kc('1 2 3 3 clear'))
    
    def test_sum(self):
        self.assertEqual(kc('0,1,2,3.1,4,5 float sum'),15.1)
        self.assertEqual(kc('5.3 float list 6.2 float list concat sum'),11.5)
        
    def test_plusdot(self):
        self.assertEqual(kc('3,7 float 5.3,6.2 float +.'),[8.3,13.2])
        
    def test_multiplydot(self):
        result = kc('3,7 float 5.3,6.2 float *.')
        self.assertEqual(len(result),2)
        self.assertAlmostEqual(result[0],15.899999999999999,15)
        self.assertAlmostEqual(result[1],43.4,15)
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
        self.assertFalse(kc('0 float bool delist'))
        self.assertFalse(kc('0 int bool delist'))
        self.assertFalse(kc("' bool"))
        self.assertTrue(kc('1 bool'))
        self.assertTrue(kc('1 float bool delist'))
        self.assertTrue(kc('1 int bool delist'))
        self.assertTrue(kc('Hello bool'))
        self.assertTrue(kc('2 bool'))
        self.assertTrue(kc('2 float bool delist'))
        self.assertTrue(kc('2 int bool delist'))
    def test_multiply(self):
        self.assertEqual(kc('0 1 *'),0.0)
        self.assertEqual(kc('1 1 *'),1.0)
        self.assertEqual(kc('2 3 *'),6.0)

    def test_dict(self):
        self.assertEqual(kc('1,2,3,4,5 int 5,4,3,2,1 int dict print'), {1: 5, 2: 4, 3: 3, 4: 2, 5: 1})

if __name__ == '__main__':
    unittest.main()
   