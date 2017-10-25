from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accessible_text_color.calculator import Color, TextColorCalculator


def main_view(request):
    page_data = {
        'page': {
            'title': 'a11y Color Generator'
        },
        'hue_range': list(range(0, 360, 10)),
    }
    return render(request,
                  "accessible_text_color/index.html",
                  context=page_data)


@api_view(['POST'])
def post_bgcolor(request):
    """Take a bg color, return a list of acceptable text colors"""
    bg_color = Color(request.data.get('color'))

    aa_colors = list(map(str, TextColorCalculator().AA_textcolors(bg_color)))
    aaa_colors = list(map(str, TextColorCalculator().AAA_textcolors(bg_color)))

    return Response({
        'background_color': str(bg_color),
        'aa_colors': aa_colors,
        'aaa_colors': aaa_colors,
    })
