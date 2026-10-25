# 历史承接：后续写入包含已完成的历史

在固定成员、历史只增且确认前持久化的模型中，写入者在前次写入完成后才发起 Quorum 读取，并在完整读并集上追加，生成的新历史就包含前次写入的全部记录。

## 证明：读并集包含旧历史，追加保留读并集

将前次写入的记录集合记为 `committed_history`，本次读回复并集记为 `read_history`，追加后的记录集合记为 `next_history`。

1. 根据[[quorum-visibility|Quorum 可见性]]，本次读取发起于前次写入完成之后，前次写入的每条记录都会进入本次读并集，因而 `committed_history ⊆ read_history`。
2. 写入者保留整个 `read_history`，从中选择已有节点作为父节点。根据[[history-tree-extension|历史树追加]]，添加新子节点后，`read_history ⊆ next_history`。
3. 集合包含关系具有传递性，因此 `committed_history ⊆ next_history`。写入者将这份完整的新历史作为后续写入的内容。

## 例子：在另一条分支追加仍保留旧记录

前次写入已提交 `root → A`。后续读取的并集同时包含 `root → A` 和 `root → B`。在 `B` 下追加 `C` 后，新历史仍保留 `root → A`，并增加路径 `root → B → C`。

## 来源：原文的 Quorum 读取、合并与追加

《重新理解分布式共识：Raft 与 Paxos 的共同结构》“完整的多历史 consensus 框架”与“多历史 consensus 的一个具体的读写流程”（183–201 行）。本卡片证明整棵历史树的记录包含关系。
