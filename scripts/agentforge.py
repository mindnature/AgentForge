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
from runtime.mvp import build_mvp_experiment
from runtime.redteam import evaluate_red_team
from runtime.scoring import evaluate
from runtime.state import advance, load_session, new_session, record_facts, save_session, session_snapshot, set_artifact
from runtime.validation import build_validation_plan


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(prog="agentforge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("start", help="Start a stateful AgentForge session from one rough idea")
    p_start.add_argument("--idea", required=True)
    p_start.add_argument("--session", required=True)
    p_status = sub.add_parser("status", help="Show current stage and next action")
    p_status.add_argument("--session", required=True)
    p_answer = sub.add_parser("record-facts", help="Record user/Agent inferred discovery facts")
    p_answer.add_argument("--session", required=True)
    p_answer.add_argument("--input", required=True)
    p_artifact = sub.add_parser("set-artifact", help="Persist one stage artifact")
    p_artifact.add_argument("--session", required=True)
    p_artifact.add_argument("--name", required=True)
    p_artifact.add_argument("--input", required=True)
    p_advance = sub.add_parser("advance", help="Advance only when the current stage gate is satisfied")
    p_advance.add_argument("--session", required=True)
    p_score = sub.add_parser("score", help="Score a pain point / AI-fit payload")
    p_score.add_argument("--input", required=True)
    p_assess = sub.add_parser("assess", help="Run structured assessment")
    p_assess.add_argument("--input", required=True)
    p_assess.add_argument("--output")
    p_red = sub.add_parser("red-team", help="Run the architecture downgrade gate")
    p_red.add_argument("--input", required=True)
    p_val = sub.add_parser("validation-plan", help="Validate/build a structured Validator plan")
    p_val.add_argument("--input", required=True)
    p_mvp = sub.add_parser("mvp", help="Validate/build a dangerous-assumption MVP experiment")
    p_mvp.add_argument("--input", required=True)
    p_spec = sub.add_parser("build-spec", help="Build an expanded One-page Spec")
    p_spec.add_argument("--input", required=True)
    p_spec.add_argument("--output")

    args = parser.parse_args()
    try:
        if args.cmd == "start":
            state = new_session(args.idea)
            path = save_session(state, Path(args.session))
            dump({"session": str(path.resolve()), **session_snapshot(state)})
        elif args.cmd == "status":
            dump(session_snapshot(load_session(Path(args.session))))
        elif args.cmd == "record-facts":
            path = Path(args.session)
            state = load_session(path)
            record_facts(state, load_json(args.input))
            save_session(state, path)
            dump(session_snapshot(state))
        elif args.cmd == "set-artifact":
            path = Path(args.session)
            state = load_session(path)
            set_artifact(state, args.name, load_json(args.input))
            save_session(state, path)
            dump(session_snapshot(state))
        elif args.cmd == "advance":
            path = Path(args.session)
            state = load_session(path)
            advance(state)
            save_session(state, path)
            dump(session_snapshot(state))
        elif args.cmd == "score":
            dump(evaluate(load_json(args.input)))
        elif args.cmd == "assess":
            result = project_assessment(load_json(args.input))
            print(write_json(result, Path(args.output)).resolve()) if args.output else dump(result)
        elif args.cmd == "red-team":
            dump(evaluate_red_team(load_json(args.input)))
        elif args.cmd == "validation-plan":
            dump(build_validation_plan(load_json(args.input)["checks"]))
        elif args.cmd == "mvp":
            dump(build_mvp_experiment(load_json(args.input)))
        elif args.cmd == "build-spec":
            result = build_one_page_spec(load_json(args.input))
            print(write_json(result, Path(args.output)).resolve()) if args.output else dump(result)
        return 0
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
