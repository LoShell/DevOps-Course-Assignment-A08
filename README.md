# DevOps Course Assignment - A08

本仓库用于记录 A08 小组从 E2 开始的课程作业，并在后续阶段开发
BuildChecker 和 EChecker。

## 当前阶段

E2“需求与接口契约”已经完成并合并到 `main`。

当前任务为 E3“并行测试基线”。A08 负责准备可复现的 GNU Make 小型项目、
固定 MD/RD 样本以及 C0/C1/C2 增量构建样本，并保存真实 Commit SHA、
预期结果、执行命令、输出和失败记录。本阶段准备测试基线，不实现
BuildChecker 或 EChecker。

目前 C0 初始项目已在 Ubuntu 24.04 宿主机和容器中完成构建与行为验证，
并由 `e3-c0` 标签固定。验证依据见
[`E3/evidence/environment/c0-ubuntu-24.04.md`](E3/evidence/environment/c0-ubuntu-24.04.md)；
固定 MD/RD 与 C1/C2 仍在准备中。

## 配对信息

| 项目 | 内容 |
|---|---|
| 配对编号 | `A08-B08` |
| A08 仓库 | `https://github.com/LoShell/DevOps-Course-Assignment-A08` |
| B08 仓库 | `https://github.com/Delario17/DevOps-Course-Assignment` |
| A08 E3 工作分支 | `a08/e3-baseline` |

## 目录

- `E2/`：已完成的需求与接口契约评审材料。
- `E3/`：当前并行测试基线、实验样本和复现证据。

E3 的范围、分工和操作流程见 [`E3/README.md`](E3/README.md) 和
[`E3/WORKFLOW.md`](E3/WORKFLOW.md)。
