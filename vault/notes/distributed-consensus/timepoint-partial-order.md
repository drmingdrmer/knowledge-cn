# TimePoint 偏序：比较关系允许节点不可比

TimePoint 偏序（Partial Order）是协议显式给定的比较关系，须满足自反性、反对称性和传递性。两个不同 TimePoint 可以彼此不可比。

## 定义：比较关系须满足三条公理

用 `≼` 表示“不大于”。对给定集合中的任意 TimePoint，要求：

1. 自反性：`point ≼ point`。
2. 反对称性：若 `first ≼ second` 且 `second ≼ first`，则 `first = second`。
3. 传递性：若 `first ≼ second` 且 `second ≼ third`，则 `first ≼ third`。

当 `first ≼ second` 且两者不同，记作 `first ≺ second`，表示严格小于。若两个方向的比较都不成立，就称两个 TimePoint 不可比。

本卡片比较候选历史的 TimePoint；[[topological-order-and-linear-extension|命令 DAG]] 的执行依赖则定义另一个偏序。具体协议需要明确自己的 TimePoint 比较规则，并逐项验证这三条公理。

## 例子：共同前驱之后的两个点可以不可比

取三个点 `base、left、right`，规定 `base ≺ left`、`base ≺ right`，再补上每个点与自身的关系。这个关系满足三条公理，同时 `left` 与 `right` 不可比。

## 来源：原文的 TimePoint partial order

《重新理解分布式共识：Raft 与 Paxos 的共同结构》“确定地选择一条历史分支”“TimePoint 之间形成 partial order”（233–241 行）。本卡片将偏序公理作为显式模型前提。
