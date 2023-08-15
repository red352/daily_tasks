import smtplib

import requests
from urllib3.exceptions import InsecureRequestWarning
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == '__main__':
    msg_from = '3502913960@qq.com'
    passwd = 'hnmadfnhdbyndaib'

    params = [
        {
            "email": "shuffling36@gmail.com",
            "passwd": "red123456"
        },
        {
            "email": "3502913960@qq.com",
            "passwd": "4h7trn6.pyPs9YR"
        },

        {
            "email": "1615703120@qq.com",
            "passwd": "lxc1615703120"
        }
    ]
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
