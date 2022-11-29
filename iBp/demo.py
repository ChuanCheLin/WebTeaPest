

import sys
import os
import re
import csv
import shutil
import cv2
import base64
from io import BytesIO
from PIL import Image
import json
import numpy as np
from mmcv.image import imread, imwrite
from datetime import datetime
from imgUp.demo import pred_img, read_label_color, pred_img_tea_bud, pred_img_cucumber
from fsdet.data.detection_utils import read_image

def demo_test():
    img_name = '0721192833.jpg'
    img = 'media/test/' + img_name
    img64 = image_to_base64(img)
    img64 = str(img64, encoding='utf-8')
    json_recieve = {
        "dataTime": "2020-08-21 12:43:45", # 影像的時間ID :"2019-11-03 21:43:45"
        "Image": img64,   # 需預測的影像 base64 編碼
    }
    ret1 = json.dumps(json_recieve)
    with open('recieve.json', 'w') as fp:
        fp.write(ret1)

    
    demoIBP('recieve.json')

def image_to_base64(image_path):
    img = Image.open(image_path)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return image_path

def demoIBP(inputjson):
    # print(type(inputjson))
    img_name = 'media/iBp_temp/input.jpg'
    out_name = 'media/iBp_temp/output.jpg'

    img_name = base64_to_image(inputjson['Image'], img_name) 

    context = init_json(inputjson['dataTime'])

    
    labels, bboxes, classes, scores = pred_img(img_name)

    colorfile = 'imgUp/color.txt'
    colors = read_label_color(colorfile)

    context, _ = draw_bboxes(img_name,
                    bboxes,
                    labels,
                    context,
                    colors=colors,
                    scores = scores,
                    class_names=classes,
                    score_thr=0.5,
                    out_file=out_name)

    context["imageURL"] = "http://140.112.183.138:1008/media/iBp_temp/output.jpg"
    write_base64 = True
    if write_base64:
        out64 = image_to_base64(out_name)
        context["resultImage"] = str(out64, encoding='utf-8')

    return context

def demoIBP_cucumber(inputjson):

    img_name = 'media/iBp_temp/input.jpg'
    out_name = 'media/iBp_temp/output.jpg'

    img_name = base64_to_image(inputjson['Image'], img_name) 

    context = init_json_cucumber(inputjson['dataTime'])


    labels, bboxes, classes, scores = pred_img_cucumber(img_name)
    print(labels, bboxes, classes, scores)

    colorfile = 'imgUp/color.txt'
    colors = read_label_color(colorfile)

    context, _ = draw_bboxes(img_name,
                    bboxes,
                    labels,
                    context,
                    colors=colors,
                    scores = scores,
                    class_names=classes,
                    score_thr=0.5,
                    out_file=out_name)


    context["imageURL"] = "http://140.112.183.138:1007/media/iBp_temp/output.jpg"
    write_base64 = True
    if write_base64:
        out64 = image_to_base64(out_name)
        context["resultImage"] = str(out64, encoding='utf-8')

    return context

def demoLinebot(inputimage):
    # print(type(inputjson))

    img_name = inputimage 
    out_name = 'media/iBp_temp/output.jpg'
    context = init_json(1)
    
    labels, bboxes, classes, scores = pred_img(img_name)

    colorfile = 'imgUp/color.txt'
    colors = read_label_color(colorfile)

    context, sequence_disease = draw_bboxes(img_name,
                    bboxes,
                    labels,
                    context,
                    colors=colors,
                    scores = scores,
                    class_names=classes,
                    score_thr=0.5,
                    out_file=out_name)

    write_base64 = True
    if write_base64:
        out64 = image_to_base64(out_name)
        context["resultImage"] = out64
        

    return context, sequence_disease

def demoLinebot_cucumber(inputimage):
    # print(type(inputjson))

    img_name = inputimage 
    out_name = 'media/iBp_temp/output.jpg'
    context = init_json_cucumber(1)
    
    labels, bboxes, classes, scores = pred_img_cucumber(img_name)

    colorfile = 'imgUp/color.txt'
    colors = read_label_color(colorfile)

    context, sequence_disease = draw_bboxes(img_name,
                    bboxes,
                    labels,
                    context,
                    colors=colors,
                    scores = scores,
                    class_names=classes,
                    score_thr=0.5,
                    out_file=out_name)

    write_base64 = True
    if write_base64:
        out64 = image_to_base64(out_name)
        context["resultImage"] = out64        

    return context, sequence_disease

def demoTeabud(inputjson):
    # print(type(inputjson))
    img_name = 'media/iBp_temp/input.jpg'

    img_name = base64_to_image(inputjson['Image'], img_name) 

    context = init_json_teabud(inputjson['dataTime'])

    labels, bboxes, classes, scores = pred_img_tea_bud(img_name)

    context["numofPredictions"] = len(labels)

    return context
    

def draw_bboxes(img_name,
                bboxes,
                labels,
                context,
                colors,
                scores,
                width=None,
                class_names=None,
                score_thr=0.5,
                out_file=None
                ):
    """Draw bboxes and class labels (with scores) on an image.

    Args:
        img (str or ndarray): The image to be displayed.
        bboxes (ndarray): Bounding boxes (with scores), shaped (n, 4) or
            (n, 5).
        labels (ndarray): Labels of bboxes.
        class_names (list[str]): Names of each classes.
        score_thr (float): Minimum score of bboxes to be shown.
        out_file (str or None): The filename to write the image.
    """
    if len(scores) != 0:
        assert bboxes.ndim == 2
        assert labels.ndim == 1
        assert bboxes.shape[0] == labels.shape[0]
        assert bboxes.shape[1] == 4 or bboxes.shape[1] == 5

    img = read_image(img_name, format="BGR")
    img = img.copy()
    
    ori_size = img.shape

    width = ori_size[0]
    ratio = 1
    pr = ori_size[0]/800

    # if score_thr > 0.0:
    #     assert bboxes.shape[1] == 5
    #     inds = scores > score_thr
    #     bboxes = bboxes[inds, :]
    #     labels = labels[inds]
    #     scores = scores[inds]

    pred_num = labels.shape[0]
    context["numofPredictions"] = pred_num

    ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i = 0
    sequence_disease = []

    if len(scores) != 0:
        for bbox, label, score in zip(bboxes, labels, scores):
            
            pred_cls = class_names[label]
            color = colors[pred_cls]
            box_id = ABC[i]
            
            bbox = bbox*ratio
            bbox_int = bbox.astype(np.int32)

            det =  {"bboxId":box_id, "score": float(score) ,
                    "xmin":int(bbox_int[0]), "ymin":int(bbox_int[1]),
                    "xmax":int(bbox_int[2]), "ymax":int(bbox_int[3]) }

            context["pestTable"][pred_cls].append(det)

            sequence_disease.append(pred_cls)
           
            left_top = (bbox_int[0], bbox_int[1])
            right_bottom = (bbox_int[2], bbox_int[3])
            
            cv2.rectangle(img, (left_top[0], left_top[1]),
                        (right_bottom[0], right_bottom[1]), color, int(4*pr))
            text_size, baseline = cv2.getTextSize(box_id,
                                                cv2.FONT_HERSHEY_SIMPLEX, int(1.3*pr), int(2*pr))
            p1 = (left_top[0], left_top[1] + text_size[1])
            cv2.rectangle(img, tuple(left_top), (p1[0] + text_size[0], p1[1]+1 ), color, -1)
            cv2.putText(img, box_id, (p1[0], p1[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, int(1.3*pr), (255,255,255), int(2*pr), 8)
            
            i += 1

    print('done   '+ str(out_file))
        
    imwrite(img, out_file)
    
    return context, sequence_disease

def remove_outliers(data):

    q1 = np.quantile(data, 0.25)
    q3 = np.quantile(data, 0.75)
    iqr = q3 - q1

    upper_bound = q3 + (1.5 * iqr)
    lower_bound = q1 - (1.5 * iqr)

    for i in data:
        if i < lower_bound or i > upper_bound:
            data.remove(i)

    average_data = sum(data) / len(data)
        
    return average_data

def gompertz(t, a, b, c):
    return a * np.exp(-np.exp(b - c * t)) + bias

def recip_exp(t, a, b):
    return a * np.exp(- b * t)

def tea_bud_predictiion(data):
    from sympy import diff, Symbol, exp
    from scipy.optimize import curve_fit
    from sklearn.metrics import r2_score, mean_squared_error

    n = len(data)
    pred_curve = []
    AGRmax = 0
    AGRmax_idx = 0
    key = True
    choose_day = 15
    ypme = np.empty(n)
    global bias

    day = np.empty(n)
    for i in range(n):
        day[i] = i+1

    inve, _ = curve_fit(recip_exp, day[:choose_day], data[:choose_day]) 
    for i in range(n):
        ypme[i] = recip_exp(i+1, inve[0], inve[1])
    
    bias = ypme[14] #sepatrate reciprocal and gompertz

    gcoe, _ = curve_fit(gompertz, day, data)

    print(gcoe)

    # gcoe = [22.5296142, 34.80393294, 0.93934673] #gompertz parameters
    
    t = Symbol('t')
    gom_diff = diff(gcoe[0] * exp(-exp(gcoe[1] - gcoe[2] * t)), t)
    
    for d in range(len(data)):
        if 0 < round(float(gom_diff.subs(t, d)), 1) and key:
            growth_time_idx = int(d)
            growth_time = gom_diff.subs(t, d)
            key = False

        if AGRmax < gom_diff.subs(t, d):
            AGRmax_idx = int(d)
            AGRmax = gom_diff.subs(t, d)

    harvest_time = 0
    for d in range(len(data)):
        if d >= AGRmax_idx:
            # print(round(float(gom_diff.subs(t, d)), 1))
            if round(float(gom_diff.subs(t, d)), 1) <= 0:
                harvest_time = int(d)
                break
    
    

    for t in range(len(data)):
        if t >= 0 and t <=14:
            pred_curve.append(ypme[t])
        else:
            pred_curve.append(gompertz(t, gcoe[0], gcoe[1], gcoe[2]))

    if harvest_time == 0:
        harvest_time = len(data)

    return pred_curve, harvest_time

def init_json(dataTime):
    context = {
        "dataTime": dataTime, # 時間ID, 與原來接收之ID相同
        "imageURL":"",
        "resultImage": "",
        "numofPredictions": 0,           # int, 總計辨識框數量，通常不會多於20
        "pestTable": {   # 共12種病蟲害，每一項目皆為陣列，內含該種類之所有預測結果
            'mosquito_early':[],
            'mosquito_late':[],                                 #'盲椿象_晚期',
            'brownblight': [],                                  #'赤葉枯病',
            'fungi_early': [],   #'真菌性病害_早期',
            'blister': [],                                      #'茶餅病',
            'algal': [],                                        #'藻斑病',
            'miner': [],                                        #'潛葉蠅',
            'thrips': [],        #'薊馬',
            'roller': [],                                       #'茶捲葉蛾_傷口',
            'moth': [],                                         #'茶姬捲葉蛾_傷口',
            'tortrix': [],                                      #'茶姬捲葉蛾_捲葉',
            'flushworm': [],                                    #'黑姬捲葉蛾',
            'formosa': [],
            'caloptilia' : [],
            'tetrany': [],
            'sunburn': [],
            'other': [],
            },
    }

    return context

def init_json_cucumber(dataTime):
    context = {
        "dataTime": dataTime, # 時間ID, 與原來接收之ID相同
        "imageURL":"",
        "resultImage": "",
        "numofPredictions": 0,           # int, 總計辨識框數量，通常不會多於20
        "pestTable": {   # 共12種病蟲害，每一項目皆為陣列，內含該種類之所有預測結果
            'health':[],
            'virus':[],                                 #'盲椿象_晚期',
            'anthracnose': [],                                  #'赤葉枯病',
            'downy': [],   #'真菌性病害_早期',
            'corynespora': [],                                      #'茶餅病',
            'powdery': [],                                        #'藻斑病',
            'malnutrition': [],                                        #'潛葉蠅',
            'leafminer': [],        #'薊馬',
            },
    }

    return context

def init_json_teabud(dataTime):
    context = {
        "dataTime": dataTime, # 時間ID, 與原來接收之ID相同
        "numofPredictions": 0,           # int, 總計辨識框數量，通常不會多於20
    }

    return context

# def write_det(Pred, box_id, pred_cls, score, bbox_int):
#     table = {
#         'mosquito_early': '盲椿象_早期',
#         'mosquito_late':'盲椿象_晚期',
#         'brownblight': '赤葉枯病',
#         'fungi_early': '真菌性病害_早期',
#         'blister': '茶餅病',
#         'algal': '藻斑病',
#         'miner': '潛葉蠅',
#         'thrips':'薊馬',
#         'roller': '茶捲葉蛾',
#         'mosquito_late': '盲椿象_晚期',
#         'mosquito_early': '盲椿象_早期',
#         'moth': '茶姬捲葉蛾',
#         'tortrix': '茶姬捲葉蛾',
#         'flushworm': '黑姬捲葉蛾',
#         'formosa': '小綠葉蟬',
#         'caloptilia' : '茶細蛾',
#         'tetrany': '蟎類',
#         'sunburn': '日燒症',
#         'other': '其他',
#     }

#     htable = {
#         'mosquito_early': 'mosquito',
#         'mosquito_late':'mosquito',
#         'brownblight': 'brownblight',
#         'fungi_early': 'fungi_early',
#         'blister': 'blister',
#         'algal': 'algal',
#         'miner': 'miner',
#         'thrips':'thrips',
#         'roller': 'roller',
#         'moth': 'tortrix',
#         'tortrix': 'tortrix',
#         'flushworm': 'flushworm',
#     }

#     pred_id = str(Pred).split('.')[0] + '_' + box_id

#     context = '{:s}: {:s} score: {:.3f}'.format(box_id, table[pred_cls], score)
#     print(context)
#     det = Detection(
#         pred_id = pred_id,
#         img_name = Pred,
#         box_id = box_id,
#         pred_cls = pred_cls,
#         html_file = htable[pred_cls],
#         score = score,
#         xmin = bbox_int[0],
#         ymin = bbox_int[1],
#         xmax = bbox_int[2],
#         ymax = bbox_int[3],
#         context = context,
#     )
#     det.save()
