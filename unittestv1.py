def cube(n):
    return n ** 2

import unittest

class myTest(unittest.TestCase):
    def test1(self):
        self.assertEqual( cube(5), 25 )

unittest.main()