# Quorum 相交约束：每个读集合都与每个写集合重叠

协议需要选定读 Quorum 与写 Quorum，使每个允许的读 Quorum 都与每个允许的写 Quorum 至少共享一个成员。读写两边都使用同一固定成员集合的多数派，就满足这一约束。

## 推导：先规定集合族，再证明跨集合族相交

Quorum 是足以完成某个协议步骤的参与者集合。Quorum 相交性（Quorum Intersection）是对允许集合的设计约束。

在本历史存储模型中，写入者等待一个写 Quorum 全部确认，读取者收集一个读 Quorum 的全部回复。相交约束为后续读取提供至少一个曾确认写入的成员。

如果读写两边都使用多数派，根据[[majority|多数派相交性]]，每一种允许的读写组合都相交。Canvas 中从多数派相交性到本卡片的箭头，证明的是这个特例。

设成员总数为 `member_count`，读、写 Quorum 的最小人数分别为 `read_count` 和 `write_count`。如果允许任意满足人数要求的子集，`read_count + write_count > member_count` 就足以保证相交：若某对读写集合互不相交，它们的总人数就会超过整个成员集合。

## 例子：五个副本可以使用读二写四

成员总数为五时，可以选择任意四个成员作为写 Quorum，任意两个成员作为读 Quorum。由于 `4 + 2 > 5`，每个读 Quorum 都与每个写 Quorum 相交。

## 补充：不同协议步骤需要各自的相交论证

这里的读写名称对应存储操作。Paxos 中准备阶段与接受阶段使用的 Quorum，也需要跨阶段相交。具体协议还需结合持久化、承诺和提案选择规则来利用交集中的成员。

## 来源：跨阶段相交允许不同大小的 Quorum

[Flexible Paxos: Quorum intersection revisited](https://arxiv.org/pdf/1608.06696)；[Paxos Made Simple，第 2.2 节](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)。
