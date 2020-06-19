# :tv: Analyzing TV reviews from Amazon.com

<br>

## :one: Overview

- Amazon.com의 TV 모델 정보와 리뷰 데이터를 분석하는 빅데이터 프로젝트
- 빅데이터를 분석을 통해 고객과 기업 모두에게 의미있는 인사이트를 주는 것을 목표로 구현

<br>

## :two: Project Schedule

![schedule](https://user-images.githubusercontent.com/52685250/85049418-9c7ce980-b1cf-11ea-9288-22a6546a55c4.png)

<br>

## :three: Tech Stack & Architecture

![flow](https://user-images.githubusercontent.com/52685250/85049425-9e46ad00-b1cf-11ea-8e9b-fa36340fc41a.png)

:round_pushpin: <b>Frontend</b> : `Vue.js`

:round_pushpin: <b>Backend</b> : `Flask`

:round_pushpin: <b>Database</b> : `ElasticSearch`

:round_pushpin: <b>Library</b> : `iview`, `echarts`

:round_pushpin: <b>Development Enviornment</b> : Windows 10, Node.js 10 or higher, Vue CLI 3 or higher, Python 3.7.x or higher

:round_pushpin: <b>Using Editor</b> : Visual Studio Code

<br>

## :four: Description

### (1) TV Model's Review List

![01](https://user-images.githubusercontent.com/52685250/85049427-9e46ad00-b1cf-11ea-95ff-dc368b0d9bdc.png)

- 상단 `Brand Select`에서 선택한 브랜드들의 TV 모델 리뷰를 볼 수 있다.
- 선택한 브랜드에 따라 우측의 `Model Select`에 나오는 TV 모델명이 달라지고 특정 TV 모델들을 선택하면 해당 모델들의 리뷰만 모아서 볼 수 있다.
- 각 리뷰의 내용이 길 수 있기 때문에 선택하면 `Modal` Component 형태로 전체 리뷰 내용이 나오도록 구현했다.

<br>

### (2) Analyzing Review Data

![02](https://user-images.githubusercontent.com/52685250/85049431-9edf4380-b1cf-11ea-805f-f1b16d1223e6.png)

- Query DSL의 `aggregations`, `filter` 속성을 이용하여 선택한 모델의 리뷰 정보를 `Elasticsearch`의 DB에서 가져온다.
- 가져온 리뷰 데이터를 기반으로 `echarts` library를 이용하여 분석한 리뷰 데이터를 차트로 표현했다.
- 최근 2년간 월별 리뷰의 총 개수와 평점 평균 분포를 통해 해당 TV 모델의 고객의 반응 변화를 파악할 수 있다.

![03](https://user-images.githubusercontent.com/52685250/85049432-9edf4380-b1cf-11ea-895e-c6a7d8a55c1a.png)

- 위 두 차트도 동일하게 `aggregations`, `filter` 속성을 이용하여 선택한 모델의 리뷰 정보를 가져온 후 분석하여 차트로 표현했다.
- 특히 각 모델 별 리뷰의 반응은 각 리뷰의 텍스트를 분석해 긍정적인 표현이 많으면 `1`, 부정적인 표현이 많으면 `-1`로 인식하여 긍정적인 리뷰와 부정적인 리뷰를 각각 계산했다.
- 또한 각 모델 별 전체 기간의 리뷰 평점 분포 현황을 알 수 있도록 구현했다.

![04](https://user-images.githubusercontent.com/52685250/85049433-9f77da00-b1cf-11ea-8690-17ad07e35072.png)

- `vue.js`에서 차트 라이브러리를 이용해 빅데이터를 분석하여 차트로 표현한 내용 이외에 `Kibana`의 Dashboard를 통해서 다양한 형태의 정보로 시각화해서 볼 수 있도록 구성했다.

<br>

## :five: Insight

### (1) 빅데이터 분석 == 의미있는 인사이트를 얻는 것

- 단순히 분석하고 계산된 데이터를 받아 차트로 보여주는 것에서 그치는 것이 아니라 해당 정보를 보는 대상이 누구인지에 따라 분석된 정보를 보고 새로운 가치나 의미를 얻는 것이 중요하다.
- 이번 프로젝트를 통해서는 TV 모델들의 리뷰 데이터를 분석하여 차트로 보여줌으로써 TV를 구매하고자 하는 고객들은 여러 모델들을 비교하여 수치적으로 명확히 비교하여 옳은 선택을 할 수 있도록 도움을 받을 수 있다.
- TV를 만드는 기업은 차트를 통해서 각 모델의 소비자들의 반응과 동향을 월별로 명확하게 파악할 수 있고 메인화면 좌측의 리뷰 내용도 함께 보면서 보완해나가야할 방향을 뚜렷하게 잡는데 도움을 받을 수 있다.

<br>

### (2) 차트 배치 순서 하나도 신중하게!

- 이번 프로젝트에서 차트를 구현한 후 고민했던 부분 중의 하나는 구현된 네 개의 차트의 배치 순서였다.
- 단순하게 생각하면 근사하고 화려한 차트를 가장 먼저 보여주면 홈페이지에 들어왔을 때 시각적으로 한 번에 매료되게 할 수 있다.
- 물론 근사하게 보이는 것도 중요하지만 조금 더 깊게 생각해서 화려한 측면을 강조하는 것 보다 배치 순서를 신중하게 고려해서 홈페이지에 방문해서 분석한 TV 모델 데이터를 보려는 사람들로 하여금 차트를 차례대로 보면서 의미를 얻는데 조금이나마 도움이 되도록 했다.

<img src="https://user-images.githubusercontent.com/52685250/85052453-e8ca2880-b1d3-11ea-8c54-86c64cc95e2d.JPG" width="700">

- 우측 상단의 차트 메뉴 탭에서 보시다시피 배치 순서를 다음과 같이 정했다.
  - 최근 2년간 월별 리뷰 총 개수
  - 최근 2년간 월별 리뷰 평점 평균
  - 각 모델 별 리뷰의 반응 분석
  - 각 모델 별 리뷰의 평점 분포 현황
- 월별 리뷰 총 개수와 평점 평균을 우선 배치함으로써  최근 2년이라는 긴 기간을 가지고 큰 숲을 보면서 해당 TV 모델들의 전반적인 반응과 흐름, 동향을 파악할 수 있도록 했다.
- 큰 숲을 본 후에는 작은 나무들을 보는 것 처럼 세 번째와 네 번째 차트로 각 모델들의 리뷰 반응과 평점 분포 현황을 배치함으로써 각 모델들의 디테일한 정보를 파악할 수 있도록 했다.
- 차트나 데이터의 배치 순서는 정답은 없지만 개발자의 의도에 따라 서비스를 이용하는 사람들에게 주고자하는 분명한 의미가 있다면 명확한 의도와 사용자에게 주고자하는 인사이트를 반영하여 배치 순서를 정하면 될 것 같다.