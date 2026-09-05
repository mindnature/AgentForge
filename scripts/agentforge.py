#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.core import build_one_page_spec, project_assessment, write_json
from runtime.scoring import evaluate


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(prog="agentforge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score", help="Score a pain point / AI-fit payload")
    p_score.add_argument("--input", required=True)

    p_assess = sub.add_parser("assess", help="Run full structured assessment")
    p_assess.add_argument("--input", required=True)
    p_assess.add_argument("--output")

    p_spec = sub.add_parser("build-spec", help="Build a One-page Spec from structured JSON")
    p_spec.add_argument("--input", required=True)
    p_spec.add_argument("--output")

    args = parser.parse_args()
    try:
        if args.cmd == "score":
            result = evaluate(load_json(args.input))
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.cmd == "assess":
            result = project_assessment(load_json(args.input))
            if args.output:
                print(write_json(result, Path(args.output)).resolve())
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.cmd == "build-spec":
            result = build_one_page_spec(load_json(args.input))
            if args.output:
                print(write_json(result, Path(args.output)).resolve())
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
