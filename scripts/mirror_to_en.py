#!/usr/bin/env python3
"""Mirror FR docs to EN scaffolds using suffix .en.md.

Keeps FR immutable: creates docs/**/*.en.md sibling for each FR md file if missing.
Idempotent: does not overwrite existing .en.md.
Usage:
  python scripts/mirror_to_en.py              # all
  python scripts/mirror_to_en.py --only index # only index.md
  python scripts/mirror_to_en.py --section docker
"""
import argparse
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def should_skip(fr: pathlib.Path) -> bool:
    # skip already EN files, superpowers specs/plans (not part of nav)
    if ".en.md" in fr.name:
        return True
    if "superpowers" in fr.parts:
        return True
    return False


def mirror(fr: pathlib.Path):
    en = fr.parent / (fr.stem + ".en.md")
    if not en.exists():
        shutil.copy2(fr, en)
        print(f"mirrored {fr.relative_to(ROOT)} -> {en.relative_to(ROOT)}")
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="only mirror matching substring")
    parser.add_argument("--section", help="mirror only docs/<section>/")
    args = parser.parse_args()

    count = 0
    for fr in sorted(DOCS.rglob("*.md")):
        if should_skip(fr):
            continue
        if args.only and args.only not in str(fr):
            continue
        if args.section and f"docs/{args.section}/" not in str(fr):
            continue
        if mirror(fr):
            count += 1
    print(f"Done: {count} files mirrored.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
