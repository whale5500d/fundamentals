# 데이터 전처리

## Feature Engineering

- 모델 정확도를 높이기 위해 주어진 데이터를 잘 표현할 수 있는 features로 변형시키는 과정
- 데이터의 도메인 지식을 활용해 feature를 만듦
- Feature = 각 데이터의 특징

- Data Process
  1. Data gathering (Raw Data 반환)
  2. Feature Engineering (Raw Data 사용, Training Data 반환)
  3. Modeling (Training Data 사용)
- Feature Engineering 단계를 거쳐야 Modeling에 필요한 Training Data가 된다.

## Feature Engineering 하는 방법

1. Binning
   - 연속형 변수를 범주형 변수로 만드는 방법
   - 연속형 변수를 그룹으로 지어주면 데이터를 이해하기 더 쉬워짐.
   - 예시: 나이로 10대, 20대로 구분하기, 수능 성적으로 등급으로 구분하기 등

   - cut(): 원하는 길이로 구간 나누기, 사용자가 구간값을 직접 입력
   - qcut(): 동일 개수로 구간 나누기, 사용자가 구간 개수를 입력

2. Scaling
   - 숫자 데이터 간의 상대적 크기 차이를 제거하는 방법
   - 각 컬럼에 들어있는 데이터의 상대적 크기에 따라 분석이나 모델링 결과가 달라짐.

   - ⚠️ StandardScaler(): 각 특성의 평균을 0, 분산을 1로 스케일링함. 즉, 데이터를 정규분포로 만듦
   - ⚠️ RobustScaler(): 평균과 분산 대신에 중간값과 사분위 값을 사용함. 전체 데이터와 아주 동떨어진 데이터에 영향을 받지 않음.
   - MinMaxScaler(): 각 특성에 0과 1 사이에 위치하도록 스케일링함. 분류보다 회귀에 유용함
   - ⚠️ MaxAbsScaler(): 각 특성의 절대값이 0과 1 사이가 되도록 스케일링함. 모든 값은 -1 ~ 1 사이로 표현되며, 데이터가 양수일 경우 MinMaxScaler와 같음.

3. Label Encoding
   - 범주형 변수의 문자열 값을 숫자로 매핑하는 방법
   - 컴퓨터는 0과 1로 이해하므로, 범주형 변수의 값을 숫자로 변환한다.
   1. One Hot Encoding: 하나의 데이터만 1, 나머지는 0으로 만드는 방법
      - `pd.get_dummies` 함수로 구현 가능
      - 예시: red, green, blue를 0, 1, 2로 인코딩하면, 0 < 2이므로, red < blue라는 이상한 수식이 만들어짐.
      - 대신, [1, 0, 0], [0, 1, 0], [0, 0, 1]로 행렬 테이블로 만드는 One Hot Encoding 방법을 사용
   2. ⚠️ 날짜 데이터 변형
      - 시계열 데이터를 분석하여 날짜 및 방문객 수로 증가 추세 확인
      - `pd.to_datetime` 함수로 문자열 날짜 데이터를 숫자형 날짜로 변환
      - `dayofweek` 함수로 요일 데이터를 숫자형 데이터로 변환
   3. PCA 차원축소
      - IRIS 4개의 변수(컬럼)을 한꺼번에 그래프에 표현하려면?
      - 4개의 데이터를 그래프에 그리려면 4차원 그래프가 된다. 차원을 축소해서 사람이 이해할 수 있는 그래프로 표현한다.

## Key Point

1. 이상치 처리
   - 이상치: 추세에서 벗어나거나 잘못된 값을 말함
   - 이상치 확인: 시각화
   - 이상치 처리: 삭제, 대체
2. Feature Engineering
   - 기존 컬럼 데이터를 가지고 새로운 칼럼 데이터를 생성
   - 새로운 인사이트를 발견하거나 모델 성능을 높일 때 주로 사용
3. Feature Engineerning 방법
   - 대표적인 방법: Binning 구간화, 날짜 데이터 변형
   - Scaling, Label Encoding, One Hot Encoding, PCA 차원축소
