# feat: 기능 추가
# fix: 버그 수정
# style: CSS 수정
# refactor: 코드 리팩토링

# 반드시 선행
# develop branch로 변경
git checkout develop
# 코드 가져오기 (최신 코드 동기화)
git pull origin develop

# 새로운 branch 생성
git checkout -b feature/기능명

### 작업 후
# branch가 새로 생성한 branch가 맞는지 반드시 확인
git branch
git add .
git commit -m "feat: -- 기능 구현"
git push origin feature/기능명


### push 후에 github 웹에서 진행
feature/기능명 -> develop으로 Pull Request 생성
코드 리뷰 후 merge

# 로컬 삭제
git branch -d feature/기능명
# 원격 삭제
git push origin --delete feature/기능명


### 최종 배포
# develop 최신화
git checkout develop
git pull origin develop

# main으로 이동
git checkout main
git pull origin main

# develop → main 머지
git merge develop

# 푸시
git push origin main