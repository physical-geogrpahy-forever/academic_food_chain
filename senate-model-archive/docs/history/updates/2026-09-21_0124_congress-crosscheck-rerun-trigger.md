# Congress service cross-check rerun trigger

## 날짜
2026-09-21

## 원인

- 직전 GitHub Actions run #23, #24는 모두 main workflow의 PyYAML 설치 단계가 반영되기 전 버전으로 실행되어 `ModuleNotFoundError: No module named 'yaml'`에서 중단됐다.
- `fetch_congress_legislators.py` 단계까지는 정상 동작했으며 current/historical YAML 다운로드 자체는 성공했다.

## 수정

- main branch runner에 `python -m pip install pyyaml` 단계를 추가했다.
- `crosscheck_congress_service.py`는 실제 headline target 열인 `d_side_candidate`, `r_side_candidate`를 우선 사용하도록 수정했다.
- 이 커밋은 PR #5에 `synchronize` 이벤트를 발생시켜 최신 main workflow로 다시 실행하기 위한 명시적 재실행 지점이다.

## 다음

- 새 Actions run에서 PyYAML 설치 성공 여부 확인
- 198 candidate-side rows의 Congress term-date match 결과 저장
- 자동 선거이력 기반 Senate/House/현직 proxy와 term-date 결과 차이 목록화
