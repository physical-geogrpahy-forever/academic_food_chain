# RelativeEconomicGrowth run 1 failure

## 날짜
2026-09-21

## 결과

첫 경제항 성능 run은 모델 적합 전에 `BadZipFile`로 중단됐다.

## 원인

BEA regional download는 개별 표 `SQINC1.zip`이 아니라 계정 묶음 `SQINC.zip`을 제공하고, 그 ZIP 내부에 `SQINC1__ALL_AREAS_*.csv`가 포함된다.

## 수정

다운로드 endpoint를 `https://apps.bea.gov/regional/zip/SQINC.zip`으로 수정했다. 내부에서는 `SQINC1`이 포함된 가장 큰 CSV를 선택하는 기존 로직을 그대로 사용한다.

## 성능 판정

이번 run은 예측값을 생성하지 않았으므로 성능 결과가 아니다. 동일 99-row OOS를 수정본으로 재실행한다.
