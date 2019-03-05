import requests
from pyquery import PyQuery as pq
from PIL import Image
import csv

# 初始信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
}

username = '******'    # 账号
password = '******'    # 密码

login_url = 'http://202.200.112.210/Default2.aspx'
url_1 = 'http://202.200.112.210/xs_main.aspx?xh=' + username
url_get_kaoshi = 'http://202.200.112.210/xskscx.aspx?xh=' + username + '&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121604'

# 获取验证码、参数
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

Image.open('captcha.jpg').show()
    
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
response3 = session.get(url_1, headers=headers)

if response3.status_code == 200:
    headers2 = {
        'Connection': 'keep-alive',
        'Upgrade-insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Referer':'http://202.200.112.210/xs_main.aspx?xh=3170932008',
        'DNT':'1'
    }
    response4 = session.get(url_get_kaoshi, headers=headers2)
    doc2 = pq(response4.text)
    trs = doc2.find('#DataGrid1 tr').items()

    # 源码中表格数据的处理
    uli = []
    for tr in trs:
        ui = []
        tds = tr.find('td').items()
        for td in tds:
            ui.append(td.text())
        uli.append(ui)
    with open('kaoshi.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(len(uli)):
            writer.writerow([uli[i][0], uli[i][1], uli[i][2], uli[i][3], uli[i][4], uli[i][6], uli[i][7]])
    if uli: print('写入成功')
else:
    print('登录失败')
    
