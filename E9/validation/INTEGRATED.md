# E9 集成运行与原包核验

2026-11-18，源码 `04f386971d8f924cbdd85401c1f3583935c9b1c4`，用户在服务器执行，电脑只读核验，不重跑实验。

OUT为work/e9-A-manual.i2Us3t，共用回归目录work/e89-241250088-integrated-dmvueNDG，16项/3.582s/退出0。C0—C3及逐项预期见 [共同报告](../../docs/e9-a.md)。C1/C2/C3三集合与全量一致；最终真实动态实际/声明图对象投影一致，只余RD unused.h。

bundle恢复精确四提交，相邻变更main.c/main.c/Makefile，最终受版本控制源码与动态检测副本相同；三份构建日志、五份成功步骤及原始trace/声明行核验通过，见 [审计JSON](integrated-local-audit.json)。

| 文件 | SHA-256 |
| --- | --- |
| student-source.tar | 6a224603a8ab44c5bb9ba106190e7d21d76b162b9d1112ca911390fe88e2f583 |
| E9-project.bundle | 2db65f320e6cd1f1a27b0fb5689cc60293a9405dc128d86e6037d0887b2f8284 |
| E9-integrated-evidence.tar.gz | 747468d3826a8563c8ae2ab1ea0e0c739b6aad352d53b653b1b82e36c779b685 |

服务器：/root/devops-submissions/241250088/E9/integrated/run-2RkkZuoK。
电脑：D:\MYfile\3-1\Devops\Lab\241250088\E9\integrated。
双端与清单哈希一致。源码包与E8同版本，原始证据包不同，不能相互替代。
