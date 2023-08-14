import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == '__main__':
    request = requests.session()
    params = {
        "email": "shuffling36@gmail.com",
        "passwd": "red123456"
    }
    re = request.post(url='https://ikuuu.art/auth/login', params=params, verify=False)
    print(re.cookies)
    re = request.post(url='https://ikuuu.art/user/checkin', verify=False)
    print(re.json())
    re = request.get(url='https://ikuuu.art/user/logout', verify=False)
    print(re.cookies)
    print("退出登入")
