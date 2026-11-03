# A08 E5：论文 1 原始复现

使用教学 md-rd 样例采集真实构建记录，人工比较实际依赖与 Make 声明，
解释缺失依赖（MD）和冗余依赖（RD）。E6 再自动检测并修复复检。
两阶段联合安排、分别上传。当前处于报告期：四人已回报同基准运行成功，
组长个人记录和论文说明已审阅，原始与构建包已核验。
PR #6、#7、#8 已审核合并，088 与 076 原包对照通过，当前准备最终报告包。进度更新于 2026-11-03。

## 文档入口

- [人工分析报告](../docs/e5-a.md)：保留整理手册指定的报告路径。
- [联合分工](WORKFLOW.md)、[任务清单](BACKLOG.md)、[贡献记录](CONTRIBUTIONS.md)。
- [个人记录模板](records/TEMPLATE.md)、[审阅模板](review/TEMPLATE.md)。
- [组长个人记录](records/241250088.md)、[论文对应与差异](PAPER_COMPARISON.md)、[整合审阅](review/integration.md)。
- [独立提交检查表](SUBMISSION.md)、[AI 使用记录](AI_USAGE.md)。

本地依据：`Lab/lab5/03_E5论文复现/A组操作手册.md`、
`Lab/lab5/06_提交与排错/01_提交与验收.md`。
小组 README、分工和目录布局是组织安排，平台提交格式待核对。

## 运行条件

每人在 `/root/<学号>/buildchecker` 使用自己的 Git 作者、GitHub 认证和镜像。
本轮运行基准为 `25e57544fe7b98e496aeea8681e5cfaca128a255`，
核对工作区后构建对应的个人服务镜像；报告提交不改变既定实验基准。
服务器为课程统一配发的 2 vCPU、2 GiB ECS，可见内存约 1.7 GiB。
新模板要求 4 GiB，共同运行基准已纳入最低可见内存 1.5 GiB 的课程规格适配，
保留建议资源警告。组长 build-02 保存日志确认构建/单测 0、15 passed，详见个人记录。其他三人文档已核对，076 原包已抽查通过。
共享服务器上的构建和实验仍依次执行。

## 执行入口

在服务器个人仓库根目录执行。输出目录已有内容时换新编号，不覆盖旧证据。

```bash
pwd
git config --local user.name
git rev-parse HEAD
git status --short
python3 scripts/course.py e5 --out work/e5-01
E5_CODE=$?
printf 'E5_EXIT_CODE=%s\n' "$E5_CODE"
git rev-parse HEAD > work/e5-01/source-commit.txt
```

立即保存退出码，失败时先检查日志。运行前核对 HEAD 与工作区。

## 预期及证据

输入为 `fixtures/md-rd/`，实际采集副本在 `work/e5-01/evidence/`。
入口预期退出 0、程序输出 1。组长已按原始包核对下表结论，三位成员回报一致。

| 目标 | 预期实际依赖 | 预期 Make 声明 | 预期结论 |
| --- | --- | --- | --- |
| main.o | main.c、config.h | main.c、unused.h | MD config.h；RD unused.h |
| app | main.o | main.o | 相同 |

保留完整本次目录：版本、invocation、容器 ID、runner，以及 evidence 中的输入、
trace、Make 数据库、构建日志、程序输出和产物。检查成功读打开与所属作业，
以成功只读打开和进程归属判定依赖。按项目边界过滤系统文件，
RD 结论仅对应本次配置。报告写真实 PID、文件与行号，并说明与论文的机制及规模差异。
