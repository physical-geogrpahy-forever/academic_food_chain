from __future__ import annotations

import csv
from pathlib import Path

TECH_MASTER = Path("tech_reference/MASTER_TECHNOLOGY_UNLOCKS_109_V2.csv")
CIVIC_MASTER = Path("civics_reference/MASTER_CIVIC_UNLOCKS_72_V3.csv")

TECH_PATCHES = {
    "Writing": ["Scriptorium with Written Culture"],
    "Irrigation": ["Garden with Civil Service"],
    "Printing": ["Newspaper Office with Public Sphere"],
    "Cartography": ["Navigation School with Exploration"],
    "Mass Production": ["Shopping Mall with Capitalism"],
    "Rocketry": ["Space Launch Center with Space Race"],
}

CIVIC_PATCHES = {
    "Foreign Trade": ["Caravansary with Horseback Riding"],
    "Code of Laws": ["Mint with Currency"],
    "Guilds": ["Cloth Mill with Manufacturing"],
    "Military Training": [
        "Armory with Military Engineering",
        "Arsenal with Metallurgy",
        "Military Academy with Military Science",
    ],
    "Patronage": [
        "Opera House with Acoustics",
        "Musicians' Guild with Acoustics",
    ],
    "Mercantilism": ["Customs Office with Economics"],
    "Sovereignty": ["Telegraph Office with Telegraph"],
    "Civil Engineering": [
        "Power Plant with Electricity",
        "Nuclear Power Plant with Nuclear Fission",
    ],
    "Urbanization": [
        "Hospital with Biology",
        "Medical Lab with Penicillin",
    ],
    "Mass Media": [
        "Airport with Radar",
        "Film Studio with Radio",
    ],
    "Mobilization": ["Radar Station with Radar"],
    "Environmentalism": [
        "Recycling Center with Ecology",
        "Solar Plant with Ecology",
    ],
    "Global Warming Mitigation": [
        "Grid Battery Storage with Advanced Power Cells",
    ],
}


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_semicolon_items(existing: str, additions: list[str]) -> str:
    items = [x.strip() for x in (existing or "").split(";") if x.strip()]
    for addition in additions:
        if addition not in items:
            items.append(addition)
    return "; ".join(items)


def patch_csv(path: Path, key_field: str, value_field: str, patches: dict[str, list[str]]):
    rows, fieldnames = read_csv(path)
    if key_field not in fieldnames or value_field not in fieldnames:
        raise ValueError(f"{path}: expected fields {key_field}, {value_field}")

    by_key = {r[key_field]: r for r in rows}
    missing = sorted(set(patches) - set(by_key))
    if missing:
        raise ValueError(f"{path}: missing keys: {missing}")

    changed = False
    source_patches: dict[Path, dict[str, list[str]]] = {}
    for key, additions in patches.items():
        row = by_key[key]
        new_value = append_semicolon_items(row.get(value_field, ""), additions)
        if new_value != row.get(value_field, ""):
            row[value_field] = new_value
            changed = True

        source = row.get("SUMMARY_SOURCE", "").strip()
        if source:
            source_patches.setdefault(Path(source), {})[key] = additions

    if changed:
        write_csv(path, rows, fieldnames)

    return changed, source_patches


def patch_source_files(source_patches, key_field, value_field):
    changed_files = []
    for path, patches in sorted(source_patches.items(), key=lambda x: str(x[0])):
        if not path.exists():
            raise FileNotFoundError(f"summary source not found: {path}")
        changed, _ = patch_csv(path, key_field, value_field, patches)
        if changed:
            changed_files.append(path)
    return changed_files


def main():
    changed_files = []

    tech_changed, tech_sources = patch_csv(
        TECH_MASTER, "TECH_EN", "CITY_BUILDINGS", TECH_PATCHES
    )
    if tech_changed:
        changed_files.append(TECH_MASTER)
    changed_files.extend(
        patch_source_files(tech_sources, "TECH_EN", "CITY_BUILDINGS")
    )

    civic_changed, civic_sources = patch_csv(
        CIVIC_MASTER, "CIVIC_EN", "FINAL_UNLOCKS_SYSTEMS", CIVIC_PATCHES
    )
    if civic_changed:
        changed_files.append(CIVIC_MASTER)
    changed_files.extend(
        patch_source_files(civic_sources, "CIVIC_EN", "FINAL_UNLOCKS_SYSTEMS")
    )

    unique = []
    seen = set()
    for path in changed_files:
        text = str(path)
        if text not in seen:
            seen.add(text)
            unique.append(text)

    print(f"BUILDING_GATE_MASTER_REPAIR: PASS changed_files={len(unique)}")
    for path in unique:
        print(path)


if __name__ == "__main__":
    main()
