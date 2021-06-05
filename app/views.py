from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import shortuuid
import json
from .models import Accessdata, Urldata
from django.views.decorators.csrf import csrf_exempt
import requests
from .utility import error_handler, success_response, custom_response, get_client_ip
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


limit = 5

@error_handler
def index(request):
    return success_response(request, "API IS WORKING")


#@error_handler
def report(request):
    return render(request, 'dashboard.html', context={})


@error_handler
def login_page(request):
    return render(request, 'login.html', context={})


@error_handler
def logout_view(request):
    logout(request)
    return redirect(reverse('login_page'))


@error_handler
def login_handler(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('report'))
    else:
        return redirect(reverse('login_page'))


@error_handler
def report_code(request,code):
    return HttpResponse("REPORT PAGE FOR THE CODE : {}".format(code))


@error_handler
def code_handler(request, code):
    if request.method == "GET":
        if not code:
            raise Exception("No Shortcode found")
        else:
            url_object = Urldata.objects.filter(shortcode = code).first()
            if not url_object:
                return custom_response(request, "Invalid Short URL", status_code=404) 
            useragent = request.META['HTTP_USER_AGENT']
            ip = get_client_ip(request)
            shorturlid = url_object
            referer = request.headers.get("Referer", "N/A")
            useragent = request.META.get('HTTP_USER_AGENT', "N/A")
            ip = get_client_ip(request) if get_client_ip(request) else "N/A"
            devicetype = "Mobile" if request.user_agent.is_mobile else "Tablet" if request.user_agent.is_tablet else "PC" if request.user_agent.is_pc else "BOT" if request.user_agent.is_bot else "N/A"
            os = "{} {}".format(request.user_agent.os.family , request.user_agent.os.version_string)
            touchsupport = str(request.user_agent.is_touch_capable)
            browser = "{} {}".format(request.user_agent.browser.family, request.user_agent.browser.version_string)
            devicefamily = request.user_agent.device.family
            locationcountry = locationregion = locationcity = "N/A"
            lat = lon = None
            geo_data = requests.get(url="http://ip-api.com/json/{}".format(ip)).json() if get_client_ip(request) else None
            if geo_data and geo_data.get("status") and geo_data.get("status") == "success":
                locationcountry = geo_data.get("country", "N/A")
                locationregion = geo_data.get("regionName", "N/A")
                locationcity = geo_data.get("country", "N/A")
                lat = geo_data.get("lat")
                lon = geo_data.get("lon")
            
            newAccessData = Accessdata(shorturlid = shorturlid,
                                        referer = referer,
                                        useragent = useragent,
                                        ip = ip,
                                        locationcountry = locationcountry,
                                        locationregion = locationregion,
                                        locationcity = locationcity,
                                        devicetype = devicetype,
                                        os = os,
                                        touchsupport = touchsupport,
                                        browser = browser,
                                        devicefamily = devicefamily,
                                        lat = lat,
                                        lon = lon
                                    )
            newAccessData.save()
            return redirect(url_object.url)
            #return success_response(request,"Data fetched", data=dict(url=url_object.url))
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


#@error_handler
def search_code(request):
    if request.method == "GET":
        q = request.GET.get('q', None)
        print(q)
        if q:
            search_obj = Urldata.objects.filter(Q(shortcode__contains=q)|Q(url__contains=q)).order_by('-lastupdate')[:10].values()
            return success_response(request, "Successfully Fetched Data", data=list(search_obj))
        else:
            return custom_response(request,"Please provide the search query", status_code=404)
    else:
        raise Exception("Method Not Allowed")