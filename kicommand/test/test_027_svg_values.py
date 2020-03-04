from __future__ import print_function

import os, sys
import unittest
from kicommand.kicommand import kc
import pcbnew

KICAD_INSTALL = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))

class TestSVGClass(unittest.TestCase):

    def test_fromsvg(self):
        kc(': dim "Elements Get width, height, x, y of the board" board list GetBoundingBox call copy copy copy GetWidth call swap GetHeight call extend swap GetCenter call flatlist extend -2 roundn int ;') # we don't care about differences less than 100nm
        kc(': tomm "Conversion [LIST] Convert nm to mm" 1 1 mm / list *. ;')
        kc('newboard')
        self.assertEqual(kc('4,2,3 mm F.SilkS drawparams getparams'),
        {'h': 3000000.0, 'zp': 0, 'zt': 0, 't': 4000000.0, 'w': 2000000.0, 'l': 'F.SilkS'})

        kc('"m 81.38357,74.230848 5.612659,1.870887 5.211757,3.474503 2.138156,2.138157 10.958048,-6.1472 0.53454,5.078121 -1.06908,4.009044 -2.80633,4.276312 -2.539056,1.603616 1.202716,4.276312 9.48806,-2.939963 13.36348,8.686253 -8.95353,-0.4009 -2.13815,5.34539 -5.21176,-2.67269 -4.67722,4.54358 -2.40542,-3.0736 -4.009046,6.94901 -3.741775,4.27631 -4.142676,2.53906 1.870887,3.34087 v 3.34087 l -4.409948,2.53906 h -2.806329 l -2.80633,-0.53454 -0.267271,-2.00452 1.469982,-1.60362 0.668176,-0.4009 -0.53454,-1.73726 -4.142676,0.53454 -4.677217,-0.93544 -3.34087,-0.66817 -1.336347,-0.13364 -2.405428,3.87541 -1.469982,1.33635 -1.603616,0.66817 -5.479026,-0.66817 -2.405425,-2.80633 -0.133636,-1.60362 3.207235,-3.34087 1.870887,-2.53906 -2.80633,-2.93996 -2.672696,-4.40995 -0.668174,-2.40543 -4.409945,5.47903 -3.207234,-5.34539 -5.078121,2.13815 -3.474506,-6.14719 -8.285356,0.26726 13.229844,-8.418985 10.022607,4.81085 0.400905,-5.34539 -3.741775,-2.138156 -2.405425,-3.474503 -0.668173,-3.073601 v -7.884451 l 13.363474,5.078121 3.608139,-2.939965 5.211757,-2.271789 3.875408,-1.33635 2.138156,0.133636 3.207234,-3.474503 4.677217,-2.939965 2.405425,-0.668174 z" 1 mm fromsvg drawsegments')
        self.assertEqual(kc('drawings len'),64)
        self.assertEqual(kc('dim'),[98613400, 63868400, 76171800, 97349700])

    def t_SVGValues(self):
        self.maxDiff = None
        svgdirectory = os.path.abspath(os.path.join(__file__,'..','loadable'))
        svgfiles = []
        for root, dirs, files in os.walk(svgdirectory):
            demoboards.extend([os.path.join(root,file) for file in files if file.endswith('.txt')])
        print ('\nSVG file results:')
        # print('\n'.join(demoboards))
        fullresult = {}
        for svgfile in svgfiles:
            #print(demoboard)
            result = kc('clear "%s" loadboard getbottomrowcounts stack'%demoboard)
            # remove install directory from printing demoboard
            fullresult[os.path.relpath(demoboard,KICAD_INSTALL)] = result
        print(fullresult)
        valuefile = os.path.join(os.path.dirname(__file__),'demoboard_values.txt')
        print("Reading comparison values from", valuefile)
        with open(valuefile,'r') as f:
           compare = eval(f.read())
        # now we need to compare the two dictionaries: fullresult and compare
        for key in set(fullresult.keys()).intersection(compare.keys()):
            self.assertEqual(fullresult.pop(key),compare.pop(key,None))
        #self.assertEqual(fullresult,compare)
        # the dictionaries should now be empty (and equal)
        self.assertEqual(fullresult,compare)
