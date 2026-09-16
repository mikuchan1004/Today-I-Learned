# pandas : DB처럼 표 형태의 데이터를 다루는 라이브러리 
# 모든 머신러닝에서 데이터를 가져오고 확인하고 정리하는 용도로 사용된다.

# 데이터 구조 
# Serial : 1차원 배열 
# DataFrame : 2차원 테이블(액셀의 시트, DB의 테이블)

# 주요 기능 
# 자료 입출력 : csv, 액셀, txt, json, sql
# 데이터 정제 : 중복 제거, 데이터 타입 변경, 결측치(null, NaN) 제거
# 가공 및 분석 : 필터링, 정렬, 그룹화

import pandas as pd

dataFrame = pd.read_csv('wine+quality/winequality-red.csv' , sep=';')

# 기본 상위 5줄의 값을 가져온다.
# print(dataFrame.head())
# 가져오고 싶은 줄(행)을 지정할 수 있다.
#  하는 이유는 대충 hello world 느낌으로 로딩이 잘 됐는지 확인 용도
print(dataFrame.head(2))

# shape : 데이터프레임의 크기(행의 개수, 열의 개수)
print('dataFrame.shape :' ,  dataFrame.shape)

# info : 요약 정보 
# 출력 결과 : 컬럼 이름들, 데이터 개수, 타입, 메모리 사용량, 결측치 유무
dataFrame.info()

# 정답 데이터 만들기
# True = 1 , False = 0
dataFrame['good'] = (dataFrame['quality'] >= 7).astype(int)
y = dataFrame['good']
# quality는 정수로 되어있는데 이를 단순하게 0과 1로 구분한다
# 데이터 전처리, feature, engineering
# 전처리 : 분석 전에 불순물 제거

# 문제 데이터 만들기
X = dataFrame.drop(
    columns = ['quality' , 'good']
)
# 깊은 복사 : 원본이 지워지는게 아니다 
# 문제지에서 정답을 지운 상태

# 데이터 쪼개기
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# test_size = 0.2  : 전체 데이터 중에서 20%를 테스트 데이터로 사용하라.
# 그러면 80%는 학습 데이터가 된다.

# random_state = 42 :
# 데이터를 나누는 과정을 고정한다. 
# 값을 바꾸면 나누는 방법이 계속 바뀐다.
# 42 대신 아무 숫자나 사용해도 되지만, 같은 값을 사용해야 결과도 같다.
# 난수표의 시작 값(seed)이라고 생각하면 편하다.
# 동일 설정으로 다시 실행 했을 때 결과를 재현하기 쉽다.

# stratify : 그룹별로 나눈다 계층화 한다. 
# stratify = y : y 즉 정답의 비율을 유지하면서 나눠라

# 의사 결정 트리  Decision Tree 
# 스무고개 하듯 질문하면서 학습 - 갈래로 나뉘어서 나무 모양이 된다. 
# 너무 나누면  과적합(over fitting)되서 예측이 어렵게 된다.
# 가지치기 (Pruning)

# RandomForestClassifier는 분류 문제에 상용하는 머신러닝 알고리즘이다.
# RandomForest는 여러 개의 decision tree를 만들어서 결과를 종합하는 방식
# 여러 나무의 결과를 종합해서 안정적인 예측을 한다.
from sklearn.ensemble import RandomForestClassifier

# 어떻게 할지 선언
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
# n_estimators = 100  : decision tree 100개를 사용해라.
# 나무가 많아지면 안정적인데 시간이 늘어난다. (안정적이지만 품질이 좋아지는건 별개다.)

model.fit(X_train, y_train) # 학습
#fit() : 머신러닝 모델을 실제 데이터에 학습시키기 
# 실제 데이터를 학습시키기 
# X_train : 입력(문제) 데이터 (전달인자)
# y_train : 정답 데이터
# 학습이 끝나면 model 안에 저장된다. 

# 실전 데이터
# 학습하지 않은 새로운 값으로 학습한 내용에 따른 예측 결과 확인용
wine = [[
    7.4,
    0.70,
    0.00,
    1.9,
    0.076,
    11.0,
    34.0,
    0.9978,
    3.54,
    0.80,
    10.4
]]

# 모델 학습에 사용한 X와 같은 형태로 만들기
wine_df = pd.DataFrame(wine)

# predict : 예측
# 결과는 배열로 나온다.
# 만약에 여러개를 주면 [1,0,1]
wine_pred = model.predict(wine_df)
print( '예측 결과 : ' , wine_pred)

# predict_proba  : 예측 확률 
# proba - > probability (확률)
# 비교할 가짓수를 클래스라고 한다(현재 0과 1)
# 새로운 데이터의 각 클래스가 될 확률을 계산한다. 
wine_prob = model.predict_proba(wine_df)
print('예측 결과 :' , wine_prob )

