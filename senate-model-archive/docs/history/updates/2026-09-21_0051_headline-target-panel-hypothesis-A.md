# GitHub Actions run: Core V2-R headline target panel, Hypothesis A

- Generated UTC: 2026-09-20T16:58:32.001224+00:00
- Execution: GitHub Actions
- Scope: 2014, 2018, 2022 Senate general elections

## Result

- Included races: 99
- Excluded by Hypothesis A: 5
- Unresolved processing issues: 0
- Cycle counts: 2014=33, 2018=33, 2022=33

## Margin definitions preserved

- margin_d_minus_r_total_pctpt = (D-side votes - R-side votes) / all valid candidate votes * 100
- margin_d_minus_r_two_party_pctpt = (D-side votes - R-side votes) / (D-side + R-side votes) * 100

The surviving handoff does not uniquely identify which target-margin denominator the original Core V2 used, so both are retained. Neither is discarded until OOS reproduction resolves the ambiguity.

## Hypothesis A alignment

- 2018 ME Angus King -> Democratic-aligned side
- 2018 VT Bernie Sanders -> Democratic-aligned side
- Exclude 2014 AL, 2014 KS, 2018 CA, 2022 AK, 2022 UT
- Ordinary special elections remain included when a unique D and R side exists
- Fusion ballot lines for the same candidate are aggregated
- Ranked-choice records use the maximum recorded round rather than summing rounds

## Status

This is a reconstruction hypothesis, not an assertion that the original Core V2 used exactly these rules.

## Output

- data/processed/core_v2r_headline_target_hypothesis_A.csv

## Next

Build the 2006-2022 partisan-alignment override map and canonical OOS target panel, then add PVI and SameSeat before fitting any model.

## Excluded races

- 2022 UT Class III: unaffiliated Evan McMullin faced Republican Mike Lee with no Democratic ballot nominee; Hypothesis A excludes rather than partisan-aligns
- 2022 AK Class III: ranked-choice contest with multiple Republican candidates; Hypothesis A excludes from headline reconstruction
- 2018 CA Class I: top-two general election was Democrat versus Democrat
- 2014 KS Class II: independent Greg Orman faced Republican Pat Roberts after Democratic withdrawal; Hypothesis A excludes rather than partisan-aligns
- 2014 AL Class II: no Democratic-side opponent in general election; implied by 99-race denominator
