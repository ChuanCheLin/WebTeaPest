from django.shortcuts import render, redirect
import requests
from .demo import demoIBP
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@method_decorator(csrf_exempt)
def ibpinterface(request):
    print("recieve from iBP!")
    # print(request)
    if request.method == 'POST':
        # print(dir(request))
        body = request.body
        body = body.decode('utf8')
        data = json.loads(body)
        try:
            data = json.loads(data)
        except:
            pass
        #print(type(data))
        #print(data)
        # if True:
        try:
            if 'Image' in data:

                context = demoIBP(data)
                # print(context)
                return JsonResponse(context)
            else:
                context = {"fail":000}
            
        except:
            context = {"fail":000}

        return JsonResponse(context)

