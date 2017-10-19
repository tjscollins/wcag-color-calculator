from unittest import TestCase, main

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')


class NewVisitorTest(TestCase):
    """Test that page loads correctly with correct content"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_can_enter_a_color_into_form(self):
        # As an unauthenticated user I can load the page
        self.browser.get('http://localhost:8000')

        # I see the page title is "WCAG Text Color Calculator"
        self.assertEqual(self.browser.title, 'WCAG Color Calculator')

        self.fail('Finish the tests')


if __name__ == '__main__':
    main()
