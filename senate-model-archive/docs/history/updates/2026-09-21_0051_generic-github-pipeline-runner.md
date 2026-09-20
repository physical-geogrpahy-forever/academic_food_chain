# Generic GitHub pipeline runner enabled

## 날짜
2026-09-21

## 변경

- main branch의 GitHub Actions workflow를 더 이상 단계별로 수정하지 않도록 generic runner로 고정했다.
- archive branch의 scripts/run_pipeline.py가 실행할 단계 목록을 관리한다.
- 새 단계 추가 시 archive branch의 script와 run_pipeline.py만 수정하면 draft PR이 synchronize되고 GitHub Actions가 자동 실행된다.
- generated CSV와 update MD는 github-actions bot이 archive branch에 다시 커밋한다.

## 현재 pipeline

1. historical Senate race audit
2. 2006-2022 OOS exception-race audit
3. headline validation sample-size inference

## 다음

현재 main runner를 기준으로 draft PR을 다시 열고 세 단계를 일괄 실행한다.