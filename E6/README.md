# A08 E6：自动依赖检测与修复复检

状态：四人个人PR已合并，组长集成19项测试通过；集成原包核验及两人同基线对照通过。下一步提交收尾文档、合入main并打包上传。

E5 已完成原始采集和人工 MD/RD。E6 使用现有 fullcheck.py 自动建立实际图、声明图，生成检测报告，修复副本后复检，并增加个人测试。

## 导航

- [共同报告](../docs/e6-a.md)、[集成验收表](records/integrated-验收记录.csv)、[整合审阅](review/integration.md)。
- [分工与版本](WORKFLOW.md)、[测试题目](TEST_PLAN.md)、[任务清单](BACKLOG.md)。
- [个人贡献](CONTRIBUTIONS.md)、[个人报告模板](templates/E6实验报告.md)、[验收模板](templates/E6验收记录.csv)。
- [审阅模板](review/TEMPLATE.md)、[提交清单](SUBMISSION.md)、[AI记录](AI_USAGE.md)。
- 独立操作指南位于工作区 `Lab/E6操作指南.md`，另行发群。

各自在原来的 /root/学号/buildchecker 操作。继续使用 scripts/course.py 和个人镜像标签，2 GiB 服务器依次构建、运行。公共安装与资源适配沿用现有配置。

每人完成基线和个人修改后两轮，填写个人报告、验收 CSV 和专项审阅；组长另执行一次集成验证并汇总共同报告。

## 验证结果

| 阶段 | 实际结果 |
| --- | --- |
| 基线构建 | 服务单测 15 passed，构建和单测均退出 0 |
| 原始检测 | status=SUCCEEDED；clean/build=0；精确 MISSING(main.o, config.h)、REDUNDANT(main.o, unused.h)；入口退出 1 |
| 修复复检 | findings=[]，入口退出 0 |
| 报告校验 | passed=true，changed_inputs=["Makefile"] |
| 个人新增测试后 | 四人各新增一项，个人镜像重建后16项通过，重新检测与复检通过 |
| 四项测试整合后 | 19 passed in 0.25s；原始检测、修复复检与校验通过 |

基线SHA：`aff4eba7dca7a09a372d1264375d9fe9cd11354f`。
集成SHA：`9716ae3a20cae6ff8eda89d69733ab71d4a7b3e6`。
集成目录：`work/e6-integrated-20261106-111142`。
核验摘要：[集成原包](validation/integrated-audit-20261106.json)、[088与097同基线对照](validation/baseline-comparison-20261106.json)。

依据：Lab/lab6/docs/02_A操作指南.md、04_实现与测试任务.md、05_验收与提交.md，以及 Lab/lab5-论文复现1/04_E6核心实现/A组操作手册.md。
