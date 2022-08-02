from django.db import models
from datetime import datetime
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
from smart_selects.db_fields import GroupedForeignKey
from TeaData.models import County, City

import os
    


def custum_path(instance, filename):
    """
    image upload directory setting
    e.g)
        img/{year-month-day-uuid}
        img/2020-12-10-167943.png
    """

    now = datetime.now()
    new_filename = "{date}-{microsecond}{extension}".format(
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[-1],
    )

    path = "img/{filename}".format(
        filename=new_filename,
    )

    return path



# Create your models here.
class Img(models.Model):

    img_id = models.CharField(max_length=100, default='unknow', help_text='image name of the prediction')
    img_url = models.ImageField(upload_to=custum_path)
    date = models.DateTimeField(default=datetime.now)
    pred_num = models.IntegerField(default=0)


    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    city = GroupedForeignKey(City, "County", null=True,  on_delete=models.SET_NULL)

    # county = models.CharField(max_length=100, null=True, help_text='拍攝地 ex. 新北市')
    # region = models.CharField(max_length=100, null=True, help_text='拍攝地 ex. 坪林區')
    altitude = models.CharField(max_length=20, blank=True, help_text='海拔高度')
    gps = models.CharField(max_length=30, blank=True, help_text='gps 位址')

    class Meta:
        ordering = ['-date']
        get_latest_by = "date"

    def __str__(self):
        return str(self.img_id)
    
    @property
    def image_preview(self):
        if self.img_url:
            thumbnail = get_thumbnail(self.img_url,
                                   '300x300',
                                   upscale=False,
                                   crop=False,
                                   quality=100)
            # print(thumbnail.url)
            try:
                return format_html('<img src="{}" width="{}" height="{}">'.format(thumbnail.url, thumbnail.width, thumbnail.height))
            except:
                return format_html('<img src="../../../media/noimg.jpg" width="225">')
        return ""




# class Prediction(models.Model):
#     '''
#     img_name = '0001.jpg'
#     pred_num = 5
#     img = img
#     '''
#     img_name = models.CharField(max_length=100, help_text='image name of the prediction')
#     pred_num = models.IntegerField()
#     img = models.OneToOneField(Img, on_delete=models.CASCADE)

#     class Meta:
#         ordering = ['img']

#     def __str__(self):
#         return self.img_name

class Detection(models.Model):
    '''
    store three highest pred result
    pred_id = '0001_A'
    img_name = '0001.jpg'
    box_id = 'A'
    pred_cls = 'brownblight' 
    score = 0.995
    pred_box = [100,100,200,200]
    context = 'A: brownblight score: 0.995'
    feedback = '判別錯誤'
    '''
    
    pred_id = models.CharField(max_length=100, primary_key=True)
    img_name = models.CharField(max_length=100, null=True)
    img_data = models.ForeignKey(Img, null=True,  on_delete=models.CASCADE)
    
    box_id = models.CharField(max_length=1, help_text='ABCDE')
    pred_cls = models.CharField(max_length=20)
    html_file = models.CharField(max_length=20, null=True)
    score = models.FloatField()
    xmin = models.IntegerField()
    ymin = models.IntegerField()
    xmax = models.IntegerField()
    ymax = models.IntegerField()
    context = models.TextField(max_length=100, help_text='A: 赤葉枯病 score: 0.995')
    # feedback = models.TextField(max_length=100, null=True, blank=True, help_text='user feedback')

    class Meta:
        ordering = ['img_data', 'box_id']
    
    def __str__(self):
        return str(self.img_name).split('.')[0] + ' ' + self.context


issue = [
    ('wrong','病蟲害種類誤判'),
    ('background','背景或健康葉片被誤判'),
    ('nodetect', '病蟲害未被辨識'),
    ('other','其他'),
]

pest = [
    ('mosquito_early', 'tea mosquito-early'),
    ('mosquito_late','tea mosquito-late'),
    ('brownblight', 'brown blight'),
    ('fungi_early', 'fungi disease-early'),
    ('blister', 'blister blight'),
    ('algal', 'algal leaf spot'),
    ('miner', 'leaf miner'),
    ('thrips', 'tea thrips'),
    ('orient', 'oriental tea tortrix'),
    ('moth', 'small tea tortrix-bite'),
    ('tortrix',  'small tea tortrix-roll'),
    ('flushworm', 'tea flushworm'),
    ('not', 'not a disease'),
    ('unknown', 'unknown disease'),
]

class Feedback(models.Model):
    '''
    trueLabel: 原有13類、非病蟲害、未知病蟲害
    '''
    feedbackID = models.CharField(max_length=20,default='2011270122A')
    pred = models.ForeignKey(Detection, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    @property
    def image_preview(self):
        imgd = self.pred.img_data
        if imgd.img_url:
            thumbnail = get_thumbnail(imgd.img_url,
                                   '300x300',
                                   upscale=False,
                                   crop=False,
                                   quality=100)
            return format_html('<img src="{}" width="{}" height="{}">'.format(thumbnail.url, thumbnail.width, thumbnail.height))
        return ""
    @property
    def image_link(self):
        # home = 
        url = self.pred.img_data.img_url.url
        # return format_html('<a href="%s">%s</a>' % (url, url))
        return url

    issue = models.CharField(max_length=50, default='other', choices=issue)
    feedback = models.TextField(max_length=100, null=True, blank=True, help_text='user feedback')
    true_label = models.CharField(max_length=20, null=True, choices=pest)
    review = models.TextField(max_length=100, null=True, blank=True, help_text='profesional review')
    contact = models.EmailField(max_length=254, null=True, blank=True)
    finishCheck = models.BooleanField(default=False)


    class Meta:
        ordering = ['-date']
        get_latest_by = "date"

    def __str__(self):
        return str(self.pred)


