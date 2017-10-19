from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from accessible_text_color.views import main_view
# Create your tests here.


class MainViewTests(TestCase):

    def test_root_view_resolves_to_main_view_func(self):
        found = resolve('/')
        self.assertEqual(found.func, main_view)

    def test_landing_page_returns_correct_html(self):
        request = HttpRequest()
        response = main_view(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>WCAG Color Calculator</title>', html)
        self.assertTrue(html.endswith('</html>'))
