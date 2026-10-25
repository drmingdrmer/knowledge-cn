# 最大 leaf：唯一确定一条历史分支

给定一份不可变历史树视图和一个 TimePoint 偏序，若该视图的 leaf 集合存在最大元，它就唯一确定一条从根到该 leaf 的历史分支。

## 证明：最大元唯一，根路径也唯一

最大 leaf 的条件是：视图中的每个 leaf 都不大于它。

1. 假设 `first` 与 `second` 都满足最大 leaf 条件。因为它们都在同一 leaf 集合中，所以 `first ≼ second` 且 `second ≼ first`。
2. 根据[[timepoint-partial-order|TimePoint 偏序]]的反对称性，`first = second`，因此最大 leaf 唯一。
3. 根据[[immutable-history-trees|不可变历史树]]，这个 leaf 的节点标识固定其父节点与命令，沿父节点回溯得到唯一的根路径。

所以，在相同视图与相同比较关系下，选择最大 leaf 的根路径会得到同一条历史分支。

## 例子：最大 leaf 选中自己的根路径

树包含 `root → left` 与 `root → right` 两条分支。若给定的比较关系满足 `left ≺ right`，最大 leaf 就是 `right`，选中的路径为 `root → right`。路径由父节点记录确定。

## 来源：原文的唯一最大 TimePoint 与分支选择

《重新理解分布式共识：Raft 与 Paxos 的共同结构》“TimePoint 之间形成 partial order”及“在已经读到的分支上追加”（241、247、259 行）。本结论以视图中存在最大 leaf 为条件。
