import os
import code
import unittest
import pdb
from kicommand import run as kc

KICAD_INSTALL = r'C:\Program Files\KiCad'

class TestPCBLoad(unittest.TestCase):
    # for kc command, the entire stack is returned
    def tearDown(self):
        kc('Board spop clear')
    def setUp(self):
        file = os.path.join(KICAD_INSTALL,r'share\kicad\demos\complex_hierarchy\complex_hierarchy.kicad_pcb')
        self.pcb = kc('clear pcbnew list "%s" list list LoadBoard callargs '
            'delist Board spush Board scopy'%file)
        
    def test_pcb_load(self):
    	self.assertNotEqual(self.pcb,None)

    def test_pcb_track_count(self):
    	# self.assertEqual(len(tracks),361)
        
    	#self.assertTrue(kc('clear tracks ilist len list 360 int = delist')[-1])
    	self.assertEqual(kc('clear tracks ilist len'),360)

    def test_pcb_modules(self):
        #self.assertEqual(len(modules), 72)
        
    	self.assertTrue(kc('clear modules ilist len list 68 int = delist'))

    def test_pcb_module_references(self):
            
            
        self.assertTrue(kc(
            'Q1,R4,Q3,Q2,Q5,Q4,Q7,Q6,Q8,U1,U3,U2,R7,C12,C11,C10,C14,R16,'
            'R17,R14,R15,R12,R13,R10,R11,R3,R18,R19,C9,C8,U4,C3,C2,C1,C7,'
            'C6,C5,C4,P2,P3,R6,P1,P6,P4,P5,R28,R8,R9,R23,RV1,R27,R26,R5,R25,'
            'R24,RV2,R20,R22,D8,D9,D6,D7,D4,D5,D2,D3,R21,D1 '
            'split iset list referencetext iset ='))

    	# known_refs = [u'P1', u'P3', u'C2', u'C1', u'D1', u'Q3', u'Q5', u'Q7', 
    				  # u'Q6', u'Q1', u'Q2', u'Q4', u'Q8', u'P2', u'U1', u'U4',
    				  # u'P4', u'P5', u'P6', u'U3', u'R9', u'R15', u'RV1', u'RV2', 
    				  # u'C3', u'C4', u'C5', u'C6', u'C7', u'C8', u'C9', u'D2', 
    				  # u'D3', u'D4', u'D5', u'D6', u'D7', u'R3', u'R4', u'R5', 
    				  # u'R6', u'R7', u'R8', u'R10', u'R11', u'R12', u'R13', 
    				  # u'R14', u'R16', u'R17', u'R18', u'R19', u'R20', u'R21', 
    				  # u'R22', u'MIRE', u'C10', u'C11', 
    				  # u'U2', u'C14', u'C12', u'R23', u'R24', u'D9', u'D8', u'R25', 
    				  # u'R26', u'R27', u'R28']

    	# for ref in known_refs:
    		# self.assertTrue(ref in board_refs)
        # set([u'Q1', u'R4', u'Q3', u'Q2', u'Q5', u'Q4', u'Q7', u'Q6', u'Q8', u'U1', u'U3', u'U2', u'R7', u'C12', u'C11', u'C10', u'C14', u'R16', u'R17', u'R14', u'R15', u'R12', u'R13', u'R10', u'R11', u'R3', u'R18', u'R19', u'C9', u'C8', u'U4', u'C3', u'C2', u'C1', u'C7', u'C6', u'C5', u'C4', u'P2', u'P3', u'R6', u'P1', u'P6',        u'P4', u'P5', u'R28', u'R8', u'R9', u'R23', u'RV1', u'R27', u'R26', u'R5',             u'R25', u'R24', u'RV2', u'R20', u'R22', u'D8',          u'D9', u'D6', u'D7', u'D4', u'D5', u'D2', u'D3', u'R21', u'D1']) 
        # set([u'Q1', u'R4', u'Q3', u'Q2', u'Q5', u'Q4', u'Q7', u'Q6', u'Q8', u'U1', u'U3',        u'R7', u'C12',         u'C10', u'C14', u'R16', u'R17', u'R14', u'R15', u'R12', u'R13', u'R10', u'R11', u'R3', u'R18', u'R19', u'C9', u'C8', u'U4', u'C3', u'C2', u'C1', u'C7', u'C6', u'C5', u'C4', u'P2', u'P3', u'R6', u'P1', u'P6', u'D8', u'P4', u'P5', u'R28', u'R8', u'R9', u'RV2', u'RV1', u'R27', u'R26', u'C11.U2', u'R23', u'R25', u'R24',         u'R20', u'R22', u'MIRE', u'R5', u'D9', u'D6', u'D7', u'D4', u'D5', u'D2', u'D3', u'R21', u'D1'])

        # Check value:
        # P1,P3,C2,C1,D1,Q3,Q5,Q7,Q6,Q1,Q2,Q4,Q8,P2,U1,U4,P4,P5,P6,U3,R9,R15,RV1,RV2,C3,C4,C5,C6,C7,C8,C9,D2,D3,D4,D5,D6,D7,R3,R4,R5,R6,R7,R8,R10,R11,R12,R13,R14,R16,R17,R18,R19,R20,R21,R22,MIRE,C10,C11,U2,C14,C12,R23,R24,D9,D8,R25,R26,R27,R28 split iset
    
    def test_pcb_netcount(self):
        #self.assertTrue(kc('board list GetNetCount call 51 int = delist')[-1])

        self.assertEqual(kc('board list GetNetCount call delist'),53)

    #def test_interactive(self):
    #	code.interact(local=locals())

if __name__ == '__main__':
    unittest.main()
