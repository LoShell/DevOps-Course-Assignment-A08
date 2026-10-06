# A08 E3 Backlog

| 编号 | 事项 | 负责人 | 状态 | 完成证据 |
|---|---|---|---|---|
| E3-01 | 建立 E3 公共骨架并确认工作流 | 刘馨雅 | Done | `README.md`、`WORKFLOW.md` |
| E3-02 | 建立 Ubuntu 24.04 可运行项目和 C0 | 刘馨雅 | Done | `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`、`e3-c0`、`evidence/environment/c0-ubuntu-24.04.md` |
| E3-03 | 构造固定 MD/RD 样本及人工 oracle | 邱莉扉 | Done | 本地实现完成；Ubuntu 22.04/24.04 验证通过，成员 2 已确认 oracle；见 `evidence/md-rd/oracle-review-20261006-132502/REVIEW.md`。SHA 和配置标识归入 E3-06 待补 |
| E3-04 | 构造 C1 新增头文件读取场景 | 范从钰 | Todo | C1 SHA、`e3-c1`、增量检查证据 |
| E3-05 | 构造 C2 编译命令变化场景 | 叶原原 | Todo | C2 SHA、`e3-c2`、增量/干净构建证据 |
| E3-06 | 汇总配置标识、完整构建日志、失败记录和贡献追溯 | 全员，刘馨雅汇总 | In Progress | C0 验证记录与贡献 SHA 已填写；C0 完整 Docker 原始日志、`configuration_id` 和成员 2 样例提交 SHA 待补；成员 2 容器完整日志已保存 |
| E3-07 | 完成最终干净环境复现 | 全员 | Todo | 最终检查记录 |

状态使用 `Todo`、`In Progress`、`Blocked` 或 `Done`。任务完成时必须同时填写
“完成证据”，不能只修改状态。
