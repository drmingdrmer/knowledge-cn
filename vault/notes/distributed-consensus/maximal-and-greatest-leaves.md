# 极大 leaf 未必是最大 leaf

对同一组按 TimePoint 偏序比较的 leaf，可以同时存在多个极大元，却没有最大元。

## 反例：两个不可比 leaf 同时极大

在一个固定的 leaf 集合中，依据[[timepoint-partial-order|TimePoint 偏序]]，区分两种条件：

- 极大元（Maximal Element）：集合中没有严格大于它的 leaf。
- 最大元（Greatest Element，也称 Maximum Element）：集合中的每个 leaf 都不大于它。

取只有 `left` 与 `right` 的 leaf 集合，比较关系仅包含两个点各自的自反关系，因此二者不可比。这个关系满足偏序的三条公理。

两个 leaf 都没有严格更大的 leaf，因此都是极大元。但 `right ≼ left` 与 `left ≼ right` 都不成立，两个候选都不满足最大元条件。因此，这组 leaf 有两个极大元，却没有最大元。

## 来源：原文区分最大 leaf 与多个极大 leaf

《重新理解分布式共识：Raft 与 Paxos 的共同结构》“分支间是偏序关系而不是全序关系的原因”及“在已经读到的分支上追加”（237、259 行）。本卡片用两元素偏序给出反例。
