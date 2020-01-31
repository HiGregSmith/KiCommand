import code
import unittest
import os
import pcbnew
import pdb
import tempfile
from kicommand import run as kc


from pcbnew import *


BACK_COPPER = 'Back_Copper'
B_CU = 'B.Cu'
NEW_NAME = 'My_Fancy_Layer_Name'
KICAD_INSTALL = r'C:\Program Files\KiCad'

class TestBoardClass(unittest.TestCase):

    def setUp(self):
        file = os.path.join(KICAD_INSTALL,r'share\kicad\demos\complex_hierarchy\complex_hierarchy.kicad_pcb')
        self.pcb = kc(
            'clear pcbnew list "%s" list list LoadBoard callargs '
            'delist Board spush board'%file)
        #self.pcb = LoadBoard("data/complex_hierarchy.kicad_pcb")
        self.TITLE="Test Board"
        self.COMMENT1="For load/save test"
        self.FILENAME=tempfile.mktemp()+".kicad_pcb"

    def test_pcb_find_module(self):
        reference = kc('board list P1 list list FindModule callargs GetReference call delist')
        self.assertEqual(reference,'P1')
        # module = self.pcb.FindModule('P1')
        # self.assertEqual(module.GetReference(),'P1')

    def test_pcb_get_track_count(self):
    # :persist newboard "Elements Create a new empty board and make it the current board." pcbnew list BOARD call delist Board spush ;
    # : newtrack "Elements Create bare, undefined track on current board" pcbnew list board list list TRACK callargs board list swap list Add callargs ;
    
        # new board
        pcb = kc('clear pcbnew list BOARD call delist Board spush board')

        num = kc('list GetNumSegmTrack call delist')
        self.assertEqual(num,0)
        
        # Creates a new track
        kc('clear pcbnew list board list list TRACK callargs')
        
        # Adds track to Board
        kc('Board scopy list swap list Add callargs')
        
        # Obtain the number of tracks on this board 
        num = kc('board list GetNumSegmTrack call delist')
        self.assertEqual(num,1)

        #kc(':persist newadd "Elements [TYPE PARENT] Add create a element of TYPE (TRACK, PAD) and add it to the PARENT." pcbnew list swap board list list swap stack')
        # Creates a new track
        # Adds track to Board
        kc('clear pcbnew list board list list TRACK callargs')
        kc('board list swap list Add callargs')
        num = kc('board list GetNumSegmTrack call delist')
        self.assertEqual(num,2)

        # pcb = BOARD()

        # self.assertEqual(pcb.GetNumSegmTrack(),0)

        # track0 = TRACK(pcb)
        # pcb.Add(track0)
        # self.assertEqual(pcb.GetNumSegmTrack(),1)

        # track1 = TRACK(pcb)
        # pcb.Add(track1)
        # self.assertEqual(pcb.GetNumSegmTrack(),2)

    def test_pcb_bounding_box(self):
        kc(':persist newboard "Elements Create a new empty board and make it the current board." pcbnew list BOARD call delist Board spush ;')
        # create new board
        pcb = kc('clear newboard board')
        # put one track on it (front copper trace 0.5mm thickness from 10,10 to 20,30)
        track = kc('clear 0.5 mm t param F.Cu l param 10,10,20,30 mm '
                        'drawpoly delist delist')

        # 5.3.3 note: Bounding Box no longer includes clearance value
        # wval, hval = kc('list GetClearance call '
                        # 'copy concat copy 30,-10,0.5 mm concat sum swap '
                        # '20,-10,0.5 mm concat sum',returnval=-1)
        wval, hval = kc('clear 0 float list '
                        'copy concat copy 30,-10,0.5 mm concat sum swap '
                        '20,-10,0.5 mm concat sum',returnval=-1)
                        
        #             float is because integer doesn't compare to float in assertAlmostEqual----+
        #             ilist is to create a list from the wxRect---------------------------+     |         
        #             copy is to keep bb reference in memory----------v                   v     v
        height, width = kc('board list ComputeBoundingBox call GetSize call delist ilist float')
        
        #height, width = bounding_box.GetSize()
        self.assertAlmostEqual(ToMM(height), ToMM(hval), 2)
        self.assertAlmostEqual(ToMM(width ), ToMM(wval), 2)

        # pcb = BOARD()
        # track = TRACK(pcb)
        # pcb.Add(track)

        # track.SetStartEnd(wxPointMM(10.0, 10.0),
                         # wxPointMM(20.0, 30.0))
        
        # track.SetStart(wxPointMM(10.0, 10.0))
        # track.SetEnd  (wxPointMM(20.0, 30.0))

        # track.SetWidth(FromMM(0.5))

        #!!! THIS FAILS? == 0.0 x 0.0 ??
        height, width = ToMM(pcb.ComputeBoundingBox().GetSize())
        # bounding_box = pcb.ComputeBoundingBox()
        # height, width = ToMM(bounding_box.GetSize())

        clearance = ToMM(track.GetClearance()*2)
        # 5.3.3 note: Size, like Bounding Box, no longer includes clearance value
        clearance = 0
        self.assertAlmostEqual(width,  (30-10) + 0.5 + clearance, 2)
        self.assertAlmostEqual(height, (20-10) + 0.5 + clearance, 2)

    def test_pcb_get_pad(self):
        pcb = kc('newboard board')
        # pcb = BOARD()

        # add a new (empty) module/footprint
        module = kc('MODULE swap newadd')
        #MODULE board list copy pcbnew list swap list 3 pick callargs 1 pick 1 pick list Add callargs pop swap pop swap pop delist
        # module = MODULE(pcb)
        # pcb.Add(module)
        
        # add a new pad
        pad = kc('D_PAD swap newadd') 
        
        #pad = D_PAD(module)
        #kc('list list Add callargs pop pop')
        #module.Add(pad)
# newboard board MODULE swap newadd delist D_PAD swap newadd delist
        try:
            pad.SetShape(PAD_SHAPE_OVAL) # 5.x nightly
        except:
            pad.SetShape(PAD_OVAL) # 4.0.7
        pad.SetSize(wxSizeMM(2.0, 3.0))
        pad.SetPosition(wxPointMM(0,0))
        
        # easy case
        p1 = pcb.GetPad(wxPointMM(0,0))

        # top side. Pad is centered on 0,0 and with 2mm width. This should grab the pad.
        p2 = pcb.GetPad(wxPointMM(0.9,0.0))

        # bottom side. Pad is centered on 0,0 and with 3mm height. This should grab the pad.
        p3 = pcb.GetPad(wxPointMM(0,1.4))

        # TODO: get pad == p1 evaluated as true instead
        #       of relying in the internal C++ object pointer
        self.assertIsNotNone(p1,msg="Pad not found from center point")
        self.assertEqual(pad.this, p1.this)
        # self.assertIsNotNone(p2,msg="Pad not found from left point")
        # self.assertEqual(pad.this, p2.this)
        # self.assertIsNotNone(p3,msg="Pad not found from bottom point")
        # self.assertEqual(pad.this, p3.this)

    def test_pcb_save_and_load(self):
        pcb = BOARD()
        pcb.GetTitleBlock().SetTitle(self.TITLE)
        pcb.GetTitleBlock().SetComment1(self.COMMENT1)
        result = SaveBoard(self.FILENAME,pcb)
        self.assertTrue(result)
        
        pcb2 = LoadBoard(self.FILENAME)
        self.assertNotEqual(pcb2,None)

        tb = pcb2.GetTitleBlock()
        self.assertEqual(tb.GetTitle(),self.TITLE)
        self.assertEqual(tb.GetComment1(),self.COMMENT1)

        os.remove(self.FILENAME)

    def test_pcb_layer_name_set_get(self):
        pcb = kc('newboard board list 31 int list %s list concat list SetLayerName callargs board'%BACK_COPPER)
        # pcb = BOARD()
        # pcb.SetLayerName(31, BACK_COPPER)
        self.assertEqual(pcb.GetLayerName(31), BACK_COPPER)

    def test_pcb_layer_name_set_get2(self):
        pcb = BOARD()
        pcb.SetLayerName(31, BACK_COPPER)
        self.assertEqual(pcb.GetLayerName(31), BACK_COPPER)

    def test_pcb_layer_id_get(self):
        # pcb = BOARD()
        pcb = kc('newboard board')
        b_cu_id = kc('%s layernums delist'%B_CU)

        #b_cu_id = pcb.GetLayerID(B_CU)
        #pcb.SetLayerName(b_cu_id, NEW_NAME)
        kc('%d,%s'%(b_cu_id,NEW_NAME))
        kc('board list swap int list SetLayerName callargs pop')

        # ensure we can get the ID for the new name
        self.assertEqual(pcb.GetLayerID(NEW_NAME), b_cu_id)

        # ensure we can get to the ID via the STD name too
        self.assertEqual(pcb.GetLayerID(B_CU), b_cu_id)

    #def test_interactive(self):
    # 	code.interact(local=locals())

if __name__ == '__main__':
    unittest.main()
