import unittest

class TestQAWorks(unittest.TestCase):

    def setUp(self):
        self.pcb = None

    def test_asserttrue( self ):
        self.assertTrue( True )

    def test_assertequal( self ):
        self.assertEqual(2, 1+1)


if __name__ == '__main__':
    unittest.main()
   