# GitHub Actions run: congress-legislators source freeze

- Generated UTC: 2026-09-20T16:43:09.067214+00:00
- Source repository: unitedstates/congress-legislators
- Source branch: main
- Purpose: authoritative-ish term-date cross-check for prior Senate and House service, including appointments not recoverable from election-win history alone.

## Frozen files

| file | bytes | sha256 |
|---|---:|---|
| legislators-current.yaml | 1081081 | `a90636aef9e7c613b53b24eeadc8612ea946669a7ec8118e08833a01ded08cd2` |
| legislators-historical.yaml | 8997407 | `9641615f336b3113d6f89152e3441128cbdc3f61ccf87c65da3a015076c78c91` |

## Rule

These term records are used to audit congressional service only. Governor experience remains a separate source problem and is not inferred from congressional data.

## Next

Match the 198 headline candidates to legislator records and compare Senate/House service plus incumbency against the election-history proxy.
