"""
抓包分析的登陆逻辑，照它的逻辑发请求即可。
验证码用的打码平台
各个步骤的参数都有的获取
"""
import pickle
import random
import re
import requests
import time

import urllib3
from urllib.parse import urljoin

from cjy import ChaojiyingClient

urllib3.disable_warnings()
# 新的页面跳转response会有set-cookies，都给存下来，否则只取最后post请求的cookies值，不全
cookie_dict = {}

headers = {
    'referer': 'https://www.javbus.com/forum/forum.php',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

# 登陆页面url
login_web_url = 'https://www.javbus.com/forum/member.php?mod=logging&action=login&referer=%2F%2Fwww.javbus.com%2Fstar%2F6xe'

session = requests.session()
session.headers = headers
session.verify = False

login_web = session.get(url=login_web_url)
for cookie in login_web.cookies:
    cookie_dict[cookie.name] = cookie.value
REGEX_IDHASH = re.compile(r'.*?>updateseccode\(\'(.*?)\',')
REGEX_LOGIN_ACTION = re.compile(r'action="(.*?)"')
REGEX_FORMHASH = re.compile(r'formhash.*?value="(.*?)"')
idhash = REGEX_IDHASH.findall(login_web.text)[0]
login_action = ''.join(REGEX_LOGIN_ACTION.findall(login_web.text)[0].split('amp;'))
form_hash = REGEX_FORMHASH.findall(login_web.text)[0]

# 动态插入验证码的url
sec_code_url = f'https://www.javbus.com/forum/misc.php?mod=seccode&action=update&idhash={idhash}&{random.random()}&modid=member::logging'
session.headers['referer'] = login_web_url
sec_code_text = session.get(url=sec_code_url).text
REGEX_SECCODE = re.compile(r'<span id=.*?<img.*?height.*?src="(.*?)".*?span>')
sec_code_source_path = REGEX_SECCODE.findall(sec_code_text)[0]  # 提取出验证码的资源path

# 获取验证码图片
sec_code_img_url = urljoin('https://www.javbus.com/forum/', sec_code_source_path)   # 构造完整的验证码url
session.headers['referer'] = sec_code_url

sec_code_img_bytes = session.get(url=sec_code_img_url).content
# 将验证码存到本地
with open('seccode_normal.png', 'wb') as f:
    f.write(sec_code_img_bytes)

# 超级鹰打码
chaojiying = ChaojiyingClient('超级鹰账号', '超级鹰密码', 'soft_id')
im = open('seccode_normal.png', 'rb').read()
sec_code_value = chaojiying.PostPic(im, 1902).get('pic_str')    # 识别的验证码值

# 网站验证，输完验证码，input失去焦点会发送这个ajax请求验证
check_seccode_url = f'https://www.javbus.com/forum/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash={idhash}&secverify={sec_code_value}'
session.headers['referer'] = login_web_url

check_result = session.get(check_seccode_url)
is_success = re.search(r'succeed', check_result.text)
if is_success:
    print("验证通过")
else:
    print("验证失败")

# 登陆
login_url = urljoin('https://www.javbus.com/forum/', login_action)
form_data = {
    'formhash': form_hash,  # 登陆页面有的提取
    'referer': '//www.javbus.com/',
    'loginfield': 'username',
    'username': '论坛账号',    # 账号
    'password': '论坛密码',   # 密码
    'questionid': 0,
    'answer': '',
    'seccodehash': '',
    'seccodemodid':'member::logging',
    'seccodeverify': sec_code_value # 验证码
}

response = session.post(url=login_url, data=form_data)

time.sleep(random.randint(5, 9))
for cookie in response.cookies:
    cookie_dict[cookie.name] = cookie.value

print(cookie_dict)
pickle.dump(cookie_dict, open('javbus_normal.cookie', 'wb'))