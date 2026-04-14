# 🚀 Git Flow Workflow (Team Collaboration Guide)

## 📌 브랜치 네이밍 컨벤션

- `feat/` : 기능 추가
- `fix/` : 버그 수정
- `style/` : CSS 수정
- `refactor/` : 코드 리팩토링

---

# 🧑‍💻 개발 프로세스

## 1️⃣ 반드시 develop 브랜치로 이동 (선행)

`git checkout develop`

## 2️⃣ 최신 코드 동기화

`git pull origin develop`

## 3️⃣ 새로운 feature 브랜치 생성

`git checkout -b feature/기능명`

---

# ✍️ 작업 단계

## 4️⃣ 현재 브랜치 확인 (필수)

`git branch`

👉 \* feature/기능명 인지 반드시 확인

---

## 5️⃣ 작업 후 커밋 & 푸시

`git add .`<br><br>
`git commit -m "feat: 기능 구현 설명"`<br><br>
`git push origin feature/기능명`

---

# 🌐 Pull Request (PR)

👉 GitHub 페이지에서 진행

- feature/기능명 → develop Pull Request 생성
- 코드 리뷰 진행
- 승인 후 merge

---

# 🧹 브랜치 삭제 (merge 후)

## ✔ 로컬 브랜치 삭제

`git branch -D feature/기능명`

## ✔ 원격 브랜치 삭제

`git push origin --delete feature/기능명`

---

# 🚀 최종 배포 프로세스

## 1️⃣ develop 최신화

`git checkout develop`
`git pull origin develop`

## 2️⃣ main 브랜치 이동

`git checkout main`
`git pull origin main`

## 3️⃣ develop → main 머지

`git merge develop`

## 4️⃣ 원격 배포

`git push origin main`

---

# 🎯 전체 흐름 요약

develop → feature → develop → main

---

# 💡 핵심 규칙

- 항상 develop에서 시작한다
- feature/\*는 기능 단위 작업 브랜치다
- 작업 후 반드시 PR로 develop에 반영한다
- main은 배포 전용 브랜치다
- merge된 feature 브랜치는 반드시 삭제한다
