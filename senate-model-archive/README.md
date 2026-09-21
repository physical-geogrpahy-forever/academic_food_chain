# 2026 U.S. Senate Forecast Model Archive

이 디렉터리는 2026 미국 상원 예측모형 프로젝트의 **복구 가능한 기준선, 발전 내역, 데이터 스냅샷, 재현 규칙**을 Git으로 보존하기 위한 아카이브다.

## 현재 상태

- 확정 production 기준선: **Core V2-R Direction Production 2026**
- 현재 방향성 기준 clean nested OOS headline: **96/99 = 97.0%**
- 기존 Core V2의 RMSE/MAE 수치는 역사 보존값으로 유지하되, 현재 primary objective는 winner-direction accuracy
- 채팅 길이 제한으로 Core V2 문서 작성 이후의 일부 진전이 유실되었을 가능성이 있다.
- 따라서 handoff의 `authoritative/latest` 표기는 작성 당시 기준이며, 더 뒤의 보존 자료가 발견되면 그 자료가 우선한다.
- 원본 historical Core V2의 exact 산출 CSV와 original config는 여전히 미복구다. 다만 현재 확정된 Core V2-R의 96/99 clean nested와 98/99 retrospective 산출물은 `final/validation/`에 canonical bundle로 고정되어 있다.

## Core V2 고정 원칙

`PVI + National + SameSeat prior margin + SameSeat gap + IncumbencyDiff + OutPartyIncumbent + RelativeEconomicGrowth + incumbency/out-party Era interactions`

Candidate experience, PersonalVote, FEC finance are retained as auxiliary diagnostics and are not terms in the canonical 98/99 production calculation.\n\nPoll은 fundamentals prior를 대체하지 않고 observation layer로 업데이트한다.

```text
w_max = 0.75
k = 0.5
```

지역 평균 residual은 margin에 직접 더하지 않고 national/regional/state 공분산과 uncertainty에만 사용한다.

## 45일 스냅샷

- 2026 general election: 2026-11-03
- 정확한 45-day snapshot: **2026-09-19**
- 45-day 경제항: **BEA 2026 Q1**
- 2026-09-30 공개 예정 Q2는 45-day benchmark에 소급 투입 금지

## 폴더

- `docs/handoffs/`: 살아남은 master handoff
- `docs/audits/`: 최신성, 누출, production input 감사
- `docs/history/`: 복구 및 발전 로그
- `data/benchmarks/`: 보존된 성능 및 지역잔차
- `data/snapshots/`: 2026 정보시점 및 변수 상태
- `data/schema/`: 앞으로 생성해야 할 exact outputs의 schema
- `config/`: 보존된 Core V2 설정과 불확실 항목

## 현재 모델과 검증 기준

- 정식 잠금 모델: **Core V2-R Direction Production 2026**
- 정식 production rule의 retrospective 기록: **98/99 = 99.0%**
- clean nested OOS 검증치: **96/99 = 97.0%**
- 96/99는 별도 production 모델이 아니라 clean nested 검증 기준이다.
- 98/99는 OOS가 아니라 retrospective 기록이다.
- 98/99의 유일 오답: **2014 North Carolina**
- 94/99 대비 production selector가 교정한 경주: **2018 Nevada, Missouri, Florida, Indiana**

canonical bundle:
- `final/validation/README.md`
- `final/validation/manifest.json`
- `final/validation/verification_report.json`

다음 채팅이나 복구 작업에서는 실험 폴더보다 이 bundle을 먼저 읽는다.


## 2026 production lock

현재 production 설정은 다음 파일에 고정되어 있다.

- `docs/final/MODEL_FINAL_LOCK_2026-09-21.md`
- `config/core_v2r_direction_2026_production.json`

이후의 구조 변경은 실험판으로만 추가하며 이 설정을 덮어쓰지 않는다.

## 2026 analysis

첫 입력 진단:
- `docs/analysis/2026_SENATE_INPUT_DIAGNOSTIC_2026-09-21.md`
- `data/snapshots/2026_competitive_race_input_diagnostic_2026-09-21.csv`

