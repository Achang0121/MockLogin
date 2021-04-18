import pickle
import time
from selenium import webdriver


browser = webdriver.Chrome()

browser.get('https://passport.58.com/login')
browser.find_element_by_xpath('//input[@id="mask_body_item_username"]').send_keys('account')
browser.find_element_by_xpath('//input[@id="mask_body_item_newpassword"]').send_keys('password')
browser.find_element_by_xpath('//button[@id="mask_body_item_login"]').click()

time.sleep(10)

cookies = browser.get_cookies()
pickle.dump(cookies, open('58tc.cookies', 'wb'))
