import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == '__main__':
    request = requests.session()
    params = [
        {
            "email": "shuffling36@gmail.com",
            "passwd": "red123456"
        },
        {
            "email": "3502913960@qq.com",
            "passwd": "4h7trn6.pyPs9YR"
        }
    ]
    for param in params:
        re = request.post(url='https://ikuuu.art/auth/login', params=param, verify=False)
        print(re.cookies)
        re = request.post(url='https://ikuuu.art/user/checkin', verify=False)
        print(re.json())
        re = request.get(url='https://ikuuu.art/user/logout', verify=False)
        print(re.cookies)
        print("退出登入")
