"""Temp test"""

import unittest


class MyTest(unittest.TestCase):
    """Create class for Mytest"""

    def test_addition(self) -> None:
        """test"""
        self.assertEqual(2 + 2, 4)

    def test_subtraction(self) -> None:
        """test"""
        self.assertEqual(5 - 3, 2)


if __name__ == "__main__":
    unittest.main()
