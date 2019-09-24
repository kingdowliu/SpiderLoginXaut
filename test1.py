import requests
from pyquery import PyQuery as pq
from PIL import Image
from urllib import parse
import csv
import time
import re
import json


class XAUT(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
        }
        self.username = '**********'  # 学号
        self.password = '**********'  # 密码
        self.name = ''
        self.url_base = 'http://202.200.112.210/'
        self.raw_url = self.url_base + 'default2.aspx'
        self.url_1 = ''
        self.login_url = ''
        self.real_url = ''
        self.session = requests.Session()

        self.get_real_url()
        self.login()

    def get_real_url(self):
        response1 = self.session.get(self.raw_url, headers=self.headers)
        self.login_url = response1.url
        self.real_url = re.match('(.*)\/default2.aspx', self.login_url).group(1)
        self.url_1 = self.real_url + '/xs_main.aspx?xh=' + self.username
        # print(self.real_url)
        # print(self.login_url)
        # print(self.url_1)

    def login(self):
        response2 = self.session.get(self.login_url, headers=self.headers)
        text = response2.text
        doc = pq(text)
        get_captcha_src = doc.find('#icode').attr("src")
        _VIEWSTATE = doc.find('#form1 input').attr("value")
        _VIEWSTATEGENERATOR = doc.find("#form1 input[name='__VIEWSTATEGENERATOR']").attr('value')

        captcha_url = self.real_url + '/' + get_captcha_src
        captcha = self.session.get(captcha_url).content

        # 保存验证码
        with open('captcha.jpg', 'wb') as f:
            f.write(captcha)

        Image.open('captcha.jpg').show()

        # 手动输入验证码
        captcha = input('Enter the captcha:')

        # 登录过程
        post_data = {
            '__VIEWSTATE': _VIEWSTATE,
            '__VIEWSTATEGENERATOR': _VIEWSTATEGENERATOR,
            'Button1': '',
            'hidPdis': '',
            'hidsc': '',
            'IbLanguage': '',
            'RadioButtonList1': '%D1%A7%C9%FA',
            'Textbox1': '',
            'TextBox2': self.password,
            'txtSecretCode': captcha,
            'txtUserName': self.username
        }

        response3 = self.session.post(self.login_url, headers=self.headers, data=post_data)
        self.name = pq(response3.text).find('#xhxm').text().replace('同学', '')
        if '欢迎您：' in response3.text:
            print('登录成功！', self.name)
        else:
            print('登录失败！')

    def querySchedule(self):
        '''
        课表查询
        :return: table
        '''
        url_schedule = self.url_base + 'xskbcx.aspx?xh=' + self.username + '&xm='+ parse.quote(self.name) + '&gnmkdm=N121603'
        response_schedule = self.session.get(url=url_schedule, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Referer': self.url_1
        })
        return pq(response_schedule.text).find('#Table1')


    def qk(self):
        self.get_real_url()
        self.login()
        course_ordered = self.session.get(
            self.real_url + '/xsxk.aspx?xh=' + self.username + '&xm=' + self.name + '&gnmkdm=N121101',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
                     'Upgrade-Insecure-Requests': '1',
                     'DNT': '1',
                     'Referer': self.real_url + '/xs_main.aspx?xh=' + self.username}
            )

        doc1 = pq(course_ordered.text)
        _VIEWSTATE1 = doc1.find("#xsxk_form input[name='__VIEWSTATE']").attr('value')
        _VIEWSTATEGENERATOR1 = doc1.find("#xsxk_form input[name='__VIEWSTATEGENERATOR']").attr('value')
        zymc = parse.quote(doc1.find("#zymc").attr('value'), encoding='gb2312')

        tmp = self.session.post(
            url=self.real_url + '/xsxk.aspx?xh=' + self.username + '&xm=' + self.name + '&gnmkdm=N121101',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
                'Upgrade-Insecure-Requests': '1',
                'DNT': '1',
                'Referer': self.real_url + '/xsxk.aspx?xh=' + self.username + '&xm=' + self.name + '&gnmkdm=N121101',
            },
            data={'__EVENTTARGET': '',
                  '__EVENTARGUMENT': '',
                  '__VIEWSTATE': _VIEWSTATE1,
                  '__VIEWSTATEGENERATOR': _VIEWSTATEGENERATOR1,
                  'zymc': zymc,
                  'xx': '',
                  'Button2': '%D0%A3%BC%B6%D1%A1%D0%DE%BF%CE'})
        doc2 = pq(tmp.text)
        _VIEWSTATE2 = doc2.find("#xsxk_form input[name='__VIEWSTATE']").attr('value')

        data = {'__EVENTTARGET': 'zymc',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': _VIEWSTATE2,
                '__VIEWSTATEGENERATOR': _VIEWSTATEGENERATOR1,
                'zymc': '%C8%AB%B2%BF%7C%7C%D1%A1%D0%DE%BF%CE5',
                'xx': ''}

        time.sleep(3.3)

        response3 = self.session.post(
            url=self.real_url + '/xsxk.aspx?xh=' + self.username + '&xm=' + self.name + '&gnmkdm=N121101',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
                     'Upgrade-Insecure-Requests': '1',
                     'Referer': self.real_url + '/xsxk.aspx?xh=' + self.username + '&xm=' + self.name + '&gnmkdm=N121101',
                     'DNT': '1',
                     'Host': '202.200.112.246',
                     'Content-Type': 'application/x-www-form-urlencoded'}, data=json.dumps(data))
        print(response3.text)
        print(response3.status_code)


if __name__ == '__main__':
    ob = XAUT()
    # ob.qk()
    ob.querySchedule()

