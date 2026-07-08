# Transformer 개선 작업

## 배경

- `custom_transformer`를 사용해 모델의 개선 작업을 진행하고자 합니다. 문제를 성격별로 분류하고, 우선순위가 높은 것부터 하나씩 "문제 재현 → 진단 → 개선 → 재검증" 순서로 다룰 예정입니다.

## 개선 작업 로드맵

**표 1. 개선 작업 로드맵**
| 단계 | 다루는 문제 | 상태 |
| --- | --- | --- |
| A | weight tying 버그 (`transformer_decoder.py`) | 진단 완료, 수정 대기 |
| B | 클래스 불균형 (응:아니 = 3:1) | 예정 |
| C | 과적합 (데이터 24개 vs 파라미터 수백만) | 예정 |
| D | 문형 단일성 (일반화 실패) | 예정 |
| E | Post-LN → Pre-LN | 예정 |
| F | mask 차원, batch 생성 | 예정 |

## 진단 방법

- `test_parameter_counting.py`로 파라미터 개수를 확인합니다. 전체 파라미터 개수와 각 텐서별 파라미터 개수를 확인할 수 있습니다.
- `test_layer_independence.py`로 4개 층의 객체 id가 실제로 다른지 확인합니다.

```bash
python3 src/custom_transformer/test_parameter_counting.py
python3 src/custom_transformer/test_layer_independence.py
```

## A단계: weight tying 버그

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
