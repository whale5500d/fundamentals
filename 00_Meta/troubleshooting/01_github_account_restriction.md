# GitHub 계정 제한 트러블슈팅

## 목차

1. [계정 활동 악용 여부 확인 방법 부재](#트러블-슈팅-1---계정-활동-악용-여부-확인-방법-부재)
2. [Security log에서 발견된 webhook의 실제 출처 규명](#트러블-슈팅-2---security-log에서-발견된-webhook의-실제-출처-규명)
3. [계정 제한의 실제 원인 후보 특정](#트러블-슈팅-3---계정-제한의-실제-원인-후보-특정)
4. [Archived 티켓에 대한 후속 대응 방법](#트러블-슈팅-4---archived-티켓에-대한-후속-대응-방법)
5. [Support 사용 목적 문의에 대한 답변 수준 결정](#트러블-슈팅-5---support-사용-목적-문의에-대한-답변-수준-결정)

---

## 트러블 슈팅 1 - 계정 활동 악용 여부 확인 방법 부재

### 문제 상황

GitHub Support로부터 "Some activity on your account was flagged by our abuse-detection systems for manual review"라는 답변만 받았고, 계정이 실제로 탈취되거나 악용되었는지 확인할 방법이 없었음.

### 고려한 옵션

- Cesium ion 토큰 사용량(usage) 조회
- GitHub Security log(계정 활동 로그) JSON export 조회
- GitHub Actions billing 사용량 조회

### 결정 및 이유

세 경로를 모두 병행 확인하기로 결정. Cesium 토큰은 이미 regenerate되어 과거 사용 이력 자체를 조회할 수 없어 배제, Security log는 로그인·OAuth 인가·토큰 발급 이벤트를 직접 검토, Actions billing은 크립토 마이닝 등 컴퓨트 악용 여부를 과금 이력으로 즉시 판별 가능해 세 경로 병행이 가장 빠르게 원인 후보를 좁히는 방법이라 판단함.

---

## 트러블 슈팅 2 - Security log에서 발견된 webhook의 실제 출처 규명

### 문제 상황

Security log 분석 중 axios User-Agent로 생성된 미인식 webhook(`hook.create`) 2건 발견. 브라우저가 아닌 HTTP 클라이언트로 직접 API를 호출한 흔적이라 PAT(Personal Access Token) 유출을 의심함.

### 원인 분석

Classic/Fine-grained PAT 목록 어디에도 해당 저장소 관련 토큰이 없음을 확인. 로그 레코드 전체 필드를 재검토한 결과, `oauth_application: "Notion"`, `programmatic_access_type: OAuth access token`으로 명시되어 있었고, webhook URL 패턴(`notion.so/eap/webhook/...`)이 Notion의 GitHub 링크 자동 연동 기능과 일치함을 확인함.

### 결정 및 대응

본인이 해당 두 저장소 링크를 Notion 페이지에 붙여넣은 사실을 확인해 정상 동작으로 결론. 이미 삭제한 webhook은 재생성하지 않고 종결 처리함.

### 인사이트

GitHub의 인증 메커니즘은 PAT(Developer settings)와 OAuth App(Authorized OAuth Apps)이 완전히 별개 경로로 관리된다. "PAT 목록에 없다"는 사실만으로는 제3자 접근 가능성을 배제할 수 없으며, 이상 징후 조사 시 두 경로를 모두 확인해야 한다.

---

## 트러블 슈팅 3 - 계정 제한의 실제 원인 후보 특정

### 문제 상황

자격증명 관련 원인 후보(계정 탈취, PAT 유출, Actions 악용, OAuth App 오작동)를 모두 배제했음에도 계정 제한의 원인이 여전히 불명확했음.

### 원인 분석

남은 유일한 후보로 저장소 콘텐츠 자체를 재검토함. `fullstack_iran-osint-4d-map` 저장소의 README가 특정 국가의 군사·분쟁 상황(공습 대응, 비행 금지 구역 탐지, GPS 재밍 탐지 등)을 실시간 추적하는 프레이밍으로 작성되어 있었음. GitHub Acceptable Use Policies상 다중 서비스 자동 스크래핑과 분쟁 관련 프레이밍의 조합이 자동 탐지 대상이 될 수 있음을 확인함.

### 결정 및 대응

해당 저장소를 즉시 private으로 전환. GitHub Support에 조사 과정 전체(자격증명 관련 배제 근거 포함)와 함께 해당 저장소를 원인으로 특정해 재문의함. 추후 비민감 소재(예: 자연재해 모니터링)로 재작성 후 공개 전환 예정.

### 인사이트

플랫폼의 자동 탐지 시스템은 자격증명 유출뿐 아니라 콘텐츠 프레이밍만으로도 발동할 수 있다. 기술적으로 완전히 안전한 프로젝트라도, README 등 설명 문구의 표현 방식(특히 실제 분쟁 상황과 결부된 서술)에 따라 플랫폼 정책 위반으로 분류될 위험이 있다.

---

## 트러블 슈팅 4 - Archived 티켓에 대한 후속 대응 방법

### 문제 상황

기존 GitHub Support 티켓(#4346072)이 Archived 상태로 전환되어 있어, 조사 결과를 정리한 뒤 해당 스레드에 직접 답장할 수 없었음.

### 고려한 옵션

- 그대로 방치하고 별도 대응하지 않음
- 다른 문의 채널로 새로 연락
- Follow-up 티켓을 새로 생성

### 결정 및 이유

Follow-up 티켓 생성을 선택함. 본문 서두에 이전 티켓 번호(#4346072)를 명시해, 담당자가 기존 맥락(원 문의 내용, 이전 답변)을 바로 참조할 수 있도록 연속성을 확보하는 방식이 가장 효율적이라 판단함.

---

## 트러블 슈팅 5 - Support 사용 목적 문의에 대한 답변 수준 결정

### 문제 상황

Support 담당자(Ivy)가 "GitHub을 어떻게 사용할 계획인지" 질문함. 실제 저장소 목록이 코드네임(예: `dang_geune_daong`, `fires_investment`) 형태로 구성되어 있어, 어느 수준까지 구체적으로 설명해야 할지 불명확했음.

### 고려한 옵션

- 저장소를 하나하나 이름과 함께 상세 나열
- Project / PL / TIL 카테고리 단위로 간결하게 설명

### 결정 및 이유

카테고리 단위 설명을 선택함. 코드네임을 그대로 나열하면 담당자가 각각의 의미를 되물어야 해 처리가 오히려 지연될 우려가 있었고, 카테고리 설명만으로도 Public/Private 혼재 이유와 문제 저장소의 위치(Project 카테고리 내)를 자연스럽게 포괄할 수 있어 더 효율적이라 판단함.
