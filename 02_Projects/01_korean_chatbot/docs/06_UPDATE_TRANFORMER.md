# Transformer 개선 작업

## 배경

- `custom_transformer`를 사용해 모델의 개선 작업을 진행하고자 합니다. 문제를 성격별로 분류하고, 우선순위가 높은 것부터 하나씩 "문제 재현 → 진단 → 개선 → 재검증" 순서로 다룰 예정입니다.

## 개선 작업 로드맵

**표 1. 개선 작업 로드맵**
| 단계 | 다루는 문제 | 상태 |
| --- | --- | --- |
| A | causal mask 부재 (`scaled_dot_product_attention.py`, `transformer_model.py`) | 완료 ✅ |
| B | weight tying 버그 (`transformer_decoder.py`) | 완료 ✅ |
| C | 클래스 불균형 (응:아니 = 17:7) | 부분 개선 ✅ |
| D | 과적합 (데이터 24개 vs 파라미터 수백만) | 부분 개선 ✅ |
| E | 문형 단일성 (일반화 실패) | 예정 |
| F | Post-LN → Pre-LN | 예정 |
| G | mask 차원, batch 생성 | 예정 |

## A단계: causal mask 부재

### 진단 방법

- `test_class_balance.py`로 데이터 응/아니 비율과, 미학습 프롬프트에 대한
  생성 편향을 확인합니다.
- `test_sequential_interference.py`로 학습 종료 후 24개 샘플을 개별
  재평가하고, 답변의 첫 토큰(응/아니가 갈리는 지점)만의 개별 loss와
  실제 greedy 생성 결과를 같은 모델 인스턴스에서 비교합니다.
- `test_causal_mask_leak.py`로, 같은 논리적 위치(질문의 마지막 토큰)의
  logits이 그 뒤에 어떤 토큰이 이어붙는지에 따라 달라지는지 직접 비교합니다.

```bash
python3 src/custom_transformer/test_class_balance.py
python3 src/custom_transformer/test_sequential_interference.py
python3 src/custom_transformer/test_causal_mask_leak.py
```

### 진단 결과

**1. 데이터 분포 및 생성 편향 확인 (`test_class_balance.py`)**

```bash
전체 QA 쌍: 24개
'응'으로 시작: 17개
'아니'로 시작: 7개
응:아니 비율 = 17:7 (약 2.4:1)

미학습 프롬프트(번복 없이 응으로만 고정된 명사 5개)에 대한 생성 결과:
  '내일 운동 갈 거야?' -> '아니,'
  '오늘 공부 할 거야?' -> '아니,'
  '오늘 베이킹 할 거야?' -> '아니,'
  '내일 출근 할 거야?' -> '아니,'
  '내일 친구 만날 거야?' -> '아니,'

미학습 프롬프트 5개 중 '응'으로 시작: 0개 (0.0%)

학습 데이터 원문을 그대로 넣었을 때도(암기 확인):
  '내일 운동 할 거야?' -> '아니,' (암기 실패)
  '내일 공부 할 거야?' -> '아니,' (암기 실패)
  '내일 베이킹 할 거야?' -> '아니,' (암기 실패)
  '오늘 출근 할 거야?' -> '아니,' (암기 실패)
  '오늘 친구 만날 거야?' -> '아니,' (암기 실패)

원문 그대로 넣었을 때 정답률: 0/5 (0.0%)
```

- 데이터 응:아니 비율(17:7)만으로는 설명되지 않는 결과입니다. 데이터에서
  '응'으로만 100% 고정됐던 명사조차, 학습 데이터 원문을 그대로 넣어도
  전부 '아니'로 생성되어 암기 자체가 실패했습니다.
- 클래스 불균형 가설(원래 B단계, 현 C단계)로는 이 결과를 설명할 수 없어,
  더 근본적인 원인 조사가 필요했습니다.

**2. 순차 학습 간섭 가설 검증 (`test_sequential_interference.py`)**

```bash
재평가 평균 loss: 0.0010 (24개 샘플 전부 0.0006~0.0014 범위, 매우 낮음)
loss가 1.0을 넘는(사실상 학습이 안 된) 샘플 개수: 0개

첫 토큰(응/아니 분기점)만 개별 확인 + 같은 모델로 실제 greedy 생성:
  [ 2] '오늘 조깅 할 거야?'  정답='응,' 첫토큰loss=0.0006  greedy='아니,' (불일치)
  [ 4] '오늘 여행 갈 거야?'  정답='응,' 첫토큰loss=0.0007  greedy='아니,' (불일치)
  [ 5] '내일 공부 할 거야?'  정답='응,' 첫토큰loss=0.0007  greedy='아니,' (불일치)
  ... (고유 질문 13개 중 7개 불일치)
```

- 셔플 없는 순차 학습이 원인이라는 가설은 기각되었습니다. 24개 전부(중복
  질문 포함) teacher forcing 기준 loss가 극히 낮았기 때문입니다.
- 다만 중복(번복) 질문이 아닌, 정답이 유일하게 정해진 고유 질문 13개 중
  7개에서 "첫 토큰 loss는 극히 낮은데(0.0006~0.0008, 사실상 확신) greedy
  생성은 반대로 나온다"는 모순이 발견되었습니다. 이 모순이 다음 검증으로
  이어졌습니다.

**3. causal mask 결함 직접 검증 (`test_causal_mask_leak.py`)**

```bash
=== causal mask 결함 검증 (학습 전, 무작위 초기화 상태) ===

검증 대상 질문: '오늘 조깅 할 거야?'

(1) 질문만 입력했을 때, 질문 마지막 위치의 logits 앞 5개:
[-0.9910, -0.5336, 0.7548, 0.4665, 0.9181]
(2) 질문+정답 이어붙였을 때, 같은 위치의 logits 앞 5개:
[-0.5051, -0.5571, 0.9510, 0.5149, 0.9154]

두 logits이 완전히 동일한가: False
최대 절댓값 차이: 0.56482679
```

- 학습을 하지 않은 무작위 초기화 상태에서도, 같은 논리적 위치(질문의
  마지막 토큰)의 출력이 그 뒤에 정답 토큰이 이어붙는지 여부에 따라
  달라졌습니다. 이는 causal(자기회귀적) 구조가 구조적으로 깨져 있다는
  직접적인 증거입니다.
- 실제 코드베이스를 전수 검색한 결과, causal mask를 생성하는 코드
  (`torch.tril`, `torch.triu` 등)가 프로젝트 전체에 단 한 줄도
  존재하지 않았습니다.

```bash
$ grep -rn 'causal' src/custom_transformer/
(진단 스크립트 자체의 주석/문자열 외에는 결과 없음)

$ grep -rn 'tril\|triu\|mask =' src/custom_transformer/
src/custom_transformer/model/scaled_dot_product_attention.py:36:
            scores = scores.masked_fill(mask == 0, float('-inf'))
(mask를 "사용"하는 코드만 존재, "생성"하는 코드는 없음)
```

- `transformer_model.py`의 `forward(self, input_ids, mask=None)`은
  기본값이 `None`이고, `train.py`가 `model(inputs_tensor)`를 호출할 때
  `mask` 인자를 전혀 넘기지 않습니다. 따라서 `ScaledDotProductAttention`의
  `if mask is not None:` 블록이 실행 경로 전체에서 단 한 번도 작동하지
  않습니다.

**결론: 이 프로젝트는 처음 만들어진 이후 단 한 번도 causal(자기회귀적)
구조로 작동한 적이 없습니다. 학습 시(질문+정답이 함께 입력됨) 모델이
아직 생성하지 않은 미래의 정답 토큰을 attention으로 몰래 참조할 수 있어,
loss는 낮게 나오지만(`0.0006~0.0014`) 실제 생성(질문만 입력)에서는 이
정보가 없어 정답률이 크게 떨어집니다. 이는 weight tying(구 A단계, 현
B단계)보다 근본적이고 우선순위가 높은 결함이며, C단계(클래스 불균형)에서
관찰했던 이상 현상들의 실제 원인일 가능성이 큽니다.**

### 원인 분석

- `scaled_dot_product_attention.py`는 `mask`가 주어지면 미래 위치를
  `-inf`로 채워 가리는 로직(`masked_fill`)은 갖추고 있지만, 그 `mask`
  자체를 생성하는 코드는 프로젝트 어디에도 없습니다.
- `transformer_model.py`의 `forward()`가 `mask=None`을 기본값으로 받고,
  `train.py`의 학습 루프와 `generate()` 메서드 둘 다 `model()`을 호출할
  때 `mask` 인자를 전달하지 않습니다.
- 결과적으로 `DecoderLayer` → `MultiHeadAttention` → `ScaledDotProductAttention`
  전체 호출 체인에서 `mask`는 항상 `None`으로 유지되어, "미래 토큰을
  가린다"는 Transformer decoder의 핵심 전제 자체가 적용되지 않고
  있었습니다.

### 개선 방법

`transformer_model.py`에 causal mask를 생성하는 함수를 추가하고, `forward()`가 `mask`를 받지 못했을 때 이 함수로 자동 생성하도록 수정합니다. `train.py`, `generate()` 등 호출부 코드는 전혀 수정하지 않아도, `forward()` 내부에서 처리됩니다.

```python
# 신규 추가 함수
def generate_causal_mask(seq_len: int, device=None) -> torch.Tensor:
    """
    causal mask(인과 마스크) 생성.

    mask[i, j] = 1  (j <= i, 자기 자신과 과거 위치는 허용)
    mask[i, j] = 0  (j > i, 미래 위치는 차단 -> masked_fill(mask==0, -inf)에서 -inf로 채워짐)

    (1, 1, seq_len, seq_len) 모양으로 반환. multi_head_attention.py에서
    attention score의 모양이 (batch, num_heads, seq, seq)이므로, 앞의 두
    차원(1, 1)이 배치·헤드 차원에 브로드캐스팅되도록 맞춘 것.
    """
    mask = torch.tril(torch.ones(seq_len, seq_len, device=device))
    return mask.unsqueeze(0).unsqueeze(0)


# Before — TransformerLanguageModel.forward()
def forward(self, input_ids, mask=None):
    x = self.embedding(input_ids) * (self.d_model ** 0.5)
    x = self.pos_encoding(x)
    x = self.decoder(x, mask)
    logits = self.output_linear(x)
    return logits

# After
def forward(self, input_ids, mask=None):
    if mask is None:
        seq_len = input_ids.size(1)
        mask = generate_causal_mask(seq_len, device=input_ids.device)

    x = self.embedding(input_ids) * (self.d_model ** 0.5)
    x = self.pos_encoding(x)
    x = self.decoder(x, mask)
    logits = self.output_linear(x)
    return logits
```

- `generate()`는 매 스텝마다 길이가 늘어난 `input_ids`로 `self(input_ids)`를 반복 호출합니다. `forward()`가 매번 그 시점의 `seq_len`에 맞는 mask를 자동으로 새로 만들기 때문에, `generate()` 코드를 고치지 않아도 모든 생성 스텝에 causal mask가 적용됩니다.

### 개선 결과

**1. causal mask 결함 재검증 (`test_causal_mask_fixed.py`)**

```bash
두 logits이 동일한가: True
최대 절댓값 차이: 0.00000000
PASS: causal mask가 정상적으로 미래 토큰을 차단하고 있음을 확인
```

- 수정 전 최대 차이 `0.56482679`였던 것이, 수정 후 `0.00000000`으로
  완전히 일치했습니다. 같은 논리적 위치(질문의 마지막 토큰)의 출력이
  이제 뒤에 무엇이 이어붙든 달라지지 않습니다.

**2. `test_class_balance.py` 재실행 결과**

```bash
--- 3-0. 학습 데이터 원문 자체를 암기했는지 먼저 확인 ---
  '내일 운동 할 거야?' -> '응,' (정답)
  '내일 공부 할 거야?' -> '응,' (정답)
  '내일 베이킹 할 거야?' -> '응,' (정답)
  '오늘 출근 할 거야?' -> '응,' (정답)
  '오늘 친구 만날 거야?' -> '응,' (정답)

원문 그대로 넣었을 때 정답률: 5/5 (100.0%)

--- 3. 미학습 프롬프트에 대한 생성 편향 확인 ---
  '내일 운동 갈 거야?' -> '응,' (응 편향)
  '오늘 공부 할 거야?' -> '응,' (응 편향)
  '오늘 베이킹 할 거야?' -> '응,' (응 편향)
  '내일 출근 할 거야?' -> '응,' (응 편향)
  '내일 친구 만날 거야?' -> '응,' (응 편향)

미학습 프롬프트 5개 중 '응'으로 시작: 5개 (100.0%)
```

**표 1. A단계 수정 전후 완전 대조**
| 검증 항목 | 수정 전 | 수정 후 |
| --- | --- | --- |
| causal mask logits 동일성 | `False` (최대 차이 `0.565`) | `True` (최대 차이 `0.0`) |
| 학습 원문 암기 정답률 | 0/5 (0.0%) | 5/5 (100.0%) |
| 미학습 프롬프트(응으로만 고정된 명사) 생성 결과 | 전부 '아니' (0.0%) | 전부 '응' (100.0%) |

**결론: A단계(causal mask 부재) 수정으로, 암기(3-0)와 일반화(3) 둘 다 완전히 정상화되었습니다. 지금까지 이상 현상(암기 실패, 편향처럼 보였던 생성 결과)이 실제로는 causal mask 결함의 증상이었습니다.**

## B단계: weight tying 버그

### 진단 방법

- `test_parameter_counting.py`로 파라미터 개수를 확인합니다. 전체 파라미터 개수와 각 텐서별 파라미터 개수를 확인할 수 있습니다.
- `test_layer_independence.py`로 4개 층의 객체 id가 실제로 다른지 확인합니다.

```bash
python3 src/custom_transformer/test_parameter_counting.py
python3 src/custom_transformer/test_layer_independence.py
```

### 진단 결과

**1. 파라미터 개수 역산**

```bash
전체 파라미터 수: 943,660
embedding.weight: 76,800개
decoder.layers.0.self_attention.q_linear.weight: 65,536개
decoder.layers.0.self_attention.q_linear.bias: 256개
decoder.layers.0.self_attention.k_linear.weight: 65,536개
decoder.layers.0.self_attention.k_linear.bias: 256개
decoder.layers.0.self_attention.v_linear.weight: 65,536개
decoder.layers.0.self_attention.v_linear.bias: 256개
decoder.layers.0.self_attention.out_linear.weight: 65,536개
decoder.layers.0.self_attention.out_linear.bias: 256개
decoder.layers.0.norm1.weight: 256개
decoder.layers.0.norm1.bias: 256개
decoder.layers.0.ffn.0.weight: 262,144개
decoder.layers.0.ffn.0.bias: 1,024개
decoder.layers.0.ffn.3.weight: 262,144개
decoder.layers.0.ffn.3.bias: 256개
decoder.layers.0.norm2.weight: 256개
decoder.layers.0.norm2.bias: 256개
output_linear.weight: 76,800개
output_linear.bias: 300개
```

- 전체 파라미터 수: `943,660`
- `named_parameters()` 출력에 `decoder.layers.0...`만 존재하고,
  `decoder.layers.1`, `2`, `3`은 전혀 출력되지 않음.
- `decoder.layers.0` 하나의 파라미터 합(`789,760`) + `embedding`(`76,800`) +
  `output_linear`(`77,100`) = `943,660` — 실제 전체 파라미터 수와 정확히 일치.
- 만약 4개 층이 독립적이었다면 예상 총합은 `3,312,940`이어야 하나, 실제로는
  1개 층 분량만 반영됨.

**2. 객체 id 다른지 재현**

- 원본 코드(수정 전)에 검증 스크립트를 실행한 결과, 1번에서 역산했던 가설이 코드 레벨에서 그대로 확인되었습니다.
- 4개 층의 객체 id가 전부 동일한 값(`4557340160`)으로 나와, 첫 번째 검증에서 `AssertionError`가 발생했습니다.

```bash
AssertionError: 4개 층 중 일부가 같은 객체를 공유하고 있음: [4557340160, 4557340160, 4557340160, 4557340160]
```

**결론: 파라미터 개수 역산(1)과 코드 레벨 직접 확인(2), 두 가지 독립된 방법으로 "4개 층이 완전히 같은 객체를 공유하고 있다"는 것이 확인됨.**

### 원인 분석

- `transformer_decoder.py`의 `self.layers = nn.ModuleList([decoder_layer for _ in range(num_layers)])`는 `decoder_layer` 객체 하나를 `num_layers`번 리스트에 담는 코드입니다.
- 이는 서로 다른 파라미터를 가진 `num_layers`개의 독립적인 층을 만드는 게 아니라, 같은 객체를 `num_layers`번 참조하는 것입니다.

### 개선 방법

```python
# Before
self.layers = nn.ModuleList([decoder_layer for _ in range(num_layers)])

# After
import copy
self.layers = nn.ModuleList([copy.deepcopy(decoder_layer) for _ in range(num_layers)])
```

### 개선 결과

**1. 파라미터 개수**

```bash
전체 파라미터 수: 3,312,940
embedding.weight: 76,800개
decoder.layers.0.self_attention.q_linear.weight: 65,536개
decoder.layers.0.self_attention.q_linear.bias: 256개
decoder.layers.0.self_attention.k_linear.weight: 65,536개
decoder.layers.0.self_attention.k_linear.bias: 256개
decoder.layers.0.self_attention.v_linear.weight: 65,536개
decoder.layers.0.self_attention.v_linear.bias: 256개
decoder.layers.0.self_attention.out_linear.weight: 65,536개
decoder.layers.0.self_attention.out_linear.bias: 256개
decoder.layers.0.norm1.weight: 256개
decoder.layers.0.norm1.bias: 256개
decoder.layers.0.ffn.0.weight: 262,144개
decoder.layers.0.ffn.0.bias: 1,024개
decoder.layers.0.ffn.3.weight: 262,144개
decoder.layers.0.ffn.3.bias: 256개
decoder.layers.0.norm2.weight: 256개
decoder.layers.0.norm2.bias: 256개
decoder.layers.1.self_attention.q_linear.weight: 65,536개
decoder.layers.1.self_attention.q_linear.bias: 256개
decoder.layers.1.self_attention.k_linear.weight: 65,536개
decoder.layers.1.self_attention.k_linear.bias: 256개
decoder.layers.1.self_attention.v_linear.weight: 65,536개
decoder.layers.1.self_attention.v_linear.bias: 256개
decoder.layers.1.self_attention.out_linear.weight: 65,536개
decoder.layers.1.self_attention.out_linear.bias: 256개
decoder.layers.1.norm1.weight: 256개
decoder.layers.1.norm1.bias: 256개
decoder.layers.1.ffn.0.weight: 262,144개
decoder.layers.1.ffn.0.bias: 1,024개
decoder.layers.1.ffn.3.weight: 262,144개
decoder.layers.1.ffn.3.bias: 256개
decoder.layers.1.norm2.weight: 256개
decoder.layers.1.norm2.bias: 256개
decoder.layers.2.self_attention.q_linear.weight: 65,536개
decoder.layers.2.self_attention.q_linear.bias: 256개
decoder.layers.2.self_attention.k_linear.weight: 65,536개
decoder.layers.2.self_attention.k_linear.bias: 256개
decoder.layers.2.self_attention.v_linear.weight: 65,536개
decoder.layers.2.self_attention.v_linear.bias: 256개
decoder.layers.2.self_attention.out_linear.weight: 65,536개
decoder.layers.2.self_attention.out_linear.bias: 256개
decoder.layers.2.norm1.weight: 256개
decoder.layers.2.norm1.bias: 256개
decoder.layers.2.ffn.0.weight: 262,144개
decoder.layers.2.ffn.0.bias: 1,024개
decoder.layers.2.ffn.3.weight: 262,144개
decoder.layers.2.ffn.3.bias: 256개
decoder.layers.2.norm2.weight: 256개
decoder.layers.2.norm2.bias: 256개
decoder.layers.3.self_attention.q_linear.weight: 65,536개
decoder.layers.3.self_attention.q_linear.bias: 256개
decoder.layers.3.self_attention.k_linear.weight: 65,536개
decoder.layers.3.self_attention.k_linear.bias: 256개
decoder.layers.3.self_attention.v_linear.weight: 65,536개
decoder.layers.3.self_attention.v_linear.bias: 256개
decoder.layers.3.self_attention.out_linear.weight: 65,536개
decoder.layers.3.self_attention.out_linear.bias: 256개
decoder.layers.3.norm1.weight: 256개
decoder.layers.3.norm1.bias: 256개
decoder.layers.3.ffn.0.weight: 262,144개
decoder.layers.3.ffn.0.bias: 1,024개
decoder.layers.3.ffn.3.weight: 262,144개
decoder.layers.3.ffn.3.bias: 256개
decoder.layers.3.norm2.weight: 256개
decoder.layers.3.norm2.bias: 256개
output_linear.weight: 76,800개
output_linear.bias: 300개
```

- `decoder.layers.0`부터 `decoder.layers.3`까지 전부 독립적으로 출력되고, 전체 파라미터 수가 진단 단계에서 역산했던 예상값(`3,312,940`)과 정확히 일치합니다.

**2. 학습 발산 재검증**

```bash
=== A단계 재검증: weight tying 수정 후 학습 발산 확인 ===

PASS: test_layers_are_independent_objects (4개 층의 객체 id 전부 다름:
[4564901776, 4564903696, 4562579408, 4562580928])
학습 전 층 간 L2 거리:
  layer0 vs layer1: 0.000000
  layer0 vs layer2: 0.000000
  layer0 vs layer3: 0.000000
  layer1 vs layer2: 0.000000
  layer1 vs layer3: 0.000000
  layer2 vs layer3: 0.000000
학습 후 층 간 L2 거리:
  layer0 vs layer1: 1.711410
  layer0 vs layer2: 1.841736
  layer0 vs layer3: 1.810457
  layer1 vs layer2: 1.163518
  layer1 vs layer3: 1.630758
  layer2 vs layer3: 1.120531
PASS: test_layers_diverge_after_training (학습 후 모든 층 쌍의 L2 거리가 0.0001 초과, 독립적으로 학습됨 확인)

모든 검증 통과: A단계(weight tying 버그) 수정이 완전히 확인됨.
```

**표 1. 진단 vs 결과 대조**
| 항목 | 진단 (수정 전) | 결과 (수정 후) |
| --- | --- | --- |
| 4개 층의 객체 id | 전부 동일 → `AssertionError` | 전부 다름 |
| 학습 전 층 간 L2 거리 | 확인 불가 (진단 단계에서 에러로 중단) | 전부 `0.000000` |
| 학습 후 층 간 L2 거리 | 확인 불가 | `1.120531 ~ 1.841736` |

1. **`named_parameters()`에 `decoder.layers.0`부터 `decoder.layers.3`까지 전부 출력되는가**: YES. 수정 전에는 `layers.0`만 존재했으나, 수정 후 실행 로그에 `layers.0`, `layers.1`, `layers.2`, `layers.3`이 각각 독립적인 파라미터 집합으로 전부 출력됩니다.

2. **전체 파라미터 수가 `3,312,940`에 근접하는가**: YES. 실행 로그의 `전체 파라미터 수: 3,312,940`이 진단 단계에서 역산했던 예상값과 정확히 일치합니다.

3. **학습 후 4개 층의 가중치가 서로 다른 값으로 발산하는가**: YES. 학습 전에는 층 간 L2 거리가 전부 `0.000000`이었으나 학습 후에는 `1.120531~1.841736` 범위로 모든 층 쌍이 뚜렷하게 발산했습니다.

**결론: A단계(weight tying 버그)가 진단(파라미터 개수 역산 + 코드 레벨 재현) → 원인 분석 → 개선(deepcopy) → 결과(구조·학습 발산 확인) 전 과정을 완결**

## C단계: 클래스 불균형

### 진단 방법

- `test_class_balance.py`로 데이터 응/아니 비율을 확인하고, 학습 데이터 원문 암기 여부와 미학습 프롬프트에 대한 클래스별(응/아니) 생성 정확도를 확인합니다.
- `test_class_balance_repeated.py`로 동일한 파이프라인(학습→평가)을 `seed` 고정 없이 5회 반복 실행하여, 결과의 안정성을 확인합니다.

```bash
python3 src/custom_transformer/test_class_balance.py
python3 src/custom_transformer/test_class_balance_repeated.py
```

### 진단 결과 (A단계 수정 후, 데이터 확장 전 — 24개 기준)

```bash
전체 QA 쌍: 24개
'응'으로 시작: 17개
'아니'로 시작: 7개
응:아니 비율 = 17:7 (약 2.4:1)

미학습 프롬프트 클래스별 정확도:
  '응' 그룹: 5/5 (100.0%)
  '아니' 그룹: 2/3 (66.7%) -- '오늘 쇼핑 할 거야?' 오답
```

- '아니' 그룹에서 유일하게 틀린 "쇼핑" 사례를 분석한 결과, 진단 프롬프트 자체가 원본 데이터의 '응' 케이스(내일+할)와 '아니' 케이스(오늘+갈) 사이에서 요일·어미가 절반씩 겹치는 애매한 조합이었다는 것이 확인됐습니다.
- 다만 표본 수(응 5개 vs 아니 3개) 자체가 너무 적어, 이 결과만으로 "클래스 불균형이 문제다/아니다"를 결론짓기 어려웠습니다.

### 원인 분석

- 데이터 24개 중, 요일·어미·번복이 뒤섞이지 않고 순수하게 한쪽 클래스로만 고정된 "순수 케이스"는 응 5개, 아니 2~3개뿐이었습니다.
- 표본이 이렇게 적으면, 특정 단어 하나의 우연한 얽힘(예: 쇼핑)이 전체 클래스 정확도를 크게 흔들어버려 정확한 진단이 어렵습니다.
- 데이터를 무작정 늘리기보다, 명사당 정답을 하나로 고정하고 어미·요일을 다양화하는 방식(통제된 확장)으로 순수 케이스 자체를 늘리기로 했습니다.

### 개선 방법

- `korean_qa.txt`에 새로운 명사 6개(수영, 등산, 낚시 — 아니 클래스 / 요가, 캠핑, 청소 — 응 클래스)를 추가했습니다. 각 명사는 어미·요일을 다양화하되 정답 클래스는 고정해서, "이 명사는 항상 이 클래스"라는 관계가 명확하게 드러나도록 설계했습니다.

  ```txt
  <!-- 신규 추가 9개 줄 (기존 24개는 그대로 유지) -->
  오늘 수영 할 거야?	아니, 수영 대신 산책 할 거야
  내일 수영 갈 거야?	아니, 수영 대신 산책 할 거야
  오늘 등산 갈 거야?	아니, 등산 대신 헬스장 갈 거야
  내일 등산 할 거야?	아니, 등산 대신 헬스장 갈 거야
  오늘 낚시 갈 거야?	아니, 낚시 대신 독서 할 거야
  오늘 요가 할 거야?	응, 요가 할 거야
  내일 요가 갈 거야?	응, 요가 갈 거야
  내일 캠핑 갈 거야?	응, 캠핑 갈 거야
  오늘 청소 할 거야?	응, 청소 할 거야
  ```

- 전체 데이터: 24개 → 33개
- 응:아니 비율: 17:7(2.4:1) → 21:12(1.8:1)로 완만해짐

### 개선 결과

**1. 1회 재검증 (`test_class_balance.py`, 데이터 33개)**

```bash
'응' 그룹 정확도: 5/5 (100.0%)
'아니' 그룹 정확도: 3/3 (100.0%)  -- '쇼핑'도 이번엔 정답
```

- 지난번 유일한 실패 사례였던 "쇼핑"까지 포함해 전부 정답이 나왔으나, `seed`가 고정되지 않아 이 결과가 데이터 확장의 실제 효과인지 우연인지 구분이 어렵습니다.

**2. 5회 반복 검증 (`test_class_balance_repeated.py`, seed 고정 없음)**

```bash
'응' 그룹 정확도: [100%, 100%, 100%, 100%, 100%]
  평균: 100.0%, 최솟값: 100.0%, 최댓값: 100.0%
'아니' 그룹 정확도: [100%, 100%, 67%, 100%, 33%]
  평균: 80.0%, 최솟값: 33.3%, 최댓값: 100.0%
```

**표 1. 클래스별 안정성 비교**
| 그룹 | 표본 수 | 5회 평균 | 5회 최솟값 | 안정성 |
| --- | --- | --- | --- | --- |
| 응 | 21개 | 100.0% | 100.0% | 매우 안정적 |
| 아니 | 12개 | 80.0% | 33.3% | 불안정 (시행마다 편차 큼) |

**결론: "응" 그룹은 표본이 더 많음에도 5회 모두 완벽했던 반면, "아니" 그룹은 표본이 상대적으로 적어(12개) 학습 시행마다 결과가 크게 흔들렸습니다. 이는 클래스 불균형이 실제 문제라는 가설을 뒷받침하며, 24개에서 33개로의 확장은 평균 정확도(80%)를 개선했지만 안정성 문제를 완전히 해소하지는 못했습니다.**

## 한계 (부분 개선)

- 데이터 확장(24개 → 33개)으로 "아니" 그룹 평균 정확도가 개선되었으나 (이전 66.7% 단일 시행 → 80.0% 5회 평균), 여전히 시행 간 편차가 크게 남아있어 완전히 해결되지 않았습니다.
- 향후 추가 조치로 다음 두 방향을 고려할 수 있습니다.
  1. "아니" 클래스 표본을 "응" 클래스 수준(21개 근처)까지 추가로 확장
  2. 데이터 추가 대신 정규화(dropout 조정) 또는 조기 종료 등 학습 방식 자체를 개선하는 방향
- D단계(과적합)와 근본 원인이 겹칠 가능성이 있어, D단계 진행 시 이 문제를 함께 다룰 수 있습니다.

## D단계: 과적합

### 진단 방법

- `test_overfitting.py`로 33개 데이터 중 7개(응 4개, 아니 3개)를 학습에서 완전히 제외한 validation set으로 떼어두고, epoch마다 train loss와 validation loss를 함께 측정합니다.

```bash
python3 src/custom_transformer/test_overfitting.py
```

### 진단 결과

```bash
train: 26개, validation: 7개

 epoch |   train_loss |     val_loss
     1 |       2.5318 |       2.2371
    10 |       0.1705 |       1.5225
    30 |       0.0569 |       1.3938
    40 |       0.0506 |       1.3913
    70 |       0.0459 |       1.4011
    80 |       0.7949 |       2.2071
   100 |       0.0492 |       1.9831

validation loss가 최소였던 epoch: 39 (val_loss=1.3319)
마지막 epoch(100): train_loss=0.0492, val_loss=1.9831
```

- `train_loss`는 `2.53 → 0.05`까지 계속 낮게 유지되는 반면, `val_loss`는 epoch 39(`1.3319`)에서 최저점을 찍은 뒤 epoch 100 시점엔 `1.9831`로 다시 크게 올랐습니다(최저 대비 +48.9%). 학습 loss는 계속 낮은데 검증 loss만 다시 오르는 전형적인 과적합 신호입니다.

### 원인 분석

- 현재 모델(`d_model=256, num_layers=4, d_ff=1024`)은 파라미터 `3,312,940`개(B단계 weight tying 수정 후 기준)를 갖는 반면, 학습 데이터는 33개(train 26개)뿐입니다. 모델의 표현력(capacity)이 데이터 규모에 비해 압도적으로 커서, 데이터를 일반화하기보다 암기하기 쉬운 구조입니다.

### 개선 방법 및 결과 (7개 조건 비교)

3가지 개선 방향(조기 종료, 모델 축소, dropout 상향)을 단독으로, 이어서 가장 효과적이었던 모델 축소를 기준으로 3가지 조합을 추가 실험했습니다. 모든 조건에서 `test_overfitting.py`와 동일한 train/validation 분리와 측정 방식을 유지했습니다.

```bash
python3 src/custom_transformer/test_overfitting_improvements.py
```

**표 1. 7개 조건 최종 비교**
| 조건 | 설정 | best*val_loss | 종료 epoch | 반등폭 |
| --- | --- | --- | --- | --- |
| 베이스라인 | d_model=256, layers=4, dropout=0.1, 조기종료 없음 | 1.5214 | 100 | +20.1% |
| 개선1*조기종료 | 베이스라인 + 조기종료(patience=10) | 1.4832 | 27 | +15.3% |
| **개선2\_모델축소** | d*model=64, layers=2, d_ff=256 + 조기종료 | 1.6216 | 44 | **+1.7%** |
| 개선3_dropout상향 | 베이스라인, dropout=0.4 + 조기종료 | 1.5760 | 17 | +8.0% |
| 조합1*축소+dropout0.15 | 개선2 + dropout=0.15 | 1.7340 | 30 | +3.6% |
| 조합2*축소+dropout0.2 | 개선2 + dropout=0.2 | 1.8307 | 31 | +4.4% |
| 조합3*축소+patience5 | 개선2 + patience=5 | 1.6710 | 23 | +2.0% |

- 조합 실험(dropout 추가, patience 축소)은 전부 개선2(순수 모델 축소)
  대비 오히려 악화됐습니다. 이미 축소된 모델에 dropout을 더하면
  underfitting(모델이 데이터를 충분히 학습하기도 전에 정규화가 과도하게
  작용하는 현상)이 심해지고, patience를 더 줄이면 학습이 덜 된 상태에서
  일찍 멈춰 best_val_loss가 소폭 나빠집니다.
- 절대 성능(best_val_loss)만 보면 개선1(조기 종료만, `1.4832`)이
  가장 낮았지만, 반등폭은 개선2(모델 축소, `1.7%`)가 압도적으로
  낮았습니다(개선1은 `15.3%`).

### 최종 채택: 개선2 (모델 축소 + 조기 종료)

- 절대 성능(개선1)과 안정성(개선2) 중, 이번 프로젝트의 목적(Transformer 구성 요소를 근본적으로 이해하는 학습 목적)에 맞춰 **안정성**을 우선했습니다. 개선2는 D단계 원인 분석("모델이 데이터 대비 과도하게 크다")과 개선 방법(모델을 줄인다)이 직접 대응되는 반면, 개선1(조기 종료만)은 근본 원인을 건드리지 않고 증상만 완화하는 조치이기 때문입니다.
- `d_model=256->64`, `num_layers=4->2`로 파라미터를 크게 줄였음에도 validation loss 최저값은 베이스라인과 대등했고(`1.6216` vs `1.5214`), 반등폭은 `20.1% → 1.7%`로 대폭 개선됐습니다.

```bash
전체 파라미터 수: 336,812
embedding.weight: 19,200개
decoder.layers.0.self_attention.q_linear.weight: 4,096개
decoder.layers.0.self_attention.q_linear.bias: 64개
decoder.layers.0.self_attention.k_linear.weight: 4,096개
decoder.layers.0.self_attention.k_linear.bias: 64개
decoder.layers.0.self_attention.v_linear.weight: 4,096개
decoder.layers.0.self_attention.v_linear.bias: 64개
decoder.layers.0.self_attention.out_linear.weight: 4,096개
decoder.layers.0.self_attention.out_linear.bias: 64개
decoder.layers.0.norm1.weight: 64개
decoder.layers.0.norm1.bias: 64개
decoder.layers.0.ffn.0.weight: 65,536개
decoder.layers.0.ffn.0.bias: 1,024개
decoder.layers.0.ffn.3.weight: 65,536개
decoder.layers.0.ffn.3.bias: 64개
decoder.layers.0.norm2.weight: 64개
decoder.layers.0.norm2.bias: 64개
decoder.layers.1.self_attention.q_linear.weight: 4,096개
decoder.layers.1.self_attention.q_linear.bias: 64개
decoder.layers.1.self_attention.k_linear.weight: 4,096개
decoder.layers.1.self_attention.k_linear.bias: 64개
decoder.layers.1.self_attention.v_linear.weight: 4,096개
decoder.layers.1.self_attention.v_linear.bias: 64개
decoder.layers.1.self_attention.out_linear.weight: 4,096개
decoder.layers.1.self_attention.out_linear.bias: 64개
decoder.layers.1.norm1.weight: 64개
decoder.layers.1.norm1.bias: 64개
decoder.layers.1.ffn.0.weight: 65,536개
decoder.layers.1.ffn.0.bias: 1,024개
decoder.layers.1.ffn.3.weight: 65,536개
decoder.layers.1.ffn.3.bias: 64개
decoder.layers.1.norm2.weight: 64개
decoder.layers.1.norm2.bias: 64개
output_linear.weight: 19,200개
output_linear.bias: 300개
```

### 한계

- 개선2를 적용해도 반등폭이 완전히 0은 아닙니다(`1.7%`). 이는 모델 크기를 줄이는 것만으로 과적합이 완전히 사라지는 게 아니라, **데이터 양(33개) 자체의 한계가 여전히 남아있다는 신호**입니다.
  - **`반등폭(rebound_pct)` 지표 자체의 한계**: 이 지표는 논문이나 업계 표준으로 정의된 공식 지표가 아니라, 이번 진단을 위해 임의로 정의한 계산식입니다. 일반적으로 실무에서는 대략 5% 미만은 무시 가능한 수준, 5~15%는 경미한 신호, 20~30% 이상을 명확한 과적합으로 보는 경험칙이 통용되지만, 이는 공인된 기준이 아니라 관용적 어림값입니다.
  - **validation 표본 수(7개)로 인한 통계적 불안정성**: validation set이 7개뿐이라, 샘플 1개의 loss가 소폭(약 1.0)만 바뀌어도 전체 평균이 약 10.6%로 흔들릴 수 있습니다. 따라서 개선2(`1.7%`)와 조합3(`2.0%`)처럼 차이가 작은 조건끼리는 실제로 의미 있는 차이인지 통계적으로 확신하기 어렵습니다. 다만 베이스라인(`20.1%`)과 개선2(`1.7%`) 사이의 10배 이상 격차는 이 노이즈 수준을 훨씬 벗어나므로, "모델 축소가 과적합을 뚜렷하게 완화했다"는 결론 자체는 신뢰할 수 있습니다.
- C단계(클래스 불균형)에서 이미 "아니" 클래스 표본 부족(12개)이 학습 안정성을 떨어뜨린다는 게 확인된 바 있는데, D단계의 이 잔여 반등폭도 같은 근본 원인(데이터 절대량 부족)을 공유하는 것으로 판단됩니다.
- 향후 데이터를 추가로 확보하면, 모델 크기를 다시 늘려도 반등폭이 억제되는지 재검증할 필요가 있습니다. 지금 시점에서는 "작은 데이터에는 작은 모델"이라는 원칙을 확인한 것으로 D단계를 마무리했습니다.
