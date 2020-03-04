import unittest
from kicommand.kicommand import kc

class TestDrawing(unittest.TestCase):

    def test_getparams_drawparams(self):
        self.assertEqual(kc('F.SilkS l param getparams'),{'h': 1000000.0, 'zp': 0, 'zt': 0, 't': 500000.0, 'w': 1000000.0, 'l': 'F.SilkS'} )
        self.assertEqual(kc('4,2,3 mm B.Cu drawparams getparams'),{'h': 3000000.0, 'zp': 0, 'zt': 0, 't': 4000000.0, 'w': 2000000.0, 'l': 'B.Cu'} )
        
    # def test_drawsegments(self):
        # track = kc('clear 0.5 mm t param F.Cu l param 10,10,20,30 mm '
                        # 'drawsegments delist delist')

    def test_drawsegments_wxpoint_attr_length(self):
        result = kc('clear 0,0,1,1 mm drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0]),1)
        # Test single list of list of numbers:
        result = kc('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kc('clear 0,0,1,1 mm list drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        result = kc('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        # Test single list of numbers:
        result = kc('clear 0,0,1,1,2,2,3,3 mm list drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kc('delist length roundint')
        self.assertEqual(result,[1414214.0, 1414214.0, 1414214.0]);
        # result = kc('delist remove',returnval=-1)
        # self.assertEqual(result,[])
        
        # Test two lists of numbers:
        result = kc('clear 0,0,1,1 mm list 2,2,3,3 mm list extend drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        self.assertEqual(len(result[0][1]),1)
        result = kc('copy 1 index remove 0 index remove',returnval=-1)
        self.assertEqual(result,[])
        
		# list of numbers as comma-seperated string
        result = kc('clear 0,0,1000000,1000000 ,2000000,2000000,3000000,3000000 concat drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kc('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kc('clear 0,0,1000000,1000000,2000000,2000000,3000000,3000000 drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kc('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kc('clear 0,0,1000000,1000000 list 2000000,2000000,3000000,3000000 list extend drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        self.assertEqual(len(result[0][1]),1)
        result = kc('copy 1 index remove 0 index remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kc('clear 0,0 mm wxpoint list 1,1 mm wxpoint append 2,2 mm wxpoint append 3,3 mm wxpoint append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kc('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kc('clear 0,0 mm wxpoint list 1,1 mm wxpoint append list 2,2 mm wxpoint list 3,3 mm wxpoint append append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        self.assertEqual(len(result[0][1]),1)
        result = kc('copy 1 index remove 0 index remove',returnval=-1)
        self.assertEqual(result,[])
        self.assertEqual(kc("clear 0,1 mm wxpoint list 2,3 mm wxpoint append 'x attr"),[0, 2000000])
        self.assertEqual(kc("clear 0,1 mm wxpoint list 2,3 mm wxpoint append 'y attr"),[1000000, 3000000])


if __name__ == '__main__':
    unittest.main()
   