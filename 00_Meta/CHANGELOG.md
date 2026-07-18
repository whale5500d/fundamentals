# Changelog

## 2026-07-15 (Repository Consolidation)

1. 진행 작업
   - 00_BASIC의 python/java/javascript 폴더 → `06_Programing_Language/01_Basic` 이관 (완료 ✅)
     - 경로 rename이 필요해 filter-repo + merge 방식 사용
   - 00_BASIC의 04_algorithm 폴더 → `06_Programing_Language/03_Algorithms` 이관 (완료 ✅)
   - 00_BASIC의 06_math 폴더 → `06_Programing_Language/02_Math` 이관 (완료 ✅)
2. 결정 사항
   - TIL 병합 보류. 기존 TIL 저장소 내용은 이번 fundamentals 구조의 TIL과 성격이 다름(부트캠프 학습 내용 등 별도 재정의 필요)
3. 관련 문서
   - [GitHub 계정 제한 트러블슈팅](./troubleshooting/01_github_account_restriction.md)
   - [Git History Consolidation 트러블슈팅](./troubleshooting/02_git_history_consolidation.md)

## 2026-07-16 (Repository Consolidation)

1. 진행 작업
   - `01_FE/04_dang_geune_daong` → 새 계정(`whale5500d`) 저장소 `01_dang_geune_daong`로 이관 (완료)
   - `01_FE/05_fires` → 새 계정(`whale5500d`) 저장소 `02_snowball`로 이관 (완료)
   - `01_FE/06_account_stop_the_store` → 새 계정(`whale5500d`) 저장소 `03_account_stop_the_store`로 이관 (완료)
   - `01_FE/02_kakao_enterprise/kakaoenterprise_ce_fe_report_임경락` → 새 계정(`whale5500d`) 저장소 `04_kakao_enterprise_assignment`로 이관 (완료)
2. 결정 사항
   - 저장소 네이밍 규칙 확정: 기본값은 접두사 없음(암묵적 public), private인 경우만 `private_` 접두사 부여

## 2026-07-17 (Repository Consolidation)

1. 진행 작업
   - `01_dev`가 단일 저장소가 아닌 11개(client, project\_\_etc 제외 시 9개)의 개별 git 히스토리로 구성되어 있음을 확인
   - `module__front__icon`, `module__front__ui`, `module__front__util` → Organization(`whale5500d-crypto`) 저장소 `private_module__front__icon/ui/util`로 각각 이관 (완료 ✅)
   - `project__front__explorer`, `project__front__bitcoint-landing`, `project__front__dapping-landing`, `project__front__wallet` → Organization 저장소 `private_project__front__*`로 각각 이관 (완료 ✅)
   - `frontend-mono` → Organization 저장소 `private_frontend-mono`로 이관 (완료 ✅, 기본 브랜치 `dev` 유지)
   - `project__front__hyper-liquid` → Personal 계정 저장소 `05_crypto_exchange_clone_hyperliquid`로 이관 (완료 ✅, public)
   - `client`(wallet 실행용 백엔드), `project__etc`(연습 코드)는 이번 이관에서 보류
   - `03_FullStack/01_Ringle` → 새 계정(`whale5500d`) 저장소 `06_ringle_assignment`로 이관 (완료 ✅)
   - `02_Projects/01_korean_chatbot` → 별도 저장소 `07_scheduling_ai_chatbot`로 분리 (완료 ✅, `git filter-repo --subdirectory-filter` 방식 사용, 히스토리 보존)
     - `checkpoints/korean_model.pt`는 `.gitignore` 대상이라 히스토리 이관 없이 로컬 파일만 새 위치로 직접 복사
     - `fundamentals`에서 `02_Projects/01_korean_chatbot` 제거 완료
   - `02_certificate`(AICE BASIC/ASSOCIATE 학습 자료) → `03_Technologies/01_AI/aice_certificate`로 병합 (완료 ✅, filter-repo + merge 방식, 히스토리 보존)
2. 결정 사항
   - `module_*`, `project_*`, `frontend-mono`는 서로 강하게 연관된 프로젝트군이라 판단, Organization(`whale5500d-crypto`)을 신설해 그룹으로 관리하기로 결정
   - Organization 소속 저장소는 넘버링·긴 접두사 없이 `private_원본폴더명` 형식으로 네이밍
