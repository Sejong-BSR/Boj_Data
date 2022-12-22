from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pickle

data = []

options = webdriver.ChromeOptions() # 옵션 설정
options.add_argument("headless") # 창 안뜨게
driver = webdriver.Chrome('C:/Users/jaehoon/chromedriver',options=options) # driver 경로 local에 맞게 수정바람

url_temp = f"https://www.acmicpc.net/login?next=%2Fproblem%2F1001"
driver.get(url_temp)
cookies = pickle.load(open("back.pkl", "rb")) # 로그인 쿠키 불러오기
for cookie in cookies: # 로그인 쿠키 driver에 적용
    driver.add_cookie(cookie)

driver.get(url_temp) # 로그인 페이지, 로그인 진행

for i in tqdm(range(1000,26625)):
    single_data = dict()
    url_temp = f"https://www.acmicpc.net/problem/{i}" # 문제 번호
    driver.get(url_temp)
    try:
        single_data['name'] = driver.find_elements(By.XPATH, f'//*[@id="problem_title"]')[0].get_attribute('innerText')
    except:
        continue

    # 기본 정보 추출 및 저장 [번호,이름,시간제한,메모리제한,제출수,정답수,맞힌사람수,정답비율,난이도,유형]
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

# data 저장
# with open('data_dict.pkl','wb') as f:
#     pickle.dump(data,f)

# data 불러오기
# with open('data_dict.pkl','rb') as f:
#     mydict = pickle.load(f)
# print(mydict)


# 제출 현황 크롤링
logs = dict()
start = 40000000
end = 40000000
for i in tqdm(range(start,end,20)): # 제출 번호 start to end
    url_temp = f"https://www.acmicpc.net/status?top={i}" # 해당 제출 번호 기준 내림차순 20개씩 출력
    driver.get(url_temp)
    elements = driver.find_elements(By.CSS_SELECTOR, f'tbody > tr > td')
    for idx,val in enumerate(elements):
        if idx % 9 == 0:
            temp = val.get_attribute('innerText')
            logs[f'{temp}'] = []
        else:
            logs[f'{temp}'].append(val.get_attribute('innerText'))

driver.quit()