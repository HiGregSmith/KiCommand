import unittest
from kicommand.kicommand import kc

class TestDrawing2(unittest.TestCase):

    # def test_showparams_drawparams(self):
        # result = kc('clear F.SilkS layernums l param 0,0,0,1,1,1,1,0,0,0 mm 10 int list *. drawsegments delist 1 mm list swap round',returnval=-1)
    # # def test_drawsegments(self):
        # # track = kc('clear 0.5 mm t param F.Cu l param 10,10,20,30 mm '
                        # # 'drawsegments delist delist')

    def test_rotate_round_flatlist_select_selected(self):        
        kc(': dim "Elements Get width, height, x, y of the board" board list GetBoundingBox call copy copy copy GetWidth call swap GetHeight call extend swap GetCenter call flatlist extend -2 roundn int ;') # we don't care about differences less than 100nm
        kc(': tomm "Conversion [LIST] Convert nm to mm" 1 1 mm / list *. ;')
        kc('newboard')
        self.assertEqual(kc('4,2,3 mm F.SilkS drawparams showparams'),
        {'h': 3000000.0, 'zp': 0, 'zt': 0, 't': 4000000.0, 'w': 2000000.0, 'l': 'F.SilkS'})
        self.assertEqual(kc('clear 0,0,10,0 mm list drawsegments dim drawings len append'),[14000000,4000000,5000000,0, 1])
        self.assertEqual(kc('drawings len'),1)
        self.assertEqual(kc('drawings 90 rotate dim'),[4000000, 14000000, 5000000, 0] )
        self.assertEqual(kc('drawings 45 rotate dim'),[11071100, 11071100, 5000000, 0] )
        self.assertEqual(kc('drawings 45 rotate dim'),[14000000, 4000000, 5000000, 0] )
        self.assertEqual(kc('drawings 180 rotate dim'),[14000000,4000000,5000000,0])
        self.assertEqual(kc('clear 10,0,10,10 mm list drawsegments dim'),[14000000, 14000000, 5000000, 5000000] )
        self.assertEqual(kc('drawings len'),2)

        self.assertEqual(kc('drawings 1 mm list swap round dim'),[14000000, 14000000, 5000000, 5000000] )
        self.assertEqual(kc('drawings len'),3)
        self.assertEqual(kc('drawings 90 rotate dim'),[14000000, 14000000, 10666700, 5000000] )
        self.assertEqual(kc('drawings 45 rotate dim'),[10656900, 18142100, 8511800, 2166700] )
        self.assertEqual(kc('drawings 45 rotate dim'),[14000000, 14000000, 10666700, -666700] )
        self.assertEqual(kc('drawings 180 rotate dim'),[14000000, 14000000, 5000000, 5000000] )
        self.assertEqual(kc('drawings selected len'),0 )        
        self.assertEqual(kc('drawings select drawings len list drawings selected len append'),[3,3] )        
        self.assertEqual(kc('drawings selected length -2 roundn int'),[1414200, 9000000, 9000000] )        
   
    def test_layernums(self):
        self.maxDiff = None
        self.assertEqual(kc('newboard board list 0,64,1 range list. GetLayerName callargs'),[u'F.Cu', u'In1.Cu', u'In2.Cu', u'In3.Cu', u'In4.Cu', u'In5.Cu', u'In6.Cu', u'In7.Cu', u'In8.Cu', u'In9.Cu', u'In10.Cu', u'In11.Cu', u'In12.Cu', u'In13.Cu', u'In14.Cu', u'In15.Cu', u'In16.Cu', u'In17.Cu', u'In18.Cu', u'In19.Cu', u'In20.Cu', u'In21.Cu', u'In22.Cu', u'In23.Cu', u'In24.Cu', u'In25.Cu', u'In26.Cu', u'In27.Cu', u'In28.Cu', u'In29.Cu', u'In30.Cu', u'B.Cu', u'B.Adhes', u'F.Adhes', u'B.Paste', u'F.Paste', u'B.SilkS', u'F.SilkS', u'B.Mask', u'F.Mask', u'Dwgs.User', u'Cmts.User', u'Eco1.User', u'Eco2.User', u'Edge.Cuts', u'Margin', u'B.CrtYd', u'F.CrtYd', u'B.Fab', u'F.Fab', u'Rescue', u'BAD INDEX!', u'BAD INDEX!',u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!'])
        #self.assertEqual(kc('newboard board list 0,64,1 range list. GetLayerName callargs'),[u'top_copper', u'In1.Cu', u'In2.Cu', u'In3.Cu', u'In4.Cu', u'In5.Cu', u'In6.Cu', u'In7.Cu', u'In8.Cu', u'In9.Cu', u'In10.Cu', u'In11.Cu', u'In12.Cu', u'In13.Cu', u'In14.Cu', u'In15.Cu', u'In16.Cu', u'In17.Cu', u'In18.Cu', u'In19.Cu', u'In20.Cu', u'In21.Cu', u'In22.Cu', u'In23.Cu', u'In24.Cu', u'In25.Cu', u'In26.Cu', u'In27.Cu', u'In28.Cu', u'In29.Cu', u'In30.Cu', u'bottom_copper', u'B.Adhes', u'F.Adhes', u'B.Paste', u'F.Paste', u'B.SilkS', u'F.SilkS', u'B.Mask', u'F.Mask', u'Dwgs.User', u'Cmts.User', u'Eco1.User', u'Eco2.User', u'Edge.Cuts', u'Margin', u'B.CrtYd', u'F.CrtYd', u'B.Fab', u'F.Fab', u'Rescue', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!', u'BAD INDEX!'])
        
if __name__ == '__main__':
    unittest.main()
   