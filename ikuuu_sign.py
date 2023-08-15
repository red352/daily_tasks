import smtplib
import os

import requests
from urllib3.exceptions import InsecureRequestWarning
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == '__main__':
    msg_from = os.environ.get("USER_EMAIL")
    passwd = os.environ.get("EMAIL_PWD")

    params = [
        {
            "email": os.environ.get("GMAIL_SHUFFLING36"),
            "passwd": os.environ.get("GMAIL_SHUFFLING36_PWD_IKUUU")
        },
        {
            "email": os.environ.get("USER_EMAIL"),
            "passwd": os.environ.get("USER_PASSWORD")
        },

        {
            "email": os.environ.get("QQ_1615703120"),
            "passwd": os.environ.get("QQ_1615703120_PWD_IKUUU")
        }
    ]
    print(os.environ)
    print(params)
    request = requests.session()

    for param in params:
        msg = MIMEMultipart()
        re = request.post(url='https://ikuuu.art/auth/login', params=param, verify=False)
        print(re.json()['msg'])
        msg.attach(MIMEText(re.json()['msg'] + '\r\n', 'plain', 'utf-8'))
        re = request.post(url='https://ikuuu.art/user/checkin', verify=False)
        print(re.json())
        if re.json()['ret'] == 1:
            msg.attach(MIMEText(re.json()['msg'] + '\r\n', 'plain', 'utf-8'))
            re = request.get(url='https://ikuuu.art/user/logout', verify=False)
            print('已退出账号')
            msg.attach(MIMEText('已退出账号', 'plain', 'utf-8'))
            msg['Subject'] = 'ikuuu 每日流量签到提醒'
            msg['From'] = msg_from
            s = smtplib.SMTP_SSL('smtp.qq.com', 465)
            s.login(msg_from, passwd)
            if param['email'].__eq__('shuffling36@gmail.com'):
                param['email'] = '1829462342@qq.com'
            s.sendmail(msg_from, param['email'], msg.as_string())
            print(f'邮件发送成功:{msg_from}  ---> {param["email"]}')
            continue
        re = request.get(url='https://ikuuu.art/user/logout', verify=False)
        print('已退出账号')
