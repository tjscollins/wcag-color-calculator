from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accessible_text_color.calculator import TextColorCalculator
# Create your views here.


def main_view(request):
    page_data = {
        'page': {
            'title': 'WCAG Color Calculator'
        }
    }
    return render(request,
                  "accessible_text_color/index.html",
                  context=page_data)


@api_view(['POST'])
def post_bgcolor(request):
    """Take a bg color, return a list of acceptable text colors"""
    bg_color = request.data.get('color')

    return Response({'color': bg_color})
