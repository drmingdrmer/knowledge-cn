# Raft and Paxos knowledge extraction plan

Source article: [重新理解分布式共识：Raft 与 Paxos 的共同结构](/Users/drdrxp/xp/vcs/github.com/openacid/openacid.github.io/_draft/raft-intuitive/2026-08-08-raft-intuitive-cn.md).

This proposal contains **23 cards: 19 new cards and four existing cards to expand**.

Each card should state one claim, its assumptions, and a short proof. In the table, `6, 10 → 11` means card 11 uses both cards 6 and 10. Definitions and protocol rules enter the graph as explicit premises.

## Proposed cards and their proof premises

| ID | Knowledge card and its main claim | Direct proof premises |
|---|---|---|
| 1 | **Deterministic replay.** The same initial state and command sequence produce the same state and outputs. | Deterministic state-machine model |
| 2 | **Prefix-compatible histories.** Replicas may execute different-length prefixes while agreeing throughout their shared execution. | 1 |
| 3 | **Immutable history trees.** Each globally unique node ID identifies one immutable parent and command. | Model assumptions: `cm1`–`cm3` |
| 4 | **Monotone union.** Compatible history trees merge by union without overwriting nodes. Concurrent branches remain represented. | 3 |
| 5 | **Majority intersection — existing.** Two majorities of the same replica set share a member. | Counting argument |
| 6 | **Quorum intersection — existing.** Every allowed read quorum must intersect every allowed write quorum. | Explicit quorum assumption; 5 proves the majority case |
| 7 | **Durable evidence.** Acknowledged history, accepted proposals, and promises survive the crashes allowed by the model. | Crash/recovery and storage assumptions |
| 8 | **Quorum visibility.** After a completed write, every later completed quorum read discovers its immutable history. | 4, 6, 7 |
| 9 | **Writer epochs and history ancestry are different orders.** A higher ballot or term identifies a newer attempt; ancestry identifies which commands it preserves. | Definitions of epoch order and history ancestry |
| 10 | **Acceptor promises — existing.** Recording a durable promise before returning accepted state prevents later acceptance of lower ballots. | 7, 9; promise-and-read protocol rule |
| 11 | **The fenced-quorum witness.** Any lower ballot that can still become chosen has a prepare-quorum member that accepted it before promising. | 6, 10 |
| 12 | **Highest-accepted-value adoption.** Adopting the highest accepted ballot’s value preserves any previously chosen value. | 9, 11; adoption rule; induction over ballots |
| 13 | **Single-decree Paxos — existing.** All chosen proposals contain the same value. | 12; unique ballots and quorum acceptance |
| 14 | **Raft Election Safety.** Majority intersection and one durable vote per term permit at most one leader per term. | 5, 7; voting rule |
| 15 | **Raft Log Matching.** Matching `(term, index)` entries imply matching prefixes. | 14; leader append rules and AppendEntries consistency checks |
| 16 | **Raft election freshness.** Granted votes certify that the candidate is at least as up-to-date as every granting voter. | Voting rule comparing `(lastLogTerm, lastLogIndex)` |
| 17 | **Raft’s current-term commit rule.** A leader counts replicas directly only for entries from its current term. | Protocol rule; an old-term counterexample explains its necessity |
| 18 | **Raft Leader Completeness.** Every later leader contains all committed entries. | 6, 10, 14–17 |
| 19 | **Replicated-state-machine safety.** Replicas agree on commands at each applied index and on the resulting execution. | 1, 2, 15, 18; apply-only-committed rule |
| 20 | **Logical history versus physical storage.** Replacing tentative data can preserve the chosen history. | 13 for Paxos; 15, 18 for Raft |
| 21 | **Safe reads.** A read needs commitment evidence and, for leader reads, confirmation of current authority. | 8, 13, 19; read protocol |
| 22 | **Safety and progress require different arguments.** Repeated higher promises can prevent every writer from finishing. | 10, 11; concurrent execution counterexample |
| 23 | **Safe membership changes.** Joint quorums connect configurations while committed history carries forward. | 6, 18; configuration-transition rules |

## Central proof paths

```text
Immutable nodes → Monotone union ──────────────┐
Quorum intersection + Durable storage ────────┴→ Quorum visibility

Quorum intersection + Durable promises
    → Fenced-quorum witness
    → Highest-accepted-value adoption
    → Paxos agreement

Majority intersection + One vote per term
    → Election Safety
    → Log Matching ───────────────────────────┐
Freshness voting + Current-term commit rule ─┴→ Leader Completeness
    → Replicated-state-machine safety
```

The table supplies the additional premises omitted from this compact diagram. The protocol-specific steps follow [Paxos Made Simple, §2](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf) and the [Raft paper, §§5–8](https://raft.github.io/raft.pdf).

## Proposed corrections before extracting the cards

- **Call `cm1`–`cm4` a grow-only replicated history model.** Those constraints preserve branches; agreement requires additional rules.
- **Replace `cs1-global-max` with preservation of chosen history.** Paxos can choose a proposal while a higher ballot exists elsewhere. Ballot order alone does not prove preservation. [Paxos, §2.2](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- **Make fence equality consistent.** A promise must allow its own ballot’s accept requests. [Paxos, §2.2](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- **Strengthen the read rule.** Selecting the largest observed leaf can expose tentative data. Raft reads require commitment knowledge and current authority. [Raft, §8](https://raft.github.io/raft.pdf)
