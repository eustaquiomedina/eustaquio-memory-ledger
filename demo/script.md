# Demo script - Eustaquio Memory Ledger

Target duration: 2-5 minutes.

1. Problem: an agent evaluating bounties, grants and marketplaces builds real judgment over days. A fresh session forgets that judgment and repeats dead work.
2. Session one: run `python main.py seed`. Show several decisions written to Sibyl Memory with dates.
3. Fresh session: stop/reopen the Codespace or terminal. Show `git log -1` or `date` so the session boundary is visible.
4. Recall: run `python main.py next-action`. The first three candidates are skipped because memory says they were discarded/blocked; Sibyl Hackathon is selected.
5. Deletion test: run `python main.py next-action --no-memory`. It incorrectly recommends Opire again. This proves memory is load-bearing.
6. Base read: run `python main.py onchain-check`. It reads Base mainnet balances through public RPC without signing or spending.
7. Close on the public repo and README, pointing to `agent/ledger.py`.
