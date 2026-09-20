# QualityChallenger office-history fallback

## 날짜
2026-09-21

## 문제

Wikidata P39만 사용한 자동 감사에서 선거 전 state/local elected office가 누락되는 사례가 확인됐다. 원인은 후보 이름 alias 불일치와 날짜 qualifier가 없는 P39 claim이다. 이 때문에 2014 North Carolina의 Tillis와 2018 Missouri의 Hawley 등 일부 도전자가 quality=0으로 남아 학습 자체가 왜곡됐다.

## 수정 원칙

특정 오답 후보만 수동 코딩하지 않는다. 자동 state/local quality tier가 0이거나 undated eligible office review가 있는 모든 후보에 동일한 Wikipedia intro fallback을 적용한다.

선거 전 연도가 같은 문장에 명시된 경우에만 state/local elected office를 자동 인정한다. state-wide elected executive, state legislature, local elected office 순으로 tier 3, 2, 1을 부여한다. 미국 연방 하원 경력과 주지사 경력은 기존 audited fields를 계속 사용한다.

## 누출 방지

선거 이후 연도만 등장하는 직위는 quality에 포함하지 않는다. Wikipedia fallback의 페이지와 감지 근거는 quality_candidate_audit.csv에 기록한다.

## 다음 판정

동일한 99-race QualityChallenger OOS 실험을 다시 실행한다. 2018 조정계수는 2014 결과에서만 선택하고, 2022는 2014+2018에서만 선택한다.
