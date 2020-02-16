import os, sys
import unittest
from kicommand.kicommand import kc
import pcbnew

KICAD_INSTALL = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))

class TestBoardClass(unittest.TestCase):

    def test_DemoboardValues(self):
        self.maxDiff = None
        demodirectory = os.path.join(KICAD_INSTALL,'share','kicad','demos')
        demoboards = []
        for root, dirs, files in os.walk(demodirectory):
            demoboards.extend([os.path.join(root,file) for file in files if file.endswith('.kicad_pcb')])
        print '\nDemo board results:'
        # print '\n'.join(demoboards)
        fullresult = {}
        for demoboard in demoboards:
            #print demoboard
            result = kc('clear "%s" loadboard getbottomrowcounts stack'%demoboard)
            # remove install directory from printing demoboard
            fullresult[os.path.relpath(demoboard,KICAD_INSTALL)] = result
        print fullresult
        valuefile = os.path.join(os.path.dirname(__file__),'demoboard_values.txt')
        print "Reading comparison values from", valuefile
        with open(valuefile,'r') as f:
           compare = eval(f.read())
        # now we need to compare the two dictionaries: fullresult and compare
        for key in set(fullresult.keys()).intersection(compare.keys()):
            self.assertEqual(fullresult.pop(key),compare.pop(key,None))
        #self.assertEqual(fullresult,compare)
        # the dictionaries should now be empty (and equal)
        self.assertEqual(fullresult,compare)
