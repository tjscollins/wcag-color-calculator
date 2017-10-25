from django import template

import webcolors

from accessible_text_color.calculator import Color

register = template.Library()

HEX_LIST = {}
for (key, value) in webcolors.css3_hex_to_names.items():
    HEX_LIST[value] = Color(key).rgb


def find_closest(rgb):
    distances = []
    for (name, color) in HEX_LIST.items():
        dist = pow(color[0] - rgb[0], 2) + \
            pow(color[1] - rgb[1], 2) + \
            pow(color[2] - rgb[2], 2)
        distances.append([name, dist])

    distances.sort(key=lambda x: x[1])
    return distances[0][0]


@register.filter
def color_name(hue):
    color = Color(hsl=(int(hue), 100, 50))
    name = find_closest(color.rgb)

    try:
        return name + ' hue'
    except KeyError:
        return str(color) + ' hue'
