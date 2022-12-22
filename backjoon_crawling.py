from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time
import pickle
import os

options = webdriver.ChromeOptions() # 옵션 설정
options.add_argument("headless") # 창 안뜨게
driver = webdriver.Chrome('C:/Users/jaehoon/chromedriver',options=options) # driver 경로 local에 맞게 수정바람

url_temp = f"https://www.acmicpc.net/login?next=%2Fproblem%2F1001"
driver.get(url_temp)
cookies = pickle.load(open("back.pkl", "rb")) # 로그인 쿠키 불러오기
for cookie in cookies: # 로그인 쿠키 driver에 적용
    driver.add_cookie(cookie)

driver.get(url_temp) # 로그인 사이트, 로그인 진행

def save_data(data):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/test_data.pkl','wb') as f:
        pickle.dump(data,f)

def load_data():
    with open('data_dict.pkl','rb') as f:
        data = pickle.load(f)
    print(data)

def background_data():
    data = []
    for i in tqdm(range(1000,26625)): # 백준 문제 번호
        single_data = dict()
        url_temp = f"https://www.acmicpc.net/problem/{i}"
        driver.get(url_temp)
        try:
            single_data['name'] = driver.find_elements(By.XPATH, f'//*[@id="problem_title"]')[0].get_attribute('innerText')
        except:
            continue

        single_data['id'] = f"{i}"
        single_data['time_limit'] = driver.find_elements(By.XPATH, f'//*[@id="problem-info"]/tbody/tr/td[1]')[0].get_attribute('innerText')
        single_data['memory_limit'] = driver.find_elements(By.XPATH, f'//*[@id="problem-info"]/tbody/tr/td[2]')[0].get_attribute('innerText')
        single_data['submit'] = driver.find_elements(By.XPATH, f'//*[@id="problem-info"]/tbody/tr/td[3]')[0].get_attribute('innerText')
        single_data['answer'] = driver.find_elements(By.XPATH, f'//*[@id="problem-info"]/tbody/tr/td[4]')[0].get_attribute('innerText')
        single_data['pass'] = driver.find_elements(By.XPATH, f'//*[@id="problem-info"]/tbody/tr/td[5]')[0].get_attribute('innerText')
        single_data['ratio'] = driver.find_elements(By.XPATH, f'//*[@id="problem-info"]/tbody/tr/td[6]')[0].get_attribute('innerText')
        single_data['rank'] = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div[3]/div[3]/div/blockquote/span')[0].get_attribute('class')[19:]
        single_data['type'] = list()
        elements = driver.find_elements(By.CSS_SELECTOR,'.spoiler-link')
        for val in elements:
            single_data['type'].append(val.get_attribute('innerText'))
        data.append(single_data)

    return data


# 제출 현황 크롤링
def crawling(i,submit_num):
    logs = dict()
    url_temp = f"https://www.acmicpc.net/status?problem_id={i}"
    for i in tqdm(range(submit_num//20)):
        driver.get(url_temp)
        elements = driver.find_elements(By.CSS_SELECTOR, f'tbody > tr > td')
        real_time = driver.find_elements(By.CSS_SELECTOR, f'.real-time-update')

        for idx,val in enumerate(elements):
            if idx % 9 == 0:
                temp = val.get_attribute('innerText')
                logs[f'{temp}'] = []
                logs[f'{temp}'].append(real_time[idx//9].get_attribute('data-original-title'))
            else:
                logs[f'{temp}'].append(val.get_attribute('innerText'))

        try:
            url_temp = driver.find_elements(By.ID, f'next_page')[0].get_attribute('href')
        except:
            return logs

    return logs

if __name__ == "__main__":
    print("hello world")
    #back_data = background_data()
    #filename = "background.pkl"
    #load_data(filename)
    #submit_data = crawling(5984, 40)  # crawling(문제번호,긁어올 제출 현황 수)
    #save_data(submit_data)