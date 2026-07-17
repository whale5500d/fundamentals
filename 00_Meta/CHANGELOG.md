# Changelog

## 2026-07-15 (Repository Consolidation)

1. 진행 작업
   - 00_BASIC의 python/java/javascript 폴더 → `06_Programing_Language/01_Basic` 이관 (완료)
     - 경로 rename이 필요해 filter-repo + merge 방식 사용
   - 00_BASIC의 04_algorithm 폴더 → `06_Programing_Language/03_Algorithms` 이관 (완료)
   - 00_BASIC의 06_math 폴더 → `06_Programing_Language/02_Math` 이관 (완료)
2. 결정 사항
   - TIL 병합 보류. 기존 TIL 저장소 내용은 이번 fundamentals 구조의 TIL과 성격이 다름(부트캠프 학습 내용 등 별도 재정의 필요)
3. 관련 문서
   - [GitHub 계정 제한 트러블슈팅](./troubleshooting/01_github_account_restriction.md)
   - [Git History Consolidation 트러블슈팅](./troubleshooting/02_git_history_consolidation.md)

## 2026-07-16 (Repository Consolidation)

1. 진행 작업
   - `01_FE/04_dang_geune_daong` → 새 계정(`whale5500d`) 저장소 `01_dang_geune_daong`로 이관 (완료)
   - `01_FE/05_fires` → 새 계정(`whale5500d`) 저장소 `02_snowball`로 이관 (완료)
2. 결정 사항
   - 저장소 네이밍 규칙 확정: 기본값은 접두사 없음(암묵적 public), private인 경우만 `private_` 접두사 부여
