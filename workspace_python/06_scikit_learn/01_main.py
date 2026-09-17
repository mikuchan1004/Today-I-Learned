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
print(dataFrame.head(3))

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
    2.05,
    8.4
]]

columns = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol"
]

# 모델 학습에 사용한 X와 같은 형태로 만들기
wine_df = pd.DataFrame(wine, columns=columns)

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

#======================
# 모델 성능 평가 
#======================

from sklearn.metrics import f1_score, roc_auc_score

# 평가 지표 : 모델이 얼마나 잘 이해했는가?를 숫자로 표현한다. 

# train 데이터로 학습한 모델에
# 모의고사 문제인 test 데이터를 예측하라고 한다.
pred = model.predict(X_test)

# 실제 정답과 예측 답으로 f1 점수를 낸다
f1 = f1_score(y_test, pred)
# f1은 정밀도와 재현율을 함께 고려하는 기준이다.
# 단지 답만 점검하는 것이 아니라 실제 좋은 와인(1)을 잘 찾았는지도 고려한다.
# 점수는 0~1까지 나오고 1이 좋은 것.
print("f1 평가 점수 :", f1)

proba = model.predict_proba(X_test)[:, 1]
# [:, 1] : 전체 행에서 두번째 컬럼(좋은 와인의 확률)만 추출

# 0~ 1
# 1 : 완벽, 0.5는 랜덤, 0.5미만은 영 좋지 않음
auc = roc_auc_score(y_test, proba)
print('roc_auc 평가 점수 :' , auc)
# ROC-AUC 지표는 얼마나 잘 구분하는가?  
# 0.5는 무작위와 비슷하다.
# 1에 가까울수록 두 클래스를 잘 구분하는 모델이다.

# f1과 roc-auc는 서로 다른 것을 기준으로 측정하기 때문에 서로 비교하지는 말자. 

#==================================
# cross validation 교차 검증 
#==================================

from sklearn.model_selection import cross_val_score

# cross validation 교차 검증 
# 데이터를 여러 부분으로 나눠서 모델을 반복적으로 학습하고 평가한다.

'''
예를 들어  
[0,1,2,3,4]중에서
1. 학습 [0,1,2,3], 연습문제[4]
2. 학습[0.1,2,4], 연습문제[3]
3. 학습[0,1,4,3], 연습문제[2]
4. 학습[0,4,2,3], 연습문제[1]
5. 학습[1,2,3,4], 연습문제[0]
'''

# 데이터가 많지 않은 경우에는 분할에 따라서 성능이 달라질 수 있기 때문에 유용하다.
# 즉, 한번의 결과만으로 모델 성능을 판단하는 문제를 줄이기 위해 사용한다.

scores = cross_val_score (
    model, X_train, y_train,
    cv = 2,
    scoring='f1'
)

# 전체 X와 y로 5번 교차 검증( 5-Fold Cross Validation)을 수행한다 
# cv = 5는 데이터를 5개 부분을 나눠서 교대로 검증한다.
# 한 번에 4개의 구분을 학습에 사용하고  1개의 구분을 검증에 사용한다.
# scoring = 'f1'  : 각 검증에서 F1-score를 계산하라

print('cross_val_score : ' , scores)

print('scores 평균 : ' , scores.mean())

# 단순하게 어떤게 좋다 나쁘다가 아니고 어떤 덩어리가 무조건 정답도 아니다

from sklearn.model_selection import GridSearchCV
prarms = {
    'n_estimators' : [50, 100],
    'max_depth' : [5,10, None]
}
# 2 * 3  = 6개의 조합
# n_estimatiors : 의사결정나무 갯수
# max_depth : 나무의 최대 깊이 (None은 제한하지 않는다.)
# 하이퍼파라미터 : 개발자가 바꿀 수 있는 값

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    prarms,
    cv=5,
    scoring='f1'
)
# GridSearchCV
# 첫 번째 전달인자 :  머신러닝 모델 
# 두 번째 전달인자 : 시험할 하이퍼파라미터 후보
# 세 번째 전달인자 : 학습 데이터의 조합 수 
# 네 번째 전달인자 : 평가 지표, 지표의 점수가 가장 높은 조합을 찾는다

grid.fit(X_train, y_train)
#지정한  6개의 하이퍼라파라미터 조합을 각각 학습하고 평가한다.

print('최적의 조합법 : ', grid.best_params_)
# 6개 조합 중 가장 좋았던 조합을 출력한다.

print('최고 점수 : ' ,grid.best_score_)
# GridSearchCV가 선택한 최적의 하이퍼파라미터 조합으로 교차검증에서 얻은 평균 F1 점수를 출력한다.
# 진짜 평가는 X_test , y_test로 평가하는게 좋다.

grid_model =  grid.best_estimator_ 
# GridSearchCV가 찾은 가장 좋은 하이퍼파라미터 조합으로 만들어진 모델을 가져온다.
# 최적의 RandomForest 모델

grid_pred = model.predict(wine_df)
print(' grid 와인 결과 예측 : ' , grid_pred)

grid_proba = model.predict_proba(wine_df)
print(' grid 와인 확률 예측 : ' , grid_proba )

from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold (
    n_splits=5,
    shuffle=True,
    random_state=42
)
# StratifiedKFold  : 분류할 때 클래스의 비율을 최대한 유지하면서 나누는 방법 
# n_splits : 5개 구역으로 쪼개기 5 Fold Cross Validation
# shuffle : 데이터를 섞은 다음에 Fold로 나눈다

scores = cross_val_score (
    grid_model, X, y,
    cv = skf,
    scoring='f1'
)
# StratifiedKFold 방식을 사용해서 Cross Validation을 수행한다.
# 위에서 배운 내용은 그냥 5개 구역으로 나눠서 진행했지만 
# 지금은 정답의 비율에 가까운  구성으로 진행한다(train_test_split 과 비슷한 역할을 한다.)

print ('skf 방식의 교차 검증 결과 : ',scores)
print('skf 방식의 교차 검증 결과의 평균' , scores.mean())