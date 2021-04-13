import requests
import pickle

headers  = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

cookies = pickle.load(open('javbus_normal.cookie', 'rb'))
print(cookies)
# cookie_dict = {}
# for cookie in cookies:
#     cookie_dict[cookie['name']] = cookie['value']

response = requests.get(url='https://www.javbus.com/forum/forum.php', cookies=cookies, verify=False)
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(response.text)