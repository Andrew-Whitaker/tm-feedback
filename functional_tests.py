from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visit_home_page(self):
        # User arrives at website
        self.browser.get('http://localhost:8000')

        # User notices the page title
        self.assertIn('TM Feedback', self.browser.title)


if __name__=='__main__':
    unittest.main(warnings='ignore')


