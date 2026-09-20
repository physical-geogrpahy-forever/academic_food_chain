# 2026 미국 상원 예측모형 Core V2
## 2026 production data audit + snapshot lock
### 작성일: 2026-09-21
### 상태: `2026_US_SENATE_MODEL_MASTER_HANDOFF_CORE_V2_2026-09-21(1).md`의 보존 기준선을 감사한 보조 문서

> 주의: 기존 handoff는 현재 남아 있는 가장 좋은 기준점이지만, 채팅 길이 제한으로 이후 진전이 유실되었을 가능성이 있다. 따라서 이 문서는 기존 handoff를 폐기하거나 모델을 새로 설계하지 않고, 2026 production 입력의 시점 정합성과 누출 방지 규칙을 추가로 고정한다.

---

# 1. 이번 감사에서 확정한 핵심

1. **Core V2는 유지한다.**
   - PVI
   - National
   - SameSeat
   - Incumbency
   - OutPartyIncumbent
   - Senate/Governor/House ExperienceDiff
   - PersonalVoteDiff
   - RelativeEconomicGrowth
   - Era interactions
   - 45일 poll observation layer

2. 현대 중간선거 headline benchmark도 유지한다.
   - RMSE 7.85%p
   - MAE 5.79%p
   - Direction 91.9%

3. 2026 정기 연방 총선일은 **2026-11-03**이다.

4. 따라서 정확한 **45-day snapshot date는 2026-09-19**이다.

5. 2026-09-21은 이미 43일 전이다. 따라서 앞으로 다음 두 제품을 구분한다.
   - `SNAPSHOT_45D`: 2026-09-19까지 실제로 공개되어 있었던 정보만 사용
   - `LIVE_NOWCAST`: 실행 당일 최신 공개자료 사용. 단, headline 7.85%p와 직접 비교하지 않고 동일 lead-time 역사 OOS를 따로 계산

6. **BEA 2026 Q2 state personal income은 2026-09-30 공개 예정**이다. 따라서 Q2는 `SNAPSHOT_45D`에 넣을 수 없다.
   - 45-day snapshot의 경제항은 2026 Q1을 유지한다.
   - 9월 30일 Q2로 갱신하면 약 34-day nowcast이므로, 역사 선거도 동일한 34-day information set으로 다시 평가해야 한다.

7. **BLS 2026년 8월 주별 고용 및 실업률은 2026-09-18 공개**되었다. 따라서 45-day snapshot 시점에는 이용 가능했다. 다만 이는 Core V2의 RelativeEconomicGrowth 대체항이 아니라 V3 증분 후보변수다.

8. **FEC standardized finance snapshot은 2026-06-30 July Quarterly가 가장 일관된 현재 cutoff**다.
   - July Quarterly close of books: 2026-06-30
   - filing deadline: 2026-07-15
   - October Quarterly close of books: 2026-09-30, filing deadline: 2026-10-15
   - 따라서 45-day snapshot에는 October Quarterly를 사용할 수 없다.

9. **Census Vintage 2025**는 2025-07-01까지의 주별 인구와 migration components를 제공하며, 2025 인구의 age/sex/race/Hispanic-origin 세부치도 2026년 6월 공개되어 있다.

10. **2025 ACS 1-year는 2026-09-21 현재 공개일이 확정되지 않았다.** 따라서 socioeconomic composition의 최신 공통 자료는 2024 ACS 1-year이다.

---

# 2. Core V2 authoritative formula

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

Poll update:

```math
M^{post}_{i}=(1-w_i)M^{prior}_{i}+w_i Poll^{adj}_{i}
```

```math
w_i=w_{max}\frac{n_i^{eff}}{n_i^{eff}+k}
```

현재 기준값:

```text
w_max = 0.75
k = 0.5
```

---

# 3. 2026 production 변수 데이터 사전

| 변수 | Core/V3 | 역사자료 요구 | 2026 최신 usable source | 45-day 시점 사용값 | release lag / cutoff | leakage 규칙 | 상태 |
|---|---|---|---|---|---|---|---|
| `PVI` | Core | 각 Senate cycle 직전 2개 대통령선거의 state margin, national margin | FEC 공식 2024 및 2020 대통령 결과 | 2024 + 2020 | 확정 결과 | test cycle 이후 대통령선거 사용 금지 | LOCKED |
| `SameSeat` | Core | 같은 Senate class의 6년 전 결과 | FEC 2020 Senate 결과 | 2020 동일 의석 결과 | 확정 결과 | 2026 이후 정보 없음 | LOCKED |
| `Incumbency` | Core | 각 cycle 후보의 선거 시점 현직 상태 | FEC 후보목록 + 의회/주 공식 후보명단 | 2026 general-election 후보 기준 | 후보 교체 발생 시 timestamp 필요 | snapshot 이후 후보교체를 과거 snapshot에 소급 금지 | LOCKED-SCHEMA |
| `OutPartyIncumbent` | Core | 현직 여부 + 대통령 소속당 | 현직 상태 + 대통령 소속당 | 2026 snapshot 상태 | 즉시 | coding 방향 고정 | LOCKED-SCHEMA |
| `SenateExperienceDiff` | Core | 후보별 prior Senate service | Biographical Directory / Senate / 공식 경력자료 | 2026 후보 경력 | 후보 확정까지 변동 가능 | snapshot date 기준만 | LOCKED-SCHEMA |
| `GovernorExperienceDiff` | Core | prior governor service | NGA/주 공식 경력자료 | 2026 후보 경력 | 후보 확정까지 변동 가능 | snapshot date 기준만 | LOCKED-SCHEMA |
| `HouseExperienceDiff` | Core | prior House service | Biographical Directory / House | 2026 후보 경력 | 후보 확정까지 변동 가능 | snapshot date 기준만 | LOCKED-SCHEMA |
| `PersonalVoteDiff` | Core | 후보의 선거 이전 statewide/House overperformance | 공식 선거결과 + 기존 historical election DB | 2024까지의 과거 성과 | 선거결과 확정 | 2026 선거 자체 결과 사용 금지 | LOCKED-SCHEMA |
| `National` | Core | generic ballot, approval, national economy, midterm environment의 역사 snapshot | 2026 raw national polls | 2026-09-19까지 공개된 poll만 | poll별 publication timestamp | snapshot 이후 공개 poll 금지 | SOURCE NOT YET FULLY LOCKED |
| `RelativeEconomicGrowth` | Core | 각 cycle 시점에서 실제 공개된 state personal income growth | BEA state personal income | **2026 Q1** | Q2는 2026-09-30 공개 | 45-day benchmark에는 Q2 금지 | LOCKED |
| `PollObservation` | Core | state Senate polls with exact historical cutoff | historical 538 archive + 2026 raw polling feed 후보 | 2026-09-19까지 공개된 polls | poll publication timestamp 필수 | field date뿐 아니라 public availability도 cutoff | SOURCE NOT YET FULLY LOCKED |
| `FundraisingShare` | V3 | 과거 cycle 동일 filing stage | FEC 2026 candidate finance | **2026-06-30 July Quarterly** | filed 2026-07-15 | October Quarterly 금지 | READY FOR OOS TEST |
| `StateEmploymentGrowth` | V3 | 과거 cycle 동일 calendar information set | BLS CES/LAUS | 2026 Aug release | released 2026-09-18 | 45-day snapshot에 사용 가능 | READY FOR OOS TEST |
| `PopulationMigration` | V3 | historical vintage-consistent estimates | Census Vintage 2025 | 2025-07-01 | released Jan 2026 | later vintage 소급 금지 | READY FOR OOS TEST |
| `AgeRaceChange` | V3 | vintage-consistent demographic estimates | Census Vintage 2025 characteristics | 2025-07-01 | released Jun 2026 | later vintage 소급 금지 | READY FOR OOS TEST |
| `ACSComposition` | V3 | ACS release available before each snapshot | ACS 2024 1-year | 2024 ACS | 2025 ACS not yet released | 2025 ACS 사용 금지 | READY, LAGGED |
| `IdeologyFit` | V3 late | historical comparable candidate ideology score | DIME/CFscore candidate coverage | 2026 후보 coverage 미확정 | source dependent | 2026 생성 가능성 확인 전 투입 금지 | HOLD |

---

# 4. PVI 정의와 2026 input lock

```math
Lean_{i,y}=StatePresMargin_{i,y}-NationalPresMargin_y
```

```math
PVI_{i,2026}=w_1 Lean_{i,2024}+w_2 Lean_{i,2020}
```

기존 handoff 기본형:

```text
w1 = 0.67
w2 = 0.33
```

단, 역사 nested OOS에서 추정한 exact 가중치가 발견되면 그 값을 우선한다. 현재는 새 가중치를 임의 튜닝하지 않는다.

---

# 5. 경제항 snapshot 규칙

Core V2의 경제항은 삭제하거나 BLS로 대체하지 않는다.

```math
Growth_{i,2026Q1}=\frac{PI_{i,2026Q1}-PI_{i,2025Q1}}{PI_{i,2025Q1}}
```

```math
RelativeEconomicGrowth_i = Growth_i - NationalGrowth
```

또는 기존 코드가 state median centering을 사용했다면 그 정의를 우선한다. 현재 보존 MD에는 둘 다 언급된 흔적이 있으므로 exact code 복구 전 임의 변경 금지.

```math
EconomicSignal_{i,t}=RelativeEconomicGrowth_{i,t}\times PresidentPartySign_t
```

## 45-day lock

- Election day: 2026-11-03
- 45 days before: **2026-09-19**
- BEA Q1 release: 2026-06-25
- BEA Q2 release: **2026-09-30 예정**

```text
SNAPSHOT_45D economy = 2026 Q1
LIVE_AFTER_2026-09-30 economy = 2026 Q2 가능
```

그러나 Q2 live nowcast는 7.85%p headline과 직접 비교 금지.

---

# 6. Poll/National 데이터의 가장 중요한 수정

단순히 `field_end <= snapshot_date`만 검사하면 future leakage가 발생할 수 있다.

poll record 최소 필드:

```text
poll_id
race_id
pollster
sponsor
partisan_sponsor
population_type
sample_size
field_start
field_end
publication_date
source_url
candidate_D
candidate_R
margin_D_minus_R
mode
internal_flag
```

45-day inclusion rule:

```text
field_end <= 2026-09-19
AND publication_date <= 2026-09-19
```

Historical OOS raw polls는 기존 538 archive를 우선 유지하고, 2026 production raw polls는 VoteHub API를 1차 ingest 후보로 사용하며 DDHQ 및 공개 source로 cross-check한다. source bridge는 coverage/de-dup audit 전까지 최종 lock이 아니다.

---

# 7. Fundraising snapshot lock

FEC 2026 quarterly schedule:

```text
April Quarterly: close 2026-03-31 / filed 2026-04-15
July Quarterly: close 2026-06-30 / filed 2026-07-15
October Quarterly: close 2026-09-30 / filed 2026-10-15
Pre-General: close 2026-10-14 / filed 2026-10-22
```

45-day snapshot에서는 **July Quarterly**를 사용한다.

```math
FundShare_i = \frac{D\ individual\ contributions}{D\ individual\ contributions + R\ individual\ contributions}
```

또는 centered form:

```math
FundShareCentered_i = 2 FundShare_i - 1
```

금지:
- October Quarterly를 45-day snapshot에 사용
- current finance와 historical election-day finance를 비교
- raw total spending을 후보질의 단순 원인변수로 간주

---

# 8. Demography snapshot lock

Census Vintage 2025에서 2025-07-01 state population, migration, age, sex, race, Hispanic origin을 사용할 수 있다.

2025 ACS 1-year는 2026-09-21 현재 공개되지 않았으므로:

```text
SNAPSHOT_45D socioeconomic composition = ACS 2024 1-year
```

---

# 9. 두 개의 생산모형 시계를 분리한다

## A. Headline comparable snapshot

```text
product_id: SENATE_2026_45D
as_of: 2026-09-19
benchmark: Core V2 modern-midterm 45-day OOS
headline baseline: RMSE 7.85%p
```

## B. Live nowcast

```text
product_id: SENATE_2026_LIVE
as_of: execution date
```

새 release를 쓰면 동일 lead-time historical OOS benchmark가 필요하다.

---

# 10. exact Core V2 outputs 복구 상태

기존 handoff가 요구한 파일:

```text
core_v2_predictions_oos.csv
core_v2_residuals_oos.csv
core_v2_region_summary.csv
core_v2_coefficients_by_cycle.csv
core_v2_poll_snapshot_45d.csv
core_v2_config.json
```

현재 Library 및 연결 GitHub에서 실제 artifact는 발견되지 않았다.

원칙:
1. MD의 7.85%p를 새 유사모형의 성능이라고 속여 재현했다고 하지 않는다.
2. exact outputs가 발견되면 authoritative implementation artifact로 승격한다.
3. 발견되지 않으면 public data로 `Core V2-R`을 재구축한다.
4. 비슷한 RMSE가 나와도 동일 모델이라고 단정하지 않는다.

---

# 11. 다음 실행 순서

```text
R0 snapshot lock 완료
R1 exact artifact search 완료 - 현재 미발견
R2 exact artifact 발견 시 V3-A로 이동
R3 미발견 시 Core V2-R 재구축
V3-A hierarchical Era partial pooling
```

채택 조건:
- 현대 중간선거 RMSE 개선
- 전체 중간선거 OOS 심각한 악화 없음
- 특정 cycle 하나에만 의존하지 않음
- 방향 정확도 및 calibration 악화 없음
- leakage 없음

---

# 12. 공식/현재 자료 출처

- FEC election information: https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/
- FEC official 2024 presidential results: https://www.fec.gov/resources/cms-content/documents/2024presgeresults.pdf
- BEA Personal Income by State: https://www.bea.gov/data/income-saving/personal-income-by-state
- BEA release schedule: https://www.bea.gov/news/schedule
- BLS State Employment and Unemployment: https://www.bls.gov/news.release/archives/laus_09182026.htm
- FEC 2026 reporting dates: https://www.fec.gov/help-candidates-and-committees/dates-and-deadlines/2026-reporting-dates/2026-quarterly-filers/
- FEC Senate data: https://www.fec.gov/data/candidates/senate/
- Census Vintage 2025: https://www.census.gov/newsroom/press-kits/2026/national-state-population-estimates.html
- Census state detail: https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-detail.html
- Census ACS: https://www.census.gov/programs-surveys/acs.html

---

# 13. 이번 감사의 가장 중요한 한 줄

**Core V2의 7.85%p headline을 보존하려면 2026 production에서도 “최신값” 자체보다 “2026-09-19에 실제 이용 가능했던 값”을 우선해야 하며, 이후 새 자료를 쓰는 live nowcast는 반드시 별도의 동일 lead-time OOS 체계로 평가해야 한다.**
