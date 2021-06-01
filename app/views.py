from django.http.response import HttpResponse
from django.shortcuts import render
from .utility import error_handler, success_response
import shortuuid
import json
from .models import Urldata
from django.views.decorators.csrf import csrf_exempt


limit = 5

@error_handler
def index(request):
    return HttpResponse("Hi")

@error_handler
def report(request):
    return HttpResponse("REPORT PAGE FOR ADMINS")

@error_handler
def code_handler(request, code):
    return HttpResponse("code = {}".format(code))


#@error_handler
@csrf_exempt
def code_generator(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        url = body['url']
        shortcode = shortuuid.uuid()[:limit]
        data = Urldata(url=url, shortcode=shortcode)
        data.save()
        if data.shortcode:
            return success_response(request, "Successfully Created", data=dict(url="{}/{}".format(request.get_host(),data.shortcode)))
        else:
            raise Exception("Unable to create a shortcode")
    else:
        raise Exception("Method Not Allowed")