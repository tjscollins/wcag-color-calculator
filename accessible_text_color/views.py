from django.shortcuts import render
from django.shortcuts import render
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
