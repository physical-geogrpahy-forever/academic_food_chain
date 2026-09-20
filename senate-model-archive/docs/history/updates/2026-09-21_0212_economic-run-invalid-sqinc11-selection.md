# Economic OOS result invalidated: SQINC11 selected instead of SQINC1

## 날짜
2026-09-21

## 발견

첫 성공 run의 로그와 MD를 검토한 결과 ZIP member가 `SQINC1__ALL_AREAS...csv`가 아니라 `SQINC11__ALL_AREAS_1998_2026.csv`였다.

원인은 파일 선택 조건이 단순 substring `SQINC1`을 사용한 뒤 가장 큰 CSV를 선택했기 때문이다. `SQINC11`도 이 조건에 걸렸다.

## 따라서 폐기하는 수치

- structural 10.6055
- 잘못 선택된 경제표를 사용한 nested 10.5828
- 명목 개선 0.0227%p

위 경제 개선 수치는 **INVALID**이며 모델 성능 향상으로 인정하지 않는다.

## 수정

ZIP member는 basename이 정확히 `SQINC1__ALL_AREAS_`로 시작하는 CSV만 허용한다.

## 다음

동일 99-row rolling OOS를 정확한 SQINC1 개인소득 표로 재실행한다.
