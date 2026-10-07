#!/usr/bin/env python3
"""
Check code-block parity between FR and EN files.

Rules (from TRANSLATION_GUIDELINES.md):
- yaml|bash|sh|dockerfile|hcl|terraform|python|console fences must be byte-identical FR<->EN
- mermaid fences: syntax preserved, human labels may be translated — compare with labels masked
- inline code/file paths/CLI flags covered indirectly via fences; paragraph text ignored.

Exit 1 on mismatch with file:line report, 0 on success.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

FENCE_RE = re.compile(r"```(\w+)?[^\n]*\n(.*?)```", re.DOTALL)
# mermaid label masking: replace [.*?] and (…) labels and quoted text?
MERMAID_LABEL_RE = re.compile(r"\[.*?\]|\(.*?\)|\".*?\"|'.*?'")


def extract_fences(text: str):
    return [(m.group(1) or "", m.group(2)) for m in FENCE_RE.finditer(text)]


def normalize_mermaid(content: str) -> str:
    # Mask human labels but keep graph syntax: graph LR, -->, ---, subgraph, end, :::
    # Replace bracket/paren/quoted labels with placeholders
    return MERMAID_LABEL_RE.sub("[LABEL]", content)


def fences_equal(fr_fences, en_fences, fr_path: pathlib.Path) -> list[str]:
    errors = []
    if len(fr_fences) != len(en_fences):
        errors.append(
            f"{fr_path}: fence count mismatch FR={len(fr_fences)} EN={len(en_fences)}"
        )
        # still compare up to min
    for idx, ((fr_lang, fr_body), (en_lang, en_body)) in enumerate(
        zip(fr_fences, en_fences)
    ):
        fr_lang = (fr_lang or "").strip().lower()
        en_lang = (en_lang or "").strip().lower()
        # language tag should match
        if fr_lang != en_lang:
            errors.append(
                f"{fr_path}: fence #{idx} language mismatch FR='{fr_lang}' EN='{en_lang}'"
            )
        # content comparison
        if fr_lang == "mermaid":
            if normalize_mermaid(fr_body.strip()) != normalize_mermaid(en_body.strip()):
                errors.append(f"{fr_path}: fence #{idx} mermaid structure mismatch")
        else:
            if fr_body.strip() != en_body.strip():
                # show diff snippet
                errors.append(f"{fr_path}: fence #{idx} ({fr_lang}) content diverged")
                # optional: print first differing line
    # extra fences in longer file
    if len(fr_fences) != len(en_fences):
        longer = fr_fences if len(fr_fences) > len(en_fences) else en_fences
        # already reported
        pass
    return errors


def find_pairs():
    pairs = []
    for fr in sorted(DOCS.rglob("*.md")):
        if ".en.md" in fr.name:
            continue
        if "superpowers" in fr.parts:
            continue
        en = fr.parent / (fr.stem + ".en.md")
        if en.exists():
            pairs.append((fr, en))
    return pairs


def main():
    errors = []
    pairs = find_pairs()
    if not pairs:
        print("No EN pairs found — run mirror_to_en.py first.")
        return 0
    for fr, en in pairs:
        fr_fences = extract_fences(fr.read_text(encoding="utf-8"))
        en_fences = extract_fences(en.read_text(encoding="utf-8"))
        errs = fences_equal(fr_fences, en_fences, fr)
        errors.extend(errs)
    if errors:
        print("Code-block parity FAILED:")
        for e in errors:
            print("  -", e)
        print("\nHint: Translate prose only. Keep yaml/bash/hcl fences byte-identical. Mermaid labels may differ but syntax must match.")
        return 1
    print(f"Parity OK: checked {len(pairs)} pairs, {sum(len(extract_fences(p[0].read_text())) for p in pairs)} fences.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
