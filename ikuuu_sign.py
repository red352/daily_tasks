import smtplib
from os import environ

import requests
from urllib3.exceptions import InsecureRequestWarning
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def is_blank(s):
    return not s or s.strip() == ''


if __name__ == '__main__':
    # 环境变量必填,可以置空但必填,数组以 `,`分割,以下示例值
    # EMAIL xxx@qq.com qq邮件地址
    # EMAIL_PWD xxxx qq邮件密码
    # TARGET_DOMAIN https://xxxx.com 签到ikuuu域名
    # LOGIN_EMAILS xxx@qq.com,sss@qq.com,sof@qq.com 签到的账号们
    # LOGIN_PASSWDS xxx,sss,ppp 签到的密码们
    # LOGIN_EMAILS_NOTIFY xxx,,xxx 账号通知的邮箱们

    msg_from = environ.get("EMAIL")
    passwd = environ.get("EMAIL_PWD")
    target_domain = environ.get("TARGET_DOMAIN")
    emails = environ.get('LOGIN_EMAILS').split(',')
    passwds = environ.get('LOGIN_PASSWDS').split(',')
    emails_to_notify = environ.get('LOGIN_EMAILS_NOTIFY').split(',')
    params = [{'email': a, 'passwd': b} for a, b in zip(emails, passwds)]
    notify_map = dict(zip(emails, emails_to_notify))
    print(params)
    request = requests.session()

    for param in params:
        if is_blank(param['email']) or is_blank(param['passwd']):
            continue
        msg = MIMEMultipart()
        re = request.post(url=target_domain + '/auth/login', params=param, verify=False)
        print(re.json()['msg'])
        msg.attach(MIMEText(re.json()['msg'] + '\r\n', 'plain', 'utf-8'))
        re = request.post(url=target_domain + '/user/checkin', verify=False)
        try:
            print(re.json())
        except Exception as e:
            msg.attach(MIMEText('签到出错' + '\r\n', 'plain', 'utf-8'))
            continue
        if re.json()['ret'] == 1:
            re = request.get(url=target_domain + '/user/logout', verify=False)
            print('已退出账号')
            msg.attach(MIMEText('已退出账号', 'plain', 'utf-8'))
        msg['Subject'] = 'ikuuu 每日流量签到提醒'
        msg['From'] = msg_from
        s = smtplib.SMTP_SSL('smtp.qq.com', 465)
        s.login(msg_from, passwd)
        email_to_notify = notify_map[param['email']]
        if is_blank(email_to_notify):
            email_to_notify = param['email']
        s.sendmail(msg_from, email_to_notify, msg.as_string())
        print(f'邮件发送成功:{msg_from}  ---> {param["email"]}')
        print('已退出账号')
