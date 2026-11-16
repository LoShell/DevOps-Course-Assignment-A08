# E7 集成与 CI 证据索引

## 组长共同基线

- 源码 SHA 为 `3a0ae35b27e783c480f66412b3e4f53802c6be68`。
- 运行根目录为 `/root/241250088/buildchecker/work/e7-241250088-baseline-nr4FTjkl`。其中 `full/gate/results.csv` 是场景明细，`full/gate/gate-result.json` 是整体判定，`gate-exit.txt` 记录退出码。
- 组长回传的结果为整体退出 0，八项均通过。逐场景状态、退出码及 trace_id 见 [回传 CSV](baseline-241250088-results.csv)。
- 服务测试为 `19 passed in 0.17s`，见 `full/gate/unit-tests/stdout.log`。镜像 ID 为 `sha256:284bdd03eedc008f724bfc9169b65de51ec60cb64d394a1a08fa7bbfd9012af4`，见 `full/gate/image/stdout.log`。
- 原始证据归档哈希已核验，见 local-archive-audit.json。

## 集成与 CI

| 阶段 | 源码 SHA / PR | 运行链接、证据路径和结果 |
| --- | --- | --- |
| 本地集成门禁 | `8aeb3220c837f0acdc65c7b71477a370c533e12f` | `work/e7-241250088-integrated-GYJmGTi1`，服务 23 项通过，gate 8/8、退出 0；[场景结果](integrated-results.csv) |
| main 正常 CI | 57e65e7 | 43437491315 成功，artifact 已归档 |
| main 分支保护 | PR #21 | 15368 / e7-a-quality-gate，strict 和管理员约束开启 |
| 演示 PR 失败 | 56546f1 / #21 | 43446202321 失败，普通合并退出 1，OPEN / BLOCKED |
| 同一 PR 恢复 | 22461fb / #21 | 43447515564 成功，MERGED，合并 d4fd214 |

下载成功和失败 artifact 后记录备份路径与 SHA-256。仓库内保存可审阅的证据索引与核验摘要。

集成镜像 ID 为 `sha256:697bcaccba2efffe93f627bf15876f4055a3bd8f5b468d4c310ee60c842335d0`。集成原始包已下载，归档哈希及门禁报告核验通过。

## 电脑归档核验

四人两轮及组长集成共 9 份原包已下载到工作区 Lab/<学号>/E7/。逐包 SHA-256 与服务器校验文件一致，包内 gate-result.json 均为八项通过。文件名、哈希和包内源码 SHA 见 [归档核验清单](local-archive-audit.json)。076 本次重新打包的原包单独列在清单中，个人报告保留其早前归档记录。

## CI 门禁闭环完成

正常运行 [43437491315](https://github.com/LoShell/DevOps-Course-Assignment-A08/actions/runs/43437491315) 成功。main 必需检查为 e7-a-quality-gate，App ID 为 15368，strict 和 enforce_admins 均已开启。

[PR #21](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/21) 的错误提交 56546f1 在运行 43446202321 中因版本返回码断言失败，1 failed、23 passed。普通合并退出 1，PR 保持 OPEN / BLOCKED。修复提交 22461fb 在运行 43447515564 恢复成功，24 项服务测试及八项门禁通过。同一 PR 已合并，合并 SHA 为 d4fd214ee2dc2dccb0d0dc100645e29208ca9cee，时间为北京时间 2026-11-13 23:00:47。

下载的 CI 包哈希、保护快照、三阶段测试及最终合并已核验，见 [CI 核验摘要](ci-audit.json)。
