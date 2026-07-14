# Linux

## 한 줄 개념 정리

### 배경 및 필요성

- 유닉스 계열 OS는 3가지 원칙에 따라 작은 도구를 조합하는 방식으로 설계. 리눅스 키워드는 해당 원칙으로 만들어진 구현체(instance)
  1. (단일 책임) Write programs that do one thing and do it well.
  2. (조합 가능성) Write programs to work together.
  3. (범용 인터페이스) Write programs to handle text streams

### 개념 정리 및 핵심 원리

- 핵심 원리
  - 다룰 대상(Entity) 기준: file, process, network, text
  - 수행 관계(Relation) 기준: read, transform, combine, manage
- 개념 정의
  - Linux: Unix 기반의 오픈소스 운영체제 커널

### Linux 사용

- (Entity 기준) **Shell Env 설정**
  - 개념
    - Linux Shell: 리눅스의 커널과 사용자를 연결해주는 인터페이스
    - 환경 변수: 프로세스가 컴퓨터의 동작 방식에 영향을 미치는 key-value
    - 편집기
      - Vi: 키워드로 파일을 편집하는 텍스트 편집기. 명령 모드, 명령행 모드, 입력 모드로 구성.
      - Nano: 유닉스 계열 컴퓨팅 시스템이나 명령줄 인터페이스를 사용하는 편집기
- (Entity 기준) **Text Stream 처리**
  - (Relation 구조 기준) 중심 명령어
    - **Pipe**: 여러 명령어를 전달하는 기능을 실행하는 중심 명령어
      - 표준 인터페이스 규약(interface contract) 따라 stdin, stdout, stderror 표기
  - (Relation 구조 기준) 세부 명령어
    - Head/Tail: Read, 기본적으로 처음/마지막 10줄
    - Grep: Read, 특정 패턴 기준으로 필터링
    - Sed: Transform, 특정 패턴 기준으로 수정 (고급 명령어)
    - Sort: Transform, 정렬
    - Uniq: Transform, 중복 제거 (정렬된 입력을 전제로 함)
    - Awk: Transform, 줄 또는 필드 기반 처리
    - Jq: Transform, JSON 전용 필드 기반 처리
    - WC: Etc(_Summary_), 줄/단어/바이트 개수 등을 집계
    - Diff: Etc(_Compare_), 두 파일을 비교
    - CMP: Etc(_Compare_), 두 파일을 비교 (무슨 차이?)
- (Entity 기준) **File System 처리**
  - 개념
    - File Permission: 파일과 디렉터리에 접근 가능한 대상을 관리하는 규칙
    - Tar: 리눅스용 파일 패키징 도구(또는 확장자)
    - inode: 메타데이터를 갖고 있는 구조체
  - 명령어
    - 프로세스 모니터링:
      - Top: 실시간 프로세스 모니터링
      - PS: 현재 시점 프로세스 모니터링 (스냅샷)
    - Link:
      - Hard Link: inode로 메타데이터까지
      - Symbolic Link: 원본 파일로 경로를 접근하는 방식
    - Disk 관리:
      - DU: Disk Usage, 사용 중인 디스크 확인
      - DF: Disk Free, 사용 가능한 디스크 확인
- (Entity 기준) **네트워크 및 패키지 처리**
  - 개념
    - SSH: 원격 컴퓨터에 접속하여 작업할 때 안전하게 사용할 수 있는 네트워크 프로토콜
    - apt: 검색, 설치, 업데이트, 삭제를 돕는 패키지 관리 도구
  - 명령어
    - Curl: 서버 통신
    - Wget: 웹 파일 다운로드
    - Nslookup: DNS 내 도메인 이름, IP 주소
    - Dig: 도메인 내 DNS 정보
    - NTP: 시간 정합성 관련 정보
    - Ping: 네트워크 대상/응답 속도/연결 여부 확인 용 ICMP 패킷
    - SS (Socket Statistics): 현재 시스템의 네트워크 연결 정보를 빠르고 상세하게 조회하는 명령어
- (Entity 기준) **Automation 처리**
  - Crontab: 특정 명령어 또는 스크립트를 정해진 일정에 자동으로 실행하도록 예약하는 명령어
  - Shell Script: 리눅스 셸 내 명령어 자동 실행 스크립트

### 기타

- 터미널, 쉘, 콘솔의 차이
  - 터미널: 시초가 하드웨어 용어
  - 쉘: 소프트웨어
  - 콘솔: 제어하는 곳을 의미
