from django.http.response import HttpResponse
from django.shortcuts import render
from .utility import error_handler, success_response, custom_response
import shortuuid
import json
from .models import Accessdata, Urldata
from django.views.decorators.csrf import csrf_exempt


limit = 5

@error_handler
def index(request):
    return success_response(request, "API IS WORKING")


@error_handler
def report(request):
    return HttpResponse("REPORT PAGE FOR ADMINS")


@error_handler
def code_handler(request, code):
    if request.method == "GET":
        if not code:
            raise Exception("No Shortcode found")
        else:
            url_object = Urldata.objects.filter(shortcode = code).first()
            if not url_object:
                return custom_response(request, "Invalid Short URL", status_code=404) 
            print(request.headers)
            return success_response(request,"Data fetched", data=dict(url=url_object.url))

    else:
        raise Exception("Method Not Allowed")


@error_handler
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