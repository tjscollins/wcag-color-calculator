import json

from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.http import HttpRequest

from accessible_text_color.views import main_view, post_bgcolor
from accessible_text_color.calculator import Color, TextColorCalculator
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


class BgColorAPITests(TestCase):

    def test_api_bgcolor(self):
        """It should return a list of acceptable text colors for a given
        background color"""

        client = Client()
        data = {
            'color': '#ffffff'
        }
        response = client.post('/api/bg-color', data=data)

        self.assertIsNotNone(response)
        self.assertIs(response.status_code, 200)


class ColorTests(TestCase):

    def test_init_method(self):
        self.assertEqual((171, 205, 239), Color(rgb="#abcdef").rgb)
        self.assertEqual((100, 100, 100), Color(rgb=(100, 100, 100)).rgb)
        self.assertEqual((169, 204, 239), Color(hsl=(210, 68, 80)).rgb)
        self.assertEqual((16, 126, 66), Color(hsl=(147, 77, 28)).rgb)

    def test_rgb_to_hsl(self):
        calculator = Color("#123456")
        self.assertEqual((210, 65, 20),
                         calculator.hsl())

        calculator = Color("#D9832E")
        self.assertEqual((30, 69, 52),
                         calculator.hsl())

        calculator = Color("#107D41")
        self.assertEqual((147, 77, 28),
                         calculator.hsl())

    def test_luminance(self):
        self.assertEqual(0, Color('#000000').luminance())
        self.assertEqual(1, Color('#ffffff').luminance())
        self.assertEqual(0.7152, Color('#00ff00').luminance())
        self.assertEqual(0.2126, Color('#ff0000').luminance())
        self.assertEqual(0.0722, Color('#0000ff').luminance())

    def test_complementary_color(self):
        self.assertEqual(Color(hsl=(180, 100, 50)).rgb,
                         Color(hsl=(0, 100, 50)).complementary_color().rgb)
        self.assertEqual(Color(hsl=(20, 100, 50)).rgb,
                         Color(hsl=(200, 100, 50)).complementary_color().rgb)
        self.assertEqual(Color(hsl=(190, 100, 50)).rgb,
                         Color(hsl=(10, 100, 50)).complementary_color().rgb)

    def test_analogous_colors(self):
        self.assertEqual([Color(hsl=(105, 100, 50)).rgb,
                          Color(hsl=(135, 100, 50)).rgb],
                         list(map(lambda x: getattr(x, 'rgb'),
                                  Color(hsl=(120, 100, 50)).analogous_colors())
                              ))
        self.assertEqual([Color(hsl=(350, 100, 50)).rgb,
                          Color(hsl=(20, 100, 50)).rgb],
                         list(map(lambda x: getattr(x, 'rgb'),
                                  Color(hsl=(5, 100, 50)).analogous_colors())
                              ))
        self.assertEqual([Color(hsl=(165, 100, 50)).rgb,
                          Color(hsl=(195, 100, 50)).rgb],
                         list(map(lambda x: getattr(x, 'rgb'),
                                  Color(hsl=(180, 100, 50)).analogous_colors())
                              ))


class TextColorCalculatorTests(TestCase):

    def test_contrast_calculation(self):
        calculator = TextColorCalculator()

        self.assertAlmostEqual(21,
                               calculator.contrast(Color(rgb="#00000"),
                                                   Color(hsl=(0, 0, 100))))

        self.assertAlmostEqual(5,
                               calculator.contrast(Color(rgb="#cc3922"),
                                                   Color(hsl=(120, 50, 100))))

        self.assertAlmostEqual(1,
                               calculator.contrast(Color(rgb="#ffffff"),
                                                   Color(hsl=(0, 0, 100))))

    def test_AA_textcolors(self):
        bg_color = Color("#ff0000")
        calculator = TextColorCalculator()
        approved_colors = calculator.AA_textcolors(bg_color)

        for color in approved_colors:
            self.assertIsInstance(color, Color)
            self.assertGreaterEqual(calculator.contrast(color, bg_color), 4.5)

    def test_AAA_textcolors(self):
        bg_color = Color("#00ff00")
        calculator = TextColorCalculator()
        approved_colors = calculator.AAA_textcolors(bg_color)

        for color in approved_colors:
            self.assertIsInstance(color, Color)
            self.assertGreaterEqual(calculator.contrast(color, bg_color), 7)
