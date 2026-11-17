# A08 E9：EChecker 逐提交更新

状态：组长参考路线、个人扩展、原包及双端哈希核验通过；PR/CI与小组验收待完成。共同分支 a08/e8-e9。

## 目标

解释 C0—C3 的图复用、失效和 MD/RD 变化。依赖图复用不代表 make 不重新编译。具体判定见 [测试计划](../E8/TEST_PLAN.md)。

| 版本 | 输入变化 | 预期 | 实际提交/结果/证据 |
| --- | --- | --- | --- |
| C0 | 原样例 | MD config.h、RD unused.h | bcfbd8c，通过 |
| C1 | 普通函数体 | 两目标图复用，发现不变 | 7bc20d2，通过；仍重编译main.o及链接 |
| C2 | main.c 新 include extra.h | 保守刷新，新增 MD extra.h | e2abdec，通过；三集合与全量一致 |
| C3 | 补 config.h/extra.h 声明 | 图复用，两项 MD 消除，RD 保留 | ad11356，通过；三集合与全量一致 |

组长实际源码 0c1e2c46eb788037f14ef7658926bbe63c8194cb，OUT work/e9-A-manual.eBhiYp。四阶段结果符合表中预期，C2/C3另保存全量三集合对照；bundle恢复检查四个提交与报告逐一相符。详情及归档哈希见 [个人记录](../E9/records/241250088.md)，检查范围见 [审计JSON](../E9/validation/baseline-241250088-local-audit.json)。

组长个人版本71a4eda新增helper函数体复用及已有桥接头间接include失效用例，定向2项、回归9项通过，持久化OUT work/e9-A-manual.WzDiYf，两步均与全量一致且最终动态重检通过。bundle与原始证据已核验，见 [个人轮审计](../E9/validation/personal-241250088-local-audit.json)。服务器归档 /root/devops-submissions/241250088/E9/personal/run-YD11gDYR，双端实际文件哈希与下载清单对照一致。

其他成员结果、PR/CI、最终集成待填写。E10 的 30 行性能矩阵属于后续阶段。
