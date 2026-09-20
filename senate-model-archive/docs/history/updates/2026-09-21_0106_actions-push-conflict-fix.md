# GitHub Actions push conflict fix

## 날짜
2026-09-21

## 문제

GitHub Actions run `35521537322`에서 계산 단계는 모두 성공했지만 마지막 결과 커밋의 push가 실패했다.

실패한 단계:
- job: `run-senate-archive`
- pipeline execution: success
- generated-output commit: local success
- push: failure

Git 로그:

```text
! [rejected] HEAD -> archive-2026-us-senate-model (fetch first)
Updates were rejected because the remote contains work that you do not have locally.
```

## 원인

이전에 만들었던 브랜치 전용 workflow `.github/workflows/senate-model-historical-audit.yml`와 새 generic PR runner가 동시에 같은 archive branch를 갱신했다.

그 결과 generic runner가 checkout한 뒤 다른 workflow가 먼저 remote branch를 전진시켜 non-fast-forward가 발생했다.

## 수정

1. archive branch의 구형 중복 workflow를 삭제했다.
2. main의 generic runner에 `concurrency`를 추가했다.
3. 결과 push 전에 다음을 실행하도록 수정했다.

```bash
git fetch origin archive-2026-us-senate-model
git rebase origin/archive-2026-us-senate-model
git push origin HEAD:archive-2026-us-senate-model
```

4. 앞으로 실행 workflow는 main의 generic runner 하나만 유지한다.
5. 실제 계산 단계 목록은 archive branch의 `scripts/run_pipeline.py`에서 관리한다.

## 결과

실패 run에서도 PVI 계산 자체는 성공했음이 로그로 확인됐다. 저장 충돌만 문제였다.

## 다음

현재 main runner를 기준으로 새 draft execution PR을 열고 수정된 PVI 파이프라인을 재실행한다.
