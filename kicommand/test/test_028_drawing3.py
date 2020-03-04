import os, sys
import unittest
from kicommand.kicommand import kc
import pcbnew

KICAD_INSTALL = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))


class TestDrawing3(unittest.TestCase):
    '''test various commands against one of the demo boards.
    if the demo board changes, some of these will fail.
    '''
# Query
# 'zones', 'tocommand', 'matchreference',  
# 'notselected', 'onlayers',
# 'keepouts',    'getboard', 'getpads', 'areacorners',
# 'areas', 'connected',
# 'corners', 'angle',
# 'deselect',  

    def test_areas_areacorners_findnet_getnetcode_gettracksinnet_areas_areacorners_findnet_getnetcode_gettracksinnet_referencetext_filterrefregex_getpads_netnames_regex_filter_filterrefregex_getreftext_iset(self):
        # self.maxDiff = None
        demodirectory = os.path.join(KICAD_INSTALL,'share','kicad','demos')
        # # demoboards = []
        # # for root, dirs, files in os.walk(demodirectory):
            # # demoboards.extend([os.path.join(root,file) for file in files if file.endswith('.kicad_pcb')])
            
        #demoboard = os.path.join(demodirectory,r'complex_hierarchy','complex_hierarchy.kicad_pcb')
        demoboard = os.path.join(demodirectory,r'kit-dev-coldfire-xilinx_5213',r'kit-dev-coldfire-xilinx_5213.kicad_pcb')
        load = kc('clear "%s" loadboard'%demoboard)
        # self.assertEqual(kc('areas'),[False])
        # self.assertEqual(kc('zones'),[False])
        # self.assertEqual(kc('keepouts'),[False])
        
        self.assertEqual(kc('clear areas areacorners copy x attr. swap y attr. swap zip2'),
        [([146050000, 60960000, 60960000, 64135000, 64135000, 74930000, 74930000, 146050000], [227965000, 227965000, 215900000, 215900000, 105410000, 105410000, 72390000, 72390000]), ([146685000, 146050000, 56515000, 56515000, 74930000, 74930000, 71120000, 71120000], [71755000, 227330000, 227330000, 97155000, 97155000, 79375000, 79375000, 71755000]), ([56300000, 56300000, 146700000, 146700000, 146400000], [71700000, 228200000, 228200000, 71700000, 71700000])])
        
        self.assertEqual(kc('clear areas corners'),
        [(72390000, 60960000, 227965001, 60960000, 227965001, 146050001, 72390000, 146050001, 72390000, 60960000), (71755000, 56515000, 227330001, 56515000, 227330001, 146685001, 71755000, 146685001, 71755000, 56515000), (71700000, 56300000, 228200001, 56300000, 228200001, 146700001, 71700000, 146700001, 71700000, 56300000)] )

        # round the total length to 100nm just to keep minor differences from causing an error.
        self.assertEqual(kc('/TCLK findnet getnetcode gettracksinnet length sum -2 roundn int'),[86261600]);
 
        self.assertEqual(kc('modules referencetext iset'),
        set([u'ABRT_SW1', u'C38', u'C35', u'C34', u'C36', u'C31', 
        u'C30', u'C33', u'C32', u'VX_EN1', u'R38', u'R34', u'R35', 
        u'R36', u'R30', u'R31', u'R32', u'VREF1', u'C22', u'C23', 
        u'C20', u'C21', u'C26', u'C27', u'C24', u'C25', u'C28', 
        u'LED_EN1', u'R8', u'R9', u'TA-1', u'J1', u'BDM_PORT1', 
        u'C57', u'C56', u'C55', u'C54', u'C53', u'U8', u'C51', 
        u'P3', u'U5', u'U4', u'U7', u'U1', u'U3', u'C58', u'R16', 
        u'R17', u'RED1', u'R15', u'R12', u'R13', u'R10', u'R11', 
        u'UARTCAN2', u'R18', u'R19', u'CAN_TERM1', u'C44', u'C45', 
        u'C46', u'P1', u'C40', u'C41', u'P4', u'C43', u'UART_EN2', 
        u'UART_EN0', u'BDM_EN1', u'R63', u'R62', u'R64', u'RS1', 
        u'CLK1', u'FB1', u'RCAN1', u'RCAN2', u'U9', u'LEDABRT1', 
        u'CAN_EN1', u'C52', u'TB1', u'C9', u'C8', u'CLKOUT1', 
        u'C3', u'C2', u'C1', u'C7', u'C6', u'C5', u'C4', u'VR1', 
        u'MCU_PORT1', u'C60', u'C61', u'C59', u'U2', u'F1', 
        u'CT1', u'R1', u'R45', u'R47', u'R46', u'SW1', u'VDDA1', 
        u'UARTCAN1', u'R33', u'R49', u'R48', u'Q1', u'R4', u'R7', 
        u'R5', u'R6', u'C18', u'C12', u'C11', u'C10', u'C17', 
        u'C16', u'C15', u'C14', u'RST_SW1', u'LV1', u'R2', 
        u'COM_SEL2', u'COM_SEL3', u'R53', u'R50', u'COM_SEL1', 
        u'R57', u'SW_ONOFF1', u'LED1', u'LED3', u'LED2', u'LED5', 
        u'LED4', u'GND1', u'R28', u'R14', u'CLK0', u'L2', 
        u'UART_EN1', u'L1', u'UARTCAN0', u'SW2', u'PULUPEN1', 
        u'ALLPST1', u'R22', u'R26', u'D8', u'D9', u'Y1', u'D7', 
        u'R25', u'R20', u'R23', u'D3', u'R21', u'D1']) 
        )
 
 
        self.assertEqual(kc('modules C3.* filterrefregex getreftext iset'),
        set([u'C35', u'C38', u'C3', u'C34', u'C36', u'C31', u'C30', u'C33', u'C32'])
        )
        # areas areacorners findnet getnetcode gettracksinnet referencetext filterrefregex getpads netnames regex filter filterrefregex getreftext iset
        self.assertEqual(kc('netnames copy /AN.* regex filter iset'),
        set([u'/AN2', u'/AN3', u'/AN0', u'/AN1', u'/AN6', u'/AN7', u'/AN4', u'/AN5']) 
        )
        self.assertEqual(kc('modules R8 filterrefregex getpads GetCenter call flatlist'),
        [170627000, 117094000, 168717000, 117094000])
        
        self.assertEqual(kc('netclassmap Default sindex GetName,GetDescription,GetClearance,GetTrackWidth,GetViaDiameter,GetViaDrill,GetuViaDiameter,GetuViaDrill,GetDiffPairWidth,GetDiffPairGap split call'),
        [u'Default', u'Ceci est la Netclass par d\xe9faut', 150000, 200000, 600000, 400000, 300000, 100000, 200000, 250000] 
        )

        #self.assertEqual(kc('angle'),[False])
        #self.assertEqual(kc('matchreference'),[False])
        #self.assertEqual(kc('deselect'),[False])
        #self.assertEqual(kc('notselected'),[False])
        #self.assertEqual(kc('connected'),[False])
        #self.assertEqual(kc('onlayers'),[False])
        #self.assertEqual(kc('getpads'),[False])
        
        # moduleelements    
        
        # getnetcodefromname
        # setnetcode        
        # setnetname        
        # netnames          
        # netnamemap        
        # netcodemap        
        # netcount          
        # getnetcode        
        # getnetname        
        # getnetclass       
        # getnetclassname   
        # getnetinfo        
        # setclass          
        # syncnetclasses    
        # maptodict         
        # netclassmap       
        # getnetclassname   
        # findnet           
        # gettracksinnet    
        # settracknetcode   


        
if __name__ == '__main__':
    unittest.main()
   