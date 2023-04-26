from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.edge.options import Options
from datetime import datetime


class DouYin:
    def __init__(self):
        self.url = 'https://live.douyin.com/80017709309'
        print('正在打开浏览器')
        options = Options()
        options.add_argument('--headless')
        self.browser = webdriver.Edge(options=options)
        print('正在打开网页')
        self.browser.get(self.url)
        print('打开成功')
        time.sleep(5)
        self.danmus = []
        self.last_danmu = ''

    def get_html(self):
        return self.browser.page_source

    def get_new_danmus(self):
        soup = BeautifulSoup(self.get_html(), features='lxml')
        tmp = soup.find_all('span', {"class": 'webcast-chatroom___content-with-emoji-text'})
        danmus = [span.get_text() for span in tmp]
        return danmus

    def flush_danmus(self):
        new_list = self.get_new_danmus()
        array = []
        array_max = 0
        for index, tmp in enumerate(new_list):
            if tmp == self.last_danmu:
                array.append(index + 1)
        for i in range(len(array)):
            array_max = array[0]
            if array_max < array[i]:
                array_max = array[i]
        if len(array) != 0:
            index = array_max
        else:
            index = 0
        self.danmus += new_list[index:]
        if len(self.danmus) > 1:
            self.last_danmu = self.danmus[-1]

    def save_danmus(self):
        df_danmus = pd.DataFrame(self.danmus)
        date = datetime.now().strftime('%m-%d')
        filename = 'danmu_' + date + '-8.csv'
        df_danmus.to_csv('./danmu/'+filename, header=0, index=None, encoding="utf_8_sig")

    def run(self, max_time=65536, flush_time=1):
        time.sleep(5)
        start_time = time.time()
        while True:
            self.flush_danmus()
            time.sleep(flush_time)
            now_time = time.time()
            print(self.danmus)
            print(len(self.danmus))
            if now_time - start_time > max_time:
                break
        self.save_danmus()
        # self.browser.quit()


if __name__ == '__main__':
    live = DouYin()
    live.run(max_time=3 * 60 * 60, flush_time=5)
