from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def main_view(request):
    return HttpResponse('<!DOCTYPE html><html><title>WCAG Color Calculator</title></html>')
