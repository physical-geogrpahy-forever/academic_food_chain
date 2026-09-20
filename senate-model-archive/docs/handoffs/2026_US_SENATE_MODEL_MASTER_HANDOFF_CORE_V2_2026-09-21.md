# 2026 미국 상원 중간선거 예측모형 MASTER HANDOFF
## Core V2 authoritative baseline + Core V3 development plan
### 작성일: 2026-09-21
### 상태: 이 문서가 2026-09-20 handoff를 대체하는 최신 기준 문서

---

# 0. 가장 먼저 읽을 것

이 프로젝트의 현재 기준안은 **Core V2**이다.

이전 handoff의 오래된 상태로 되돌아가서 다음 작업을 다시 시작하면 안 된다.

- 지역별 잔차가 아직 미완료라고 간주
- 후보질을 다시 처음부터 단순 이진변수로 설계
- 경제항이 없는 것으로 간주
- poll blending을 다시 처음부터 탐색
- 구형 Core의 10%p 이상 RMSE를 다시 기준선으로 사용

이 작업들은 이미 지나간 단계다.

현재 성능 기준선은 다음이다.

| 모델 | 검증 구간 | RMSE | MAE | 승패 방향 |
|---|---|---:|---:|---:|
| 이전 handoff 후보효과 개선형 | 2014, 2018, 2022 | 8.76%p | 미보존 | 91.9% |
| **Core V2 fundamentals** | **2014, 2018, 2022** | **7.99%p** | **6.18%p** | **90.9%** |
| **Core V2 + 45일 poll update** | **2014, 2018, 2022** | **7.85%p** | **5.79%p** | **91.9%** |
| Core V2 + poll | 2006~2022 중간선거 | 9.50%p | 6.66%p | 92.8% |
| Core V2 + poll | 2006~2022 전체 OOS | 10.14%p | 7.32%p | 91.2% |

**앞으로 Core V3 후보는 현대 중간선거 45일 스냅샷 RMSE 7.85%p를 반드시 기준으로 비교한다.**

7.85%p보다 낮아졌다고 해서 자동 채택하지 않는다. 개선이 특정 한 선거에만 의존하는지, 장기 중간선거 성능을 훼손하는지, 방향 정확도와 calibration이 악화되는지 함께 확인한다.

---

# 1. 절대 수정해서는 안 되는 핵심 원칙

## 1.1 경제항은 원래부터 Core의 필수 항이다

경제항을 새 변수로 "대체"하려고 하면 안 된다.

이전 handoff에서도 경제항은 명시적으로 필수였다.

기존 시험에서 BEA SQINC1 기반 주 개인소득 성장을 추가했을 때 2006~2022 rolling validation에서:

- 전체 RMSE: 16.45 → 16.25%p
- 경합주 RMSE: 18.87 → 18.35%p

로 소폭 개선됐다.

2022에서 문제였던 것은 **경제효과 자체가 아니라 총 개인소득에 팬데믹 이전소득과 transfer shock이 크게 들어간 것**이다.

따라서 결론은 다음이다.

> 경제항 삭제 금지.  
> 총 개인소득만을 고집하지도 말 것.  
> Core V2의 `RelativeEconomicGrowth`를 유지한 상태에서 transfer-sensitive component를 robust하게 처리한다.

BEA의 2026년 자료에서도 personal income은 earnings, transfer receipts, property income으로 분해된다. 따라서 earnings는 "경제항을 대신하는 새 변수"가 아니라 **기존 경제항의 왜곡을 진단하고 보강하는 구성요소**다.

## 1.2 후보질, 개인표, 현직효과는 서로 다른 항이다

다음 세 항을 합치면 안 된다.

1. Candidate experience
2. Personal vote / prior overperformance
3. Incumbency

특히 최근 연구는 양극화가 심화되면서 평균적인 incumbency effect는 약해졌지만 candidate-quality differential은 Senate에서 여전히 유의미할 수 있음을 보여준다.

## 1.3 지역 잔차를 고정 margin 보정치로 넣지 않는다

지역별 signed residual이 존재한다고 다음과 같이 하면 안 된다.

```math
Prediction^{new}_{i,t}
=
Prediction_{i,t}
+
MeanResidual_g
```

실제 OOS 시험에서 이러한 직접 지역 보정은 성능을 악화시켰다.

지역효과는 **점예측 평균의 고정 보정값이 아니라 오차 공분산과 uncertainty 구조**에 사용한다.

## 1.4 poll은 fundamentals를 대체하지 않는다

poll은 observation layer다.

선거 초반에는 fundamentals prior가 크고, 투표일에 가까워지면서 poll의 정보량이 증가한다.

그러나 poll이 많아져도 fundamentals를 완전히 없애지 않는다.

## 1.5 미래정보 누출 금지

모든 검증은 rolling out-of-sample이어야 한다.

예를 들어 2018을 예측할 때:

- 2020 이후 선거결과 사용 금지
- 2018 선거 이후 수정된 후보효과 사용 금지
- 선거일 45일 스냅샷 검증이면 그 뒤 poll 사용 금지
- campaign finance도 동일한 날짜 cutoff를 적용
- hyperparameter도 이전 cycle에서만 선택

---

# 2. 현재 authoritative Core V2

## 2.1 Fundamentals prior

기준식은 다음이다.

```math
\begin{aligned}
M^{prior}_{i,t} =
&\ \alpha_t
+\beta_P PVI_{i,t}
+\beta_N National_t \\
&+\beta_S SameSeat_{i,t-6}
+\beta_I Incumbency_{i,t}\\
&+\beta_{IS} OutPartyIncumbent_{i,t}\\
&+\beta_{SE} SenateExperienceDiff_{i,t}\\
&+\beta_G GovernorExperienceDiff_{i,t}\\
&+\beta_H HouseExperienceDiff_{i,t}\\
&+\beta_V PersonalVoteDiff_{i,t}\\
&+\beta_E RelativeEconomicGrowth_{i,t}\\
&+\text{Era interactions}.
\end{aligned}
```

**주의:** 이전 Core V2 요약식에서 경제항이 빠진 적이 있으나, 이는 생략 오류다.  
경제항은 이전 Core부터 존재했고 최신 authoritative formula에는 반드시 포함한다.

---

# 3. 각 항의 정의

## 3.1 PVI형 주 기본선

주 절대 대통령 margin을 그대로 쓰지 않는다.

```math
Lean_{i,t}
=
StatePresMargin_{i,t}
-
NationalPresMargin_t
```

최근 두 대통령선거를 가중한다.

과거 handoff 기본형:

```math
PVI_{i,t}
=
0.67 Lean_{t-1}
+
0.33 Lean_{t-2}
```

단, 가중치는 최종적으로 고정 상수가 아니라 historical OOS에서 추정할 수 있다.

538의 2024 Senate model 역시 최근 두 presidential election의 국가 대비 state lean을 핵심 fundamental로 사용했으며, 당시에는 최근 선거에 약 3배의 가중치를 주었다.

### 2026 적용

2026 nowcast에서는 2024와 2020 presidential lean이 핵심이다.

2016은 Core V2 기본 PVI에는 직접 들어가지 않지만, V3에서 3-cycle decay가 OOS 개선을 만드는지는 별도 시험 가능하다.

---

## 3.2 전국환경 `National_t`

전국환경은 하나의 단순 변수와 동일하지 않다.

핵심 정보:

- generic congressional ballot
- 대통령 지지율
- 대통령 소속당 midterm penalty
- national economy
- poll-level national swing

과거 검증에서 presidential approval를 기존 Core에 단독 추가하면 RMSE가 악화됐다.

따라서 presidential approval를 그대로 +x%p 하는 방식은 금지한다.

### 권장 구조

```math
National_t
=
f(
GenericBallot_t,
PresidentialApproval_t,
NationalEconomy_t,
Midterm_t
)
```

단, 다중공선성과 이중계산을 피하기 위해 partial pooling 또는 latent-factor 형태가 우선이다.

---

## 3.3 동일 의석 6년 전 효과

같은 Senate Class의 6년 전 결과는 중요한 정보다.

초기 검증:

Base:
- 전체 RMSE 16.84
- 경합주 RMSE 19.11
- 경합주 방향 66.1%

6년 전 same-seat raw margin 추가:
- 전체 RMSE 16.85
- 경합주 RMSE 17.13
- 경합주 방향 71.0%
- 최근 RMSE 9.58

따라서 전체 RMSE를 크게 낮추지는 않았지만 경합주에서 유용했다.

Hummel and Rothschild도 Senate model에서 6년 전 같은 의석의 Senate vote를 사용했다.

### Core V2

```math
SameSeat_{i,t-6}
```

을 단순 raw carryover로 두지 않고 Era interaction을 통해 시간이 갈수록 적절히 수축시킨다.

---

## 3.4 후보경력

Core V2는 후보질을 한 덩어리로 쓰지 않는다.

```math
SenateExperienceDiff
GovernorExperienceDiff
HouseExperienceDiff
```

를 분리한다.

이유:

- Senate와 governor는 statewide 인지도와 선거기반을 갖는다.
- House 경험은 federal elected experience지만 statewide 경험은 아니다.
- 경험의 효과가 시대에 따라 감소할 수 있다.
- 후보 간 "차이"가 중요한 것이지 양쪽 모두 경험자라면 net effect는 작아진다.

### 최신 문헌과의 정합성

Algara and Bae (2024)는 1900~2022 congressional elections에서 partisanship이 강해지면서 incumbency advantage는 크게 약해졌으나 candidate-quality differential은 특히 Senate에서 여전히 의미가 있다고 보고했다.

Hummel and Rothschild는 Senate 후보의 이전 직업을 여러 범주로 분리하여 사용했다.

538 2024 Senate model도 prior elected-office experience를 별도 fundamental로 사용했다.

---

## 3.5 개인표 `PersonalVoteDiff`

후보의 과거 초과성과를 사용한다.

개념:

```math
PersonalVote_c
=
ActualCandidatePerformance
-
ExpectedPartyPerformance
```

단, raw residual을 그대로 재사용하지 않는다.

필수:

- partial pooling
- Era interaction
- 후보의 과거 선거 수에 따른 shrinkage
- statewide와 district race의 정보량 차이 고려

### 과거 실험

statewide 후보효과를 추가했을 때 2014/2018/2022 RMSE가:

```text
9.63 → 8.76%p
```

방향 정확도가:

```text
89.9 → 91.9%
```

로 개선됐다.

강한 ±10%p winsorization은 최근 성능을 오히려 악화했다.

따라서 manual hard cap은 쓰지 않는다.

---

## 3.6 현직효과

현직효과와 후보질은 분리한다.

Core V2:

```math
\beta_I Incumbency
+
\beta_{IS} OutPartyIncumbent
```

그리고 Era interaction을 둔다.

### 이유

현대 양극화에서는 평균 incumbency advantage가 과거보다 약해졌다.

반대로 당파적으로 불리한 주에서 여러 번 살아남은 현직은 일반 incumbency와 다른 personal brand를 보유할 수 있다.

### 538 참고

538의 2024 Senate fundamentals는 기본 incumbency 효과를 약 0.6%p로 두었고, first-term incumbent의 효과를 더 작게 처리했다. 또한 incumbent의 과거 초과성과 중 약 30%가 다음 선거에도 이어지는 구조를 사용했다.

이 수치를 우리 모델에 그대로 복사하면 안 된다.

우리 Core V2는 자체 OOS로 계수를 추정한다.

---

# 4. 경제항: 삭제 금지, 대체 금지, robust화

## 4.1 역사적 근거

Hummel and Rothschild는 state-by-state personal income growth를 Senate와 Electoral College의 경제변수 가운데 가장 예측력이 높은 변수로 보고했다.

그들의 Senate fundamental model은 대략:

- presidential approval
- incumbency
- midterm effect
- state partisan baseline
- same-seat six-year result
- state personal income growth
- candidate experience

를 결합했다.

특히 경제는 unemployment level 같은 절대 수준보다 **income change / growth**가 더 유용했다.

## 4.2 기존 프로젝트 결과

BEA SQINC1을 이용한 실험에서 경제항은 약하지만 실제 추가 정보를 줬다.

따라서 경제항은 유지한다.

## 4.3 Core V2 authoritative economic term

기본 개념:

```math
RelativeEconomicGrowth_{i,t}
=
StateGrowth_{i,t}
-
NationalGrowth_t
```

대통령 집권당 책임방향을 반영:

```math
EconomicSignal_{i,t}
=
RelativeEconomicGrowth_{i,t}
\times
PresidentPartySign_t
```

D 대통령일 때 주 경제가 상대적으로 좋으면 D 방향,
R 대통령일 때 주 경제가 상대적으로 좋으면 R 방향으로 작동하도록 coding한다.

## 4.4 2020~2022 문제

총 personal income에는:

- transfer receipts
- property income
- earnings

이 함께 들어간다.

팬데믹 시기의 대규모 transfer 변화는 실제 노동시장 경제성과 다른 방향으로 personal income을 움직일 수 있다.

따라서 V3에서는 **경제항을 earnings로 교체하는 것이 아니라** 다음 비교를 한다.

### Baseline
```text
Relative total personal income growth
```

### Robust candidate A
```text
Relative earnings growth
```

### Robust candidate B
```text
Relative personal income growth
with transfer-shock downweighting
```

### Robust candidate C
```text
hierarchical combination:
income + earnings + wage growth
```

채택 조건은 오직 rolling OOS 개선이다.

## 4.5 2026 데이터 상태

2026-09-21 기준 BEA state personal income 최신 확정 공개치는 2026 Q1 자료다.

BEA는 SQINC1과 SQINC4를 제공한다.

SQINC4에서:

- earnings
- personal current transfer receipts
- property income

을 분리할 수 있다.

BEA의 2026 annual update와 state accounts update는 2026-09-30 예정이므로, 현재 nowcast는 Q1 기준으로 유지하고 9월 30일 이후 경제항만 재계산해야 한다.

---

# 5. Era interactions: Core V2의 핵심 개선

이전 모델은 현직, 후보경력, same-seat, personal vote가 모든 시대에 같은 크기로 작동한다고 가정하는 경향이 있었다.

Core V2는 이를 버렸다.

```math
Effect_{k,t}
=
\beta_k
+
\gamma_k Era_t
```

또는 equivalent shrinkage structure를 사용한다.

Era interaction 대상:

- SameSeat
- Incumbency
- OutPartyIncumbent
- SenateExperience
- GovernorExperience
- HouseExperience
- PersonalVote
- 필요하면 economic accountability

### 목적

- 양극화가 강해질수록 local/candidate effect가 자동 축소
- 과거 선거의 큰 incumbency effect를 2026에 그대로 이식하지 않음
- 현대 Senate에서 candidate quality가 완전히 0이 되지는 않도록 함

### Core V3 발전방향

단순 linear interaction보다 hierarchical partial pooling이 우선 후보다.

예:

```math
\beta_{k,era}
\sim
N(\mu_k,\tau_k^2)
```

각 시대 계수는 독립적으로 튀지 않고 공통 평균으로 수축된다.

---

# 6. Poll observation layer

## 6.1 기본식

```math
M^{post}_{i}
=
(1-w_i)M^{prior}_{i}
+
w_i Poll^{adj}_{i}
```

Core V2에서:

```math
w_i
=
w_{max}
\frac{n^{eff}_i}{n^{eff}_i+k}
```

nested OOS에서 현재 기준값:

```math
w_max = 0.75
k = 0.5
```

즉 poll이 많아도 fundamentals가 완전히 사라지지 않는다.

## 6.2 45일 snapshot

2026-09-21은 선거 약 6주 전이므로 역사 검증에서도 동일한 lead time을 맞춘다.

따라서 headline score는:

```text
Core V2 + 45-day poll update
RMSE 7.85%p
MAE 5.79%p
Direction 91.9%
```

이다.

선거일 직전 poll을 사용한 score와 섞으면 안 된다.

## 6.3 poll adjustment에서 고려할 요소

- pollster house effect
- pollster historical error
- LV/RV/Adult
- survey mode
- partisan sponsor
- sample size
- field date
- repeated-poll dependence
- national trend adjustment
- poll-fundamentals disagreement
- poll scarcity

## 6.4 최신 2026 poll-error 연구

Chen, Körtner, Wiederspohn, and Selb (2026)은 1990~2022의 318개 Senate election, 6,375개 preelection poll을 Bayesian hierarchical model로 분석했다.

핵심은 poll error를 하나의 고정 RMSE로 보지 않고:

```math
PollError
=
BiasComponent
+
VarianceComponent
```

로 분리하여 election context에 따라 변화시키는 것이다.

Core V3 uncertainty model은 이 구조를 반영할 가치가 높다.

---

# 7. 지역효과와 공분산

## 7.1 Core V2 지역잔차 결과

Core V2 + 45일 poll, 현대 중간선거 기준:

| 지역 | RMSE | 평균 signed residual |
|---|---:|---:|
| New England | 11.92 | R+1.17 |
| Upper Midwest | 8.76 | R+3.55 |
| Pacific/AK/HI | 8.51 | D+3.84 |
| Deep South | 8.29 | R+5.12 |
| Mountain West | 7.53 | R+2.09 |
| Mid-Atlantic | 6.82 | R+3.35 |
| Great Lakes | 6.76 | R+2.42 |
| Southeast | 6.14 | R+3.05 |
| Texas/Southwest | 5.02 | R+1.94 |

## 7.2 중요한 해석

지역마다 오차 패턴은 존재한다.

그러나 지역 평균 signed residual을 다음 선거의 deterministic correction으로 넣었을 때 OOS가 악화됐다.

따라서:

```math
E_{i,t}
=
E^{national}_t
+
E^{regional}_{g,t}
+
E^{state}_{i,t}
```

로 uncertainty를 모델링한다.

## 7.3 538 2024와의 정합성

538 2024 Senate model도 error를:

- national
- regional
- state-specific

으로 분해했다.

538의 당시 calibration에서는 margin error가 대략 7%p 규모였고, component SD는 national 약 4.8, regional 약 2.8, state 약 4.8%p였다.

이 숫자는 우리 모델에 그대로 복사하지 않는다.

하지만 **오차를 상관구조로 분해해야 한다는 설계 원칙**은 Core V2와 동일하다.

## 7.4 Core V3 권장 covariance

고정 지역만 사용하지 말고 다음 세 정보를 결합한다.

```math
\Sigma
=
\lambda_1 \Sigma_{historical\ residual}
+
\lambda_2 \Sigma_{geographic}
+
\lambda_3 \Sigma_{socioeconomic}
```

사회경제 유사도 후보:

- 교육
- 인종/ethnicity
- 도시화
- 산업구조
- 연령
- 이주
- turnout composition

점예측 평균은 건드리지 않고 Monte Carlo correlation을 개선한다.

---

# 8. 538 2024 Senate model에서 참고할 수 있는 것과 그대로 복사하면 안 되는 것

## 8.1 참고할 구조

538 2024 Senate methodology는 다음을 사용했다.

- weighted state partisan lean
- incumbency
- incumbent prior overperformance
- elected-office experience
- fundraising share
- polarization
- generic ballot
- poll average
- expert race ratings
- national/regional/state correlated uncertainty

특히 local factors의 weight를 polarization이 증가할수록 낮추고 national factors의 weight를 높였다.

이는 Core V2 Era interaction과 매우 비슷한 문제의식이다.

## 8.2 fundraising

538는 individual-contribution share를 사용했다.

그들의 2024 historical regression에서는 상대방보다 individual contributions share를 10%p 더 가져갈 때 약 1%p margin boost가 추정됐다.

**이 1:10 계수를 우리 모델에 직접 넣지 않는다.**

우리 모델은 별도 OOS 추정을 한다.

## 8.3 expert race rating

538는 qualitative ratings도 별도 predictor로 사용했다.

그러나 우리의 기본 철학은 재현 가능한 quantitative model이다.

따라서 Cook/Sabato/Inside Elections rating은:

- Core V2에 넣지 않음
- V3 optional comparator로만 시험
- 넣더라도 fundamentals/poll과 분리해 incremental OOS value를 확인

한다.

---

# 9. 선거자금: V3 후보지만 아직 기준안에 미포함

## 9.1 사용 가능한 데이터

### Historical
DIME v4.0:
- 1979~2024
- 8억 5천만건 이상의 itemized contributions
- candidate/committee records
- CFscores
- candidate identifiers

### 2026 current
FEC:
- candidate/committee receipts
- individual contributions
- disbursements
- cash on hand
- debts
- outside spending
- independent expenditures

2026 quarterly schedule:

- April Quarterly: through 2026-03-31
- July Quarterly: through 2026-06-30, filed 2026-07-15
- October Quarterly: through 2026-09-30, filed 2026-10-15
- Pre-General: through 2026-10-14, filed 2026-10-22

따라서 2026-09-21 현재 정규 quarterly 비교에서 가장 일관된 cutoff는 **2026-06-30**이다.

최근 등록 후보는 이후 filing도 존재할 수 있으므로 snapshot alignment가 필요하다.

## 9.2 왜 총지출을 바로 넣으면 안 되는가

Jacobson 연구의 핵심 문제:

- challenger spending은 경쟁력과 함께 증가
- incumbent spending은 위험한 선거일수록 증가
- 따라서 spending은 outcome의 원인이면서 동시에 expected competitiveness의 결과

즉 강한 endogeneity가 있다.

## 9.3 Core V3에서 먼저 시험할 finance 변수

우선순위:

1. individual contribution share
2. early-cycle contribution share
3. donor breadth
4. cash-on-hand share
5. outside spending은 별도

총지출 raw dollar는 우선순위가 낮다.

## 9.4 최신 early-money 연구

Case and Porter (2025)는 early fundraising을 단일 개념으로 취급하지 말고:

- candidate-centered early money
- election-centered relative early money

를 구분해야 한다고 지적했다.

우리 general-election V3에서도 같은 원칙을 적용한다.

---

# 10. 후보 이념 CFscore: 아직 V3 시험 후보일 뿐

DIME v4.0은 후보 및 정치조직의 CFscore를 제공한다.

가능한 아이디어:

```math
IdeologicalFit_i
=
-|CFscoreCandidate_i - StateIdeologicalCenter_i|
```

그러나 위험:

- CFscore와 party/PVI가 강하게 중복될 수 있음
- donor composition이 fundraising과 중복될 수 있음
- 후보 ideology 자체보다 candidate quality를 proxy할 수 있음

따라서 baseline에 넣지 않는다.

반드시 incremental rolling OOS로 시험한다.

---

# 11. 인구 및 turnout 강화모형

## 11.1 ACS

2026-09-21 현재 2025 ACS 1-year estimates는 아직 release date가 확정되지 않았다.

따라서 최신 공개 ACS 1-year는 2024다.

2025 ACS가 나왔다고 가정하고 사용하면 안 된다.

## 11.2 CPS Voting Supplement

2024 CPS Voting and Registration 자료와 2026년 8월 발표된 2024 election report를 사용할 수 있다.

활용:

- age turnout
- education turnout
- race/ethnicity turnout
- registration
- state-level composition

## 11.3 demographic term의 원칙

금지:

```text
Hispanic share +2 → D +1
```

권장:

```math
DemographicEffect_i
=
\sum_g
\Delta Share_{ig}
\times
Preference_{ig}
\times
ExpectedTurnout_{ig}
```

단, direct margin term은 강한 shrinkage.

더 안전한 용도:

- PVI trend explanation
- regional similarity
- turnout composition
- uncertainty heterogeneity

---

# 12. 2026 현재 데이터 상태

## 12.1 BEA

현재 state-level personal income/earnings:
- 2026 Q1 사용 가능
- 2026-09-30 annual/state update 예정

따라서 9월 30일 이후 economic signal을 갱신한다.

## 12.2 BLS QCEW

QCEW는 미국 일자리의 95% 이상을 포괄하는 employment/wage 자료를 state, county, industry 수준으로 제공한다.

현재 2026 Q1 자료 업데이트가 존재한다.

활용:

- wage growth robustness
- industry exposure
- tariff/energy/agriculture issue exposure

## 12.3 FEC

현재 2026 cycle candidate finance data는 live로 갱신된다.

historical validation에는 반드시 동일한 calendar cutoff를 사용한다.

## 12.4 Census

- 최신 공개 ACS 1-year: 2024
- 2025 ACS 1-year: 2026-09-21 현재 release date 미확정
- CPS 2024 Voting Supplement: 사용 가능
- 2024 Voting and Registration report: 2026-08 발표

---

# 13. Core V2 성능표를 절대 잃어버리지 말 것

## 13.1 현대 중간선거

```text
Cycles = 2014, 2018, 2022
```

### Fundamentals
```text
RMSE = 7.99%p
MAE = 6.18%p
Direction = 90.9%
```

### + 45-day poll observation
```text
RMSE = 7.85%p
MAE = 5.79%p
Direction = 91.9%
```

## 13.2 전체 중간선거 2006~2022

```text
Core V2 + poll
RMSE = 9.50%p
MAE = 6.66%p
Direction = 92.8%
```

## 13.3 전체 2006~2022 OOS

```text
Core V2 + poll
RMSE = 10.14%p
MAE = 7.32%p
Direction = 91.2%
```

## 13.4 이전 기준

```text
Previous candidate-effect model
Modern-midterm RMSE = 8.76%p
Direction = 91.9%
```

즉 Core V2는 이미 이전 기준보다 현대 RMSE를 0.91%p 개선했다.

---

# 14. Core V3의 목표

Core V3는 Core V2를 버리는 새 모델이 아니다.

다음 구조다.

```math
CoreV3
=
CoreV2
+
ValidatedMeanEnhancements
+
HierarchicalUncertainty
```

## 14.1 Mean model

후보 변수는 하나씩 추가한다.

후보:

1. hierarchical Era partial pooling
2. robust economic component
3. early fundraising share
4. donor breadth / cash-on-hand share
5. turnout composition
6. ideology fit
7. issue exposure

한 번에 여러 개를 넣지 않는다.

## 14.2 Uncertainty model

```math
\epsilon_{i,t}
=
\epsilon^{national}_t
+
\epsilon^{regional}_{g,t}
+
\epsilon^{state}_{i,t}
+
\epsilon^{poll}_{i,t}
```

그리고:

```math
\sigma_{i,t}
=
f(
PollCount,
PollDisagreement,
PollFundamentalsGap,
PartisanLeanMagnitude,
CandidateUncertainty,
HistoricalStateError
)
```

를 시험한다.

---

# 15. V3 검증 프로토콜

## 15.1 Rolling OOS

각 cycle은 이전 cycle만 학습한다.

예:

```text
2014 test: <=2012 train
2018 test: <=2016 train
2022 test: <=2020 train
```

## 15.2 현대 headline benchmark

```text
2014 + 2018 + 2022
45 days before election
```

## 15.3 hyperparameter

nested OOS로만 결정한다.

현재 cycle의 결과를 보고:

- Era shrinkage
- poll cap
- prior SD
- finance shrinkage
- covariance weight

를 튜닝하면 안 된다.

## 15.4 campaign finance snapshot

historical election에서도 2026과 같은 lead time 또는 동일 quarterly filing stage를 맞춘다.

예:

```text
July Quarterly snapshot
vs
July Quarterly snapshot
```

## 15.5 평가 지표

최소:

- RMSE
- MAE
- winner direction
- competitive-race RMSE
- competitive-race direction
- log score
- Brier score
- 50/80/95% interval coverage
- interval width
- calibration curve
- cycle-by-cycle RMSE
- region-by-region residual
- largest absolute misses

## 15.6 새 변수 채택 기준

다음 조건을 모두 본다.

1. 현대 중간선거 RMSE 개선
2. 전체 중간선거 OOS가 심하게 악화되지 않음
3. 개선이 특정 cycle 하나에만 의존하지 않음
4. 방향 accuracy가 악화되지 않음
5. uncertainty calibration이 악화되지 않음
6. future leakage 없음
7. 변수 정의가 2026에서도 실제 생성 가능

미세한 0.01~0.05%p 개선은 noise일 수 있으므로 cycle-block bootstrap 또는 paired residual comparison을 권장한다.

---

# 16. 다음 작업의 정확한 순서

## Stage V3-A: Core V2 재현 파일을 먼저 고정

새 변수 추가 전에 반드시 저장:

```text
core_v2_predictions_oos.csv
core_v2_residuals_oos.csv
core_v2_region_summary.csv
core_v2_coefficients_by_cycle.csv
core_v2_poll_snapshot_45d.csv
core_v2_config.json
```

이걸 저장하지 않고 다음 실험으로 넘어가면 다시 handoff 유실 문제가 반복된다.

## Stage V3-B: Era partial pooling

현재 Era interaction을 hierarchical structure로 변경.

비교:

```text
Core V2 fixed/linear era interactions
vs
Core V3 hierarchical era coefficients
```

## Stage V3-C: 경제항 robust화

**경제항 삭제/교체가 아니다.**

비교:

```text
A: existing RelativeEconomicGrowth
B: A + earnings robustness
C: A + transfer-adjustment
D: hierarchical income/earnings/wage signal
```

## Stage V3-D: fundraising

먼저:

```math
FundShare
=
\frac{D\ individual\ contributions}
{D + R\ individual\ contributions}
```

또는 D-R centered share.

그 다음 early money, donor breadth, COH.

## Stage V3-E: uncertainty

점예측 개선과 별도로 진행.

Chen et al. 2026식 election-level bias/variance 분리와 538식 national/regional/state covariance를 결합 검토.

## Stage V3-F: turnout/demography

CPS 2024, ACS 2024 기반.

## Stage V3-G: ideology/issues

마지막 단계.

이들은 PVI와 collinearity가 크고 subjective exposure model이 개입할 수 있으므로 앞 단계보다 후순위다.

---

# 17. 이미 실패했거나 반복하면 안 되는 접근

1. 2024 presidential margin을 그대로 2026 Senate baseline으로 사용
2. absolute presidential margin과 national environment를 중복 계산
3. presidential approval 하나만 national effect로 추가
4. 지역 평균 residual을 다음 선거 margin에 직접 더함
5. 후보 personal residual raw carryover
6. 후보효과 hard ±10%p cap
7. 후보질과 incumbency를 하나로 합침
8. Senate/Governor/House 경험을 하나의 단순 experience dummy로만 고정
9. poll이 많다는 이유로 fundamentals weight를 0에 가깝게 만듦
10. poll 안전주/경합주 hard gating
11. 각 주 election error를 독립 추출
12. total campaign spending을 단순 후보강점으로 사용
13. 경제항 삭제
14. earnings/wages를 경제항의 "대체 변수"라고 취급
15. current-cycle outcome을 이용해 hyperparameter tuning
16. election-day poll로 45-day nowcast 성능을 평가
17. 2025 ACS가 이미 공개됐다고 가정

---

# 18. 문헌에서 확인한 핵심 근거

## Hummel & Rothschild

Hummel, P., & Rothschild, D. (2014). Fundamental models for forecasting elections at the state level. Electoral Studies, 35, 123-139. https://doi.org/10.1016/j.electstud.2014.05.002

핵심:

- state-level presidential/Senate/governor fundamentals
- personal income growth가 Senate에서 중요한 economic signal
- unemployment level보다 change/growth가 유용
- six-year prior Senate result
- incumbency
- midterm
- candidate previous job/experience
- early forecast가 가능하도록 Q1 state income을 선호

## Algara & Bae

Algara, C., & Bae, B. (2024). Do Quality Candidates and Incumbents Still Matter in the Partisan World? Comparing Trends and Relationship Between Candidate Differentials and Congressional Election Outcomes, 1900-2022. Journal of Political Marketing, 23(3), 243-265. https://doi.org/10.1080/15377857.2024.2371764

핵심:

- partisanship 영향 증가
- incumbency advantage의 설명력 약화
- candidate-quality differential은 여전히 의미
- 특히 Senate에서 candidate quality가 더 중요

## Linzer

Linzer, D. A. (2013). Dynamic Bayesian Forecasting of Presidential Elections in the States. Journal of the American Statistical Association, 108(501), 124-134. https://doi.org/10.1080/01621459.2012.737735

핵심:

- fundamentals prior
- state polls
- hierarchical partial pooling
- national campaign effect
- time dynamics

직접 Senate 논문은 아니지만 poll-update 구조의 통계적 기반으로 중요.

## Heidemanns, Gelman & Morris

Heidemanns, M., Gelman, A., & Morris, G. E. (2020). An Updated Dynamic Bayesian Forecasting Model for the U.S. Presidential Election. Harvard Data Science Review, 2(4). https://doi.org/10.1162/99608f92.fc62f1e1

핵심:

- fundamentals early
- polls later
- hierarchical Bayesian dynamic updating
- nonsampling bias 고려

## Chen et al.

Chen, S., Körtner, J., Wiederspohn, J., & Selb, P. (2026). Electoral Predictors of Polling Errors. The Journal of Politics, 88(4), 1437-1449. https://doi.org/10.1086/736694

핵심:

- 6,375 polls
- 318 US Senate elections
- 1990~2022
- poll bias와 variance 분리
- hierarchical election-level poll-error model
- election context에 따라 poll-error distribution이 달라질 수 있음

## Jacobson

Jacobson, G. C. (2006). Campaign spending effects in U.S. Senate elections: Evidence from the National Annenberg Election Survey. Electoral Studies, 25(2), 195-226. https://doi.org/10.1016/j.electstud.2005.05.005

핵심:

- challenger spending과 electoral strength가 강하게 연결
- incumbent spending은 threat에 반응
- finance 변수의 강한 endogeneity

## Case & Porter

Case, C. R., & Porter, R. (2025). Conceptualizing and measuring early campaign fundraising in congressional elections. Political Science Research and Methods.

핵심:

- early money 정의에 따라 결과가 달라짐
- candidate-centered와 election-centered early fundraising을 분리해야 함

## 538 2024 Senate methodology

G. Elliott Morris, "How 538's 2024 Senate election forecast works", 2024-10-23.

핵심:

- recent presidential state lean
- generic ballot
- incumbency
- prior candidate overperformance
- experience
- fundraising
- polarization
- poll average
- expert ratings
- national/regional/state error decomposition
- predictor disagreement과 poll scarcity에 따른 heteroskedastic uncertainty

우리 모델은 538를 복제하지 않는다.  
문헌/모델 구조가 독립적으로 같은 방향을 지지하는지 확인하는 benchmark로 사용한다.

---

# 19. 데이터 소스

## Historical election
FiveThirtyEight election-results:
https://github.com/fivethirtyeight/election-results

주요 파일:
- election_results_senate.csv
- election_results_gubernatorial.csv
- election_results_house.csv

House blob SHA:
```text
562c150fe6e375b73c9a8876b042ccdfc12aa45e
```

## Historical polls
FiveThirtyEight data / pollster ratings archive.

## Economy
BEA:
https://www.bea.gov/data/income-saving/personal-income-by-state

Tables:
- SQINC1
- SQINC4
- SQGDP1
- SQGDP11

BLS QCEW:
https://www.bls.gov/cew/

## Finance
FEC:
https://www.fec.gov/data/

DIME v4:
https://data.stanford.edu/dime

## Demography / turnout
Census ACS:
https://www.census.gov/programs-surveys/acs.html

CPS Voting:
https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-voting.html

---

# 20. 다음 ChatGPT에게 주는 금지사항

다음 ChatGPT는 절대 다음과 같이 시작하지 말 것.

> "지역 잔차부터 새로 계산하겠습니다."

이미 끝났다.

다음처럼 시작하지 말 것.

> "경제 변수를 새로 넣어봅시다."

이미 있다.

다음처럼 시작하지 말 것.

> "후보질을 Senate/Governor/House로 나누는 것이 어떨까요?"

이미 Core V2에서 그렇게 했다.

다음처럼 시작하지 말 것.

> "poll 가중치를 처음부터 최적화하겠습니다."

이미 `w_max=0.75, k=0.5`가 현재 OOS 기준값이다.

다음 ChatGPT의 올바른 시작은:

> "Core V2의 7.85%p 기준선을 고정하고, 기존 예측 CSV와 잔차 CSV를 먼저 영구 산출물로 저장한 뒤, V3-A hierarchical Era partial pooling부터 동일 rolling OOS protocol로 비교하겠습니다."

---

# 21. 가장 중요한 한 줄

**현재 authoritative model은 `PVI + 전국환경 + 같은 의석 6년 전 정보 + 현직/반대당 현직 + Senate/Governor/House 후보경력 + personal vote + 기존 상대경제성장 + Era interactions`의 Core V2 fundamentals를 45일 Senate poll observation model로 업데이트하고, national/regional/state 공분산으로 uncertainty를 시뮬레이션하는 구조이며, 현대 중간선거 headline OOS 성능은 RMSE 7.85%p, MAE 5.79%p, 방향 91.9%이다.**

---

# 22. 현재 작업 재개 지점

다음 실제 작업은 아래 순서다.

```text
1. Core V2 exact outputs를 파일로 고정
2. V3-A hierarchical Era partial pooling
3. V3-B economy robustness, 경제항 유지
4. V3-C early fundraising
5. V3-D heteroskedastic poll-error + covariance
6. V3-E turnout/demography
7. V3-F ideology/issues
```

각 단계에서 이전 단계보다 OOS가 좋아지는 경우에만 채택한다.

이 문서 이전의 handoff에서 "미완료"라고 적힌 내용보다 이 문서의 상태를 우선한다.