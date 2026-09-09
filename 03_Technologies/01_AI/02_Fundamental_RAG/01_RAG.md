# RAG

## (Common) Architecture

- RAG는 시스템 패턴이다.
- 외부 지식을 검색하고, LLM 입력 프롬프트로 넣어 답변을 생성하는 시스템 패턴이다.
- 모델 자체를 다시 학습시키는 방식이 아니라, 질문 시점에 필요한 정보를 찾아 함께 사용한다.

## Indexing Step

- "문서 로딩, 전처리, 청킹, 임베딩, 벡터DB 저장" 순의 RAG 내 DB 저장 파이프라인
  - 주요 방법(시계열 기준)
    1. 초기 인덱싱: 1회
    2. 재인덱싱(증분 인덱싱): 문서 변경 시마다(비정기), 기존 벡터를 삭제하고 변경된 문서만 다시 인덱싱

- 인덱싱 품질이 검색에 미치는 영향
  - RAg의 검색 품질이 낮다는 것은 검색 알고리즘 자체의 문제보다, Indexing 품질이 낮은 경우가 많다.

### 1. Document Loading

- 문서 로딩: 다양한 형식의 원본 문서에서 텍스트를 추출하여 RAG 파이프라인에 투입할 수 있는 형태로 변환하는 과정
  - 주로 text, metadata를 함께 반환.
    - text: 파일에서 추출한 텍스트 문자열
    - metadata: 파일명, 페이지 번호, 생성일, 출처 등 부가 정보. 벡터 DB에 함께 저장하면 Metadata Filtering에 활용 가능
  - 주요 방법(가벼운 문서 형식 기준)
    1. txt, markdown: 내장 open() 함수 사용
    2. PDF: PyPDF2, pdfplumber, PyMuPDF
    3. HTML: BeautifulSoup
    4. JSON: 내장 json
    5. CSV: 내장 csv, pandas
    6. DOCX: python-docx

#### (Text Preprocessing (텍스트 전처리))

- 문서에서 추출한 텍스트를 청킹, 임베딩 전에 불필요한 노이즈를 제거하고 정리하는 과정
  - 주요 전처리 작업
    - 특수/제어 문자 제거: `\x00`, `\xad`
    - 공백 정규화
    - 빈 줄 정규화
    - 헤더/푸터 제거: PDF의 반복 헤더, 페이지 번호(`- 3 -`) 제거
    - HTML 태그 제거
    - 유니코드 정규화: NFC/NFKC 정규화

### 2. Chunking

- 청킹: 긴 문서를 검색과 임베딩에 적합한 크기의 텍스트 조각(청크)으로 분할하는 과정
  - RAG 시스템을 처음 구축할 때는 청킹 전략보다 파이프라인 전체가 동작하는지 먼저 검증이 우선
  - 주요 방법(난이도 기준)
    1. Fixed-size Chunking: 고정된 글자 수 또는 토큰 수
    2. Regex & Delimiter Chunking: 줄바꿈, 마침표, 제목 등 구분자
    3. Semantic Chunking: 문장 간 임베딩 유사도
    4. Parent-Child Chunking: 큰 청크(부모)와 작은 청크(자식) 계층

- 청크 크기 가이드라인
  - 너무 작으면 문맥이 부족하고, 너무 크면 검색 정확도가 떨어짐.
  - 용도별 추천 크기
    - 일반 QA: 500~1000자
    - 요약: 1000~2000자
    - 코드: 함수/클래스 단위

### 3. Embedding

- Tokenization: 텍스트를 모델이 처리할 수 있는 최소 단위로 분리하는 과정
  - 주요 방법(크기 단위 기준)
    1. Word 단위: 공백, 구두점 기준으로 문자열 분리
    2. Subword 단위: 빈도 기준 문자열 분리
    3. Character 단위: 글자 기준 문자열 분리
    4. Custom 단위: 개발자가 정한 분리 기준에 따라 문자열 분리

- Text Embedding: 텍스트의 의미를 보존한 채 고정 길이의 숫자 벡터로 변환하는 과정
  - (목적) 텍스트 간 유사도를 계산하기 위함
  - **주요 임베딩 모델**
    | 모델 | 제공자 | 차원 | 최대 입력 | 비용 | 특징 |
    | --- | --- | --- | --- | --- | --- |
    | all-MiniLM-L6-v2 | Sentence Transformers | 384 | 256 토큰 | 무료 (로컬) | • 가볍고 빠름<br>• 학습/실험용에 적합<br>• 영어 중심 |
    | multilingual-e5-large | Microsoft | 1024 | 512 토큰 | 무료 (로컬) | • 다국어 지원<br>• 한국어 성능 우수 |
    | text-embedding-3-small | OpenAI | 1536 | 8191 토큰 | API 유료 | • 비용 대비 성능 우수<br>• 긴 입력 지원 |
    | text-embedding-3-large | OpenAI | 3072 | 8191 토큰 | API 유료 | • 더 높은 정확도<br>• 차원 축소 가능 |
    | embed-v3 | Cohere | 1024 | 512 토큰 | API 유료 | • 검색 특화 모드(search_document/search_query) 지원 |

- Dense Vector: ??

- Sparse Vector
  - 주요 방법(이해 난이도 기준)
    1. BoW(Bag of Words): 단어 빈도
    2. TF-IDF: 단어 빈도 \* 역문서 빈도
    3. BM25: 정보 검색 점수도 표준 알고리즘

- Sentence Transformer를 사용하는 이유: 로컬 환경에서 API 비용 없이 고품질 문장 임베딩을 생성할 수 있고, 데이터가 외부 서버로 전송되지 않아 보안이 필요한 환경에서도 사용할 수 있기 때문.
  - HG에는 수천 개의 Pre-training Model이 등록되어 있음.
  - 용도(검색, 분류, 군집), 언어(영어, 다국어, 한국어), 성능/속도 균형에 따라 선택 가능
  - 필요 시 자체 데이터로 Fine-tuning하여 도메인 특화 성능을 높이는 것도 가능
  - `model.encode()`로 텍스트를 Dense Vector로 변환하는 방식 사용

- BERT vs SBERT
  - BERT: 문장, 단어의 문맥을 깊이 이해하는 데 강한 구조
  - SBERT(Sentence-BERT): 문장 전체를 하나의 벡터로 빠르게 변환하여, 문장 간 유사도 검색을 효율적으로 수행하는 구조
  - 두 문장을 유사도를 비교하려면, BERT에선 두 문장을 하나의 입력으로 넣고 모델이 그 관계를 직접 보아야 했다. 높은 정확도를 제공하지만, 리소스가 크고 검색 속도가 느리다.
  - SBERT에선 각 문장을 벡터화하여, 벡터 간 유사도를 계산한다. 리소스가 작고 검색 속도가 빠르다. 현실적인 시간 내 검색이 가능하다. 문장 검색, 의미 기반 검색, RAG Retrieval, 유사 문장 찾기에 적합하다.

### 4. Vector Store(DB)

---

## (Query Step) Retrival

### 1. Embedding

- _(상기 동일)_

### 2. Similarity Retrieval

- 유사도 검색 방법 (직관적인 방법 기준)
  1. Dot Product(내적): 두 백터의 대응 원소를 곱하여 합산하여 벡터 간 유사도나 관련성을 측정하는 연산 (양수, 0, 음수)
     - FAISS, Pinecone 등 VectorDB가 유사도 측정 방법에 Inner Product 사용
     - Transformer 아키텍처에서 Query, Key 간 관련성 계산에 Scaled Dot-Product Attention 사용
     - 벡터 크기에 영향을 받음. ($-∞$ ~ $+∞) 유사도 기준을 설정하기 어려움. 벡터 노름이 큰 항목이 더 높은 점수를 받을 수 있어, 문서 길이에 따라 관련성에 영향을 받음.
  2. Cosine Similarity(코사인 유사도): 두 벡터가 이루는 각도의 코사인 값으로 방향 유사도를 -1~1 범위로 측정하는 지표
     - 벡터 크기에 영향을 받지 않음. 벡터 크기를 나누어 정규화하므로, 유사도 기준을 설정하기 쉬움. 문서 길이에 관계없이 의미적으로 관련성이 높은 문서 탐색 가능.
     - 1이면 같은 방향, 0이면 무관, -1이면 반대 방향
     - 모델에 따라 검색 결과가 낮을 수 있음.
       - Reranking 모델을 추가하여 검색 결과를 재정렬하거나,
       - 임베딩 모델을 도메인에 맞게 Fine-tuning하면 품질이 개선될 수 있음.
     - ChromaDB, Pinecone, Weaviate 등 VectorDB가 Cosine Similarity를 기본 또는 선택 사용 가능
  3. Cosine Distance: $1- Cosine Similarty$로 계산하여, 작을수록 유사함.
     - 현재 VectorDB가 Similarity인지, Distance인지 판단이 필요함.
  4. Euclidean Distance: 벡터 간 절대 거리를 기준으로 비교, 텍스트 의미 유사도보다는 거리 자체가 중요한 문제에서 더 적합.
     - 벡터 간 절대 거리를 기준으로 비교. ($0$ ~ $∞$)
     - 군집화, 이상 탐지에 유용함.
  - 임계값 설정
    - 임베딩 모델, 문서 길이, 도메인, 검색 목적에 따라 설정할 임계값이 달라짐.
    - 절대 기준이 아니라 실무에서 참고할 수 있는 일반적인 해석 예시
      - 0.8 ~: 매우 유사
      - 0.5 ~ 0.8: 강한 관련성
      - 0.3 ~ 0.5: 약한 관련성
      - ~ 0.3: 낮은 관련성
    - 실무에서는 테스트 질문과 정답 문서를 기준으로 여러 임계값을 실험한 뒤 결정
    - 임계값이 고정 규칙이라기보다, Precision과 Recall의 균형을 조정하는 운영 파라미터

## (Query Step) Augmentation

## (Query Step) Generation, Validation
