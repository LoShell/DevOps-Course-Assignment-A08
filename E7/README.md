# A08 E7：BuildChecker 验证与 CI 门禁

共同整合分支为 `a08/e7-validation`。本阶段接续 [E6 集成结果](../docs/e6-a.md)，验证检测正确性、证据可追溯性、故障处理和合并门禁。

## 导航

- [测试计划](TEST_PLAN.md)、[协作流程](WORKFLOW.md)、[任务清单](BACKLOG.md)
- [个人贡献](CONTRIBUTIONS.md)、[个人记录说明](records/TEMPLATE.md)、[专项审阅模板](review/TEMPLATE.md)
- [CI 证据索引](validation/README.md)、[共同报告](../docs/e7-a.md)、[提交清单](SUBMISSION.md)

沿用根目录的 BuildChecker 服务、样例、`scripts/course.py`、独立判定测试和 [Actions workflow](../.github/workflows/e7-quality-gate.yml)。在原有学号目录使用各自的镜像标签。2 GiB 服务器上的构建和门禁依次执行。
