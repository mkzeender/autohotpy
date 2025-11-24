from __future__ import annotations
import ast
from pathlib import Path
import pandas as pd

def names(fp: Path) -> dict[str, Path]:
    code =compile(fp.read_text(), fp.name, mode='exec',flags=annotations.compiler_flag)
    mod = {}
    exec(code, mod)
    return dict.fromkeys(mod, fp)

data = pd.read_csv("all.txt", sep="` ", dtype=str, engine="python")
print(data.keys())
data["name"] = data["name"].str.strip()
data["doc"] = data["doc"].str.strip()
data[data["doc"] == ""] = pd.NA
data["doc"] = data["doc"].bfill()

root = Path("autohotpy")

definitions = {}
for class_file in (root / "static_typing/classes").glob("*.pyi"):
