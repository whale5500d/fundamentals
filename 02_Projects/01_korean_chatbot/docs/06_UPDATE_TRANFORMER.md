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

- `test_parameter_counting.py` 파일은 파라미터 개수를 확인하는 검수용 코드입니다. 해당 파일을 통해 전체 파라미터 개수와 각 텐서별 파라미터 개수를 확인할 수 있습니다.

```bash
python3 src/custom_transformer/test_parameter_counting.py # 실행 명령어
```
