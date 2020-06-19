import os
from selenium import webdriver

class Chrome():
    def __init__(self):
        self.browser = webdriver.Chrome(os.path.join(os.getcwd(), "res", "chromedriver.exe"))
        #self.browser = webdriver.Chrome("../res/chromedriver.exe")
        self.get("https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fkin.naver.com%2Findex.nhn")
        
    def get(self, path):
        self.browser.get(path)

if __name__ == "__main__":
    pass