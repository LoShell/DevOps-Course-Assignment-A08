# A08 E4 Backlog

| 编号 | 事项 | 负责人 | 状态 | 完成证据 |
| --- | --- | --- | --- | --- |
| E4-01 | 在 E4 分支接入 A 组模板并保留 E2/E3 | 刘馨雅 | Done | `a8cb50bb31af205e44fce09b63889d9e1592630f`；根目录入口和 E2/E3 均保留，已推送远端分支 |
| E4-02 | 核对服务器 Ubuntu、资源、Docker、Compose、Buildx 与镜像可达性 | 刘馨雅 | Done | [服务器基线](SERVER_BASELINE.md)：工具版本实测、SWR 加速器拉取固定 digest 成功；实际构建归 E4-03 |
| E4-03 | 审阅 2 GiB 资源与自检门槛，依据真实运行结果处理 | 刘馨雅、叶原原 | Done | [服务器基线](SERVER_BASELINE.md) 记录同 SHA 的干净复跑；2026-10-20 叶原原完成 AI 辅助源码复核与资源门槛隔离验证，确认 1.5 GiB 最低可见内存仍保留资源警告，见 [自检审阅](review/workflow-security.md)。本次未重新运行 ECS |
| E4-04 | 核对 A 组冒烟样本与 E3 的关系 | 邱莉扉 | Done | `01d4e6f`；[样本与冒烟审阅](review/smoke-e3.md)核对本人 `smoke.json`、E3/E4 故障结构与冒烟验证边界 |
| E4-05 | 核对 Dockerfile、Compose 与工具链记录 | 范从钰 | Done | `400fd4e`；[容器与依赖审阅](review/container-deps.md)核对固定基础镜像、资源与权限配置、构建时记录的工具版本 |
| E4-06 | 核对一键命令、证据目录和密钥扫描 | 叶原原 | Done | 2026-10-20 完成 [命令、自检与扫描审阅](review/workflow-security.md)：核查五步入口、七个证据路径、忽略规则与现有服务器记录；本地预演、资源/扫描隔离验证及工作区与历史扫描通过。已记录管道退出码和扫描覆盖边界；个人 ECS 原始证据未在本次重新读取，公共源码未修改 |
| E4-07 | 每人运行并完成同一 SHA 的重跑对照 | 全员，刘馨雅汇总 | Done | 四人均使用 `4c1ff6c`；四份 `toolchain.lock` 的 SHA-256 相同，测试均为 `3 passed`，冒烟关键结论一致；见 [服务器基线](SERVER_BASELINE.md) 和 [贡献记录](CONTRIBUTIONS.md)。个人专项审阅另见 E4-03～06 |
| E4-08 | 汇总四人复跑、专项审阅与 E4 交付边界 | 刘馨雅 | Done | [组长整合审阅](review/integration.md)：对照四份运行结果、2 GiB 适配、三份专项结论和 E5 遗留验证 |

状态使用 `Todo`、`In Progress`、`Blocked` 或 `Done`；只有真实证据到位后
才填写 `Done`，不以模板中的示例结果替代本组服务器的运行结果。
