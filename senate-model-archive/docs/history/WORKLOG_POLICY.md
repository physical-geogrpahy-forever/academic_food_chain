# Worklog Policy

## 적용 시작
2026-09-21

## 원칙
이 프로젝트에서는 앞으로 의미 있는 작업 단위가 끝날 때마다 반드시 GitHub에 Markdown 기록을 남긴다.

## 최소 기록 항목
각 업데이트 MD에는 다음을 포함한다.

1. 작업 시각 또는 날짜
2. 이번에 한 작업
3. 사용한 데이터/문헌/소스
4. 새로 확정된 사항
5. 변경된 사항
6. 실패하거나 보류한 사항
7. 생성/수정된 파일
8. 다음 작업

## 파일명 규칙

`docs/history/updates/YYYY-MM-DD_HHMM_<short-title>.md`

예:
`docs/history/updates/2026-09-21_0051_core-v2r-reconstruction-start.md`

## 중요 규칙

- 채팅에만 남기지 않는다.
- 모델 구조가 바뀌면 반드시 `CHANGELOG.md`도 갱신한다.
- 데이터 snapshot이 바뀌면 `data/snapshots/`에도 별도 파일을 남긴다.
- 성능 수치가 바뀌면 `data/benchmarks/`에 CSV를 남긴다.
- 원본 Core V2와 재구축본 Core V2-R을 혼동하지 않는다.
- exact 원본 산출물이 없는 항목은 재구축했다고 표시하고, 원본이라고 쓰지 않는다.
