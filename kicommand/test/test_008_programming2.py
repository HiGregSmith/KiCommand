import unittest
from kicommand.kicommand import kc

class TestProgramming2(unittest.TestCase):
# conversion: mils fromsvg dict mil string list ilist index. len delist float mm pairwise int iset bool split 
# remaining:  fromsvg string ilist index. pairwise iset split 


    # this uses regex which is tested in 007
    def test_isnone_isnotnone(self):
        self.assertEqual(kc('0 list 0 regex isnone'),[False])
        self.assertEqual(kc('0 list 1 regex isnone'),[True])
        self.assertEqual(kc('0 list 0 regex isnotnone'),[True])
        self.assertEqual(kc('0 list 1 regex isnotnone'),[False])
        
    def test_Conditional(self):
        self.assertEqual(kc('clear true false true false ?true',returnval=-1),[True,False,True])
        self.assertEqual(kc('clear true false true ?false',returnval=-1),[True,False,False])

if __name__ == '__main__':
    unittest.main()
   