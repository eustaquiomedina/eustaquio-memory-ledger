from agent.ledger import MemoryLedger, default_candidates
from agent.seed_data import DECISIONS


class FakeMemory:
    def __init__(self):
        self.rows = {}

    def set_entity(self, category, name, body):
        self.rows[(category, name)] = {"category": category, "name": name, "body": body}

    def get_entity(self, category, name):
        return self.rows.get((category, name))

    def search_entities(self, query):
        q = query.lower()
        return [row for row in self.rows.values() if q in str(row).lower()]


def seeded_ledger():
    memory = FakeMemory()
    ledger = MemoryLedger(client=memory)
    for item in DECISIONS:
        ledger.record_decision(item["category"], item["name"], item["body"])
    return ledger


def test_memory_filters_known_dead_ends():
    result = seeded_ledger().next_action(default_candidates())
    assert result["recommendation"]["id"] == "SIBYL-HACKATHON-2026"
    assert [x["candidate"]["id"] for x in result["skipped"]] == [
        "OPIRE-BOUNTIES",
        "AGENTLOT-MARKETPLACE",
        "TASKMARKET-LOCAL-CLI",
    ]


def test_without_memory_repeats_the_old_mistake():
    result = seeded_ledger().next_action(default_candidates(), use_memory=False)
    assert result["recommendation"]["id"] == "OPIRE-BOUNTIES"
    assert result["skipped"] == []
