

import sys
import os
import csv
import shutil
import cv2
import numpy as np
from .models import Img, Detection
from mmcv.image import imread, imwrite
import pytz
from datetime import datetime
from django.conf import settings

from fsdet.data.detection_utils import read_image
from fsdet.config import get_cfg
from .predictor import VisualizationDemo


def demo_test():
    img_name = 'test.jpg'
    img = 'media/img/' + img_name

    img = Img(img_name = img_name,
            img_url=img_name,
            date=datetime.now())
    img.save()

    
    demo(str(img_name), img)


def read_label_color(file, BGR=True):
    '''
        Parameters
        ----------
        file : txt file
            format: brownblight 255,102,0 orange
    
        Returns
        -------
        result : dict
            format: [ 'brownblight' : [255, 102, 0]]
    '''
    color_dict = {}
    
    with open(file, 'r') as f:
        lines = f.readlines()
    
    for l in lines:
        strs = l.split(' ')
        label = strs[0]
        color = list(map(int, strs[1].split(',')))
        if BGR:
            color[0], color[2] = color[2], color[0]
        color_dict[label] = color
        
    return color_dict

def pred_img(img_name):

    # print('import library')

    cfg = get_cfg()
    cfg.merge_from_file('../FSCE_tea-diseases/checkpoints/config.yaml')
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.6
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6
    cfg.freeze()

    demo = VisualizationDemo(cfg)
    
    img = read_image(img_name, format="BGR")
    predictions, visualized_output = demo.run_on_image(img)

    # bbox
    bboxes = np.array(predictions["instances"]._fields.get('pred_boxes').tensor.tolist())

    # scores
    scores = np.array(predictions["instances"]._fields.get('scores').tolist())

    # labels
    labels = np.array(predictions["instances"]._fields.get('pred_classes').tolist())
    # classes
    classes = ['brownblight', 'algal', 'blister', 'sunburn','fungi_early', 'roller',
            'moth', 'tortrix', 'flushworm', 'caloptilia', 'mosquito_early', 'mosquito_late',
            'miner', 'thrips', 'tetrany', 'formosa', 'other']

    # print(labels)
    # print(bboxes)
    # print(classes)
    # print(scores)

    other_only = True # if contains other only
    if len(scores) != 0:
        for label in labels:
            if label != 16:
                other_only = False
                break

        if other_only:
            labels = np.array([])
            bboxes = np.array([])
            scores = np.array([])

        else:
            # remove other
            bboxes, scores, labels = zip(*((x, y, z) for x, y, z in zip(bboxes, scores, labels) if z != 16)) # other's label is 16
            bboxes = np.array(list(bboxes))
            scores = np.array(list(scores))
            labels = np.array(list(labels))
       
    return labels, bboxes, classes, scores

def demo(img_name, imgd):

    labels, bboxes, classes, scores = pred_img(img_name)
    #print('drawing box')

    colorfile = os.path.join(settings.BASE_DIR, 'imgUp/color.txt')
    colors = read_label_color(colorfile)

    i = draw_det_bboxes_A(img_name,
                        bboxes,
                        labels,
                        imgd,
                        colors=colors,
                        width=800,
                        class_names=classes,
                        score_thr=0.5,
                        out_file=img_name,
                        scores = scores)
    # visualized_output.save(img_name)

    return i



def draw_det_bboxes_A(img_name,
                        bboxes,
                        labels,
                        imgd,
                        colors,
                        width=None,
                        class_names=None,
                        score_thr=0.5,
                        out_file=None,
                        scores = None):
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

    ratio = width/ori_size[0]
    img = cv2.resize(img, (int(ori_size[1]*ratio),int(ori_size[0]*ratio)))
    
    # scores = bboxes[:, -1]

    # if score_thr > 0.0:
    #     assert bboxes.shape[1] == 5
    #     inds = scores > score_thr
    #     bboxes = bboxes[inds, :]
    #     labels = labels[inds]
    #     scores = scores[inds]

    # Pred = Prediction(img_name = str(imgd),
    #                     pred_num = labels.shape[0],
    #                     img = imgd)
    # Pred.save()

    imgd.pred_num = labels.shape[0]
    imgd.save()

    if labels.shape[0]==0 :
        write_det(imgd,
                box_id='',
                pred_cls='',
                score=0,
                bbox_int=None,
                nodet=True)

    ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i = 0
    if len(scores) != 0:
        for bbox, label, score in zip(bboxes, labels, scores):
            
            pred_cls = class_names[label]
            color = colors[pred_cls]
            box_id = ABC[i]
            
            bbox = bbox*ratio
            bbox_int = bbox.astype(np.int32)

            write_det(imgd,
                    box_id,
                    pred_cls,
                    score,
                    bbox_int)
            
            left_top = (bbox_int[0], bbox_int[1])
            right_bottom = (bbox_int[2], bbox_int[3])
            
            cv2.rectangle(img, (left_top[0], left_top[1]),
                        (right_bottom[0], right_bottom[1]), color, 4)
            text_size, baseline = cv2.getTextSize(box_id,
                                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, 2)
            p1 = (left_top[0], left_top[1] + text_size[1])
            cv2.rectangle(img, tuple(left_top), (p1[0] + text_size[0], p1[1]+1 ), color, -1)
            cv2.putText(img, box_id, (p1[0], p1[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255,255,255), 2, 8)
            
            i += 1
        
    print('done   '+ str(out_file))
    
    if out_file is not None:
        imwrite(img, out_file)
    return i



def write_det(Img, box_id, pred_cls, score, bbox_int, nodet=False):
    if nodet:
        pred_id = str(Img) + '_N'
        det = Detection(
            pred_id = pred_id,
            img_name = os.path.basename(Img.img_url.url),
            img_data = Img,
            box_id = box_id,
            pred_cls = 'NaN',
            html_file = 'blank',
            score = score,
            xmin = 0,
            ymin = 0,
            xmax = 0,
            ymax = 0,
            context = '未偵測到病蟲害 No tea pest detected',
        )
        det.save()
    else:
        table = {
            'brownblight': ['赤葉枯病', 'Brown blight'],
            'fungi_early': ['真菌性病害_早期', 'Fungi disease -early'],
            'blister': ['茶餅病', 'Blister blight'],
            'algal': ['藻斑病', 'Algal leaf spot'],
            'miner': ['潛葉蠅', 'Tea leaf miner'],
            'thrips': ['薊馬', 'Tea thrips'],
            'roller': ['茶捲葉蛾', 'Oriental tea tortrix'],
            'mosquito_late': ['盲椿象_晚期', 'Tea mosquito bug -late'],
            'mosquito_early': ['盲椿象_早期', 'Tea mosquito bug -early'],
            'moth': ['茶姬捲葉蛾', 'Small tea tortrix'],
            'tortrix': ['茶姬捲葉蛾', 'Small tea tortrix'],
            'flushworm': ['黑姬捲葉蛾', 'Tea flushworm'],
            'formosa': ['小綠葉蟬', 'Jacobiasca formosana'],
            'caloptilia' : ['茶細蛾', 'Caloptilia roller'],
            'tetrany': ['蟎類', 'Tetrany'],
            'sunburn': ['日燒症', 'Sunburn'],
            'other': ['其他', 'other'],
        }

        htable = {
            'brownblight': 'brownblight',
            'fungi_early': 'fungi_early',
            'blister': 'blister',
            'algal': 'algal',
            'miner': 'miner',
            'thrips':'thrips',
            'roller': 'roller',
            'mosquito_late': 'mosquito',
            'mosquito_early': 'mosquito',
            'moth': 'tortrix',
            'tortrix': 'tortrix',
            'flushworm': 'flushworm',
            'formosa': 'formosa',
            'caloptilia' : 'caloptilia',
            'tetrany':'tetrany',
            'sunburn':'sunburn',
            'other':'other'
        }

        pred_id = str(Img) + '_' + box_id

        context = '{:s}: {:s} {:s}, score: {:.3f}'.format(box_id, *table[pred_cls], score)
        print(context)
        det = Detection(
            pred_id = pred_id,
            img_name = os.path.basename(Img.img_url.url),
            img_data = Img,
            box_id = box_id,
            pred_cls = pred_cls,
            html_file = htable[pred_cls],
            score = score,
            xmin = bbox_int[0],
            ymin = bbox_int[1],
            xmax = bbox_int[2],
            ymax = bbox_int[3],
            context = context,
        )
        det.save()