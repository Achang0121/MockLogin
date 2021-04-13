"""
selenium+chromedriver+打码平台 模拟登陆
简洁明了，还不操心
"""

import pickle
import time

from PIL import Image
from selenium import webdriver
from cjy import ChaojiyingClient

# 登陆页面url
login_web_url = 'https://www.javbus.com/forum/member.php?mod=logging&action=login&referer=%2F%2Fwww.javbus.com%2Fstar%2F6xe'


# 用selenium+chromewebdirver做了，上面的也能登陆成功，但是有个重定向很麻烦
browser = webdriver.Chrome()
browser.maximize_window()
browser.get(login_web_url)
browser.find_element_by_xpath(
    '//form[@name="login"]//input[@name="username"]').send_keys('论坛账号')
browser.find_element_by_xpath(
    '//form[@name="login"]//input[@name="password"]').send_keys('论坛密码')
time.sleep(5)
seccode_element = browser.find_element_by_xpath(
    '//span[contains(@id, "vseccode")]/img')

# 截屏
browser.get_screenshot_as_file('whole_web.png')
left = int(seccode_element.location['x'])
top = int(seccode_element.location['y'])
right = int(seccode_element.location['x'] + seccode_element.size['width'])
bottom = int(seccode_element.location['y'] + seccode_element.size['height'])

# Image处理
im = Image.open('whole_web.png')
im = im.crop((2*left, 2*top, 2*right, 2*bottom))    # 这里是13寸mac的缩放，这也是我讨厌用selenium的地方
im.save('seccode.png')

# 超级鹰打码（需要改动的地方）
chaojiying = ChaojiyingClient('超级鹰账号', '超级鹰密码', 'soft_id')
im = open('seccode.png', 'rb').read()
sec_code_value = chaojiying.PostPic(im, 1902).get('pic_str')

browser.find_element_by_xpath(
    '//form[@name="login"]//input[@name="seccodeverify"]').send_keys(sec_code_value)

browser.find_element_by_xpath(
    '//form[@name="login"]//button[@name="loginsubmit"]').click()

# 登陆成功后，会有个重定向，等跳转后再获取cookies
time.sleep(60)

cookies = browser.get_cookies()
print(cookies)
pickle.dump(cookies, open('javbus_sc.cookie', 'wb'))
browser.close()