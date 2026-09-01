# Eustaquio Memory Ledger

An autonomous work agent that remembers what it already decided, so it stops repeating discarded work every time it starts a fresh session.

## The problem

Agents evaluating opportunities such as bounties, grants and hackathons build real judgment over days: a platform has stale data, a grant requires identity up front, a local install is unsafe, or a wallet must not be funded. Without persistent memory, every fresh session starts from zero and risks repeating the same checks.

## What it does

Eustaquio Memory Ledger stores operational decisions as Sibyl Memory entities. When asked what to do next, it reads memory first, filters out anything already blocked or discarded, and returns a recommendation with the remembered reason.

## Where memory is load-bearing

Core logic lives in `agent/ledger.py`:

- `record_decision(...)` writes a durable Sibyl entity with `client.set_entity(...)`.
- `recall_decisions(...)` reads known opportunity and rule entities with the documented `client.get_entity(...)` API.
- `next_action(...)` calls `recall_decisions()` before choosing a candidate. Remove that call, or run `python main.py next-action --no-memory`, and the agent goes back to recommending a previously discarded opportunity.

That is the deletion test: memory is not decorative; it changes the chosen action.

## Run in a cloud sandbox

This project is designed to run in GitHub Codespaces so no downloaded package has to be installed on a company laptop.

```bash
pip install -r requirements.txt
python main.py seed
python main.py next-action
python main.py next-action --no-memory
python main.py onchain-check
```

## Demo behavior

With memory enabled, the agent skips stale/blocked routes and recommends the Sibyl Hackathon. With memory disabled, it repeats the old Opire bounty mistake. The visible contrast is intentional and judge-friendly.

## Partner stack

Base is used through a read-only public RPC call in `agent/onchain.py`. The demo reads ETH and USDC balances for the project wallet on Base mainnet without signing, sending a transaction, or spending funds.

Virtuals is not claimed in this build.

## Prior work declaration

The project history, Base wallet and unrelated x402 fiscal API existed before the Sibyl build window. They are used only as context and as a read-only Base address. The Sibyl Memory decision layer in `agent/` is the hackathon build and should be committed publicly during the official Sep 1-10, 2026 build window.

## License

MIT.

