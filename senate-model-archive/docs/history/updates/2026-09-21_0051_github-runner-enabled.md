# GitHub runner enabled

## 날짜
2026-09-21

## 변경

- 계산을 로컬/채팅이 아니라 GitHub Actions에서 수행하도록 전환했다.
- draft PR #2를 실행 트리거로 사용한다.
- main에는 실행용 workflow만 두고, 모델 데이터와 산출물은 archive-2026-us-senate-model 브랜치에 유지한다.
- workflow가 historical Senate audit와 OOS exception-race audit를 연속 실행하도록 갱신했다.
- 각 실행 결과 CSV와 MD는 github-actions bot이 archive branch에 다시 커밋한다.

## 다음

OOS exception-race audit 결과를 확인하고 2014/2018/2022 headline 예외 처리 규칙을 고정한다.
