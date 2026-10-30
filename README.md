# DevOps Course Assignment — A08

本仓库保存 A08 小组的 BuildChecker 课程作业、实现和实验记录。
配对 B08 仓库：<https://github.com/Delario17/DevOps-Course-Assignment>。

| 阶段 | 入口 | 当前状态 |
| --- | --- | --- |
| E2 | [需求与接口契约](E2/) | 保留历史成果 |
| E3 | [并行测试基线](E3/README.md) | 保留历史成果 |
| E4 | [可重复工程环境](E4/README.md) | 保留历史成果 |
| E5 | [复现说明](E5/README.md)、[人工分析报告](docs/e5-a.md) | 骨架已建立，正式复现待完成 |
| E6 | 自动依赖检测与修复复检 | 与 E5 联合安排、独立提交；文档待建立 |

E5/E6 共同整合分支为 `a08/e5-e6`，协作见 [WORKFLOW](E5/WORKFLOW.md)。
课程参考代码已由 [PR #4](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/4)
合并至 main；代码导入和 CI 通过不代表个人实验完成。

`services/buildchecker/` 保存服务实现与测试，`fixtures/md-rd/` 保存样例，
`scripts/` 保存入口和校验程序，`course-support/` 保存课程模板及 CI 材料。
这些源码由各阶段共用，不能因进入新阶段而删除。

在 Ubuntu 服务器各自学号目录执行实验，E5—E7 使用 `python3 scripts/course.py ...`，
按 Git 本地学号设置个人镜像；Makefile/Compose 保留为 E4 接口。
2 GiB ECS 依次构建和运行，不在共享 root 下设置全局 Git 作者或认证。
`work/` 原始证据不提交 Git，独立归档下载，见 [E5 提交检查表](E5/SUBMISSION.md)。
