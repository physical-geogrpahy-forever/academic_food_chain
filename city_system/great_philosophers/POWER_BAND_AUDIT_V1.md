# Great Philosopher Power Band Audit V1

Date: 2026-09-22
Status: FIRST NUMERICAL SCREEN COMPLETE

## Purpose

This audit screens the 227 Great Philosopher abilities for obvious within-era power outliers after the second-pass historical/gameplay effect QA.

It is not a final numerical balance pass.

## Method

A rough heuristic score was used to flag:
- large one-time Science/Culture/Faith/Gold/Production bursts;
- technology/civic percentage progress;
- Eureka/Inspiration effects;
- permanent city/empire bonuses;
- specialist bonuses;
- charge counts;
- repeated-trigger effects.

The heuristic is intentionally conservative and is only used to identify candidates for manual review.

## Result

No clear numerical outlier required an immediate balance change.

Apparent low-score cases were mostly parser false positives because the heuristic under-read conditional permanent bonuses written as:
- international trade route yields;
- institutional-diversity bonuses;
- specialist-per-city scaling;
- happiness/health conditional yields;
- government/no-government branch effects.

Examples:
- Pythagoras
- Kautilya
- Fazang
- Ibn Khaldun
- Hugo Grotius
- Gu Yanwu
- Cesare Beccaria
- Pierre-Joseph Proudhon
- Mikhail Bakunin
- William James

These are not automatically weak in actual gameplay.

The only high heuristic flag was Paul Feyerabend:
- current technology without Eureka -> Science 160;
- otherwise -> Culture 160;
- Great Philosopher Point 50.

Because Science 160 and Culture 160 are mutually exclusive rather than additive, this is not treated as an obvious outlier.

## Current conclusion

Do **not** numerically retune Philosopher abilities before global game-speed scaling and recruitment thresholds are defined.

The roster has passed:
- historical-effect diversity QA;
- duplicate-effect QA;
- later-era reference QA;
- first numerical outlier screen.

## Required later balance pass

Final numerical tuning should use:
1. Standard-speed technology and civic costs by era;
2. Great Person recruitment thresholds by era;
3. average city count and specialist count by era;
4. typical number of active thought chains per city;
5. expected international/domestic trade-route counts;
6. average duration before the next Philosopher recruitment;
7. comparison against Great Scientist, Engineer, Merchant, Writer and Prophet power.

Only then should flat values such as 40, 80, 120 or 160 and percentage values such as 5%, 10% or 15% be normalized.
