# 模拟登陆集合

> notice： 这里的chromedriver，个人放在了virtualenv的bin目录中，所以并未指定路径。

👀 [某8同城的模拟登陆](https://github.com/Achang0121/MockLogin/blob/main/58tc_mock_login/58tc_mock_login.py)

老牌大型生活服务类的网站，现在个人不大用了。广告简直丧心病狂🤔️，虚假信息不少，也不知道为啥。

登陆退出太频繁会被检测为异常。此时需要发送手机短信验证码来解除异常。

目前只用了selenium+chromedriver来登陆，先实现登陆，获取cookies，然后如果有必要再罗列加密参数还原post请求过程，不走selenium这条路。

---

🔞 [javbus_mock_login](https://github.com/Achang0121/MockLogin/tree/main/javbus_mock_login) 

这个为了登陆而登陆的，不登陆的话并不影响我抓该站的数据。

实现了两种登陆方式：

- [POST请求登陆](https://github.com/Achang0121/MockLogin/blob/main/javbus_mock_login/javbus_login_normal.py)
- [Selenium+ChromeDriver登陆](https://github.com/Achang0121/MockLogin/blob/main/javbus_mock_login/javbus_login_selenium_chromedriver.py)

---
👀 [wallhaven_mock_login](https://github.com/Achang0121/MockLogin/blob/main/wallhaven_mock_login/login.py)

这个网站资源丰富，而且是否登陆看得到的资源全然不一样。

这个只写了post请求登陆。

登陆流程比较简单，没什么参数，只有一个`_token`，请求也不复杂，验证码也没有。

---
