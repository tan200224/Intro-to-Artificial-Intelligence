import unittest
import test_sokoban
import test_sliding

if __name__ == '__main__':
    slidingSuite = test_sliding.suite()
    sokobanSuite = test_sokoban.suite()
    #suite = unittest.TestSuite([slidingSuite])
    suite = unittest.TestSuite([slidingSuite, sokobanSuite])
    unittest.TextTestRunner().run(suite)
