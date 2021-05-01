import pickle
import random
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 修改内容
USERNAME = 'account'
PASSWORD = 'password'

URL = 'https://web.shanbay.com/web/account/login/'


class ShanbayMockLogin:
    def __init__(self):
        self.url = URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD
    
    def login(self):
        """完整的登陆逻辑"""
        self.browser.get(self.url)
        # webdriver被识别，同一个窗口，同一个标签页这么做
        script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
        self.browser.execute_script(script)

        # 输入账号密码
        user_input = self.wait.until(EC.presence_of_element_located((By.ID, 'input-account')))
        self.input_message(self.username, user_input)
        time.sleep(random.randint(2, 4))

        password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'input-password')))
        self.input_message(self.password, password_input)
        time.sleep(random.randint(2, 4))

        # 点击登陆
        self.wait.until(EC.element_to_be_clickable((By.ID, 'button-login'))).click()

        time.sleep(random.randint(2, 4))

        # 二次验证，滑动验证码，从左移动到最右边
        if self.is_captcha():
            distance = self.calc_move_distance()
            track = self.get_track(distance)
            slider = self.get_slider()
            self.move_slider(slider, track)
            self.wait.until(EC.element_to_be_clickable((By.ID, 'button-login'))).click()
        time.sleep(random.randint(2, 4))


        self.wait.until(EC.presence_of_element_located((By.ID, 'newsNum')))
        return self.browser.get_cookies()

    def input_message(self, message, input_obj):
        """
        输入信息，因为太快的话容易被识别，所以拆开了输入，中间加上随机的停顿间隔
        """
        for char in message:
            input_obj.send_keys(char)
            time.sleep(random.random())
    
    def is_captcha(self):
        """判断是否弹出验证码"""
        captcha = self.wait.until(EC.presence_of_element_located((By.ID, 'no-captcha-popup-container-wrapper')))
        return captcha

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.ID, 'nc_1_n1z')))
        return slider

    def calc_move_distance(self):
        """
        计算滑块的滑动距离
        :return: 滑块需要滑动的长度
        """
        nc_2_n1t = self.wait.until(EC.presence_of_element_located((By.ID, 'nc_1_n1t')))
        distance = nc_2_n1t.size['width'] - self.get_slider().size['width']
        return distance

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        高中物理，初始速度为0，加速度固定的直线运动，麻烦在不能太慢，或者顿挫明显
        """
        track = []
        a = 6400
        v = 0
        t = 0.1
        current = 0
        while current < distance:
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def move_slider(self, slider, tracks):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for track in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(random.random())
        ActionChains(self.browser).release().perform()
        

def main():
    sb_obj = ShanbayMockLogin()
    cookies =  sb_obj.login()
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    print(cookie_dict)
    pickle.dump(cookie_dict, open('./shanbay.cookies', 'wb'))


if __name__ == '__main__':
    main()