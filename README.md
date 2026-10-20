# DevOps Course Assignment - A08

本仓库用于记录 A08 小组从 E2 开始的课程作业，并在后续阶段开发
BuildChecker 和 EChecker。

## 当前阶段

E2“需求与接口契约”和 E3“并行测试基线”已合并到 `main`。E3 的固定
MD/RD 与 C0/C1/C2 样本、人工 oracle 和复现记录保留在 [`E3/`](E3/README.md)。

当前在 `a08/e4-environment` 分支搭建 E4“可重复工程环境”。仓库根目录的
`Makefile`、`compose.yaml`、`services/buildchecker/` 与 `fixtures/md-rd/`
来自课程 A 组模板，用于构建、测试和冒烟验证。E4 的范围、分工与运行方式见
[`E4/README.md`](E4/README.md) 和 [`E4/WORKFLOW.md`](E4/WORKFLOW.md)。
E4 骨架不代表已经实现 BuildChecker/EChecker 检测算法。

## 配对信息

| 项目 | 内容 |
|---|---|
| 配对编号 | `A08-B08` |
| A08 仓库 | `https://github.com/LoShell/DevOps-Course-Assignment-A08` |
| B08 仓库 | `https://github.com/Delario17/DevOps-Course-Assignment` |
| A08 E3 工作分支 | `a08/e3-baseline` |

## 目录

- `E2/`：已完成的需求与接口契约评审材料。
- `E3/`：并行测试基线、实验样本和复现证据。
- `E4/`：环境搭建、工作流程、任务与验证记录。
- `services/`、`fixtures/`、`Makefile`、`compose.yaml`：A 组 E4 可运行模板。

E3 的历史流程见 [`E3/WORKFLOW.md`](E3/WORKFLOW.md)。
