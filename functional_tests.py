from unittest import TestCase, main

from selenium import webdriver


class NewVisitorTest(TestCase):
    """Test that page loads correctly with correct content"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_a_color_into_form(self):
        # As an unauthenticated user I can load the page
        self.browser.get('http://localhost:8000')

        # I see the page title is "WCAG Text Color Calculator"
        self.assertEqual(self.browser.title, 'WCAG Color Calculator')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('WCAG Color Calculator', header_text)

        # I see a form where I can enter a background color
        color_selector = self.browser.find_element_by_css_selector(
            '#bg-color')
        self.assertEqual(color_selector.get_attribute('placeholder'),
                         '#ffffff')

        self.fail('Finish the tests')


if __name__ == '__main__':
    main()
