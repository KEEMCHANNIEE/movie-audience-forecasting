# 🎬 Movie Audience Forecasting  
**Rolling Window 기반 영화 관객수 예측 프로젝트**

## 📌 프로젝트 소개
- 본 프로젝트는 KOFIC API 기반 영화 관객수 데이터를 수집하고, Rolling Window 기법을 활용해 특정 영화의 향후 관객수를 예측하는 모델을 개발합니다.
- 시계열 특성을 고려하여 **SARIMAX** 모델을 적용하였으며, 계절성과 외생 변수의 영향을 반영합니다.
- 주요 과정은 데이터 수집, EDA, 전처리, 변수 생성, 시계열 모델링, 성능 평가로 구성됩니다.

## 🧱 프로젝트 구조

```
movie-audience-forecasting/
├── kofic_data/                        # 원본 영화 데이터
├── processed_data/                    # 전처리된 CSV 파일들
├── trailer_data/                      # 예고편 관련 크롤링 데이터
├── [BA]_모델_구축.ipynb               # 최종 모델 구축 및 예측 notebook
├── EDA.ipynb                          # 탐색적 데이터 분석 notebook
├── SARIMAX_model.ipynb               # SARIMAX 모델링 notebook
├── 가설 검정 + 파생 변수.ipynb        # 변수 생성 및 통계 검정
├── 예고편_조회수_크롤링.ipynb         # 유튜브 예고편 조회수 크롤링
├── 데이터_크롤링_KOFIC_3주차.ipynb    # KOFIC API 데이터 수집
├── kofic_api_extract.py              # KOFIC API 호출 파이썬 스크립트
├── movie_finished_toFDA_V9.csv       # 최종 사용된 데이터
├── 전체_데이터.xlsx                   # 전체 통합 엑셀 데이터
└── README.md                          # 프로젝트 소개 파일
```



## 🔧 사용 기술
- **언어 및 라이브러리**: Python (pandas, requests, statsmodels, matplotlib 등)
- **모델링 기법**: 시계열 예측 (SARIMAX), 통계적 가설검정, Rolling Window
- **API 활용**: KOFIC 영화관 입장권 통합전산망 API
- **크롤링**: YouTube 예고편 조회수 수집

