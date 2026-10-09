# A08 E3 Backlog

| 编号 | 事项 | 负责人 | 状态 | 完成证据 |
|---|---|---|---|---|
| E3-01 | 建立 E3 公共骨架并确认工作流 | 刘馨雅 | Done | `README.md`、`WORKFLOW.md` |
| E3-02 | 建立 Ubuntu 24.04 可运行项目和 C0 | 刘馨雅 | Done | `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`、`e3-c0`、`evidence/environment/c0-ubuntu-24.04.md` |
| E3-03 | 构造固定 MD/RD 样本及人工 oracle | 邱莉扉 | Done | 本地实现完成；Ubuntu 22.04/24.04 验证通过，成员 2 已确认 oracle；见 `evidence/md-rd/oracle-review-20261006-132502/REVIEW.md`。样例 SHA：`8a9cfc46d854e697fd397c1f6c579014e219144b`；配置标识归入 E3-06 待补 |
| E3-04 | 构造 C1 新增头文件读取场景 | 范从钰 | Done | `4b70cabad1be8f6e98ee90ed9c5803b7aa793253`、远端 `e3-c1`、`evidence/c1/20261007T143349+0800/`；人工确认来源见 `oracle/incremental-review-20261009.md` |
| E3-05 | 构造 C2 编译命令变化场景 | 叶原原 | Done | `56deea9199679907893fa53add1d867ff62028e1`、远端 `e3-c2`；脚本 `03c0d28d0645699966c150fee90c4405b84947a3`、修订 `ae86618b602a08ce4d893b396dde6b6f75e3fccc`、证据 `evidence/c2/20261008T201035798727+0800/`；人工确认来源见 `oracle/incremental-review-20261009.md` |
| E3-06 | 汇总配置标识、完整构建日志、失败记录和贡献追溯 | 全员，刘馨雅汇总 | In Progress | C0 完整 Docker 原始日志已于 `c354dcb39afc0c2ff3f5486d053c369b3710da83` 补齐；MD/RD、C1→C2 组长复现证据见 `40d7da0`；失败记录及贡献可追溯。跨提交团队配置标识仍待核对，原则与限制见 `CONTRACT_REFERENCE.md` |
| E3-07 | 完成最终干净环境复现 | 刘馨雅汇总 | Done | 组长 Ubuntu 24.04 环境中 MD/RD 14/14、C1→C2 37/37、固定 C0 镜像构建及输出均通过；见 `evidence/final-review-20261009.md` 和三组原始证据 |

状态使用 `Todo`、`In Progress`、`Blocked` 或 `Done`。任务完成时必须同时填写
“完成证据”，不能只修改状态。
