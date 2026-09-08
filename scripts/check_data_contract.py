from __future__ import annotations
import argparse, json, sys
from medlake.contracts import validate_event_dict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="data/ci_valid_events.jsonl")
    ap.add_argument("--max-errors", type=int, default=25)
    a = ap.parse_args()
    errors = []
    seen = set()
    with open(a.path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            event = json.loads(line)
            event_errors = validate_event_dict(event)
            if event["event_id"] in seen:
                event_errors.append("duplicate_event_id")
            seen.add(event["event_id"])
            for err in event_errors:
                errors.append((line_no, event.get("event_id"), err))
    if errors:
        [print("ERROR", x) for x in errors[: a.max_errors]]
        sys.exit(1)
    print("Data contract: PASS")


if __name__ == "__main__":
    main()
