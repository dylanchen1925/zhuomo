#!/usr/bin/env python3
"""Read/write ~/.zhuomo/config.json (paths only, no corpus)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".zhuomo" / "config.json"
DEFAULT = {"version": 1, "vault_path": "", "raw_path": "", "wiki_subdir": "wiki/"}


def load() -> dict:
    if not CONFIG_PATH.is_file():
        return dict(DEFAULT)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_show = sub.add_parser("show", help="Print config path and JSON")
    p_show.set_defaults(cmd="show")

    p_set = sub.add_parser("set", help="Set vault_path and raw_path")
    p_set.add_argument("--vault", required=True)
    p_set.add_argument("--raw", required=True)
    p_set.add_argument("--wiki-subdir", default="wiki/")

    args = ap.parse_args()
    if args.cmd == "show":
        print(f"config: {CONFIG_PATH}")
        print(json.dumps(load(), indent=2))
        return 0
    if args.cmd == "set":
        cfg = load()
        cfg["vault_path"] = args.vault.rstrip("/") + "/"
        cfg["raw_path"] = args.raw.rstrip("/") + "/"
        cfg["wiki_subdir"] = args.wiki_subdir
        save(cfg)
        print(f"Wrote {CONFIG_PATH}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
