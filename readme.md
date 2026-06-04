# 검진모아 🏥
> 건강검진 데이터 통합 관리 플랫폼

[![Live](https://img.shields.io/badge/Live-gumjinmoa.kro.kr-teal)](http://gumjinmoa.kro.kr/)

## 프로젝트 소개

건강검진 결과를 한 곳에서 통합 관리하고, 직관적인 시각화로 건강 추이를 파악할 수 있는 웹 플랫폼입니다.

| 문제 | 해결 방법 |
|------|-----------|
| 일회성으로 끝나는 검진 결과 | OCR 인식 및 PDF 저장 |
| 건강 추이 파악의 어려움 | 그래프를 통한 시계열 추이 시각화 |
| 이해하기 어려운 수치 지표 | 직관적인 색상 및 점수 피드백 |

## 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap |
| Backend | Python, Flask, Gunicorn |
| Database | MySQL |
| OCR | Google Vision API (Node.js 서버) |
| Infra | GCP (VM 인스턴스), Nginx, HTTPS |

## 시스템 아키텍처

```
사용자 (HTTPS)
    ↕
gumjinmoa.kro.kr (임시 도메인)
    ↕
GCP VM 인스턴스
    ├── Nginx (리버스 프록시)
    ├── Gunicorn (WSGI 서버)
    ├── Flask / Python (백엔드)
    ├── MySQL (데이터베이스)
    └── Node.js OCR 서버 (port 4000)
            ↕
        Google Vision API
```

## 주요 기능

### 🔐 로그인 / 회원가입
- Parsley.js + 정규식 기반 입력값 검증
- argon2 라이브러리를 활용한 비밀번호 해싱
- 데코레이터를 통한 페이지 접근 제어

### 📷 OCR 자동입력
- 검진 결과 이미지 업로드 → Google Vision API 텍스트 추출
- 키워드 기반 수치 파싱 후 입력 폼 자동 완성

### 📊 건강 점수 알고리즘
- 100점 만점 기준, 항목별 정상/비정상 구간 판별
- 카테고리별 리스크 그룹화 및 최대값 기준 감점
- 최종 점수 + 등급 + 항목별 색상 피드백 제공

### 📈 건강 추이 그래프
- 연도별 수치 변화 시각화
- 연령대 비교 그래프

### 💾 이미지 / PDF 저장
- Canvas 기반 결과 화면을 PNG 또는 PDF로 다운로드
- jsPDF를 활용한 A4 크기 다중 페이지 처리

### 📋 검진 목록 & 페이지네이션
- 연도 필터, 이름 검색, 날짜 정렬 지원
- LIMIT / OFFSET 기반 서버사이드 페이지네이션 (5건/페이지)

## 프로젝트 구조

```
health-check-app/
├── app.py              # 애플리케이션 진입점
├── constants/          # 공통 상수
├── dao/                # DB SQL 쿼리 및 로직
├── db/                 # MySQL 연결 처리
├── health-ocr/         # OCR Node.js 서버
├── routes/             # Flask 라우팅
├── static/             # CSS, JS, 이미지 등 정적 파일
├── templates/          # Jinja2 HTML 템플릿
│   ├── auth/
│   ├── components/     # header, sidebar, footer
│   └── health/
└── .env                # 환경변수
```

## 향후 개선 방향

- **JWT 토큰** 기반 인증 시스템으로 전환
- **CI/CD 파이프라인** 구축으로 자동 배포
- 검진 항목별 **더 세분화된 기준 구간** 적용
- **건강검진 일정 관리** 및 주변 병원 정보 제공