import requests
from pyquery import PyQuery as pq
import time
import csv

#初始信息
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Host':' *************** '
}
username='*********'
password='*********'
login_url='http://202.200.112.202/(e30ego55rerta245paemxj2f)/Default2.aspx'
url_1='http://202.200.112.202/(3cw4ei553wrqxz452v5goyu3)/xs_main.aspx?xh='+username
url_get_kaoshi='http://202.200.112.202/(3cw4ei553wrqxz452v5goyu3)/xskscx.aspx?xh='+username+'&xm=%C1%F5%D7%E6%B7%E5&gnmkdm=N121604'

#获取验证码
session=requests.Session()
response1=session.get(login_url,headers=headers)
text=response1.text
doc=pq(text)
get_captcha_src=doc.find('#icode').attr('src')
captcha_url='http://202.200.112.202/(1h1db2zpz2plj045fc0fxl55)/'+get_captcha_src
captcha=session.get(captcha_url).content

#保存验证码
with open('e://captcha.jpg','wb') as f:
    f.write(captcha)
    
#手动输入验证码
input('Enter the captcha:')

#登录过程
post_data={
    '_VIEWSTATE':'dDwtNTE2MjI4MTQ7Oz7kJtcAf+3Zb+DIk24ttW3XepgK9Q==',
    'Button1':'',
    'hidpdis':'',
    'hidsc':'',
    'IbLanguage':'',
    'RadioButtonList1':'%D1%A7%C9%FA',
    'Textbox1':'',
    'TextBox2':password,
    'txtSecretCode':captcha,
    'txtUserName':username
}
time.sleep(2)
response2=session.post(login_url,headers=headers,data=post_data)
response3=session.get(url_1,headers=headers)
if response3.status_code==200:
    headers2={
        'Connection':'keep-alive',
        'Host':'*****************',
        'Upgrade-insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    response4=session.get(url_get_kaoshi,headers=headers2)
    doc2=pq(response4.text)
    trs=doc2.find('#DataGrid1 tr').items()

#源码中表格数据的处理
    uli=[]
    for tr in trs:
        ui=[]
        tds=tr.find('td').items()
        for td in tds:
            ui.append(td.text())
        uli.append(ui)
    print(uli)
    with open('e://kaoshi.csv','w') as f:
        writer=csv.writer(f)
        for i in range(len(uli)):
            writer.writerow([uli[i][0],uli[i][1],uli[i][2],uli[i][3],uli[i][4],uli[i][6],uli[i][7]])
    if uli:print('写入成功')
    print('写入失败')
else:print('登录失败')
