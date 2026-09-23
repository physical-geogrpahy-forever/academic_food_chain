# Vox Populi 시스템 도입 마스터 정리 V1

기준일: 2026-09-23

대상 프로젝트: `physical-geogrpahy-forever/academic_food_chain`  
기준 브랜치: `civ-game-map-stage1b-etopo2022`

## 0. 목적

본 문서는 Civilization V: Brave New World의 대형 오버홀인 **Vox Populi(VP)**의 주요 시스템을 현재 제작 중인 문명형 세계전략게임에 거의 전부 도입하기 위한 기준 문서다.

원칙은 다음과 같다.

1. VP의 핵심 게임플레이 시스템은 원칙적으로 채택한다.
2. 단순히 VP 수치를 복사하지 않고, 우리 게임의 시대 구분, 세계지도, Health, Power, 동적 자원, 기업, 역사적 문명 등장 시스템에 맞게 재조정한다.
3. VP에 없는 우리 게임 고유 시스템은 VP 위에 추가한다.
4. VP의 지도 스크립트, UI 구현, 문명별 고유특성 수치까지 그대로 복사하는 것은 목표가 아니다.
5. 시스템 설계는 VP를 기본 골격으로 삼되, 세부 수치는 별도 밸런스 단계에서 확정한다.

## 1. Vox Populi란 무엇인가

Vox Populi는 Civilization V BNW용 Community Patch Project에서 발전한 대형 오버홀이다.

- **Community Patch**
  - DLL 기반 버그 수정
  - 성능 개선
  - AI 개선
  - 멀티플레이 관련 수정
  - 핵심 게임 로직 확장 기반
- **Vox Populi**
  - 기술
  - 정책
  - 정부/이념
  - 도시
  - Happiness
  - 외교
  - 도시국가
  - 종교
  - 전투
  - 유닛
  - 건물
  - 자원
  - 기업
  - 위인
  - 승리조건
  - 난이도
  - 기타 대부분의 게임플레이를 재설계
- **EUI**
  - 선택적 UI 개선층

공식 저장소는 VP가 City-State Diplomacy, Civ IV Diplomacy Features, More Luxuries 등을 통합한 Civilization V의 전면적 확장/재설계 프로젝트임을 명시한다.

## 2. 우리 프로젝트의 채택 원칙

### 2.1 채택 등급

- **직접 채택**: VP의 설계 방향을 거의 그대로 사용
- **확장 채택**: VP 구조를 기본으로 하되 우리 게임 시스템을 추가
- **참고만**: VP 구현은 확인하되 우리 프로젝트 구조와 맞지 않아 그대로 사용하지 않음

## 3. 전체 시스템 채택표

| 분야 | VP 요소 | 우리 프로젝트 방침 |
|---|---|---|
| AI | 전술, 전략, 외교, 경제 AI 대폭 개선 | 직접 채택 |
| 성능/버그 수정 | Community Patch 기반 개선 | 직접 채택 철학 |
| 도시 Happiness | 도시별 Needs와 불행 원인 | 확장 채택 |
| 전쟁피로 | 장기전의 국내 부담 | 직접 채택 |
| 군사 보급 | Unit Supply | 확장 채택 |
| 외교 | 확장된 협정과 외교 AI | 직접 채택 |
| 종속국 | Vassalage | 확장 채택 |
| 도시국가 | 외교유닛, 퀘스트, 영향력 경쟁 | 직접 채택 |
| 무역 | 국내/국제 교역로 확장 | 확장 채택 |
| 자원 독점 | Monopoly | 직접 채택 후 수치 재설계 |
| 기업 | Corporation/Franchise | 확장 채택 |
| 사치자원 | More Luxuries 계열 확장 | 직접 채택 철학 |
| 유닛 계보 | 전 시대 업그레이드 트리 | 직접 채택 |
| 후기 개척자 | Settler → Pioneer → Colonist | 직접 채택 + 식민정부 연결 |
| 승급 | 전투 역할별 승급 체계 | 직접 채택 |
| 전투 | 전투 밸런스 전면 개편 | 직접 채택 기반 |
| 도시전투 | 도시 방어, 공성 역할 재조정 | 직접 채택 기반 |
| 야만인 | 출현, 전투, 캠프 밸런스 | 직접 채택 기반 |
| 기술 | 기술트리 재배치와 시대 페이싱 | 참고 + 우리 기술트리에 통합 |
| 정책 | 정책트리 전면 재설계 | 확장 채택 |
| 이념 | 후기 정치체제/정책 | 확장 채택 |
| 종교 | Pantheon, Belief, 개혁, 종교경쟁 | 확장 채택 |
| 첩보 | 스파이 기능 확장 | 직접 채택 기반 |
| 위인 | 위인 역할/발생/소비 재설계 | 확장 채택 |
| 전문가 | Specialist 가치 강화 | 직접 채택 기반 |
| 건물 | 단순 산출보다 도시 문제 해결 | 직접 채택 |
| 불가사의 | 시대별 역할과 경쟁 재조정 | 직접 채택 기반 |
| 국가불가사의 | 국가 발전 단계 반영 | 직접 채택 기반 |
| 문화 | Great Work, 문화산출 재조정 | 직접 채택 기반 |
| 관광 | 외교/문화와 연동 | 직접 채택 기반 |
| 고고학 | Archaeology 역할 강화 | 직접 채택 기반 |
| 세계의회 | 국제결의와 외교 승리 | 확장 채택 |
| 승리조건 | 과학, 문화, 외교, 정복 재조정 | 참고 후 통합 |
| 난이도 | AI 보너스와 플레이어 난이도 재조정 | 직접 채택 철학 |
| 맵 생성 | Communitu 등 개선 맵 | 참고만 |
| UI | EUI | 참고만 |

## 4. AI와 Community Patch

VP에서 가장 먼저 가져와야 하는 것은 개별 콘텐츠보다 **AI 개선 철학**이다.

### 채택

- 전술 AI
- 전쟁 목표 선정
- 전선 형성
- 유닛 역할 이해
- 공성전 판단
- 해군 운용
- 도시 건설 위치
- 노동자 개선
- 자원 활용
- 외교 판단
- 정책 선택
- 종교 선택
- 기술 선택
- 도시 생산 선택
- 위인 사용 판단
- 교역로 선정

우리 게임의 AI는 단순한 보너스 지급으로 난이도를 만드는 것보다 **규칙을 실제로 이해하고 사용하는 AI**를 목표로 한다.

### 우리 게임 확장

- 역사적 문명 등장
- 식민정부
- 자치령
- 독립
- Great Revolutionary
- Health
- Power
- 동적 자원 발견/확산
- 기업
- 시대별 국가 형성

## 5. 도시 Happiness와 Needs

VP는 도시의 불행을 단일 원인으로 취급하지 않고 대표적으로 다음 Needs를 구분한다.

- Distress
- Poverty
- Illiteracy
- Boredom
- Religious Unrest

### 우리 게임 채택 방식

별도의 복잡한 5개 게이지는 만들지 않는다.

최종적으로 플레이어가 관리하는 핵심값은:

- 도시 Happiness
- 국가 Stability

다만 Happiness 감소 원인은 내부적으로 분해한다.

### 우리 게임 Happiness 원인

- 생활/식량 부족
- 경제적 빈곤
- 교육/지식 부족
- 문화적 불만
- 종교적 갈등
- Health 문제
- 전쟁피로
- 점령
- 식민통치
- 과도한 세금/부담
- 기타 정책 효과

예:

```text
서울 Happiness: -5

원인
전쟁피로      -2
Health        -1
경제적 빈곤   -1
문화 부족     -1
```

VP의 장점인 **문제의 원인이 보이는 도시 운영**은 유지하되 UI 복잡도는 낮춘다.

## 6. Stability

Stability는 VP의 Happiness를 그대로 복사하는 것이 아니라 우리 게임에서 새로 추가하는 국가 단위 정치 변수다.

**Happiness**
- 도시 주민의 만족도

**Stability**
- 국가 정권과 정치질서의 안정성

### Stability 하락 요인

- 장기전
- 패전
- 전쟁피로
- 급진적 정부교체
- 대규모 불행
- 경제위기
- 점령지 증가
- 식민정부 갈등
- 내전
- 반란
- 심각한 정책 실패

### 용도

- 정부교체 비용
- 반란
- 식민지 독립
- 내전
- 혁명
- 점령지 복귀
- 국가 분열

## 7. 전쟁피로

VP의 War Weariness 구조를 채택한다.

### 주요 입력

- 전쟁 기간
- 전사자
- 민간/도시 피해
- 영토 상실
- 패전
- 본토 침공
- 장거리 해외전쟁

### 결과

- Happiness 감소
- 생산효율 저하 가능
- Gold 부담
- Stability 감소 가능
- 식민정부 통제 약화
- 독립/혁명 조건 악화

## 8. 군사 보급

VP의 Unit Supply 개념을 채택한다.

보급한도는 다음 요소에 의해 결정된다.

- 인구
- 군사 건물
- 정부
- 정책
- 기술
- 도로/철도
- 항구
- 해상보급
- 식민정부
- 해외기지

특히 해외군은 본토군보다 유지와 보급 부담이 크도록 한다.

## 9. 개척자 계보

VP에는 후기 개척 유닛이 존재한다.

```text
Settler
↓
Pioneer
↓
Colonist
```

우리 게임에서도 시대별 개척자를 둔다.

잠정 구조:

```text
고대~중세
Settler / 개척자

탐험시대
Pioneer / 선구자

계몽시대~산업시대
Colonist / 식민개척자
```

정확한 해금 기술/사회제도는 이후 확정한다.

## 10. 식민정부

이것은 VP의 Pioneer/Colonist와 우리 게임의 역사적 문명 등장 시스템을 결합한 **우리 게임 고유 확장**이다.

후기 개척자가 본국과 다른 대륙 또는 지정된 해외 권역에 도시를 건설하면 조건에 따라 **식민정부**가 형성된다.

```text
본국
│
├─ 본토 도시
└─ 식민정부
   ├─ 식민도시 A
   ├─ 식민도시 B
   └─ 식민도시 C
```

### 식민정부 기능

- 도시 생산
- 지역 확장
- 방어
- 일부 경제
- 일부 건설
- 지역 군사
- 지역 정책

본국은 식민정부에서:

- 세금
- 무역수익 일부
- 자원 일부
- 전략적 권리
- 군사적 접근권

등을 얻는다.

## 11. Great Revolutionary Point와 식민지 독립

식민정부는 본국과 별도로 **Great Revolutionary Point(GReP)**를 축적할 수 있다.

### GReP 발생

- 식민정부의 문화/정치 발전
- 특정 사회제도
- 특정 철학가
- 낮은 Happiness
- 본국의 낮은 Stability
- 전쟁피로
- 과도한 식민부담
- 정치사건
- 독립운동

단, 단순히 Happiness를 의도적으로 낮추는 것이 최적화되지 않도록 **불만 + 정치조직/사상/제도 조건**을 요구한다.

### 독립

```text
식민정부
↓
GReP 축적
↓
Great Revolutionary 등장
↓
독립 가능
```

독립은 종주국 플레이어가 임의로 승인해야만 발생하는 구조로 만들지 않는다.

식민정부 AI 또는 정치사건이 자체적으로 독립을 결정할 수 있다.

### 역사적 등장 연동

```text
북아메리카 식민정부
+ 계몽시대
+ 미국 등장 조건 해금
+ Great Revolutionary
→ 미국 독립 가능
```

```text
남아메리카 식민정부
+ 산업시대
+ 해당 지역 신생 문명 후보
+ Great Revolutionary
→ 독립국 등장 가능
```

## 12. 정책과 정부

### 정책카드

- 사회제도 완료 직후: 무료 정책 재편
- 그 외 시점: Culture 비용
- 여러 장 교체: 비용 증가

### 정부교체

정부교체는 무료가 아니다.

정부 변경 시:

- Culture 비용
- Stability 감소
- 과도기

를 적용한다.

전환 규모:

- 개혁
- 체제전환
- 혁명적 전환

의 세 단계 정도로 단순화한다.

### Great Revolutionary

위대한 혁명가는 다음 기능 중 하나를 가질 수 있다.

- 정부교체 비용 감소/제거
- 과도기 단축
- 정책 전면 재편
- Stability 충격 완화
- 식민정부 독립
- 사회혁명
- 특정 경우 외국 혁명 지원

## 13. 외교와 종속국

VP의 Civ IV Diplomacy Features 계열을 적극 채택한다.

### 도입 대상

- 종속국
- 자치국
- 방위/보호 관계
- 외교적 요구
- 전쟁과 평화조건 세분화
- 해방
- 국제관계에 따른 외교평가
- 장기 동맹/적대 기억

### 우리 게임 확장

```text
직할영토
↓
식민정부
↓
자치령
↓
종속국 / 보호국
↓
완전독립국
```

## 14. 도시국가 외교

VP의 City-State Diplomacy를 거의 그대로 설계 참고 대상으로 삼는다.

- 외교유닛
- 임무
- 퀘스트
- 보호
- 교역
- 군사원조
- 영향력
- 외교 경쟁

우리 게임에서는 도시국가가 역사적 국가 등장 시스템과도 연결될 수 있다.

## 15. 자원 독점

VP의 Monopoly 시스템을 채택한다.

우리 게임에서는 다음을 함께 고려한다.

- 세계 공급량
- 현재 실질 생산량
- 교역권
- 식민지 생산
- 기업 소유
- 시장 접근

정확한 VP 임계값은 그대로 복사하지 않는다.

## 16. 기업

VP의 Corporation/Franchise 시스템을 적극 채택한다.

```text
자원
+
기술
+
조건
→ 기업 본사 설립
→ 국내/해외 지사
→ 경제적 보너스
```

우리 게임에서는:

- Great Merchant 창업
- Great Engineer 창업
- 역사적 기업 창업자
- 원료
- 가공품
- 서비스
- 석유제품
- 금융
- 문화/관광 서비스
- 산업기업
- 해외지사

와 통합한다.

## 17. 자원과 More Luxuries

VP에 통합된 More Luxuries의 철학을 채택한다.

우리 게임은 이미 고유 자원 체계를 별도로 설계 중이므로 VP 자원 목록을 그대로 복사하지 않는다.

대신:

- 사치자원 다양성
- 지역 특화
- 자원별 고유효과
- 독점
- 무역
- 기업

이라는 구조를 가져온다.

## 18. 건물

VP의 핵심 설계원칙은 **건물이 단순 산출량 증가만이 아니라 도시의 문제를 해결한다**는 점이다.

예:

- Hospital → Health
- Medical Lab → 고급 Health
- Bank → 경제 문제
- Market → 교역/경제
- Police Station → 치안/Stability/첩보
- Theater/Cinema → Culture/Happiness
- School/University → 교육/Science
- Power Plant → Power
- Sewer → Health/도시환경

기존 건물표를 VP의 역할 분화 관점으로 다시 감사한다.

## 19. 전문가와 위인

VP의 Specialist 가치 강화 방향을 채택한다.

우리 게임의 위인 직군:

- Great Scientist
- Great Engineer
- Great Merchant
- Great Writer
- Great Artist
- Great Musician
- Great Director
- Great General
- Great Admiral
- Great Prophet
- Great Philosopher
- Great Revolutionary

각 위인은 고유 역사적 능력을 가진다.

## 20. Great Philosopher와 Great Revolutionary 연동

철학가는 혁명가가 아니다.

하지만 혁명적 정치사상을 만든 철학가는 GReP에 영향을 줄 수 있다.

예:

- Rousseau
- Marx
- Locke 등 일부 인물

```text
사상
↓
사회제도/정치운동
↓
GReP
↓
Great Revolutionary
↓
체제변동 또는 독립
```

모든 정치철학자가 GReP를 생성하지는 않는다.

## 21. 유닛 계보

VP의 유닛 업그레이드 계보를 기본 참고로 사용한다.

- 근접
- 원거리
- 공성
- 기병
- 정찰
- 해군
- 항공
- 지원
- 민간

역할별 계보를 명확하게 유지한다.

## 22. 승급

VP의 역할별 Promotion 구조를 적극 참고한다.

- 공격형
- 방어형
- 도시공성형
- 대기병형
- 정찰형
- 해군형
- 항공형
- 지원형

승급은 단순 +10% 반복보다 실제 전술 차이를 만드는 방향으로 설계한다.

## 23. 전투

VP 전투 개편을 기본 참고로 사용한다.

- 유닛 전투력 재배치
- 공성유닛 역할 강화
- 해군 역할 구분
- 원거리전 밸런스
- 도시 방어
- 업그레이드 간격
- 전략자원 의존성
- 승급
- AI 전투 판단

정확한 VP 수치는 세계지도 크기와 우리 게임 턴 구조에 맞게 다시 계산한다.

## 24. 종교

VP의 종교 개편을 폭넓게 채택한다.

- Pantheon 다양화
- 창시자 효과
- 추종자 효과
- 강화 효과
- 개혁 효과
- 종교건물
- 종교 경쟁
- 종교 압력
- 선교
- 종교와 외교

우리 게임의 Great Prophet은 기존 방침대로 Faith 직접 구매를 유지한다.

## 25. 첩보

VP의 첩보 확장을 기본으로 한다.

- 기술 절도
- 방첩
- 외교정보
- 도시국가 영향
- 정치공작
- 기업정보
- 군사정보

Spy는 은밀한 개입, Great Revolutionary는 공개적 체제변동과 정치운동으로 역할을 구분한다.

## 26. 문화와 관광

VP의 문화/관광 시스템 재조정을 적극 참고한다.

- Great Works
- 문화건물
- 관광
- 고고학
- 문화적 영향력
- 외교적 연계
- 정책/이념과 문화승리 연결

Great Philosopher에는 Great Work of Philosophy를 별도로 만들지 않는 기존 방침을 유지한다.

## 27. 고고학

Archaeologist 계열은 유지한다.

- 유적
- 박물관
- 역사적 유산
- 관광
- 문화
- 국가정체성

과 연결한다.

## 28. 세계의회와 국제정치

VP의 World Congress 개편을 참고해 국제정치 시스템을 강화한다.

- 제재
- 자원 규제
- 무역 규제
- 국제 프로젝트
- 세계유산
- 외교승리
- 전쟁 관련 결의
- 식민주의/탈식민주의 관련 결의
- 기업 규제
- 환경 결의

## 29. 정책과 이념

VP처럼 정책은 단순 영구 보너스 묶음이 아니라 실제 플레이 방향을 정하게 한다.

우리 게임에서는:

- 사회제도
- 정책카드
- 정부
- 이념

을 구분하되 서로 연동한다.

## 30. 기술트리

VP의 기술트리 자체는 복사하지 않는다.

대신 다음 원칙을 채택한다.

- 빈 기술 최소화
- 한 기술에 지나친 콘텐츠 집중 방지
- 군사/경제/과학/문화 해금 균형
- 시대별 유닛 계보 연속성
- 건물의 실제 역사적 시기 고려
- 후기 시대의 플레이 밀도 유지

## 31. 불가사의와 국가불가사의

VP의 전면 재균형 철학을 채택한다.

- 모든 불가사의에 명확한 역할
- 단순 산출량 덩어리 방지
- 시대와 역사적 맥락 일치
- 특정 승리조건과 지나친 독점 방지
- 국가불가사의는 국가 발전단계 반영

## 32. 난이도

VP처럼 AI가 규칙을 제대로 활용하도록 먼저 개선하고, 난이도 보너스는 보조적으로 사용한다.

## 33. 야만인

VP의 야만인 밸런스를 참고한다.

우리 게임에서는 추후 다음과 분리 가능하다.

- 비국가 집단
- 부족집단
- 해적
- 반군
- 독립군

## 34. 교역로

VP의 내부/국제 교역 재조정 원칙을 가져온다.

교역로는 다음과 연결한다.

- Food
- Production
- Gold
- Science
- Culture
- 종교
- 외교
- 기업
- 자원 인지/확산
- 식민지
- 질병 확산 가능성

## 35. 도시 점령과 속국

도시를 직접 합병하는 것만이 정답이 아니도록 한다.

가능한 선택:

- 합병
- 점령
- 괴뢰
- 해방
- 속국화
- 보호국
- 자치정부

## 36. 이벤트와 조건부 시스템

복잡한 새 게이지를 계속 추가하기보다 정치, 독립, 혁명, 경제위기를 조건부 사건으로 처리한다.

예:

```text
식민정부 존재
+ 낮은 식민지 Happiness
+ 낮은 본국 Stability
+ 적절한 시대
+ Great Revolutionary
→ 독립 사건
```

## 37. 지도 시스템

VP의 Communitu 등 맵 스크립트는 참고만 한다.

우리 프로젝트는:

- ETOPO 기반 세계지도
- hex 내부 지형 집계
- 역사적 자원 원산지
- 실제 세계 지리

를 사용한다.

## 38. UI

EUI의 정보표시 철학은 참고한다.

- 도시 문제 원인 즉시 표시
- 산출량 출처 추적
- 외교정보 접근성
- 유닛 업그레이드 계보 가시화
- 자원/독점/기업 상태 가시화
- Happiness와 Stability 원인 툴팁
- 식민정부 상태 표시

## 39. VP에서 그대로 복사하지 않을 것

"거의 다 도입"은 "모든 숫자와 데이터 행을 복사"한다는 의미가 아니다.

1. VP의 정확한 수치 밸런스
2. VP의 기술트리 전체
3. VP의 문명별 UA/UU/UB 전체
4. VP의 맵 생성 자체
5. EUI 코드 자체
6. Civ V 엔진에만 필요한 내부 보정
7. 우리 시대 구분과 충돌하는 해금시점
8. 우리 동적 자원 시스템과 충돌하는 정적 자원 규칙
9. 우리 Health/Power 시스템과 중복되는 부분

## 40. 우리 게임에서 VP보다 추가되는 시스템

- 역사적 문명 등장시기
- 역사적 지역 기반 신생국 등장
- 식민정부
- 식민정부 자동운영
- Great Revolutionary
- Great Philosopher
- 정부교체 비용
- Stability
- 독립
- 동적 자원 발견
- 접촉 기반 자원 인지
- 콜럼버스 교환과 같은 동적 자원 확산
- Health
- 질병
- Power
- 역사적 기업 창업자
- 기능성 기업 상품/서비스
- 전세계 ETOPO 기반 실제 지형

## 41. 현재 정치 시스템과 VP 통합 최종 구조

```text
사회제도
↓
정책카드
↓
정부

도시 Happiness
+
국가 Stability
+
전쟁피로
↓
정치적 안정/위기

후기 개척자
↓
해외 개척
↓
식민정부
↓
본국에 세금/자원/교역 이익

식민정부 내부
↓
Great Revolutionary Point
↓
Great Revolutionary
↓
독립 또는 체제변동
↓
역사적 신생 문명 등장
```

## 42. 구현 우선순위

### 1단계: VP 기반 도시/경제 골격
- Happiness 원인
- Buildings
- Trade
- Monopoly
- Corporation
- Specialist
- Great People

### 2단계: 군사/전쟁
- Unit tree
- Promotion
- Supply
- War Weariness
- Combat rebalance

### 3단계: 정치/외교
- Diplomacy
- City-State Diplomacy
- Vassalage
- Policies
- Government
- Stability
- World Congress

### 4단계: 식민/독립
- Pioneer
- Colonist
- Colonial Government
- Great Revolutionary Point
- Great Revolutionary
- Independence
- Historical civ emergence

### 5단계: 문화/종교/첩보
- Religion
- Espionage
- Tourism
- Archaeology
- Great Works
- Ideology

### 6단계: AI
실제로는 모든 단계에서 AI를 함께 구현해야 한다.

## 43. 현재 확정 결론

**Vox Populi를 우리 게임의 기본 설계 레퍼런스로 사용한다.**

```text
Civilization V BNW
+
Vox Populi의 거의 모든 핵심 시스템
+
Civilization VI의 일부 유용한 요소
+
우리 게임의 역사적 시대/문명/자원/정치 시스템
```

특히 다음 VP 요소는 앞으로 "도입 여부를 다시 논의"하는 대상이 아니라 **기본 채택 상태**로 취급한다.

- Happiness/Needs 철학
- War Weariness
- Unit Supply
- City-State Diplomacy
- Vassalage
- Monopoly
- Corporation
- Franchise
- 후기 개척자
- 유닛 계보
- 전투/승급 재설계
- 건물 역할 재설계
- 전문가 강화
- 종교 재설계
- 첩보 확장
- 문화/관광
- 고고학
- World Congress
- 정책/이념 확장
- AI 개선
- 난이도 개선

## 44. 후속 작업

- `VP_HAPPINESS_STABILITY_ADAPTATION_V1.md`
- `VP_MILITARY_WAR_WEARINESS_SUPPLY_V1.md`
- `VP_DIPLOMACY_VASSAL_CITYSTATE_V1.md`
- `VP_MONOPOLY_CORPORATION_ADAPTATION_V1.md`
- `VP_PIONEER_COLONIST_COLONIAL_GOVERNMENT_V1.md`
- `GREAT_REVOLUTIONARY_SYSTEM_V1.md`
- `GOVERNMENT_POLICY_SWITCHING_COST_V1.md`

## 45. 주요 확인 자료

- Vox Populi 공식 저장소  
  https://github.com/LoneGazebo/Community-Patch-DLL

- 공식 README  
  https://github.com/LoneGazebo/Community-Patch-DLL/blob/master/README.md

- Vox Populi 프로젝트 파일  
  https://github.com/LoneGazebo/Community-Patch-DLL/blob/master/%282%29%20Vox%20Populi/Vox%20Populi.civ5proj

- 후기 개척자 계보를 포함한 Units 데이터  
  `Settler → Pioneer → Colonist`  
  https://github.com/LoneGazebo/Community-Patch-DLL/blob/master/%282%29%20Vox%20Populi/Database%20Changes/Units/UnitChanges2.sql

## 46. 상태

**상태: VP 거의 전면 채택 방침 확정**

이 문서는 이후 세부 시스템 설계의 상위 기준문서로 사용한다.
