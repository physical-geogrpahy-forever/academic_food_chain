# Strategic resource source plan v1

This file locks the evidence hierarchy for the seven strategic resources on the
canonical ~50 km Civ world hex map. It does not finalize gameplay thinning.

## General rule

- Each strategic-resource hex stores an integer quantity.
- Quantity is derived within each resource separately.
- Physical tonnage is never compared between different resources.
- Source evidence is preserved before any gameplay thinning.
- Candidate quantity is not final placement.

## HORSES

Primary source:
- Global horse distribution 2015, Harvard Dataverse DOI 10.7910/DVN/JJGCTX.

Evidence:
- mean horse density in hex
- maximum source-cell horse density in hex

Quantity range:
- 2..4

## IRON

Primary source:
- USGS Mineral Resources Data System (MRDS).

Evidence hierarchy:
1. MRDS deposit-size code when present: Small=1, Medium=2, Large=3
2. commodity priority: primary > secondary > tertiary
3. count of matched deposits/occurrences inside the hex

Quantity range:
- 2..6

## NITER

Niter is treated as historically extractable nitrate supply potential, not as a
modern mine-only commodity.

Reason:
- major natural sodium-nitrate deposits are concentrated in northern Chile
- historically important potassium nitrate was also extracted/manufactured from
  nitrate-bearing soils, cave sediments and accumulated organic wastes in India,
  China, Korea, Japan and the Ottoman world

Evidence policy:
1. documented natural nitrate provinces
2. documented historical saltpetre production districts with spatially explicit
   evidence
3. minor documented natural/cave nitrate occurrences

Do not create candidate hexes solely from climate or population proxies.

Quantity range:
- 2..6

## COAL

Primary source:
- Global Energy Monitor, Global Coal Mine Tracker, current 2026 release.

Evidence hierarchy:
1. reported reserve/resource tonnes where available
2. annual production
3. designed capacity
4. mine/project status and number of mines

Quantity range:
- 2..7

## OIL

Primary source:
- Global Energy Monitor, Global Oil and Gas Extraction Tracker, March 2026.

Evidence hierarchy:
1. reported reserves
2. production
3. number/status of oil or oil-and-gas fields
4. field polygons, when available, are intersected with all hexes they occupy;
   quantitative field evidence is divided among intersected hexes to avoid
   duplicating a whole field's reserves into every touched hex

Both land and water hexes may carry oil evidence.

Quantity range:
- 2..7

## ALUMINUM

Game resource represents bauxite/aluminium ore potential.

Primary source:
- USGS MRDS bauxite/aluminum records.

Evidence hierarchy:
1. MRDS deposit-size code
2. commodity priority
3. count of matched deposits/occurrences

Quantity range:
- 3..8

## URANIUM

Preferred source:
- IAEA UThDEPO (World Distribution of Uranium and Thorium Deposits and Occurrences).

Preferred evidence:
1. uranium deposit resource range
2. number of UThDEPO uranium deposits in the hex
3. MRDS uranium deposit size/commodity evidence as fallback

UThDEPO locations are approximate and resource estimates may use different
reporting standards or historical estimates; these limitations must remain in
metadata.

Quantity range:
- 1..4

## Quantization

Each resource obtains a positive evidence score E. Positive hexes are ranked
within that resource only to obtain strength S in (0,1].

For quantity range [Qmin,Qmax]:

    n = Qmax - Qmin + 1
    Q = Qmin + floor(min(S, 1-epsilon) * n)

and Q is clipped to Qmax. Hexes with no evidence have Q=0.

This produces intermediate values (for example iron 2,3,4,5,6), not only a
binary small/large deposit.

## Current implementation files

- resource_catalog_v1.yaml
- build_stage10c_mrds_evidence.py
- build_stage10f_goget_evidence.py
- build_stage10i_horse_evidence.py
- build_stage10j_coal_evidence.py
- build_strategic_candidates.py
