# Raft and Paxos knowledge extraction plan

Source article: [重新理解分布式共识：Raft 与 Paxos 的共同结构](/Users/drdrxp/xp/vcs/github.com/openacid/openacid.github.io/_draft/raft-intuitive/2026-08-08-raft-intuitive-cn.md).

This plan contains **30 cards: 23 Raft and Paxos cards and seven DAG execution cards**. The Chinese canvas contains **15 completed cards: 1–8 and 24–30**. Cards 9–23 remain to be created. Linked titles below point to completed Chinese cards.

Each card should state one claim, its assumptions, and a short proof. In the table, `6, 10 → 11` means card 11 uses both cards 6 and 10. Definitions and protocol rules enter the graph as explicit premises.

## Raft and Paxos cards and their proof premises

| ID | Knowledge card and its main claim | Direct proof premises |
|---|---|---|
| 1 | **[Deterministic State Machines](../notes/distributed-consensus/deterministic-state-machine.md).** The same initial state and command sequence produce the same state and outputs. | Deterministic state-machine model |
| 2 | **[Prefix-compatible histories](../notes/distributed-consensus/prefix-compatible-histories.md).** Replicas may execute different-length prefixes while agreeing throughout their shared execution. | 1 |
| 3 | **[Immutable history trees](../notes/distributed-consensus/immutable-history-trees.md).** Each globally unique node ID identifies one immutable parent and command. | Model assumptions: `cm1`–`cm3` |
| 4 | **[Monotone union](../notes/distributed-consensus/monotone-union.md).** Compatible history trees merge by union without overwriting nodes. Concurrent branches remain represented. | 3 |
| 5 | **[Majority intersection](../notes/distributed-consensus/majority.md).** Two majorities of the same replica set share a member. | Counting argument |
| 6 | **[Quorum intersection](../notes/distributed-consensus/quorum-intersection.md).** Every allowed read quorum must intersect every allowed write quorum. | Explicit quorum assumption; 5 proves the majority case |
| 7 | **[Durable evidence](../notes/distributed-consensus/durable-evidence.md).** Acknowledged history, accepted proposals, and promises survive the crashes allowed by the model. | Crash/recovery and storage assumptions; evidence still required by the protocol |
| 8 | **[Quorum visibility](../notes/distributed-consensus/quorum-visibility.md).** After a completed write, every later completed quorum read discovers its immutable history. | 4, 6, 7; write-acknowledgement and fresh full-history read rules |
| 9 | **Writer epochs and history ancestry are different orders.** A higher ballot or term identifies a newer attempt; ancestry identifies which commands it preserves. | Definitions of epoch order and history ancestry |
| 10 | **Acceptor promises.** Recording a durable promise before returning accepted state prevents later acceptance of lower ballots. | 7, 9; promise-and-read protocol rule |
| 11 | **The fenced-quorum witness.** Any lower ballot that can still become chosen has a prepare-quorum member that accepted it before promising. | 6, 10 |
| 12 | **Highest-accepted-value adoption.** Adopting the highest accepted ballot’s value preserves any previously chosen value. | 9, 11; adoption rule; induction over ballots |
| 13 | **Single-decree Paxos.** All chosen proposals contain the same value. | 12; unique ballots and quorum acceptance |
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
Deterministic state machine → Prefix-compatible execution

Majority intersection → Quorum intersection (majority case)
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

## 已创建的 DAG 执行卡片与证明关系

中文 [Canvas](../canvases/distributed-consensus.canvas) 已包含[确定性状态机](../notes/distributed-consensus/deterministic-state-machine.md)及以下七张卡片。Canvas 中的箭头从证明前提指向使用前提的结论；卡片讨论的命令 DAG 则用箭头表示命令执行的先后约束。

| ID | 已创建的知识卡片及主要结论 | 直接证明前提 |
|---|---|---|
| 24 | [拓扑序与线性扩张](../notes/distributed-consensus/topological-order-and-linear-extension.md)：有限 DAG 定义偏序，拓扑序是保留该偏序的全序。 | 有限 DAG 模型与可达关系定义 |
| 25 | [命令可交换性](../notes/distributed-consensus/command-commutativity.md)：交换两条命令保持最终状态；保持逐命令返回值需要更强的语义。 | 确定且有定义的命令转移模型；可交换性定义 |
| 26 | [依赖完备性](../notes/distributed-consensus/conflict-coverage.md)：每对不可交换命令都由依赖路径排序。 | 系统设计约束，需由依赖生成规则保证 |
| 27 | [拓扑序的相邻交换引理](../notes/distributed-consensus/adjacent-swap-lemma.md)：任意两种拓扑序可通过交换相邻不可比节点互达。 | 24 |
| 28 | [拓扑序无关性](../notes/distributed-consensus/topological-order-independence.md)：相同初态与依赖完备的有限 DAG，在任意合法顺序下得到相同终态。 | 1、25、26、27；每个命令实例恰好执行一次 |
| 29 | [依赖闭合集](../notes/distributed-consensus/dependency-closed-execution.md)：合法执行的已执行集合包含每个节点的全部祖先。 | 24；执行节点前先执行全部直接前驱 |
| 30 | [相同已执行集合的状态唯一性](../notes/distributed-consensus/state-determined-by-executed-set.md)：相同初态、命令 DAG 和有限依赖闭合集确定唯一状态。 | 28、29 |

```text
24 拓扑序与线性扩张 → 27 相邻交换引理 ─┐
1  确定性状态机 ─────────────────────┤
25 命令可交换性 ─────────────────────┼→ 28 拓扑序无关性 ─┐
26 依赖完备性（系统约束）─────────────┘                  ├→ 30 相同已执行集合的状态唯一性
24 拓扑序与线性扩张 → 29 依赖闭合集 ────────────────────┘
```

执行分支固定相同初态、命令内容与确定性转移规则，并要求每个命令实例恰好执行一次。依赖完备性按选定的结果语义判定冲突：若结论覆盖客户端返回值，就按命令标识比较各次返回值，并使用保持这些返回值的可交换性。依赖完备性是拓扑序无关性的充分条件。

持续增长的 DAG 日志还需要协议保证命令与依赖在应用前确定，并保持已执行节点的祖先集合稳定。原计划中的提案历史树与本节的命令依赖 DAG 属于不同模型；共识协议需要另行证明副本对命令与依赖达成一致。

## Proposed corrections before extracting the cards

- **Call `cm1`–`cm4` a grow-only replicated history model.** Those constraints preserve branches; agreement requires additional rules.
- **Replace `cs1-global-max` with preservation of chosen history.** Paxos can choose a proposal while a higher ballot exists elsewhere. Ballot order alone does not prove preservation. [Paxos, §2.2](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- **Make fence equality consistent.** A promise must allow its own ballot’s accept requests. [Paxos, §2.2](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- **Strengthen the read rule.** Selecting the largest observed leaf can expose tentative data. Raft reads require commitment knowledge and current authority. [Raft, §8](https://raft.github.io/raft.pdf)
