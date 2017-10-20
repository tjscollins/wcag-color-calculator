import colorsys


class Color():
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
            raise TypeError('Color constructor expects hsl to be a tuple')

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


class TextColorCalculator():

    def constrast(self, text_color, bg_color):
        ratio = (text_color.luminance() + .05) / (bg_color.luminance() + .05)

        if ratio < 1:
            ratio = 1 / ratio

        return round(ratio, 1)

    def AA_textcolors(self, bg_color):
        pass

    def AAA_textcolors(self, bg_color):
        pass
