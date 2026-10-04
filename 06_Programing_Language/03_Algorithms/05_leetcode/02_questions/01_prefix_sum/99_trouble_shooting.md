# Trouble Shooting

## 260923

### 추론 검증 정리 - Prefix Sum 구간 합 공식에서 prefix[0] = 0 초기화가 필요한 이유

**문제 상황**: LeetCode 303 (Range Sum Query - Immutable)에서 `sumRange(left, right)`를 prefix sum (누적합)으로 구현하는 과정에서, 정답 코드가 `self.prefix = [0]`으로 초기화하고 `prefix[right + 1] - prefix[left]`를 사용하는 이유를 확인함.

**추론한 내용**: 구간 합은 (`right`까지의 합) - (`left - 1`까지의 합)이므로 `prefix[right] - prefix[left - 1]`이며, `prefix`는 `[]`로 초기화하고 `prefix[i]`는 `nums[0..i]`의 합이다.

**검증 결과**: 부분 성공. 구간 합 = (`right`까지의 합) - (`left - 1`까지의 합)이라는 일반형은 정확함. 부정확한 부분은 `prefix[i]`를 원소가 1개 이상인 구간의 합으로만 정의한 점이며, `left == 0`일 때 필요한 `nums[0..-1]`(원소 0개인 구간의 합, 값 `0`)을 저장할 인덱스가 없어 식이 `left == 0` 분기와 그 외로 갈라짐.

**결론**: `prefix[0] = 0`(빈 구간의 합)을 포함하도록 `prefix`의 정의를 `nums`의 앞 `i`개 원소의 합으로 확장함. 이 정의에서 `nums[0..right]`는 앞의 `right + 1`개, `nums[0..left-1]`는 앞의 `left`개이므로 공식은 `prefix[right + 1] - prefix[left]`이고, 모든 `left`에서 분기 없이 하나의 식으로 처리됨.

**개념이 포함된 섹션**: Algorithms

**개념이 포함된 섹션**: PL
