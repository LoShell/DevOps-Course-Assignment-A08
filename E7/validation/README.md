# E7 集成与 CI 证据索引

## 组长共同基线

- 源码 SHA 为 `3a0ae35b27e783c480f66412b3e4f53802c6be68`。
- 运行根目录为 `/root/241250088/buildchecker/work/e7-241250088-baseline-nr4FTjklv`。其中 `full/gate/results.csv` 是场景明细，`full/gate/gate-result.json` 是整体判定，`gate-exit.txt` 记录退出码。
- 组长回传的结果为整体退出 0，八项均通过。逐场景状态、退出码及 trace_id 见 [回传 CSV](baseline-241250088-results.csv)。
- 镜像 ID、服务测试数及原始归档哈希待从服务器证据补录。

## 集成与 CI

| 阶段 | 源码 SHA / PR | 运行链接、证据路径和结果 |
| --- | --- | --- |
| 本地集成门禁 | 待填写 | 独立判定、服务测试、gate JSON/CSV、镜像 ID |
| main 正常 CI | 待填写 | 成功 run、artifact、commit.txt |
| main 分支保护 | 待填写 | 必需检查名与实际 App ID、strict、管理员约束的快照 |
| 演示 PR 失败 | 待填写 | 失败 run 与 artifact、断言日志、OPEN / BLOCKED、普通合并拒绝日志及退出码 |
| 同一 PR 恢复 | 待填写 | 修复 SHA、成功 run 与 artifact、MERGED、mergeCommit、mergedAt |

下载成功和失败 artifact 后记录备份路径与 SHA-256。仓库内保存可审阅的证据索引与核验摘要。
