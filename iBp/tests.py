from django.test import TestCase

# Create your tests here.


# from django.test import Client
# >>> c = Client()
# >>> response = c.post('/login/', {'username': 'john', 'password': 'smith'})
# >>> response.status_code
# 200
# >>> response = c.get('/customer/details/')
# >>> response.content


# def json_test():

#     img_name = '0721192833.jpg'
#     img = 'media/test/' + img_name
#     img64 = image_to_base64(img)
#     img64 = str(img64, encoding='utf-8')
#     json_recieve = {
#         "dataTime": "2020-08-21 12:43:45", # 影像的時間ID :"2019-11-03 21:43:45"
#         "Image": img64,   # 需預測的影像 base64 編碼
#     }
#     ret1 = json.dumps(json_recieve)
#     with open('recieve.json', 'w') as fp:
#         fp.write(ret1)

    
#     demoIBP('recieve.json')