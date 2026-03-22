# 📧 HR 채용 결과 안내 자동화 시스템 (HR Email Automation)

> **"반복되는 단순 업무를 줄이고, 인사 담당자(HR)가 더 중요한 업무에 집중할 수 있도록 돕는 이메일 자동 발송 스크립트"**

## 🚀 1. 프로젝트 개요 (Overview)
- **개발 기간:** 2024년 (개인 포트폴리오 기획)
- **개발 목표:** 서류 전형 또는 면접 전형 이후 다수의 지원자에게 합격/불합격 여부를 개인화하여 자동 발송하는 파이썬 시스템 구축
- **핵심 키워드:** `#업무자동화(RPA)`, `#Python`, `#SMTP`, `#보안강화`

---

## 💡 2. 기획 배경 (Background & Motivation)
기업의 채용 과정에서는 **지원자 수십~수백 명에게 결과를 개별적으로 통보해야 하는 단순 반복적인 업무**가 발생합니다.
자칫 수기(Manually)로 메일을 템플릿화하여 발송할 경우 다음과 같은 문제점이 생길 수 있습니다.
1. **Human Error (휴먼 에러):** 'A' 지원자의 메일에 'B' 지원자의 이름으로 발송하는 치명적 실수 발생 가능
2. **비효율성:** 수백 건의 메일을 일일이 복사+붙여넣기 하는 시간적 소모
3. **보안 이슈:** 이메일 주소 등이 Bcc(숨은참조) 누락으로 대량 유출될 위험성

이를 해결하기 위해, CSV로 정리된 결과 데이터를 읽어 **각 지원자의 이름과 결과에 맞는 내용으로 변환하여 안전하고 빠르게 자동 메일을 발송**하는 파이썬 자동화 스크립트를 기획하게 되었습니다.

---

## 🛠 3. 사용 기술 (Tech Stack)
- **Language:** Python
- **Libraries (Built-in):** `smtplib` (메일 서버 연결), `email.mime` (메일 객체 구성), `csv` (데이터 로드)
- **Libraries (External):** `python-dotenv` (환경 변수 보안 관리)
- **Environment:** Windows / macOS 지원

---

## 🔑 4. 핵심 기능 (Key Features)

### ① 동적 콘텐츠 생성 (Personalization)
CSV 파일(데이터베이스 대체)에 기록된 지원자 정보를 `csv.DictReader`로 순회하며, 각 지원자의 `이름(name)`, `이메일(email)`, `결과(result)`를 추출 후 **f-string 방식**을 통해 다이내믹 텍스트 생성을 수행합니다.

### ② 조건부 템플릿 로직 (Condition-based Routing)
결과 데이터(`합격` / `불합격`)에 따라 **if/else 로직**으로 분기하여 메일 제목(Subject)과 본문(Body) 내용을 완전히 다르게 구성합니다. 합격자에게는 다음 전형의 기대감을, 불합격자에게는 정중하고 배려 깊은 메시지를 보낼 수 있도록 구성했습니다.

### ③ 환경 변수를 이용한 보안 강화 (Security - `.env`)
발송용 이메일 계정 및 비밀번호와 같은 **민감 정보(Credentials)**가 소스 코드(GitHub 등)에 하드코딩 되어 노출되는 것을 방지하기 위해 `python-dotenv` 패키지를 도입했습니다.
또한 계정 해킹 방지를 위해 일반 비밀번호가 아닌 이메일 플랫폼의 **'2단계 인증 앱 비밀번호(App Password)'**만을 사용하도록 보안 기준을 적용했습니다.

### ④ 예외 처리 및 로깅 (Error Handling)
운영 과정에서 발생할 수 있는 주요 에러들을 `try-except` 블록으로 핸들링하여 중간에 프로그램이 뻗지 않고 유연하게 대응하도록 설계하였습니다.
- `FileNotFoundError`: 대상 CSV 파일 누락 시 알림
- `SMTPAuthenticationError`: 앱 비밀번호 오기입/세팅 오류 등 권한 문제 방어
- `Exception`: 기타 런타임 에러 출력

---

## 📁 5. 프로젝트 구조 (Project Structure)

```text
📂 hr-send-result/
├── email_automation.py   # 메인 이메일 자동 발송 스크립트 
├── applicants.csv        # 발송 대상자 데이터베이스 리스트 (이름, 이메일, 결과)
├── .env                  # 환경 변수 (이메일 및 앱 비밀번호 저장 / Git 제외)
├── .gitignore            # Git 관리에 제외할 파일 명시 (.env, 가상환경 등)
└── README.md             # 프로젝트 소개 문서
```

---

## ⚙️ 6. 실행 방법 (Getting Started)

1. **저장소 클론 및 패키지 설치**
   ```bash
   git clone [레포지토리 주소]
   cd hr-send-result
   pip install -r requirements.txt  # (또는 pip install python-dotenv)
   ```

2. **환경변수(.env) 설정**
   루트 경로에 `.env` 파일을 생성하고 발신자 정보를 기입합니다.
   ```text
   # .env
   SENDER_EMAIL=본인의_이메일_주소@naver.com (또는 gmail.com)
   SENDER_PASSWORD=발급받은_16자리_앱비밀번호
   ```

3. **CSV 데이터 업데이트**
   `applicants.csv` 내에 발송할 지원자의 이름, 이메일, 결과(합격/불합격) 리스트를 작성합니다.

4. **스크립트 실행**
   ```bash
   python email_automation.py
   ```
   *실행 후 콘솔 성공 출력 예시:*
   `✅ [합격] 홍길동 (test@example.com) 님께 실제 메일 발송 완료!`

---

## ❗ 7. 트러블슈팅 (Troubleshooting & Learnings)

- **Issue 1:** `ModuleNotFoundError: No module named 'dotenv'`
  - **원인/해결:** 가상환경(`.venv`)과 글로벌 파이썬 인터프리터 설정이 분리되어 일어난 문제로, 현재 IDE가 바라보는 인터프리터 경로를 정확히 파악하여 해당 환경에 `python -m pip install python-dotenv` 명령어를 통해 명확하게 의존성을 해결함.
- **Issue 2:** `SMTPAuthenticationError` 발생
  - **원인/해결:** 단순 로그인 비밀번호를 입력 시 네이버/구글 등에서 보안상 API 접근을 거부하는 현상 발생. 2단계 보안 인증 활성화 및 '애플리케이션 전용 비밀번호(16자리)'를 별도 발급받아 환경변수에 맵핑시킨 뒤 성공적으로 SMTP 통신 문제 해결.

---

## 🎯 8. 기대 효과 및 향후 발전 방향 (Impacts & Next Steps)
- 통상 100건 발송 시 수작업으로 소요되는 시간(~2시간)을 **약 1분 이내로 단축**시켜 HR 팀의 주요 업무 리소스를 대폭 확보하게 됩니다.
- 추후 `applicants.csv` 대신 데이터베이스(MySQL, PostgreSQL 등)를 연동하거나 Google Sheets API를 통해 인사 담당자가 클라우드에서 편하게 조작하는 대로 발송되도록 파이프라인 확장을 고려해볼 수 있습니다. 
- 메일 본문을 Plain Text가 아닌 HTML 템플릿(MIMEText의 `html` 방식)으로 변경하여 이미지가 포함된 더 미려하고 기업 브랜딩이 담긴 웹 템플릿으로 고도화할 예정입니다.