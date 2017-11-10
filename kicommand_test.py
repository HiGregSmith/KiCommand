import unittest
import kicommand

class TestKiCommand(unittest.TestCase):
    def test_load(self):
        pcommands = ['moduletextobj', 'wxpoint', 'outlinetoptext', 'setselect', 'referencetextobj', 'outlinepads', 'valuetextobj', 'drawparams', 'textfromobj', 'referencetext', 'toptextobj', 'outlinetext', 'clearallselected', 'not', 'orthogonal', 'copy', 'clearselect', 'texttosegments', 'valuetext']
        self.assertTrue(set(pcommands) <= set(kicommand._dictionary['persist'].keys()))
        self.assertFalse(set(['thiscommand doesnt exist']) < set(kicommand._dictionary['persist'].keys()))
        

#unittest.main()

# The following lines enable testing from pcbnew Script Console
# just "import kicommand_test" and you can view the output in the
# Script Console window.
suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
unittest.TextTestRunner(verbosity=2).run(suite)