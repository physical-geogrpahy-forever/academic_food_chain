# Partisan-alignment override map v1

## 날짜
2026-09-21

## 목적

Core V2-R 역사 Senate target과 SameSeat를 재구축할 때 단순 DEM/REP ballot label만으로 처리할 수 없는 예외 선거를 명시적으로 관리한다.

## 원칙

- 공식 정당 또는 Senate caucus 관계가 명확한 경우에만 `ALIGN`.
- 두 주요 정당 가운데 한쪽 후보가 없거나 top-two 구조가 D-D인 경우 `EXCLUDE` 또는 별도 검토.
- 같은 진영 후보가 복수로 경쟁한 경우 임의 합산하지 않는다.
- 99개 headline 표본을 맞추기 위한 항목은 `RECONSTRUCTION_HYPOTHESIS`라고 명시하며 사실 확정과 구분한다.
- 2026 결과는 어떤 규칙 선택에도 사용하지 않는다.

## source-supported alignments

- 2006 CT Joseph Lieberman: Independent Democrat, Democratic caucus 쪽으로 정렬.
- 2006 VT Bernie Sanders: Independent, Democratic caucus 쪽으로 정렬.
- 2008 MS special Ronnie Musgrove: FEC candidate record의 Democratic Party를 사용.
- 2012/2018 ME Angus King: Independent, Democratic caucus 쪽으로 정렬.
- 2012/2018 VT Bernie Sanders: Democratic caucus 쪽으로 정렬.

## 아직 잠금하지 않은 사례

- 2010 AK: Murkowski가 R/W였지만 Joe Miller도 Republican 후보였으므로 단순 R-side 단일후보화하지 않는다.
- 2014 KS, 2022 UT: 민주당 공식 후보가 없는 상태의 independent를 자동으로 D-side로 바꾸지 않는다.
- 2022 AK: ranked-choice와 복수 Republican 때문에 별도 처리.

## 파일

- `config/partisan_alignment_overrides_v1.csv`

## 다음

이 override map을 이용해 SameSeat exact-6-year와 last-prior-same-class를 동시에 생성하고, headline 99개 표본의 exact-6-year coverage를 감사한다.
