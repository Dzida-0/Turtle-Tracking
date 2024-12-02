import unittest


class TestDataParsing(unittest.TestCase):
    # Test for remove_HTML_element function
    def test_remove_HTML_elements(self):
        self.assertEqual(test_remove_HTML_elements("Text Test Text"), "Text Test Text")
        self.assertEqual(test_remove_HTML_elements("<p>Text</p>"), "Text")
        self.assertEqual(test_remove_HTML_elements("<h1><p>Text</p></h1>"), "Text")
        self.assertEqual(test_remove_HTML_elements("&nbsp;<h1><p>Text</p>&nbsp;</h1>"), "Text")
        self.assertEqual(test_remove_HTML_elements("Test&nbsp;<h1><p>Text</p>&nbsp;</h1>Test"), "Test Text Test")
        self.assertEqual(
            test_remove_HTML_elements("Test&nbsp;<h1><p>Text</p>&nbsp;</h1>Test<p>Text</p>"),"Test Text Test Text")
        # add assertion here


if __name__ == '__main__':
    unittest.main()
