"""Decision ledger backed by Sibyl Memory.

The memory calls in this file are deliberately small and visible: judges should
be able to see exactly where the agent writes memory and where it depends on
recall before deciding what to do next.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

BLOCKED_STATUSES = {"blocked", "discarded", "empty_market", "closed", "requires_payment"}
KNOWN_RULES = ("no-local-install", "no-self-funding")


def _default_db_path() -> Path:
    return Path.cwd() / ".memory" / "eustaquio.db"


def _load_sibyl_client(db_path: Path):
    try:
        from sibyl_memory_client import MemoryClient
    except ImportError as exc:  # pragma: no cover - exercised in Codespace setup only
        raise RuntimeError(
            "sibyl-memory-client is not installed. Open this repository in a "
            "GitHub Codespace and run: pip install -r requirements.txt"
        ) from exc

    db_path.parent.mkdir(parents=True, exist_ok=True)
    return MemoryClient.local(path=db_path)


def _normalize_entity(category: str, name: str, entity: Any) -> dict[str, Any] | None:
    if entity is None:
        return None
    if isinstance(entity, dict):
        body = entity.get("body", entity)
    else:
        body = getattr(entity, "body", None) or getattr(entity, "data", None) or entity
    return {"category": category, "name": name, "body": body}


@dataclass
class MemoryLedger:
    """Thin wrapper around Sibyl Memory for opportunity decisions."""

    client: Any | None = None
    db_path: Path | None = None

    def __post_init__(self) -> None:
        if self.client is None:
            self.client = _load_sibyl_client(self.db_path or _default_db_path())

    def record_decision(self, category: str, name: str, body: dict[str, Any]) -> None:
        """Write a durable decision entity to Sibyl Memory."""
        self.client.set_entity(category, name, body)

    def recall_decisions(self, candidate_ids: Iterable[str]) -> list[dict[str, Any]]:
        """Read exact entities from Sibyl Memory before acting.

        Sibyl documents `get_entity(kind, name)` as the stable warm-memory read
        API. We intentionally query only known candidate/rule names instead of
        relying on a broad list method that may not exist in the SDK.
        """
        rows: list[dict[str, Any]] = []
        for name in candidate_ids:
            entity = self.client.get_entity("opportunity", name)
            row = _normalize_entity("opportunity", name, entity)
            if row:
                rows.append(row)
        for name in KNOWN_RULES:
            entity = self.client.get_entity("rule", name)
            row = _normalize_entity("rule", name, entity)
            if row:
                rows.append(row)
        return rows

    def search_memory(self, query: str) -> list[dict[str, Any]]:
        """Search Sibyl Memory using the documented FTS helper."""
        return self.client.search_entities(query)

    def next_action(self, candidates: Iterable[dict[str, Any]], use_memory: bool = True) -> dict[str, Any]:
        """Choose the next action, filtering candidates by recalled memory.

        Deletion test: remove the call to ``recall_decisions`` below, or run
        with ``use_memory=False``, and the function loses its protection against
        already-discarded work.
        """
        candidate_list = list(candidates)
        remembered: dict[str, dict[str, Any]] = {}

        if use_memory:
            candidate_ids = [candidate["id"] for candidate in candidate_list]
            for row in self.recall_decisions(candidate_ids):
                body = row.get("body") or {}
                name = row.get("name") or row.get("key") or ""
                remembered[name] = {
                    "category": row.get("category"),
                    "name": name,
                    "status": body.get("status"),
                    "reason": body.get("reason") or body.get("text"),
                    "date": body.get("date"),
                }

        skipped: list[dict[str, Any]] = []
        for candidate in candidate_list:
            prior = remembered.get(candidate["id"])
            if prior and prior.get("status") in BLOCKED_STATUSES:
                skipped.append({"candidate": candidate, "memory": prior})
                continue
            return {
                "recommendation": candidate,
                "used_memory": use_memory,
                "skipped": skipped,
                "why": "Selected the first candidate not blocked by recalled decisions.",
            }

        return {
            "recommendation": None,
            "used_memory": use_memory,
            "skipped": skipped,
            "why": "Every candidate was blocked by recalled memory.",
        }


def default_candidates() -> list[dict[str, Any]]:
    return [
        {"id": "OPIRE-BOUNTIES", "label": "Re-check Opire bounty listings", "value": "possible small bounty"},
        {"id": "AGENTLOT-MARKETPLACE", "label": "List a service on AgentLot", "value": "possible agent marketplace"},
        {"id": "TASKMARKET-LOCAL-CLI", "label": "Submit prepared Taskmarket work locally", "value": "1-2 USDC"},
        {"id": "SIBYL-HACKATHON-2026", "label": "Build Sibyl Memory Ledger", "value": "10,000 USDC prize pool"},
    ]
