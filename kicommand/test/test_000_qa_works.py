import unittest

class TestQAWorks(unittest.TestCase):

    def setUp(self):
        self.pcb = None

    def test_asserttrue( self ):
        self.assertTrue( True )

    def test_assertfalse( self ):
        self.assertFalse( False )

    def test_assertIsNone( self ):
        self.assertIsNone( None )

    def test_assertIsNotNone( self ):
        self.assertIsNotNone( 1 )

    def test_assertfalse( self ):
        self.assertFalse( False )

    def test_assertequal( self ):
        self.assertEqual(2, 1+1)


if __name__ == '__main__':
    unittest.main()
   