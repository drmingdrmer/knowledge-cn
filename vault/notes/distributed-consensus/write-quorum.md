# Write Quorum：一次写入需要覆盖的副本集合

Write Quorum 是协议要求写入覆盖的副本集合。在本历史模型中，目标历史须持久化到其中每个成员，才满足一次写入的 Quorum 覆盖要求。

## 定义：目标历史需要保存在整个写集合中

协议先规定允许的写 [[quorum|Quorum]] 集合族。一次写入选定其中一个集合，要求每个成员都保存同一份目标历史，包括目标节点及其完整祖先路径。

[[durable-evidence|持久化证据]]规定如何保存可恢复的历史；[[multi-history-commit|多历史提交]]规定写入者何时收齐成功确认并宣布完成。

## 例子：写四配置需要覆盖四个成员

五个副本允许任意四个组成 Write Quorum。选中 `{A, B, C, D}` 后，目标历史需要在这四个成员上全部持久化，才满足本次写入的覆盖要求。

## 来源：原文的 WriteQuorum 与 write phase

《重新理解分布式共识：Raft 与 Paxos 的共同结构》“从 fault tolerance 到 quorum”与“多历史 consensus 的一个具体的读写流程”（155–166、201 行）。
