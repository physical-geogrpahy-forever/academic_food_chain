# Congress candidate matching performance fix

## 날짜
2026-09-21

## 문제

첫 `crosscheck_congress_service.py`는 198 candidate-side rows 각각을 전체 historical legislator 목록과 비교하면서 매번 이름 variant를 다시 계산했다. 의회 경력이 없는 후보도 동일하게 전수 비교했기 때문에 불필요하게 느렸다.

## 수정

- 의원 자료를 normalized surname별로 인덱싱했다.
- 후보는 같은 surname 후보군을 우선 비교한다.
- 이름 variant를 사전에 계산해 반복 생성을 제거했다.
- 의회 경력이 없는 후보의 unmatched는 정상 상태로 처리한다.
- review는 다음 경우에만 생성한다.
  1. 이름 매칭이 애매함
  2. 선거이력상 의회경력이 있어야 하는데 term record가 매칭되지 않음
  3. 실제 term-date flag와 election-history proxy가 다름
- headline cycle별 실제 general-election date를 사용한다.

## 기대효과

실행시간을 크게 줄이면서, 실제로 중요한 appointment/incumbency/House-Senate service 차이만 검토 대상으로 남긴다.

## 다음

Actions 재실행 후 review row를 검토하고 지원되는 보정값만 override table로 고정한다.
