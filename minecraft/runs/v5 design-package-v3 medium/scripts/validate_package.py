#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def main():
    cfg=yaml.safe_load((ROOT/"layout.yaml").read_text()); errors=[]
    required=["README.md","design-package.md","proposal-v5.md","layout.yaml","generation-record.yaml"]
    for name in required:
        if not (ROOT/name).exists(): errors.append(f"missing {name}")
    for key,note in cfg["notes"].items():
        code=key[3:]
        for side in ("recto","verso"):
            p=ROOT/f"outputs/notes/EUR{code}_{side}.png"
            if not p.exists(): errors.append(f"missing {p.name}"); continue
            if Image.open(p).size != tuple(note["size"]): errors.append(f"wrong size {p.name}: {Image.open(p).size}")
            for kind in ("scene","ornament"):
                q=ROOT/f"generated/{'scenes' if kind=='scene' else 'ornaments'}/EUR{code}_{side}_{kind}.png"
                if not q.exists(): errors.append(f"missing {q.relative_to(ROOT)}")
        for q in [ROOT/f"generated/badges/EUR{code}_recto_badge.png",ROOT/f"assets/ore_blocks/ore_{note['motif']}_iso.webp"]:
            if not q.exists(): errors.append(f"missing {q.relative_to(ROOT)}")
    for c in ("rectos_contact","versos_contact","series_paired_contact"):
        if not (ROOT/f"outputs/contacts/{c}.png").exists(): errors.append(f"missing contact {c}")
    if errors:
        print("VALIDATION FAILED"); print("\n".join(errors)); sys.exit(1)
    print("VALIDATION PASSED: 12 exact-size notes, 12 scenes, 12 ornaments, 6 badges, 3 contact sheets")

if __name__=="__main__": main()
