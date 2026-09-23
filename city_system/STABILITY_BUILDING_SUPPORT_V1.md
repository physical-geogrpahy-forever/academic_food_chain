# Building Stability Support V1

기준일: 2026-09-23
상태: BUILDING SUPPORT VALUES LOCKED / STATE STABILITY AGGREGATION FORMULA NOT YET LOCKED

상위 문서:

- `city_system/VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`
- `city_system/GOVERNMENT_POLICY_SWITCHING_COST_V1.md`
- `city_system/GREAT_REVOLUTIONARY_SYSTEM_V1.md`
- `city_system/VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`

## 1. 목적

기존 Building V2에서 `STABILITY_POINTS_PROVISIONAL`로 기록된 행정 및 정부 건물의 안정성 기여를 최종 건물 수치층으로 승격한다.

다만 이 점수는 국가 단위 `State Stability`에 그대로 더하는 직접 보너스가 아니다.

`STABILITY_POINTS_FINAL`의 의미는 다음과 같다.

```text
행정 및 정치 제도가 국가질서를 유지하는 데 제공하는 건물 기반 지원점수
```

따라서 향후 State Stability 계산은 도시 수, 인구, 점령지, 식민정부, 정부교체, Happiness, War Weariness 등과 함께 이 지원점수를 정규화해서 사용한다.

## 2. 국가 Stability와의 구분

기존 확정 원칙은 다음과 같다.

- City Happiness: 도시 주민의 만족도
- State Stability: 국가 및 정권의 정치질서 안정도

건물의 `STABILITY_POINTS_FINAL`은 세 번째 게이지가 아니다.

플레이어에게 별도 수치로 상시 노출할 필요도 없다. 국가 Stability의 원인 툴팁에서 `행정 및 치안 기반` 같은 항목으로 합산해 보여줄 수 있다.

## 3. 확정 건물값

기존 provisional 값은 수치 자체를 변경하지 않고 final로 승격한다.

| 건물 | Stability support |
|---|---:|
| Palace | 2 |
| Courthouse | 2 |
| Government Plaza | 2 |
| Ancestral Hall | 1 |
| Audience Chamber | 1 |
| Consulate | 1 |
| Warlord's Throne | 1 |
| Court | 1 |
| Foreign Ministry | 1 |
| Grand Master's Chapel | 1 |
| Intelligence Agency | 1 |
| Telegraph Office | 1 |
| National History Museum | 2 |
| Royal Society | 1 |
| War Department | 1 |
| Chancery | 1 |
| Constabulary | 1 |

그 외 일반 건물은 V1에서 `STABILITY_POINTS_FINAL=0`이다.

## 4. 직접 합산 금지

다음 식은 사용하지 않는다.

```text
State Stability = 기본값 + 모든 도시의 STABILITY_POINTS_FINAL 단순합
```

이렇게 하면 도시를 많이 가진 대형 제국이 Courthouse와 행정건물을 반복 건설하는 것만으로 Stability가 무한히 증가하는 문제가 생긴다.

향후 정량식은 최소한 다음을 고려해야 한다.

- 도시 또는 인구 규모에 따른 행정 수요
- 점령지와 식민정부의 추가 행정 부담
- 수도와 중앙정부 기관의 국가 단위 역할
- 일반 도시 행정건물의 지역 커버리지
- Happiness
- War Weariness
- 정부교체 충격
- 수도 상실과 경제위기 같은 국가 사건

## 5. 수치 권위

Building master에서는:

- `STABILITY_POINTS_FINAL`: gameplay 권위
- `STABILITY_POINTS_PROVISIONAL`: 과거 Building V2 결정의 provenance

으로 사용한다.

두 값이 비어 있지 않은 경우 서로 다르면 validator 실패로 처리한다.

## 6. 범위 밖

이번 V1에서 확정하지 않는 항목:

- State Stability의 0-100 최종 범위
- 행정 지원점수의 국가 Stability 변환식
- Happiness에서 Stability로 넘어가는 배율
- War Weariness에서 Stability로 넘어가는 배율
- 정부교체 단계별 Stability 손실값
- 점령지 및 식민정부 Stability 부담값
- Great Revolutionary의 Stability 완화 수치

이 값들은 각각의 입력 시스템이 정량화된 뒤 국가 Stability 통합 패스에서 확정한다.

## 7. 다음 정량화 순서

1. Happiness 정량식
2. War Weariness 정량식
3. 정부교체 비용과 Stability 충격
4. 점령 및 식민정부 Stability 부담
5. 위 입력과 `STABILITY_POINTS_FINAL`을 결합한 State Stability 전체식

상태: **17개 Building Stability support 값 확정. 국가 Stability 전체식은 미확정.**
