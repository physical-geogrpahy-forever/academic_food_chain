#!/usr/bin/env python3
"""
Fit the locked Core V2-R fundamentals prior on all eligible historical data
through 2022 for 2026 application.

This script deliberately DOES NOT score 2026 races or emit election-direction
predictions. It freezes only the production fundamentals coefficients,
standardization statistics, and fit metadata.

The historical source script must match the canonical validation manifest.
"""
import csv
import hashlib
import json
import runpy
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'performance/run_fullcycle_inc_era_oos.py'
MANIFEST = ROOT / 'final/validation/manifest.json'
OUTDIR = ROOT / 'data/snapshots'
DOC = ROOT / 'docs/analysis/2026_PRODUCTION_FUNDAMENTALS_FIT.md'

COEF = OUTDIR / '2026_production_fundamentals_coefficients.csv'
STD = OUTDIR / '2026_production_fundamentals_standardization.csv'
META = OUTDIR / '2026_production_fundamentals_fit_meta.json'

OUTDIR.mkdir(parents=True, exist_ok=True)
DOC.parent.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
expected = manifest['source_sha256']['base_script']
actual = sha256(SOURCE)
if actual != expected:
    raise RuntimeError(
        f'Canonical base source SHA mismatch: expected {expected}, got {actual}. '
        'Refusing to fit 2026 coefficients from a non-canonical source.'
    )

ns = runpy.run_path(str(SOURCE))
rows = ns['rows']
tune = ns['tune']
design = ns['design']
BASE = ns['BASE']
ARCH = ns['ARCH']

# The production fit uses every eligible historical modeling row available
# through 2022. Hyperparameters are selected by the same chronological inner
# tuning function used by the canonical historical runner.
best, trace = tune(rows)
inner_rmse, _, arch, lam_local, lam_econ, lam_nat, lam_inc, lam_era = best
features = BASE + ARCH[arch]

X, (mu, sd) = design(rows, features)
y = np.asarray([float(r['y']) for r in rows], dtype=float)

pen = np.zeros(X.shape[1], dtype=float)
for j, feat in enumerate(features, start=1):
    if feat in ('same_last', 'same_gap'):
        pen[j] = lam_local
    elif feat == 'econ':
        pen[j] = lam_econ
    elif feat == 'national':
        pen[j] = lam_nat
    elif feat in ('inc_diff', 'outparty'):
        pen[j] = lam_inc
    elif feat.endswith('_era') or feat == 'same_era':
        pen[j] = lam_era

beta = np.linalg.pinv(X.T @ X + np.diag(pen)) @ (X.T @ y)
fitted = X @ beta
train_rmse = float(np.sqrt(np.mean((fitted - y) ** 2)))
train_mae = float(np.mean(np.abs(fitted - y)))
train_direction = float(np.mean((fitted > 0) == (y > 0)) * 100.0)

raw_betas = [float(beta[j + 1] / sd[j]) for j in range(len(features))]
raw_intercept = float(beta[0] - sum(beta[j + 1] * mu[j] / sd[j] for j in range(len(features))))

coef_rows = [{
    'fit_for_cycle': 2026,
    'architecture': arch,
    'term': 'Intercept',
    'standardized_beta': float(beta[0]),
    'raw_scale_beta': raw_intercept,
    'lambda_local': lam_local,
    'lambda_econ': lam_econ,
    'lambda_national': lam_nat,
    'lambda_inc': lam_inc,
    'lambda_era': lam_era,
    'train_n': len(rows),
}]
for j, feat in enumerate(features):
    coef_rows.append({
        'fit_for_cycle': 2026,
        'architecture': arch,
        'term': feat,
        'standardized_beta': float(beta[j + 1]),
        'raw_scale_beta': raw_betas[j],
        'lambda_local': lam_local,
        'lambda_econ': lam_econ,
        'lambda_national': lam_nat,
        'lambda_inc': lam_inc,
        'lambda_era': lam_era,
        'train_n': len(rows),
    })

with COEF.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(coef_rows[0].keys()))
    w.writeheader()
    w.writerows(coef_rows)

std_rows = []
for j, feat in enumerate(features):
    std_rows.append({
        'fit_for_cycle': 2026,
        'architecture': arch,
        'term': feat,
        'mean': float(mu[j]),
        'sd': float(sd[j]),
        'train_n': len(rows),
    })
with STD.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(std_rows[0].keys()))
    w.writeheader()
    w.writerows(std_rows)

cycles = sorted({int(r['cycle']) for r in rows})
meta = {
    'generated_utc': datetime.now(timezone.utc).isoformat(),
    'fit_for_cycle': 2026,
    'historical_information_through': max(cycles),
    'training_cycles': cycles,
    'train_n': len(rows),
    'canonical_source_path': str(SOURCE.relative_to(ROOT)),
    'canonical_source_sha256': actual,
    'manifest_expected_source_sha256': expected,
    'architecture': arch,
    'features': features,
    'hyperparameters': {
        'lambda_local': lam_local,
        'lambda_econ': lam_econ,
        'lambda_national': lam_nat,
        'lambda_inc': lam_inc,
        'lambda_era': lam_era,
        'inner_rmse': float(inner_rmse),
    },
    'training_fit_diagnostics_not_oos': {
        'rmse': train_rmse,
        'mae': train_mae,
        'direction_accuracy_pct': train_direction,
    },
    'top_tuning_candidates': [
        {
            'inner_rmse': float(z[0]),
            'architecture': z[2],
            'lambda_local': z[3],
            'lambda_econ': z[4],
            'lambda_national': z[5],
            'lambda_inc': z[6],
            'lambda_era': z[7],
        }
        for z in trace[:20]
    ],
    'scope_note': (
        'This artifact freezes the fundamentals fit only. It does not score 2026 races. '
        'The locked 30-day poll blend and selector remain separate downstream layers.'
    ),
}
META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

lines = [
    '# 2026 production fundamentals fit',
    '',
    '## Status',
    '',
    '- Fits the canonical Core V2-R fundamentals source on all eligible historical rows through 2022.',
    '- The source SHA-256 is checked against final/validation/manifest.json before fitting.',
    '- This step freezes coefficients and standardization only; it does not emit 2026 race directions.',
    '',
    '## Canonical feature set',
    '',
]
for feat in features:
    lines.append(f'- {feat}')
lines += [
    '',
    '## Selected fit',
    '',
    f'- architecture: {arch}',
    f'- training rows: {len(rows)}',
    f'- training cycles: {", ".join(map(str, cycles))}',
    f'- lambda_local: {lam_local}',
    f'- lambda_econ: {lam_econ}',
    f'- lambda_national: {lam_nat}',
    f'- lambda_inc: {lam_inc}',
    f'- lambda_era: {lam_era}',
    f'- chronological inner RMSE used for tuning: {inner_rmse:.6f}',
    '',
    'Training-set diagnostics below are descriptive fit checks only, not OOS validation:',
    f'- RMSE: {train_rmse:.6f}',
    f'- MAE: {train_mae:.6f}',
    f'- direction accuracy: {train_direction:.3f}%',
    '',
    '## Outputs',
    '',
    '- data/snapshots/2026_production_fundamentals_coefficients.csv',
    '- data/snapshots/2026_production_fundamentals_standardization.csv',
    '- data/snapshots/2026_production_fundamentals_fit_meta.json',
]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines))
