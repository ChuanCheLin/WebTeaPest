from django.shortcuts import render, redirect
import requests
from .demo import demoIBP, demoTeabud, demoIBP_cucumber, remove_outliers
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
import numpy as np

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
def tea_bud_remove_outlier_API(request):
    print("tea bud remove outlier!")
    #print(request)
    if request.method == 'POST':

        body = request.body
        body = body.decode('utf8')
        data = json.loads(body)

        context = {
        "dataTime": "", # 時間ID, 與原來接收之ID相同
        "averageNum": 0,           # int, 去除離群值並平均後的單日茶芽數量
        }

        print(data)
        try:
            data = json.loads(data)
        except:
            pass

        # try:
        if 'dataTime' in data:
            context["dataTime"] = data["dataTime"]
            context["averageNum"] = remove_outliers(data = data['sequence_data'])

            return JsonResponse(context)
        #     else:
        #         context = {"fail":000}
            
        # except:
        #     context = {"fail":000}

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

