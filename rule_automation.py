from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import rule_automation_config as config
from time import sleep

browser = webdriver.Chrome()
browser.get('https://test.decisionlender.solutions/tci/#/auth/login/?returnTo=%2Fauth%2Flogin%2F')
browser.implicitly_wait(10)

compid = browser.find_element_by_id("companyid")
user = browser.find_element_by_id('username')
password = browser.find_element_by_id('password')

compid.send_keys(config.TEST_COMPID)
user.send_keys(config.TEST_USER)
password.send_keys(config.TEST_PASS)

login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()

sleep(5)
search = browser.find_element_by_xpath("//input[@type='text']")
search.send_keys('Rules')
#search.submit()

print("SUCCESS")