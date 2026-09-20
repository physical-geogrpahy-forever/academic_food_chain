# Candidate-block OOS run 1 failure

## 날짜
2026-09-21

## 결과

첫 성능 workflow는 모델 적합 단계에 도달하기 전에 중단됐다.

## 원인

독립 성능 workflow에서 `data/raw/congress-legislators/legislators-current.yaml`과 `legislators-historical.yaml`이 Git에 보존돼 있다고 가정했지만, 해당 파일은 기존 pipeline 실행 중 임시로 내려받기만 했고 archive branch에는 존재하지 않았다.

오류: `FileNotFoundError`.

## 수정

성능 스크립트가 `unitedstates/congress-legislators`의 commit `8a3c7e6987f890b32e56058f7ddbdf380860b4a3`에서 두 YAML을 직접 내려받도록 수정했다.

## 성능 판정

이번 run은 예측값을 생성하지 못했으므로 성능 결과로 간주하지 않는다. 같은 rolling OOS 실험을 수정본으로 재실행한다.
