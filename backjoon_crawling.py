import requests
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import pickle
import os
import ray

def save_data(data,problem_num):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open(f'data/{problem_num}.pkl','wb') as f:
        pickle.dump(data,f)

def load_data():
    with open('data_dict.pkl','rb') as f:
        data = pickle.load(f)
    print(data)

@ray.remote
def crawling(problem_num, submit_num):
    url_temp =  f"https://www.acmicpc.net/status?&problem_id={problem_num}"
    total_data = []
    for _ in tqdm(range(submit_num//20), miniters=int((submit_num//20)/100)):
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
    print("[START] Crawling")
    START, END = 350, 700
    id_submit_pair = np.load('id_submit_pair.npy')[START:END] # [문제 번호, 제출 수]
    ray.init(num_cpus=4)
    for problem in id_submit_pair:
        submit_data = ray.get(crawling.remote(problem[0], problem[1]))  # crawling(문제번호,긁어올 제출 현황 수)
        print(len(submit_data))
        save_data(submit_data, problem[0])
    ray.shutdown()
    print("[END] Crawling")