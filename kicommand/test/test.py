from __future__ import print_function

#import unittest
import kicommand 
#from kicommand.kicommand import kc
from kicommand.kicommand import kc
import platform
import os,sys
import pcbnew

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

KICAD_INSTALL = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))

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

    
def gettests():
    global testsuite,fullsuite
    testsuite = unittest.TestLoader().discover('kicommand.test',pattern="test_*.py")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
    fromfile = unittest.TestLoader().loadTestsFromTestCase(TestsFromFile)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    fullsuite = unittest.TestSuite((suite,testsuite,fromfile))


# kicommand.test.runtests_singly()

def runtests_singly():
    gettests()
    for t in kicommand.test.iterate_tests(kicommand.test.fullsuite):
        unittest.TextTestRunner(verbosity=100).run(t)
def runtests():
    global testsuite,fullsuite
    gettests()
    results = unittest.TextTestRunner(verbosity=100).run(fullsuite)

# import pickle

# def writetestsfile(tests):
    # kicommand_config = os.path.join(pcbnew.GetKicadConfigPath(),'kicommand')
    # if not os.path.exists(kicommand_config):
        # os.mkdir(kicommand_config)
    # testsfile = os.path.join(os.path.dirname(__file__),'tests.txt')
    # teststempfile = os.path.join(kicommand_config,'tests.txt')

def createtestsfile(tests=None):
    testsfile = os.path.join(os.path.dirname(__file__),'tests.txt')
    kicommand_config = os.path.join(pcbnew.GetKicadConfigPath(),'kicommand')
    #print('dirpath: ',', '.join(dir(os.path)))
    #print('Config exists? ',os.path.exists(kicommand_config))
    if not os.path.exists(kicommand_config):
        os.mkdir(kicommand_config)
    
    teststempfile = os.path.join(kicommand_config,'tests.txt')
    #if os.exists(kicommand_config):
    
    # structure of dictionary
    # {'testid':('description','command string',expected_result), ...}
    # Execute in testid order
    # strings and results
    if tests is None:
        tests = {
            '00010':('single value','0','0','')
            ,'00020':('int','0 int',0,'int')
            ,'00030':('int single-value list','0 int list',[0],'int list')
            ,'00040':('int list','0,1 int',[0,1],'int')
            ,'00050':('string list','0,1 split',['0','1'],'split')
            ,'00060':('raw string','0\n1',r'0\n1','')
            ,'00070':('encoded','0\n1 encoded','0\n1','encoded')
            }
    # with open(teststempfile, "wb") as fp:   #Pickling
        # pickle.dump(tests, fp)
    
    # with open(teststempfile,'r') as f:
           # tests = eval(f.read())
           
   # print tests structure in a way that eval() works and is easy to hand edit.
    with open(teststempfile,'w') as f:
        f.write("""# TESTID:['Short Description',r'input to kc()','expected result top of stack','commands tested'(optional)]
# Place "None" (without quotes) as the expected result to auto-generate result.
# After running, the actual result file can be coped over the golden test results.
# All tests should be independent and leave only one item on the stack.

""")
        f.write('{\n')
        for testid,testitem in sorted(tests.iteritems(), key = lambda (k, v) : k):
            f.write(_get_testitem_string(testid,testitem))
            # f.write('{}:[{},\n        r{},\n        {}\n        ],\n\n'.format(
                # *[repr(x) for x in [testid,testitem[0],testitem[1],testitem[2]]]))
        f.write('}')
    #with open(testsfile, "rb") as fp:   # Unpickling
    #    tests = pickle.load(fp)
    return teststempfile
    
# https://stackoverflow.com/a/2799009
class TestsFromFile(unittest.TestCase):
    pass

def create_test_method(testid,testitem):
    def test_method(self):
        self.assertEqual(kc('clear '+testitem[1]),testitem[2])
    return test_method

_test_golden_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'tests.txt'))
with open(_test_golden_file,'r') as f:
    testdict = eval(f.read())

msgmaxlen = 0
_tests_updated = False

def _get_testitem_string(testid,testitem):
    return '{}:[{},\n        {},\n        {},\n        {}\n        ],\n\n'.format(
        *[repr(x) for x in [testid,testitem[0],testitem[1],testitem[2],testitem[3]]])

for testid,testitem in testdict.iteritems():
    msgmaxlen = max(msgmaxlen,len(testitem[0]))
    # Update testitem result if current result is None
    if testitem[2] is None:
        testdict[testid][2] = kc(testitem[1])
        print( '# Manually verify result:\n',_get_testitem_string(testid,testitem))

        _tests_updated = True

if _tests_updated:
   tempfilename = createtestsfile(tests=testdict)
   print('#Test results have been updated. If all tests succeed, copy the new file\n{}\n#over the golden copy in\n{}\n'.format(tempfilename,_test_golden_file))
        
for testid,testitem in sorted(testdict.iteritems(), key=lambda (k,v):k):
    test_method = create_test_method (testid,testitem)
    test_method.__name__ = 'test_{1} {2:<{0}}'.format(msgmaxlen,testid,testitem[0])
    if len(testitem)>3:
        setattr(test_method,'_commandstested',testitem[3])
    setattr (TestsFromFile, test_method.__name__, test_method)

    
    
class TestsFromFile2(unittest.TestCase):
    # iterator=None
    # testdict = None
    # def __iter__(self):
        # # if not self.iterator:
            # # self.iterator = iter([test_DontSkip])
            # # yield self.iterator.next()
        # # return
        # if self.testdict is None:
            # with open(os.path.join(os.path.dirname(__file__),'tests.txt'),'r') as f:
                # self.testdict = eval(f.read())
                
        # for testid,testitem in sorted(testdict.iteritems(), key=lambda (k,v):k):
            # yield lambda x: self.singletest(testid,testitem)
        # return iter([self.test_TestsFromFile])
        
    # def savetests(self):
        # testsfile = os.path.join(os.path.dirname(__file__),'tests.txt')
        # with open(testsfile, "rb") as fp:   # Unpickling
            # tests = pickle.load(fp)
            
        # for testid,testitem in sorted(tests.iteritems(), key = lambda (k, v) : k):
            # print("Test: {}, {}".format(testid,testitem[0]))
            # self.AssertEqual(kc(testitem[1]),testitem[2])

# C:\Program Files\KiCad\share\kicad\scripting\plugins\kicommand\test

    def singletest(self,testid,testitem):
        print("Test: {} - {}\n    String: {}\n    Expect: {}".format(testid,testitem[0],testitem[1],testitem[2]))
        self.assertEqual(kc(testitem[1]),testitem[2],)
    def test_DontSkip(self):
        self.assertEqual(kc('1'),'1')
    def test_ShouldSkip(self):
        self.assertEqual(kc('0'),'0')
    # def test_TestsFromFile(self):
        # testsfile = os.path.join(os.path.dirname(__file__),'tests.txt')
        # print("Reading tests from", testsfile)
        # with open(testsfile,'r') as f:
           # testdict = eval(f.read())

        # for testid,testitem in sorted(testdict.iteritems(), key=lambda (k,v):k):
            # print("Test: {} - {}\n    String: {}\n    Expect: {}".format(testid,testitem[0],testitem[1],testitem[2]))
            # self.assertEqual(kc(testitem[1]),testitem[2],)
            
class TestKiCommand(unittest.TestCase):
    def get_tested_commands(self,suite):
        testedcommandsunderscore = [getattr(test, '_commandstested','a').replace(' ','_') for test in iterate_tests(fullsuite)]
        #method = getattr(self,test._testMethodName)
        ctested = [getattr(getattr(test,test._testMethodName), '_commandstested',test._testMethodName).replace(' ','_') for test in iterate_tests(fullsuite)]
        #print('ctested',ctested)
        
        # testedcommandsunderscore = [getattr(test, '_testMethodName').replace(' ','_') for test in iterate_tests(fullsuite)]
        testedcommandsarray = [c.split('_') for c in ctested if c is not '']
        testedcommands = [name for names in testedcommandsarray for name in names]
        #print('tested',testedcommands)
        #dircommand = [dir(test) for test in iterate_tests(fullsuite)]
        return testedcommands
        # print('dir',dircommand)
        # testedcommandsunderscore = [getattr(test, '_commandstested',test._testMethodName).replace(' ','_') for test in iterate_tests(fullsuite)]
        # testedcommands = [c.split('_') for c in testedcommandsunderscore]
        #testedcommands = [test._testMethodName.split('_') for test in iterate_tests(fullsuite) ]
        #print('all tested',testedcommands)
    def test_Coverage(self):
        global testsuite,fullsuite
        
        prefix = 'test_'
        #fulltestnames = filter(lambda x: x.startswith(prefix),dir(self))
        #testnames = [test._testMethodName.split('_') for test in iterate_tests(fullsuite)]
		# flatten the list of lists into a single-dimension list
        #testnames = [item for sublist in testnames for item in sublist]
        testnames = self.get_tested_commands(fullsuite)

        #print "Testnames: \n", testnames

        #testnames = set(map(lambda x:  x[len(prefix):],fulltestnames))


        #set(map(lambda x: testnames.update(x.split('_')),fulltestnames))
        
        untested = set(kicommand.kicommand._dictionary['command'].keys())
        untested.update(set(kicommand.kicommand._dictionary['persist'].keys()))
        untested -= set(testnames)
        
        # individually list tests that cannot be named python functions
		# stack, print, and printf are not tested. They don't modify the stack at all, they only print to the output window.

        # The first set are actually tested, but can't be automatically added 
        # because "test" detection is done by parsing function names, and these
        # can't be added as function names.
        # The second set is not specifically tested.
        untested = untested - set(('*','+','-','/','+.','*.','index.','<','=','?','list.','attr.')) - set((':persist',';',':'))
        untestedlist = list(untested)
        untestedlist.sort()
        print('untested',untestedlist)

    def test_SKIP_stack_print_printf_undock(self):
        # Don't really know how to test these
        # because they output directly to KiCommand window.
        pass
#unittest.main()

# The following lines enable testing from pcbnew Script Console
# just "import kicommand.test" and view the output in the
# Script Console window.
runtests()

# testing only TestKiCommand tests
# testsuite = unittest.TestLoader().discover('kicommand.test',pattern="test_*.py")
# suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
# fromfile = unittest.TestLoader().loadTestsFromTestCase(TestsFromFile)
# #unittest.TextTestRunner(verbosity=2).run(suite)
# fullsuite = unittest.TestSuite((suite,testsuite,fromfile))
# runner = unittest.TextTestRunner()
# runner.run(suite)
# end test one -----------

# testsuite = unittest.TestLoader().discover('kicommand.test',pattern="test_*.py")
# suite = unittest.TestLoader().loadTestsFromTestCase(TestKiCommand)
# unittest.TextTestRunner(verbosity=2).run(suite)

# if True:#__name__ == '__main__':
    # results = unittest.TextTestRunner(verbosity=100).run(testsuite)


# from kicommand_test import test_001_pcb_kicad