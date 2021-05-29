from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hi")


def report(request):
    return HttpResponse("REPORT PAGE FOR ADMINS")


def code_handler(request, code):
    return HttpResponse("code = {}".format(code))


def code_generator(request):
    return HttpResponse("I Will take a long URL and return a short code")