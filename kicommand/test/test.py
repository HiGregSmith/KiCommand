#import unittest
import kicommand 
#.run as kc
import platform
import sys

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

if True:#__name__ == '__main__':
    testsuite = unittest.TestLoader().discover('kicommand.test',pattern="test_*.py")
    results = unittest.TextTestRunner(verbosity=100).run(testsuite)

    # Return an error code if any of the testsuite tests fail
    # if not results.wasSuccessful():
        # sys.exit(1)

class TestKiCommand(unittest.TestCase):
    def test_load(self):
        pcommands = ['moduletextobj', 'wxpoint', 'outlinetoptext', 'setselect', 'referencetextobj', 'outlinepads', 'valuetextobj', 'drawparams', 'textfromobj', 'referencetext', 'toptextobj', 'outlinetext', 'clearallselected', 'not', 'orthogonal', 'copy', 'clearselect', 'texttosegments', 'valuetext']
        self.assertTrue(set(pcommands) <= set(kicommand.kicommand._dictionary['persist'].keys()))
        self.assertFalse(set(['thiscommand doesnt exist']) < set(kicommand.kicommand._dictionary['persist'].keys()))

    def test_drawsegments(self):
        result = kicommand.run('clear 0,0,1,1 mm drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0]),1)
        # Test single list of list of numbers:
        result = kicommand.run('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kicommand.run('clear 0,0,1,1 mm list drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        result = kicommand.run('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        # Test single list of numbers:
        result = kicommand.run('clear 0,0,1,1,2,2,3,3 mm list drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kicommand.run('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        # Test two lists of numbers:
        result = kicommand.run('clear 0,0,1,1 mm list 2,2,3,3 mm list append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        self.assertEqual(len(result[0][1]),1)
        result = kicommand.run('copy 1 index remove 0 index remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kicommand.run('clear 0,0,1000000,1000000 ,2000000,2000000,3000000,3000000 append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kicommand.run('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kicommand.run('clear 0,0,1000000,1000000,2000000,2000000,3000000,3000000 drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kicommand.run('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kicommand.run('clear 0,0,1000000,1000000 list 2000000,2000000,3000000,3000000 list append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        self.assertEqual(len(result[0][1]),1)
        result = kicommand.run('copy 1 index remove 0 index remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kicommand.run('clear 0,0 mm wxpoint 1,1 mm wxpoint append 2,2 mm wxpoint append 3,3 mm wxpoint append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),3)
        result = kicommand.run('delist remove',returnval=-1)
        self.assertEqual(result,[])
        
        result = kicommand.run('clear 0,0 mm wxpoint 1,1 mm wxpoint append list 2,2 mm wxpoint 3,3 mm wxpoint append list append drawsegments',returnval=-1)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0][0]),1)
        self.assertEqual(len(result[0][1]),1)
        result = kicommand.run('copy 1 index remove 0 index remove',returnval=-1)
        self.assertEqual(result,[])
        
    # def test_testcoverage(self):
        # prefix = 'test_'
        # testnames = filter(lambda x: x.startswith(prefix),dir(self))
        # testnames = set(map(lambda x:  x[len(prefix):],testnames))
        # untested = set(kicommand._dictionary['command'].keys()) - testnames
        # print 'untested',untested

            
#unittest.main()

# The following lines enable testing from pcbnew Script Console
# just "import kicommand_test" and you can view the output in the
# Script Console window.
suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
unittest.TextTestRunner(verbosity=2).run(suite)

# from kicommand_test import test_001_pcb_kicad