import os
import requests
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import pickle

def save_data(data,problem_num):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open(f'data/{problem_num}.pkl','wb') as f:
        pickle.dump(data,f)

def load_data():
    with open('data_dict.pkl','rb') as f:
        data = pickle.load(f)
    print(data)

def crawling(problem_num, submit_num):
    url_temp =  f"https://www.acmicpc.net/status?&problem_id={problem_num}"
    total_data = []
    for _ in tqdm(range(submit_num//20)):
        page = requests.get(url_temp)
        soup = bs(page.text, "html.parser")
        elements = soup.select('tbody > tr > td')
        real_time = soup.select('.real-time-update')
        single_data = []
        for idx,val in enumerate(elements):
            if idx % 9 == 0:
                total_data.append(single_data)
                single_data = []
                single_data.append(real_time[idx//9].attrs['title'])
            single_data.append(val.get_text())

        try:
            url_temp = "https://www.acmicpc.net" + soup.select('#next_page')[0].attrs['href']
        except:
            return total_data

    return total_data

if __name__ == "__main__":
    print("hello world")
    lst = np.load("id_submit_pair.npy")[0:343] # 343,680,1140,1975
    for problem in lst:
        if not os.path.isfile(f'data/{problem[0]}.pkl'):
            submit_data = crawling(problem[0], problem[1])  # crawling(문제번호,긁어올 제출 현황 수)
            save_data(submit_data,problem[0])
        else:
            continue


