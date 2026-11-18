# E8：EChecker 基线与历史图复用

状态：四人个人PR已合并，服务器集成16项与E8动态核对/复用验证通过，原包已核验；整合PR、最终CI归档与平台交付待完成。轨道A，第二篇论文EChecker。见 [集成证据](validation/INTEGRATED.md)。

本阶段用真实 BuildChecker 对象目标投影建立历史图，证明 main.o 缺失 config.h、冗余 unused.h；输入不变时 main.o/helper.o 图复用，刷新为空，actual/findings 不变。

共同分支 `a08/e8-e9`，个人分支 `a08/<学号>/e8-e9`。协作入口见 [流程](WORKFLOW.md)、[分工](CONTRIBUTIONS.md)、[测试计划](TEST_PLAN.md)、[交付清单](SUBMISSION.md)，共同报告见 [docs/e8-a.md](../docs/e8-a.md)。

运行代码位于 labs/e8e10/，入口为 run_lab.py。E9 见 [阶段入口](../E9/README.md)。本轮保留课程包 E10 代码，不据此申报 E10 已完成。可直接发给成员的操作文档在仓库外 Lab/lab8-9，后续按真实运行更新。
