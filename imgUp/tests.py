from django.test import TestCase

# Create your tests here.

image_file = open(r'C:\Users\99116\Desktop\James\images\0082.jpg', 'rb')

def ibp_test():

    input_json = {
    "dataTime": "2020-08-21 12:43:45", # 影像的時間ID :"2019-11-03 21:43:45"
    # "Image": image_file,   # 需預測的影像    
    }

    requests.post("140.112.183.138:1007/iBpInterface/",files=image_file, data=input_json)
