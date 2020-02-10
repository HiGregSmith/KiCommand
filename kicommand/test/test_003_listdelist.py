import unittest
from kicommand.kicommand import kc

class TestListDelist(unittest.TestCase):
# conversion: mils fromsvg dict mil string list ilist index. len delist float mm pairwise int iset bool split 
# remaining:  fromsvg string ilist index. pairwise iset split 

#returnval -1 return entire stack

    def test_string(self):
        self.assertEqual(kc('1 float string'),"1.0")

    def test_list_delist(self):
        self.assertEqual(kc('1,2,3,4,5 int list'),[[1,2,3,4,5]])
        self.assertEqual(kc('1,2,3,4,5 int delist'),1)
if __name__ == '__main__':
    unittest.main()
   