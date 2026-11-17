# E9 专项：integration

负责人：刘馨雅 241250088。状态：参考基线、个人扩展及本地原包核验通过，PR/CI待验收。

## 问题与机制

scan 对预处理指令、配方、配置和编译器签名相同的项目复用实际图。普通代码变动仍可触发真实编译；已有头文件的 include 变动则必须使图失效。本用例保留参考全目标刷新策略，不实现最小刷新集合。

## 独立预期与个人改动

新增 student_241250088_e9.py 持久化运行器和 test_student_241250088.py 中的 E9 测试。P0 预先建立 helper.c → bridge.h 并正确声明 bridge.h；P1 仅改 helper 函数体，预期两图复用、无发现变化，但 helper.o 重编译、app 重链接，main.o 不重编译。P2 只改已有 bridge.h 添加 extra.h include，源文件集合、helper.c 和 Makefile 均不变，预期两个目标刷新且仅新增 MD(helper.o, extra.h)。两步完整 actual/declared/findings 与全量一致，传入历史报告不变。

该输入区别于 E8 同时新增 bridge.h 与 helper.c include 的用例，可直接检查“只修改已有头文件”的失效逻辑。独立预期写在运行器中，测试与个人持久化实验调用同一场景；持久化模式额外选择真实 BuildChecker 动态核对。参考 lab.py 不变。

## 真实验证与证据

个人源码71a4eda，服务器定向2项、回归9项通过，OUT work/e9-A-manual.WzDiYf。P1两目标复用且helper.o实际重编译；P2只改bridge.h，两个目标刷新，仅新增helper.o缺extra.h。两步与全量一致，最终BuildChecker动态核对通过。bundle已恢复并确认修改范围；读取extra.h为t.94:102，目标写入为t.95:23。

见 [个人记录](../records/241250088.md) 及 [原包审计](../validation/personal-241250088-local-audit.json)。本地仅核验原包未执行实验；服务器归档run-YD11gDYR的三个回传哈希与本地一致。受限教学配置不能代表完整论文覆盖。
