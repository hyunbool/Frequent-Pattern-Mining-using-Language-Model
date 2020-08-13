# Frequent Pattern Mining using Language Model
언어 모델을 이용한 빈발 패턴 마이닝

## Dataset
MovieLens(https://grouplens.org/datasets/movielens/)

## Codes
* item2vec.ipynb: item2vec 이용해 이용자-아이템 셋에서 아이템 임베딩 추출
* n_gram.ipynb: n-gram 이용해 영화 추천 리스트 생성 __완료__
* apriori.ipynb: apriori rule 이용해 support 계산 __완료__
* rnnlm.py: lstm을 이용한 언어모델로 아이템 basket 생성
    * movies.py: movieLens 데이터 전처리(corpus 만들기)
* crawling.py: 네이버 영화 사이트에서 영화 목록 크롤링
* data_amplify.ipynb: support가 0.05% 이상인 아이템의 ratings만 남기는 코드(+ 그렇게 만들어진 user 데이터에서 부분집합 만들어 data 부풀릴 예정)
* data_compare.ipynb: apriori와 ngram으로 만들어 낸 아이템셋 비교 및 평가 __완료__

### 데이터 전처리
* 총 영화 갯수: 62423개
* 두개 이상의 평가가 있는 영화 갯수: 59047개(전체 데이터의 94.6%)
* ~~그중 frequent items(전체 itemset의 0.05% 차지): 8658개(전체 데이터의 14.6%)~~
* movielens의 small dataset 이용: 유저 데이터셋 1212개
* toy data: [1, 50, 110, 296, 457, 527, 588]로 부분집합 만들어 평가: 120개

## 평가
* 환경: GeForce GTX 1080 Ti, CUDA Version_10.2    
* rnnlm(using lstm):
  * 전체 데이터(2개 이상의 평가): ~~속도가 너무 느려서 정지~~
    * 에폭 2: 최종 training perlexity = 49.25, validation perplexity = 11748.59397679311

## References
* ITEM2VEC: Neural Item Embedding for Collaborative Filtering(https://arxiv.org/pdf/1603.04259.pdf)
* Tensorflow, "Text generation with an RNN", https://www.tensorflow.org/tutorials/text/text_generation
