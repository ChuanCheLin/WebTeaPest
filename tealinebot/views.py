
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, JoinEvent, LeaveEvent,ImageSendMessage, ImageMessage
import os,sys,time
from datetime import datetime
import urllib
from urllib.request import urlopen
import base64
import json
from iBp.demo import demoLinebot
from linebot.models import (
    MessageEvent,
    PostbackEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    URITemplateAction,
    PostbackTemplateAction
)

from imgUp.demo import demo

#app = Flask(__name__)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:

            user_id = event.source.user_id

            if isinstance(event, PostbackEvent):
                if event.postback.data[0:1] == 'A':
                    #mesg = event.postback.data[2:].split('&')
                    predid = event.postback.data[2:12]
                    #print(predid)
                    url = event.postback.data[13:]
                    line_bot_api.push_message(user_id,TemplateSendMessage(
                            alt_text='傳送了辨識結果給您',
                            template=ButtonsTemplate(
                                title = '請選擇項目',
                                text = '可以進行誤判回報或查看用藥資訊',
                                actions = [PostbackTemplateAction(label='誤判回報',text='誤判回報', data='B&' + predid),
                                        URITemplateAction(label='查看用藥資訊',uri = url)      
                                        ]
                                )
                            )
                        )
                elif event.postback.data[0:1] == 'B':
                    predid = event.postback.data[2:]
                    line_bot_api.push_message(user_id,TemplateSendMessage(
                            alt_text='傳送了辨識結果給您',
                            template=ButtonsTemplate(
                                title = '誤判回報',
                                text = '請選擇狀況類別',
                                actions = [PostbackTemplateAction(label='1.病蟲害種類誤判',text='病蟲害種類誤判', data='C&' + predid + '&1'),
                                            PostbackTemplateAction(label='2.背景或健康葉片被誤判',text='背景或健康葉片被誤判', data='C&' + predid + '&2'),
                                            PostbackTemplateAction(label='3.病蟲害未被辨識',text='病蟲害未被辨識', data='C&' + predid + '&3'),
                                            PostbackTemplateAction(label='4.其他',text='其他', data='C&' + predid + '&4')
                                        ]
                                )
                            )
                        )
                elif event.postback.data[0:1] == 'C':
                    pred_id = event.postback.data[2:12]
                    issue_num = event.postback.data[13:]
                    #email = request.POST['contact']
                    det = Detection.objects.get(pred_id=pred_id)
                    fb = Feedback(
                        pred = det, 
                        date = timezone.now(),
                        issue= issue_d[issue_num],
                        #contact=email,
                        #feedback = request.POST['feedback'],
                    )
                    fb.save()

                    line_bot_api.push_message(user_id, TextSendMessage(text='已收到 謝謝您的回報'))


            elif isinstance(event, MessageEvent):
                message_content = line_bot_api.get_message_content(event.message.id)
                now = timezone.now() # current date and time
                file_name = now.strftime("%Y%m%d_%H%M%S")
                file_path = 'media/linebotphoto/'+file_name+'.jpg'
                with open(file_path, 'wb') as fd:
                    for chunk in message_content.iter_content():
                        fd.write(chunk)
                        

                context = demoLinebot(file_path)

                #connect with db
                img_name, img, imgid = save_image('linebotphoto/'+file_name+'.jpg')
                # demo(img_name, img)
                

                #f = open(file_path, "rb") # open our image file as read only in binary mode
                #image_data = f.read() 

                #image_data = bytes(context["resultImage"], encoding='utf8')
                #b64_image = base64.standard_b64encode(image_data)
                b64_image = context["resultImage"]
                client_id = "534d70c4a222f1a" # put your client ID here
                headers = {'Authorization': 'Client-ID ' + client_id}
                data = {'image': b64_image, 'title': 'test'} # create a dictionary.

                #request = urllib.request.Request(url="https://api.imgur.com/3/upload.json",data=urllib.parse.urlencode(data), headers=headers)
                #response = urllib.request.urlopen(request).read()
                request = urllib.request.Request(url="https://api.imgur.com/3/upload.json",data = urllib.parse.urlencode(data).encode("utf-8") ,headers=headers)
                response = urllib.request.urlopen(request).read()
                parse = json.loads(response)
                image_url=parse['data']['link']

                line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=image_url,preview_image_url=image_url))
                user_id = event.source.user_id
                count=1
                nums=context["pestTable"]
                dets = []
                prescriptions_url = "http://teas.agiot.tw/search2#FIND:"
                for num in nums:
                    if len(nums[num])!=0 :
                        for i in range(len(nums[num])):                      
                            #中文版 
                            mesg = '%s: %s' %(tablenum.get(count), table.get(num)) 
                            
                            #Eng ver
                            #mesg = '%s: %s' %(tablenum.get(count), table_eng.get(num))

                            #處方籤
                            prescriptions_url = prescriptions_url + table_fullname.get(num) + ","
                            #print(prescriptions_url)

                            predid = imgid + '_' + tablenum.get(count)
                            uri = tableurl.get(num)
                            # line_bot_api.push_message(user_id, TextSendMessage(tablenum.get(count)))
                            # line_bot_api.push_message(user_id, TextSendMessage(table.get(num)))
                            #line_bot_api.push_message(user_id, TextSendMessage(mesg))
                            if len(dets) < 4:
                                dets.append(
                                    PostbackTemplateAction(label=mesg,text=mesg, data= 'A&' + predid + '&' + uri)
                                )
                            '''
                            line_bot_api.push_message(user_id,TemplateSendMessage(
                                alt_text='傳送了辨識結果給您',
                                template=ButtonsTemplate(
                                    #title='病蟲害檢測結果',
                                    #text='想了解更多資訊請點擊連結',
                                    title='Identification Results',
                                    text='press the link for more information',
                                    actions=[
                                        URITemplateAction(
                                            label=mesg,
                                            uri=tableurl.get(num)
                                        )
                                        ]
                                    )
                                )
                                
                            )
                            '''
                            count=count+1
                #if len(dets)==0:
                #    dets.append(URITemplateAction(label='未辨識出病蟲害',uri="https://forms.gle/26jUSkEBaNqRV1YR7"))
                #dets.append(PostbackTemplateAction(label='誤判回報',text='誤判回報', data= 'A'))

                #回報問題 測試用
                # if len(dets) < 4:
                #     dets.append(URITemplateAction(label='回報問題',uri="https://forms.gle/26jUSkEBaNqRV1YR7"))
                

                if len(dets) < 4:
                    dets.append(URITemplateAction(label='智能用藥處方籤',uri= prescriptions_url ))
                #dets.append(URITemplateAction(label=mesg,uri=tableurl.get(num)))
                

                        
                line_bot_api.push_message(user_id,TemplateSendMessage(
                    alt_text='傳送了辨識結果給您',
                    template=ButtonsTemplate(
                        title='Image ID: '+ imgid,  #病蟲害檢測結果
                        text='想了解更多資訊請點擊連結',
                        #Eng version
                        #title='Identification Results',
                        #text='press the link for more information',
                        actions = dets
                        )
                    )
                )
        return HttpResponse()    
    else:
        return HttpResponseBadRequest()

table = {
        'mosquito_early': '盲椿象_早期',
        'mosquito_late':'盲椿象_晚期',
        'brownblight': '赤葉枯病',
        'fungi_early': '真菌性病害_早期',
        'blister': '茶餅病',
        'algal': '藻斑病',
        'miner': '潛葉蠅',
        'thrips':'薊馬',
        'roller': '茶捲葉蛾',
        'mosquito_late': '盲椿象_晚期',
        'mosquito_early': '盲椿象_早期',
        'moth': '茶姬捲葉蛾',
        'tortrix': '茶姬捲葉蛾',
        'flushworm': '黑姬捲葉蛾',
        'formosa': '小綠葉蟬',
        'caloptilia' : '茶細蛾',
        'tetrany': '蟎類',
        'sunburn': '日燒症',
        'other': '其他',
    }

table_eng = {
        'mosquito_early': 'Tea Mosquito Bug Early-stage',
        'mosquito_late':'盲椿象_晚期',
        'brownblight': 'Brown Blight',
        'fungi_early': 'Fungi Disease',
        'blister': '茶餅病',
        'algal': '藻斑病',
        'miner': '潛葉蠅',
        'thrips':'Thrips',
        'roller': '茶捲葉蛾',
        'moth': '茶姬捲葉蛾',
        'tortrix': '茶姬捲葉蛾',
        'flushworm': '黑姬捲葉蛾',
    }

table_fullname = {
    'mosquito_early': 'Tea Mosquito Bug Early-stage',
    'mosquito_late':'盲椿象_晚期',
    'brownblight': '真菌及類真菌病害/赤葉枯病',
    'fungi_early': '真菌及類真菌病害',
    'blister': '真菌及類真菌病害/茶餅病',
    'algal': '藻斑病',
    'miner': '害蟲/雙翅目/潛蠅類/亞洲潛葉蠅',
    'thrips':'害蟲/薊馬類/葉部薊馬類/小黃薊馬',
    'roller': '害蟲/鱗翅目害蟲/捲葉蛾類/茶捲葉蛾',
    'moth': '害蟲/鱗翅目害蟲/捲葉蛾類/姬捲葉蛾',
    'tortrix': '害蟲/鱗翅目害蟲/捲葉蛾類/姬捲葉蛾',
    'flushworm': '害蟲/鱗翅目害蟲/捲葉蛾類/黑姬捲葉蛾',
    'formosa': '小綠葉蟬',
    'caloptilia' : '茶細蛾',
    'tetrany': '蟎類',
    'sunburn': '日燒症',
    'other': '其他',
}
tablenum = {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
    }

tableurl = {
        'mosquito_early': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C131&',
        'mosquito_late':'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C131&',
        'brownblight': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254B026&',
        'fungi_early': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254B026&',
        'blister': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254B050',
        'algal': 'https://web.tari.gov.tw/techcd/%E7%89%B9%E4%BD%9C/%E8%8C%B6%E6%A8%B9/%E7%97%85%E5%AE%B3/%E8%8C%B6%E6%A8%B9-%E8%97%BB%E6%96%91%E7%97%85.htm',
        'miner': 'https://www.baphiq.gov.tw/Publish/plant_protect_pic_8/ricePDF/03-28.pdf',
        'thrips':'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C155&',
        'roller': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'moth': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'tortrix': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'flushworm': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'formosa':'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C155&',
        'caloptilia': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'tetrany': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'sunburn': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
        'other': 'https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254C084',
    }



'''
Imgur    
Client ID:534d70c4a222f1a
Client secret:fbcb5eacf9e2212ac15a7697b285c6986004ee54

Token Name
Tealinebottoken
Access Token
0771a466eaddccdf80d771a0e9c3c222e79d5730
Token Type
bearer
expires_in
315360000
scope
refresh_token
410d4b8e5b5d34d7169c07e0f61540607d06eeaa
account_id
139491051
account_username
SSLeric







@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user id when reply
    global user_id
    user_id = event.source.user_id


            var buttonComponent = new ButtonComponent
            {
                Style = ButtonStyle.Primary,
                Action = new UriTemplateAction(
                    "Uri Button",
                    "https://otserv2.tactri.gov.tw/PPM/PLC0101.aspx?UpPage=PLC01&CropNo=00254B026&",
                    new AltUri("https://www.google.com/"))
            }

'''

import os
import shutil
import json
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import LineImg, Detection, Feedback
from TeaData.models import County, City
from datetime import datetime
from numpy.random import randint
from django.utils import timezone
import pytz

# Create your views here.

default_context = {
    'counties' : County.objects.all(),
    'cities' : City.objects.none(),
    'imgs' : LineImg.objects.none()
}


issue_d = {
    '1':'wrong',
    '2':'background',
    '3':'nodetect',
    '4':'other'
    }

            
def id2result(imgid):
    try: 
        url = reverse('show_image', kwargs={'img_id': imgid} )
        return redirect('{}#result'.format(url))
    except:
        err = 'id_not_found'
        url = reverse('error', kwargs={'issue': err} )
        return redirect('{}#upload'.format(url))

def uploadImg(request):

    if request.method == 'POST':
        # if True:
        try:
            img_name = request.FILES.get('img')
            img_name, img = save_image(img_name)

            num = demo(img_name, img)
            if request.POST.get('nope', False):
                pass
            else:
                save_region(request, img)

            return id2result(img.img_id)
        except:

            err = 'wrong_input'
            url = reverse('error', kwargs={'issue': err} )
            return redirect('{}#upload'.format(url))

    return


def save_image(img_mem):
    
    img = LineImg(img_url=img_mem)
    img.save()

    imgid = "%08d" % randint(0,99999999)
    print('img_id: ', imgid)
    img.img_id = imgid
    img.save()

    url = img.img_url.url

    basename = os.path.basename(url)
    imgname = 'media/linebotphoto/' + basename 
    copimg = 'media/linebotphoto_ori/' + basename
    shutil.copyfile(imgname, copimg)


    return imgname, img, imgid

def showHistory(request):
    try:
        imgid = request.POST['imgid']

        return id2result(imgid)
    except:
        err = 'id_not_found'
        url = reverse('error', kwargs={'issue': err} )
        return redirect('{}#upload'.format(url))

def errorpage(request, issue):
    
    errors = {
        'id_not_found': 'ERROR: 輸入ID錯誤，該影像不存在 The Image ID not exist! ',
        'wrong_input': 'ERROR: 未選擇檔案or檔名須為英文 The uploaded file must be Image!',
        'not_yet': 'ERROR: 未有影像上傳，請先上傳影像 Please upload image first.',
    }
    img = Img.objects.get(img_id='noimg')
    context = {
        'error_message' : errors[issue],
        'imgs': img,
    }
    return
    

def showHtml(request, f):
    context = {}
    values = request.path
    print(f)
    return render(request, values[1:], {**default_context, **context})

def showImg(request, img_id=None):
    
    print(img_id)
    try:
        img = Img.objects.get(img_id=img_id)
    except:
        err = 'id_not_found'
        url = reverse('error', kwargs={'issue': err} )
        return redirect('{}#upload'.format(url))
    
   
    dets = Detection.objects.filter(img_data=img)

    context = {
        'imgs': img,
        'dets': dets,
    }
    return

def feedback(request):

    if request.POST['feedback'] != '':

        pred_id = request.POST['pred_id']
        issue_num = request.POST['issue'][0]
        email = request.POST['contact']

        det = Detection.objects.get(pred_id=pred_id)
        fb = Feedback(
            pred = det, 
            date = timezone.now(),
            issue= issue_d[issue_num],
            contact=email,
            feedback = request.POST['feedback'],
        )
        fb.save()

    img_id = request.POST['img_id']
    return id2result(img_id)

def load_cities(request):
    
    # print('load city~~!!')
    if request.method == 'GET' and request.is_ajax():
        county = request.GET.get('county')
        selectCounty = County.objects.get(name=county)
        cities = City.objects.filter(County=selectCounty)
        # print("cities are: ", cities)
        result_set = []
        for city in cities:
            # print("city name", city.name)
            result_set.append({'name': city.name})
        return HttpResponse(json.dumps(result_set), content_type='application/json')
    

def save_region(request, img):

    if True:
    # try:
        county = request.POST['county']
        city = request.POST['city']
        altitude = request.POST['altitude']
        if county != "":
            img.county = County.objects.get(name=county)
        if city != "":
            if city[0] != "-":
                img.city = City.objects.get(name=city, County=img.county)
        if altitude[0] != "-":
            img.altitude = altitude

        img.save()

def add_region(request):
    # if True:
    try:
        imgid = request.POST['imgid']
        print('set region imgid:' , imgid)
        img = Img.objects.get(img_id=imgid)

        county = request.POST['county']
        city = request.POST['city']
        altitude = request.POST['altitude']

        img.county = County.objects.get(name=county)
        img.city = City.objects.get(name=city, County=img.county)
        img.altitude = altitude

        img.save()
        return id2result(imgid)
    except:
        err = 'not_yet'
        url = reverse('error', kwargs={'issue': err} )
        return redirect('{}#upload'.format(url))

    
def db_test(img, result):

    det = Detection(
        pred_id = '0001_A',
        # img_name = Pred,
        img_data = img,
        box_id = 'A',
        pred_cls = 'brownblight' ,
        score = 0.995,
        xmin = 100,
        ymin = 100,
        xmax = 200,
        ymax = 200,
        context = 'A: brownblight score: 0.995',
    )
    det.save()


def det_to_json(img_name, result, classes):
    json_name = img_name[:-4] + '.json'
    det_count = 0
    det_dict = {}
    for i in range(len(result)):
        pred_cls = classes[i]
        if len(result[i]) == 0:
            det_dict[pred_cls] = []
        else:
            pass
    
def mail_test(request):

    pass


