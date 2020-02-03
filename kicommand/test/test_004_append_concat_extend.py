import unittest
from kicommand import run as kc
import pcbnew

class TestAppendConcatExtend(unittest.TestCase):


    def test_split(self):
        self.assertEqual(kc('1,2,3 split'),[u'1', u'2', u'3'])
    def test_pairwise(self):
         self.assertEqual(kc('1,2,3,4,5,6 int list 7,8,9,10,11,12 int append pairwise'),[[(1, 2), (3, 4), (5, 6)], [(7, 8), (9, 10), (11, 12)]] )
    def test_append(self):
        self.assertEqual(kc('1,2,3 int 4,5 int append'),[1,2,3,[4,5]])
    
    def test_concat(self):
        self.assertEqual(kc('1,2,3 int 4,5 int concat'),[1,2,3,4,5])
    
    def test_extend(self):
        self.assertEqual(kc('1,2,3 int 4,5 int extend'),[1,2,3,4,5])
    

if __name__ == '__main__':
    unittest.main()
   