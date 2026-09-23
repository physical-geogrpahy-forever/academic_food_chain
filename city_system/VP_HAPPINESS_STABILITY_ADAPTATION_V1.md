# VP Happiness와 Stability 적용안 V1

기준일: 2026-09-23

상위 문서: `city_system/VOX_POPULI_SYSTEM_ADOPTION_MASTER_V1.md`

## 1. 목적

Vox Populi의 도시 Happiness/Needs 구조를 기본으로 가져오되, 우리 게임에는 별도의 국가 단위 `Stability`를 추가한다. 플레이어가 관리해야 하는 핵심 숫자를 지나치게 늘리지 않는 것이 원칙이다.

## 2. VP에서 확인된 핵심

VP는 도시의 산출량을 인구당 기준값과 비교해 Needs를 계산하며, 대표적인 불행 원인은 Distress, Poverty, Illiteracy, Boredom, Religious Unrest로 분리된다. Local Happiness도 도시별로 존재하며, 점령 또는 저항 중인 도시는 강한 불행을 만든다.

VP의 공식 개념 설명에서는 Needs Threshold를 전세계 도시의 인구당 산출량 중앙값에 기초해 계산하고, 제국 규모와 기술 진척도 등의 보정을 적용한다. 이 구조의 핵심 장점은 `왜 도시가 불행한지`가 산출량과 건물 역할에 연결된다는 점이다.

## 3. 우리 게임의 기본 원칙

우리 게임에서는 VP의 다섯 Needs를 모두 별도 게이지로 노출하지 않는다.

플레이어가 직접 보는 핵심 정치 수치는 다음 둘이다.

- `City Happiness`: 도시 주민의 만족도
- `State Stability`: 국가 정치질서의 안정도

Happiness 감소 원인은 내부적으로 세분화해 툴팁에 표시한다.

## 4. Happiness 원인

초기 분류는 다음과 같이 둔다.

| 원인 | VP 대응 | 우리 게임 해석 |
|---|---|---|
| 생활 부족 | Distress | Food, 주거, 기초 생활조건 |
| 경제적 빈곤 | Poverty | Gold, 고용, 경제상태 |
| 교육 부족 | Illiteracy | Science, 학교, 교육기관 |
| 문화적 불만 | Boredom | Culture, 오락, 문화기관 |
| 종교 갈등 | Religious Unrest | 종교 불일치와 갈등 |
| Health 문제 | 우리 확장 | 질병, 위생, 의료 부족 |
| 전쟁피로 | VP War Weariness 연결 | 장기전의 국내 불만 |
| 점령 | VP Occupied/Resistance 연결 | 외국 점령과 저항 |
| 식민통치 | 우리 확장 | 식민정부의 본국 관계 |
| 정책 부담 | 우리 확장 | 세금, 징병, 강압 정책 |

최종 Happiness는 각 원인의 합으로 계산하되, 정확한 수치식은 건물과 산출량 밸런스가 확정된 뒤 조정한다.

## 5. VP 중앙값 비교 구조의 처리

VP처럼 모든 도시를 세계 중앙값과 계속 비교하는 것은 깊이는 있지만 계산과 설명이 복잡하다.

V1에서는 다음 원칙을 채택한다.

1. 각 시대마다 기본 Needs 기대치를 둔다.
2. 세계 또는 지역 중앙값은 보조 보정값으로 사용할 수 있다.
3. 건물과 정책은 특정 원인의 필요치를 낮춘다.
4. 도시 규모가 커질수록 Needs 요구량이 증가한다.
5. 기술 발전만 빠르고 생활 인프라가 부족하면 불행이 생길 수 있다.

즉 VP의 `상대적 기대 수준` 개념은 유지하되 수식을 단순화한다.

## 6. 건물과 Happiness

건물은 단순 `Happiness +1`보다 문제 원인을 해결하는 방식이 우선이다.

예:

- Market, Bank: 경제적 빈곤 완화
- School, University: 교육 부족 완화
- Theater, Opera House, Cinema: 문화적 불만 완화
- Temple 계열: 종교 갈등 완화 또는 종교 만족 증가
- Hospital, Medical Lab: Health 문제 완화
- Sewer: Health와 생활환경 개선
- Police Station: 치안과 Stability 보조

건물 효과를 재감사할 때 이 원칙을 사용한다.

## 7. Stability 정의

Stability는 Happiness와 다른 국가 단위 값이다.

Happiness가 `사람들이 얼마나 만족하는가`라면 Stability는 `현재 국가와 정권이 얼마나 안정적으로 유지되는가`를 나타낸다.

### Stability 하락 요인

- 대규모 도시 불행
- 장기전과 패전
- 높은 War Weariness
- 급진적 정부교체
- 경제위기
- 수도 상실
- 대규모 점령지
- 반란과 내전
- 식민정부의 이탈
- 강압적 정책의 누적

### Stability 상승 요인

- 장기간 유지된 정부
- 높은 평균 Happiness
- 평화
- 성공적인 전쟁 종결
- 안정적 재정
- 행정 및 치안 건물
- 정통성 관련 정책
- 일부 위인 능력

## 8. Happiness와 Stability의 관계

둘을 동일시하지 않는다.

예:

```text
Happiness 낮음 + Stability 높음
→ 시위와 불만은 있으나 국가질서는 유지

Happiness 낮음 + Stability 낮음
→ 반란, 정부위기, 독립, 내전 가능

Happiness 높음 + Stability 낮음
→ 생활조건은 좋지만 권력투쟁, 국가분열, 정통성 위기 가능
```

Happiness는 Stability의 입력 중 하나일 뿐이다.

## 9. 점령지와 식민정부

점령지는 일반 도시보다 Happiness가 낮고 Stability에 부담을 준다.

식민정부는 별도 정치단위로 처리하므로 본국 Stability와 식민정부의 Happiness를 함께 본다.

별도의 `Independence Pressure` 게이지는 만들지 않는다.

독립 여부는 다음 조건을 이용한 사건 판정으로 처리한다.

- 식민정부 Happiness
- 본국 Stability
- 식민정부의 정치적 발전
- Great Revolutionary 보유 여부
- 역사적 문명 등장 가능 시대
- 종주국과 식민정부의 관계

## 10. UI 원칙

도시 화면에는 최종 Happiness만 크게 표시하고, 툴팁에서 원인을 분해한다.

예:

```text
Boston Happiness -4
경제적 빈곤 -1
전쟁피로 -2
식민통치 -1
```

국가 화면에는 Stability와 주요 원인만 표시한다.

```text
United Kingdom Stability 42
전쟁피로 -8
불행한 도시 -5
정부 정통성 +7
```

## 11. AI 원칙

AI는 단순히 Happiness 숫자를 올리는 것이 아니라 가장 큰 불행 원인을 먼저 해결한다.

- Poverty가 크면 경제 건물
- Illiteracy가 크면 교육 건물
- Health가 크면 의료/위생 건물
- War Weariness가 크면 평화협상 가능성 증가
- 낮은 Stability에서는 급진적 정부교체를 피하거나 혁명가를 활용

## 12. VP에서 그대로 복사하지 않는 것

- VP의 정확한 Needs Threshold 수치
- 전세계 중앙값 계산식의 모든 보정
- VP의 도시별 Happiness 분배식을 그대로 복사
- 우리 Health 시스템과 중복되는 항목

## 13. 확정 상태

- VP식 원인별 Happiness: 채택
- 도시 Local Happiness 개념: 채택
- 국가 Stability: 우리 게임 고유 추가
- Independence Pressure 별도 게이지: 사용하지 않음
- 건물은 문제 해결형 효과 우선: 확정

## 14. VP 확인 자료

- `(2) Vox Populi/Database Changes/Text/en_US/Concepts/NewConceptText.xml`
- `(2) Vox Populi/LUA/HappinessInfo.xml`

상태: **V1 구조 확정, 수치 미확정**
