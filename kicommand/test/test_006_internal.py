import unittest
import pcbnew
import kicommand
from kicommand.kicommand import kc
import datetime
import time

class TestInternal(unittest.TestCase):

    def test_pcbnew(self):
        self.assertEqual(kc('pcbnew'),pcbnew)
		
    def test_now(self):
        kcnow = kc('now')
        k = datetime.datetime.strptime(kcnow,'%a %b %d %H:%M:%S %Y')
        n = datetime.datetime(*time.localtime()[:-2])
        delta = (n-k).total_seconds()
        self.assertTrue(0 <= delta < 10,"now command expected to be within 10 seconds of current time. Delta was {} seconds.".format(delta))

        #now = time.localtime()
        #datetime.datetime.strptime(time.asctime(),'%a %b %d %H:%M:%S %Y')
        
        # datetime(*time.localtime())
        # timetuple = time.localtime([time])
        # timetuple()
    def test_load(self):
        pcommands = ['moduletextobj', 'wxpoint', 'setselect', 'referencetextobj', 'outlinepads', 'valuetextobj', 'drawparams', 'textfromobj', 'referencetext', 'toptextobj', 'outlinetext', 'clearallselected', 'not', 'orthogonal', 'copy', 'clearselect', 'texttosegments', 'valuetext']
        self.assertEqual(set(pcommands) - set(kicommand.kicommand._dictionary['persist'].keys()),set([]))
        # self.assertTrue(set(pcommands) <= set(kicommand.kicommand._dictionary['persist'].keys()))
        self.assertFalse(set(['thiscommand doesnt exist']) < set(kicommand.kicommand._dictionary['persist'].keys()))

    def test_help_helpcat_explain_see_seeall_helpall(self):
        result = kc("clear help All helpcat 'help explain seeall 'bool see helpall",returnval=-1)
        self.assertTrue(result is None or not bool(result) or len(result) == 0)
        #self.assertEqual(result,[])
        

if __name__ == '__main__':
    unittest.main()
   