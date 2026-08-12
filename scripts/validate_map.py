#!/usr/bin/env python3
"""Validate constellation nodes and edges. Born to run."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("validate_map: need pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    nodes_doc = yaml.safe_load((ROOT / "registry" / "nodes.yml").read_text())
    edges_doc = yaml.safe_load((ROOT / "registry" / "edges.yml").read_text())
    nodes = nodes_doc.get("nodes", [])
    edges = edges_doc.get("edges", [])
    ids = {n["id"] for n in nodes}
    if len(ids) != len(nodes):
        print("validate_map: fail — duplicate node ids", file=sys.stderr)
        return 1
    for n in nodes:
        for k in ("id", "name", "kind", "visibility", "role"):
            if k not in n:
                print(f"validate_map: fail — node missing {k}", file=sys.stderr)
                return 1
        if n["visibility"] == "public" and not n.get("url"):
            print(f"validate_map: fail — public node {n['id']} missing url", file=sys.stderr)
            return 1
        if n["visibility"] == "private" and n.get("url"):
            print(f"validate_map: warn — private node {n['id']} has url (check truth rule)")
    for e in edges:
        if e["from"] not in ids or e["to"] not in ids:
            print(f"validate_map: fail — edge {e} references unknown node", file=sys.stderr)
            return 1
    print(f"validate_map: ok ({len(nodes)} nodes, {len(edges)} edges)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
