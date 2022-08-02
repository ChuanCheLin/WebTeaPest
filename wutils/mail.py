from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.conf import settings
from TeaData.models import Person
'''
Title: 病蟲害辨識系統每周回報

username 您好:

本信件為茶葉病蟲害辨識系統每周報告，由系統自動發出。

以下連結為本周(week)所收到之使用者誤判回報及目前未處理之回報

本周回報列表:
http://140.112.183.138:1007/admin/imgUp/feedback/?date__gte=begin&date__lt=settle

未處理之回報列表:
http://140.112.183.138:1007/admin/imgUp/feedback/?finishCheck__exact=0

謝謝您~
'''

from_email = settings.DEFAULT_FROM_EMAIL

def mailform(user, week, begin, settle):

    with open('/home/ssl/WebTeaPest/wutils/mailsample.txt', 'r') as t:
        text = t.read()

    text = text.replace('username', user)
    text = text.replace('week', week)
    text = text.replace('begin', begin)
    text = text.replace('settle', settle)
    
    return text


def sendSimpleEmail(subject, text, mailTo):
    
    res = send_mail(subject, text, from_email, mailTo)
    return HttpResponse('%s'%res)  

def sendAttachEmail(subject, text, mailTo, attach):
    print(mailTo)
    msg = EmailMessage(subject, text, from_email, mailTo)
    msg.attach_file(attach)
    msg.send()

def getUserData():
    names = []
    mails = []
    p_data = Person.objects.filter(recieve_report=True)
    
    if len(p_data) == 0:
        return names, mails
    else:
        for p in p_data:
            names.append(p.name)
            mails.append(p.email)
        return names, mails
    



# u = '研究員'
# w = '01/01-01/07'
# b = '2020-01-01'
# s = '2020-01-07'
# test = mailform(u, w, b, s)

# print(test)