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


def success_response(request, msg, data={}):
    return JsonResponse({'status': True,'message':msg,'data':data}, 
                        status=200)


def custom_response(request, msg, data={}, status_code=200):
    return JsonResponse({'status': True,'message':msg,'data':data}, 
                        status=status_code)