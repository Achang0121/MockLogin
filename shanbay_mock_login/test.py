import pickle
import re
import requests

cookies = pickle.load(open('./shanbay.cookies', 'rb'))

headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'referer': 'https://web.shanbay.com/web/account/login/'
}

response = requests.get(url='https://www.shanbay.com/', cookies=cookies, verify=False, headers=headers)
# print(response.text)
regex = re.compile(r'.*?"/web/users/mine/zone">(.*?)</a></li>.*?')
assert regex.findall(response.text)[0] == "我的空间"