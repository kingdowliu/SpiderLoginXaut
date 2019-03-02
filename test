import requests
from pyquery import PyQuery as pq
from urllib import parse
from PIL import Image
import time
import csv

# 初始信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
}

username = '******'
password = '******'

login_url = 'http://202.200.112.210/Default2.aspx'
url_1 = 'http://202.200.112.210/xs_main.aspx?xh=' + username
url_get_kaoshi = 'http://202.200.112.210/xskscx.aspx?xh=' + username + '&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121604'

# 获取验证码
session = requests.Session()
response1 = session.get(login_url, headers=headers)
text = response1.text
doc = pq(text)
get_captcha_src = doc.find('#icode').attr('src')
_VIEWSTATE = doc.find('#form1 input').attr('value')
_VIEWSTATEGENERATOR = doc.find("#form1 input[name='__VIEWSTATEGENERATOR']").attr('value')

captcha_url = 'http://202.200.112.210/' + get_captcha_src
captcha = session.get(captcha_url).content

# 保存验证码
with open('captcha.jpg', 'wb') as f:
    f.write(captcha)

# 手动输入验证码
captcha = input('Enter the captcha:')

# 登录过程
post_data = {
    '__VIEWSTATE': _VIEWSTATE,
    '__VIEWSTATEGENERATOR':_VIEWSTATEGENERATOR,
    'Button1': '',
    'hidPdis': '',
    'hidsc': '',
    'IbLanguage': '',
    'RadioButtonList1': '%D1%A7%C9%FA',
    'Textbox1': '',
    'TextBox2': password,
    'txtSecretCode': captcha,
    'txtUserName': username
}

response2 = session.post(login_url, headers=headers, data=post_data)

course_ordered = session.get('http://202.200.112.210/xsxk.aspx?xh=3170932008&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121101',
                             headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
                                      'Upgrade-Insecure-Requests':'1',
                                      'DNT':'1',
                                      'Referer':'http://202.200.112.210/xs_main.aspx?xh=3170932008',
                                      'Cookie':'ASP.NET_SessionId=fgsrviuezma4jcmgjsgdys55'})

doc1 = pq(course_ordered.text)

_VIEWSTATE1 = doc1.find("#xsxk_form input[name='__VIEWSTATE']").attr('value')
_VIEWSTATEGENERATOR1 = doc1.find("#xsxk_form input[name='__VIEWSTATEGENERATOR']").attr('value')
zymc = parse.quote(doc1.find("#zymc").attr('value'), encoding='gb2312')

tmp = session.post(url='http://202.200.112.210/xsxk.aspx?xh=3170932008&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121101',
                   headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
                            'Upgrade-Insecure-Requests':'1',
                            'DNT':'1',
                            'Referer':'http://202.200.112.210/xsxk.aspx?xh=3170932008&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121101',
                            'Cookie':'ASP.NET_SessionId=fgsrviuezma4jcmgjsgdys55'},
                   data={'__EVENTTARGET':'',
                        '__EVENTARGUMENT':'',
                        '__VIEWSTATE':_VIEWSTATE1,
                         '__VIEWSTATEGENERATOR':_VIEWSTATEGENERATOR1,
                        'zymc':zymc,
                         'xx':'',
                         'Button2':'%D0%A3%BC%B6%D1%A1%D0%DE%BF%CE'})


doc2 = pq(tmp.text)
_VIEWSTATE2 = doc2.find("#xsxk_form input[name='__VIEWSTATE']").attr('value')

response3 = session.post(url='http://202.200.112.210/xsxk.aspx?xh=3170932008&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121101',
                         headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
                                  'Upgrade-Insecure-Requests':'1',
                                  'Referer':'http://202.200.112.210/xsxk.aspx?xh=3170932008&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121101',
                                  'DNT':'1'},
                                  #'Cookie':'ASP.NET_SessionId=fgsrviuezma4jcmgjsgdys55'},
                         data={'__EVENTTARGET':'zymc',
                               '__EVENTARGUMENT':'',
                               '__VIEWSTATE':_VIEWSTATE2,
                               '__VIEWSTATEGENERATOR':_VIEWSTATEGENERATOR1,
                               'zymc':'%C8%AB%B2%BF%7C%7C%D1%A1%D0%DE%BF%CE5',
                               'xx':''})
data={'__EVENTTARGET':'zymc','__EVENTARGUMENT':'','__VIEWSTATE':_VIEWSTATE2,'__VIEWSTATEGENERATOR':_VIEWSTATEGENERATOR1,'zymc':'%C8%AB%B2%BF%7C%7C%D1%A1%D0%DE%BF%CE5','xx':''}

print(data)

print(response3)
