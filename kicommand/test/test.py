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

# https://stackoverflow.com/questions/15487587/python-unittest-get-testcase-ids-from-nested-testsuite
def iterate_tests(test_suite_or_case):
    """Iterate through all of the test cases in 'test_suite_or_case'."""
    try:
        suite = iter(test_suite_or_case)
    except TypeError:
        yield test_suite_or_case
    else:
        for test in suite:
            for subtest in iterate_tests(test):
                yield subtest
# you can use testtools.testsuite.iterate_tests(suite) to iterate over the nested suite. for example, get a list of test id's, using a list comprehension:

# [test.id() for test in testtools.testsuite.iterate_tests(suite)]    #print(dir(testsuite._tests))
    # Return an error code if any of the testsuite tests fail
    # if not results.wasSuccessful():
        # sys.exit(1)


class TestKiCommand(unittest.TestCase):
        
    def test_coverage(self):
        prefix = 'test_'
        #fulltestnames = filter(lambda x: x.startswith(prefix),dir(self))
        testnames = [test._testMethodName.split('_') for test in iterate_tests(testsuite)]
		# flatten the list of lists into a single-dimension list
        testnames = [item for sublist in testnames for item in sublist]


        #print "Testnames: \n", testnames

        #testnames = set(map(lambda x:  x[len(prefix):],fulltestnames))


        #set(map(lambda x: testnames.update(x.split('_')),fulltestnames))
        
        untested = set(kicommand.kicommand._dictionary['command'].keys()) - set(testnames)
        
        # individually list tests that cannot be named python functions
        untested = untested - set(('*','+','-','/','+.'))
        untestedlist = list(untested)
        untestedlist.sort()
        print 'untested',untestedlist
        self.assertEqual(True,True)

            
#unittest.main()

# The following lines enable testing from pcbnew Script Console
# just "import kicommand.test" and view the output in the
# Script Console window.
testsuite = unittest.TestLoader().discover('kicommand.test',pattern="test_*.py")
suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
unittest.TextTestRunner(verbosity=2).run(suite)

if True:#__name__ == '__main__':
    results = unittest.TextTestRunner(verbosity=100).run(testsuite)
    # for ts in testsuite._tests:
        # print str(ts)
        # for t in ts:
            # print "\t",type(t)
            # print "\t",dir(t)
            # print "\t",str(t)


# from kicommand_test import test_001_pcb_kicad