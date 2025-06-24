# KOFIC 데이터에서 일별 박스오피스 정보를 추출하는 코드
# 개봉 후 15일 이후 데이터를 추출하기 위한 코드

import os
import concurrent.futures
import requests
import pandas as pd
from tqdm import tqdm

# API 키 목록 (한 API 키당 1일 3000건의 요청 가능)
key_list = ['6e927f984e0745787469e2452351991a', '430156241533f1d058c603178cc3ca0e', '460008cf22775f10a5736964c8cf47ce']

def fetch_data(date, key):
    url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={key}&targetDt={date}'
    response = requests.get(url)
    return response.json()

def process_data(d, date):
    movie_list = []
    for movie in d['boxOfficeResult']['dailyBoxOfficeList']:
        # 필요한 정보만 추출
        movie_list.append([date, movie['rank'], movie['movieCd'], movie['movieNm'], movie['openDt'], 
                           movie['salesAmt'], movie['salesShare'], movie['salesInten'], movie['salesChange'], movie['salesAcc'], 
                           movie['audiCnt'], movie['audiInten'], movie['audiChange'], movie['audiAcc'], movie['scrnCnt'], movie['showCnt']])
    return pd.DataFrame(movie_list)

def main(dates, key):
    data = pd.DataFrame()
    # 멀티프로세싱으로 병렬처리
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_date = {executor.submit(fetch_data, date, key): date for date in dates}
        for future in tqdm(concurrent.futures.as_completed(future_to_date), total=len(future_to_date), desc="Processing dates"):
            date = future_to_date[future]
            try:
                d = future.result()
                date_data = process_data(d, date)
                data = pd.concat([data, date_data], axis=0)
            except Exception as exc:
                print(f'{date} generated an exception: {exc}')
    
    return data

# Date list
date_ranges = {
    '2016년_상반기': ('20160101', '20160630'),
    '2016년_하반기': ('20160701', '20161231'),
    '2017년_상반기': ('20170101', '20170630'),
    '2017년_하반기': ('20170701', '20171231'),
    '2018년_상반기': ('20180101', '20180630'),
    '2018년_하반기': ('20180701', '20181231'),
    '2019년_상반기': ('20190101', '20190630')
    }


# Main loop
if __name__ == "__main__":
    for date_range in date_ranges.keys():
        date_tuple = date_ranges[date_range]
        date_list = [date.strftime('%Y%m%d') for date in pd.date_range(start=date_tuple[0], end=date_tuple[1])]
        
        data = main(list(date_list), key_list[2])
        data.columns = ['date', 'rank', 'movieCd', 'movieNm', 'openDt', 'salesAmt', 'salesShare', 'salesInten', 'salesChange', 'salesAcc', 'audiCnt', 'audiInten', 'audiChange', 'audiAcc', 'scrnCnt', 'showCnt']
        
        # 현 디렉토리에 kofi_data 폴더 생성
        if not os.path.exists('kofic_data'):
            os.makedirs('kofic_data')
        data.to_parquet(f"./kofic_data/{date_range}_일별상영정보.parquet", engine='pyarrow', index=False)

    # kofic_data 폴더로 이동하여 모든 파일을 읽어서 하나의 파일로 병합
    os.chdir('kofic_data')
    files = [file for file in os.listdir() if file.endswith('.parquet')]
    data = pd.DataFrame()
    for file in files:
        data = pd.concat([data, pd.read_parquet(file)], axis=0)

    data.sort_values(by=['date'], inplace=True)

    # 합친 데이터를 parquet 파일로 저장
    data.to_parquet('kofic_data.parquet', engine='pyarrow', index=False)