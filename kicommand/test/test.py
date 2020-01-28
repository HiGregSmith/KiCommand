#import unittest
import kicommand 
#.run as kc
from kicommand import run as kc
import platform
import sys
import pcbnew

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
        
    def test_coverage(self):
        prefix = 'test_'
        fulltestnames = filter(lambda x: x.startswith(prefix),dir(self))
        testnames = set()
        #testnames = set(map(lambda x:  x[len(prefix):],fulltestnames))
        set(map(lambda x: testnames.update(x.split('_')),fulltestnames))
        
        untested = set(kicommand.kicommand._dictionary['command'].keys()) - testnames
        
        # individually list tests that cannot be named python functions
        untested = untested - set(('*','+','-','/','+.'))
        print 'untested',untested
        self.assertEqual(True,True)

            
#unittest.main()

# The following lines enable testing from pcbnew Script Console
# just "import kicommand.test" and view the output in the
# Script Console window.
suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
unittest.TextTestRunner(verbosity=2).run(suite)

# from kicommand_test import test_001_pcb_kicad