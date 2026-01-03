import json
import shutil
from pathlib import Path

def cleanup_tmp(tmp_dir: Path):
    if tmp_dir.exists() and tmp_dir.is_dir():
        shutil.rmtree(tmp_dir)
from pathlib import Path

def dump_raw(rows: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)

def load_raw(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
    
def cleanup_tmp(tmp_dir: Path):
    if tmp_dir.exists() and tmp_dir.is_dir():
        shutil.rmtree(tmp_dir)
