import unittest
from ..lib.langton import LangtonSimulate

class TestLangton(unittest.TestCase):

    def test_386(self):
        lang = LangtonSimulate()
        self.assertEqual( lang.num_black(386), 60 )

    def test_negative_steps(self):
        lang = LangtonSimulate()
        with self.assertRaises(ValueError):
            lang.num_black(-3)

    def test_ant_off_grid(self):
        with self.assertRaises(IndexError):
            LangtonSimulate(10, 10000)

if __name__ == '__main__':
    unittest.main()
