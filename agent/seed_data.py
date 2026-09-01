"""Curated, anonymized seed memory from the real Eustaquio project."""

DECISIONS = [
    {
        "category": "opportunity",
        "name": "OPIRE-BOUNTIES",
        "body": {
            "status": "discarded",
            "date": "2026-08-30",
            "reason": "Third-party bounty index was not synced with GitHub reality: sampled issues were closed or repos missing.",
            "evidence": "Four low-competition candidates checked against GitHub; all failed basic freshness checks.",
        },
    },
    {
        "category": "opportunity",
        "name": "AGENTLOT-MARKETPLACE",
        "body": {
            "status": "empty_market",
            "date": "2026-08-31",
            "reason": "Marketplace was technically alive but had zero requests, zero listings, zero orders and a broken paid catalog.",
            "evidence": "Public API stats returned 12 agents, 0 listings, 0 orders, 0 open requests.",
        },
    },
    {
        "category": "opportunity",
        "name": "TASKMARKET-LOCAL-CLI",
        "body": {
            "status": "blocked",
            "date": "2026-08-31",
            "reason": "Submitting prepared work requires CLI install or wallet signing, both blocked on a company laptop without a safer sandbox.",
            "evidence": "Three submissions are prepared but not signed: TSK-ZYJ9HSS8, TSK-E58AN8KV, TSK-JXKSQ4EB.",
        },
    },
    {
        "category": "opportunity",
        "name": "SIBYL-HACKATHON-2026",
        "body": {
            "status": "active_candidate",
            "date": "2026-08-31",
            "reason": "Best current path: prize pool, agent-memory fit, no local install if built in Codespaces.",
            "evidence": "Team registered as Eustaquio Memory Ledger; build should happen in a cloud sandbox during Sep 1-10.",
        },
    },
    {
        "category": "rule",
        "name": "no-local-install",
        "body": {
            "status": "active",
            "date": "2026-08-30",
            "text": "Do not install or execute untrusted downloaded software on the company laptop. Use an online sandbox for external dependencies.",
            "source": "AGENTS.md / project operating rule",
        },
    },
    {
        "category": "rule",
        "name": "no-self-funding",
        "body": {
            "status": "active",
            "date": "2026-08-30",
            "text": "Do not fund a wallet, pay an entry fee, or sign a payment just to unlock a possible reward.",
            "source": "shared project rules",
        },
    },
]
