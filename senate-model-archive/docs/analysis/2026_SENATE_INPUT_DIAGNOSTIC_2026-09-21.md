# 2026 Senate input diagnostic snapshot

## Date
2026-09-21

## Purpose
This is an input/diagnostic snapshot for the locked Core V2-R Direction Production 2026 model.

It is not a published winner forecast. It records observable inputs and model-trigger conditions without converting them into an election verdict.

## Geographic / structural input
PVI uses the frozen 2026 definition:
PVI = 0.67 * 2024 state lean vs national + 0.33 * 2020 state lean vs national.

## External poll comparison
The poll column is a RealClearPolling current average captured on 2026-09-21.
The RCP latest-polls feed visible at capture time is dominated by Senate polls dated through 2026-09-17, so these averages are close to the exact 2026-09-19 45-day cutoff.

However, they are kept as an external diagnostic until every component poll has been audited for both field end and publication date against the exact cutoff.

## Nine-race diagnostic

| State | D candidate | R candidate | Seat | PVI D-R | RCP avg D-R | Out-party incumbent | Poll-PVI agree | Multi-candidate flag |
|---|---|---|---|---:|---:|---:|---:|---:|
| AK | Mary Peltola | Dan Sullivan | R incumbent | -13.14 | +1.7 | 0 | 0 | 1 |
| GA | Jon Ossoff | Mike Collins | D incumbent | -1.89 | +7.5 | 1 | 0 | 0 |
| IA | Josh Turek | Ashley Hinson | open R seat | -12.26 | -1.3 | 0 | 1 | 0 |
| ME | Troy Jackson | Susan Collins | R incumbent | +7.34 | +1.8 | 1 | 1 | 0 |
| MI | Abdul El-Sayed | Mike Rogers | open D seat | -0.53 | +2.1 | 0 | 0 | 0 |
| NH | Chris Pappas | John Sununu | open D seat | +3.87 | +4.8 | 0 | 1 | 0 |
| NC | Roy Cooper | Michael Whatley | open R seat | -3.13 | +8.3 | 0 | 0 | 0 |
| OH | Sherrod Brown | Jon Husted | R appointed incumbent | -10.76 | +4.8 | 1 | 0 | 0 |
| TX | James Talarico | Ken Paxton | open R seat | -11.66 | +2.6 | 0 | 0 | 0 |

## Immediate diagnostic observations
- The strongest structural disagreement between state PVI and current polling appears in several open-seat races as well as Georgia and Ohio.
- Georgia, Maine, and Ohio satisfy the structural definition of an out-party incumbent race.
- Alaska must not be forced into a two-candidate-only layer because ranked-choice voting and additional candidates are currently material.
- The locked third-party policy therefore flags Alaska for multi-candidate uncertainty rather than applying a directional minor-party correction.

## Next analysis layer
Before using the locked model operationally:
1. rebuild the exact 2026-09-19 poll snapshot at poll-row level
2. join June-30 FEC candidate finance fields
3. join SameSeat, candidate experience, PersonalVote, national environment, and RelativeEconomicGrowth
4. calculate model diagnostics and uncertainty flags under the frozen production config
5. preserve the complete input matrix and source manifest
