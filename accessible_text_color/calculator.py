import colorsys
from math import floor


class Color():
    tolerance = 100

    def __init__(self, rgb=None, hsl=None):
        if isinstance(rgb, str):
            self.rgb = self._convert_str_to_rgb(rgb)
        elif isinstance(rgb, (tuple, list)) and len(rgb) is 3:
            self.rgb = tuple(rgb)
        elif rgb is not None:
            raise TypeError(
                'Color constructor expects rgb to be a string, tuple, or None')

        if isinstance(hsl, (tuple, list)):
            self.rgb = self._convert_hsl_to_rgb(hsl)
        elif hsl is not None:
            raise TypeError(
                'Color constructor expects hsl to be a tuple or None')

    def __hash__(self):
        total = sum(self.rgb, 0)
        return hash(floor(total / self.tolerance))

    def __eq__(self, other):
        r, g, b = self.rgb
        x, y, z = other.rgb

        diff = abs(r - x) + abs(g - y) + abs(z - x)

        return diff <= self.tolerance or self.rgb == other.rgb

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        r, g, b = list(map(
            lambda s: hex(s)[2:] if s >= 16 else '0' + hex(s)[2:], self.rgb))
        return '#' + r + g + b

    def _convert_str_to_rgb(self, bg_color):
        return int(bg_color[1:3], 16), int(
            bg_color[3:5], 16), int(bg_color[5:7], 16)

    def _convert_hsl_to_rgb(self, hsl):
        h, s, l = hsl
        r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
        return tuple(map(lambda x: round(x * 255), (r, g, b)))

    def hsl(self):
        r, g, b = map(lambda x: x / 255, self.rgb)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return tuple(map(round, (h * 360, s * 100, l * 100)))

    def luminance(self):
        rgb = list(self.rgb)
        srgb = []
        for n in rgb:
            n /= 255
            n = n / 12.92 if n < 0.03928 else pow((n + 0.055) / 1.055, 2.4)
            srgb.append(n)
        return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2]

    def complementary_color(self):
        h, s, l = self.hsl()
        return Color(hsl=((h + 180) % 360, s, l))

    def analogous_colors(self):
        h, s, l = self.hsl()
        return [Color(hsl=((h + 345) % 360, s, l)),
                Color(hsl=((h + 15) % 360, s, l))]

    def triadic_colors(self):
        h, s, l = self.hsl()
        return [Color(hsl=((h + 60) % 360, s, l)),
                Color(hsl=((h + 120), s, l))]

    def tint(self, n):
        h, s, l = self.hsl()
        l = l + n
        return Color(hsl=(h, s, l if l <= 100 and l >= 0 else l % 100))

    def tone(self, n):
        h, s, l = self.hsl()
        s = s + n
        return Color(hsl=(h, s if s >= 0 and s <= 100 else s % 100, l))


class TextColorCalculator():

    def contrast(self, text_color, bg_color):
        ratio = (text_color.luminance() + .05) / (bg_color.luminance() + .05)

        if ratio < 1:
            ratio = 1 / ratio

        return round(ratio, 1)

    def AA_textcolors(self, bg_color):
        def by_hue(color):
            h, s, l = color.hsl()
            return (h, l, s)

        base_colors = [Color('#000000'), Color('#ffffff')]
        for i in range(0, 100, 25):
            base_colors.append(bg_color.tint(i))
        for i in range(0, 100, 25):
            for color in list(base_colors):
                base_colors.append(color.tone(i))

        initial_colors = []
        for color in base_colors:
            initial_colors.append(color.complementary_color())
            initial_colors.extend(color.analogous_colors())
            initial_colors.extend(color.triadic_colors())

        color_options = list(initial_colors)

        for i in range(0, 100, 10):
            for color in initial_colors:
                color_options.append(color.tint(i))
                color_options.append(color.tone(i))

        color_options = list(
            filter(lambda c: self.contrast(c, bg_color) >= 4.5, color_options))

        color_options = list(set(color_options))
        color_options.sort(key=by_hue)
        return color_options

    def AAA_textcolors(self, bg_color):
        def by_hue(color):
            h, s, l = color.hsl()
            return (h, l, s)
        aaa_colors = list(filter(lambda c: self.contrast(
            c, bg_color) >= 7, self.AA_textcolors(bg_color)))
        aaa_colors.sort(key=by_hue)
        return aaa_colors
