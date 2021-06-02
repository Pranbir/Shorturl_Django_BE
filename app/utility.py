from django.http.response import JsonResponse

def error_handler(func):

    def inner(*args, **kwargs):
        try:
            print("Error Handler ready. Function '{}' called ".format(func.__name__))
            return func(*args, **kwargs)
        except Exception as e:
            print(f" {'=='*20} {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}   {'=='*20}")
            return JsonResponse({'status':False,'message':"Internal Error Occured"}, 
                                status=500)
    return inner


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def success_response(request, msg, data={}):
    return JsonResponse({'status': True,'message':msg,'data':data}, 
                        status=200)


def custom_response(request, msg, data={}, status_code=200):
    return JsonResponse({'status': True,'message':msg,'data':data}, 
                        status=status_code)