from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.ledger import MemoryLedger, default_candidates
from agent.seed_data import DECISIONS


def _ledger(args) -> MemoryLedger:
    return MemoryLedger(db_path=Path(args.db))


def cmd_seed(args) -> int:
    ledger = _ledger(args)
    for item in DECISIONS:
        ledger.record_decision(item["category"], item["name"], item["body"])
        print(f"wrote {item['category']}/{item['name']} ({item['body'].get('status')})")
    return 0


def cmd_next_action(args) -> int:
    ledger = _ledger(args)
    result = ledger.next_action(default_candidates(), use_memory=not args.no_memory)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_show_memory(args) -> int:
    ledger = _ledger(args)
    rows = ledger.recall_decisions([c["id"] for c in default_candidates()])
    print(json.dumps(rows, indent=2, ensure_ascii=False))
    return 0


def cmd_search(args) -> int:
    ledger = _ledger(args)
    print(json.dumps(ledger.search_memory(args.query), indent=2, ensure_ascii=False))
    return 0


def cmd_onchain_check(args) -> int:
    from agent.onchain import base_snapshot

    print(json.dumps(base_snapshot(), indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Eustaquio Memory Ledger demo CLI")
    parser.add_argument("--db", default=".memory/eustaquio.db", help="Path to Sibyl Memory SQLite database")
    sub = parser.add_subparsers(dest="command", required=True)

    seed = sub.add_parser("seed", help="Write curated project decisions into Sibyl Memory")
    seed.set_defaults(func=cmd_seed)

    next_action = sub.add_parser("next-action", help="Recommend next action using recalled memory")
    next_action.add_argument("--no-memory", action="store_true", help="Deletion-test mode: choose without memory filtering")
    next_action.set_defaults(func=cmd_next_action)

    show = sub.add_parser("show-memory", help="Print stored opportunity/rule entities")
    show.set_defaults(func=cmd_show_memory)

    search = sub.add_parser("search", help="Search Sibyl Memory")
    search.add_argument("query")
    search.set_defaults(func=cmd_search)

    onchain = sub.add_parser("onchain-check", help="Read project wallet balances from Base without signing")
    onchain.set_defaults(func=cmd_onchain_check)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

