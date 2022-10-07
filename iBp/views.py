from django.shortcuts import render, redirect
import requests
from .demo import demoIBP, demoTeabud, demoIBP_cucumber
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@method_decorator(csrf_exempt)
def ibpinterface(request):
    print("recieve from iBP!")
    #print(request)
    if request.method == 'POST':
        #print(dir(request))
        body = request.body
        # print(body)
        body = body.decode('utf8')
        # print(body)

        data = json.loads(body)
        try:
            data = json.loads(data)
        except:
            pass
        # print(type(data))
        # print(data)
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


@method_decorator(csrf_exempt)
def tea_bud_counting_API(request):
    print("tea bud identification!")
    #print(request)
    if request.method == 'POST':

        body = request.body
        body = body.decode('utf8')
        data = json.loads(body)

        try:
            data = json.loads(data)
        except:
            pass

        try:
            if 'Image' in data:
                context = demoTeabud(data)
                # print(context)
                return JsonResponse(context)
            else:
                context = {"fail":000}
            
        except:
            context = {"fail":000}

        return JsonResponse(context)

@method_decorator(csrf_exempt)
def cucumber_API(request):
    print("IBP cucumber identification!")
    #print(request)
    if request.method == 'POST':

        body = request.body
        body = body.decode('utf8')
        data = json.loads(body)

        try:
            data = json.loads(data)
        except:
            pass

        # try:
        if 'Image' in data:
            context = demoIBP_cucumber(data)
            # print(context)
            return JsonResponse(context)
        #     else:
        #         context = {"fail":000}
            
        # except:
        #     context = {"fail":000}

        # return JsonResponse(context)