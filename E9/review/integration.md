# E9 专项：integration

负责人：刘馨雅 241250088。状态：参考基线与原包通过，个人扩展已编写，服务器待验证。

## 问题与机制

scan 对预处理指令、配方、配置和编译器签名相同的项目复用实际图。普通代码变动仍可触发真实编译；已有头文件的 include 变动则必须使图失效。本用例保留参考全目标刷新策略，不实现最小刷新集合。

## 独立预期与个人改动

新增 student_241250088_e9.py 持久化运行器和 test_student_241250088.py 中的 E9 测试。P0 预先建立 helper.c → bridge.h 并正确声明 bridge.h；P1 仅改 helper 函数体，预期两图复用、无发现变化，但 helper.o 重编译、app 重链接，main.o 不重编译。P2 只改已有 bridge.h 添加 extra.h include，源文件集合、helper.c 和 Makefile 均不变，预期两个目标刷新且仅新增 MD(helper.o, extra.h)。两步完整 actual/declared/findings 与全量一致，传入历史报告不变。

该输入区别于 E8 同时新增 bridge.h 与 helper.c include 的用例，可直接检查“只修改已有头文件”的失效逻辑。独立预期写在运行器中，测试与个人持久化实验调用同一场景；持久化模式额外选择真实 BuildChecker 动态核对。参考 lab.py 不变。

## 真实验证与证据

目前只进行本地语法检查，未执行个人测试或实验。实际源码SHA、服务器定向/回归日志、新OUT、动态证据和内部Git bundle待补。参考路线见个人记录；受限教学配置不能代表完整论文覆盖。
