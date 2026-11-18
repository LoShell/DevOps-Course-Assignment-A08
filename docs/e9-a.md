# A08 E9：EChecker 逐提交更新

状态：2026-11-18 四人贡献已合并，16项集成回归、服务器C0—C3、最终动态重检及原包核验通过。整合PR、最终CI归档与平台交付待完成。

## 目标

解释 C0—C3 的图复用、失效和 MD/RD 变化。依赖图复用不代表 make 不重新编译。具体判定见 [测试计划](../E8/TEST_PLAN.md)。

## 小组集成结果

实验源码 `04f386971d8f924cbdd85401c1f3583935c9b1c4`，镜像身份与E8集成相同。OUT为 `/root/241250088/buildchecker/work/e9-A-manual.i2Us3t`。

| 状态 | 内部完整提交 | 实际结果 |
| --- | --- | --- |
| C0 | 916fc084c273bc1ab346ea67e2d02b2d2f67c083 | 程序输出1，MD config.h、RD unused.h，两个对象编译并链接 |
| C1 | 4e93ec6f8ec0dfeef4d752992c90f9b120b5f1a6 | 只改main.c函数体，两目标图复用、无发现变化；实际main.o仍重编译及链接 |
| C2 | 8ce865ca68cade7dbde1393fe027d2246079db87 | 新include extra.h，两目标刷新，精确新增MD(main.o, extra.h) |
| C3 | 9186c281838a5576b42740cf18a50df97e1d6a0e | 只补Make声明，实际图复用，消除两项MD、保留RD unused.h |

C1/C2/C3各自actual/declared/findings与同状态全量一致。C3另用真实BuildChecker重检，实际/声明对象投影一致，只余预期RD，SUCCEEDED、clean/build退出0；trace_id e6-a108b95eb49d49afa6882f8b9fd3eb4b。

16项/3.582s/退出0与E8共用同一次真实集成回归日志，不重复计为32项独立测试。bundle恢复精确四提交，相邻修改文件main.c/main.c/Makefile，最终受版本控制输入与动态副本一致。三份构建日志、五份成功步骤、原始trace和声明行均已核验，见 [集成记录](../E9/validation/INTEGRATED.md) 和 [审计JSON](../E9/validation/integrated-local-audit.json)。

## 组长个人轮历史结果

| 版本 | 输入变化 | 预期 | 实际提交/结果/证据 |
| --- | --- | --- | --- |
| C0 | 原样例 | MD config.h、RD unused.h | bcfbd8c，通过 |
| C1 | 普通函数体 | 两目标图复用，发现不变 | 7bc20d2，通过；仍重编译main.o及链接 |
| C2 | main.c 新 include extra.h | 保守刷新，新增 MD extra.h | e2abdec，通过；三集合与全量一致 |
| C3 | 补 config.h/extra.h 声明 | 图复用，两项 MD 消除，RD 保留 | ad11356，通过；三集合与全量一致 |

组长实际源码 0c1e2c46eb788037f14ef7658926bbe63c8194cb，OUT work/e9-A-manual.eBhiYp。四阶段结果符合表中预期，C2/C3另保存全量三集合对照；bundle恢复检查四个提交与报告逐一相符。详情及归档哈希见 [个人记录](../E9/records/241250088.md)，检查范围见 [审计JSON](../E9/validation/baseline-241250088-local-audit.json)。

组长个人版本71a4eda新增helper函数体复用及已有桥接头间接include失效用例，定向2项、回归9项通过，持久化OUT work/e9-A-manual.WzDiYf，两步均与全量一致且最终动态重检通过。bundle与原始证据已核验，见 [个人轮审计](../E9/validation/personal-241250088-local-audit.json)。服务器归档 /root/devops-submissions/241250088/E9/personal/run-YD11gDYR，双端实际文件哈希与下载清单对照一致。

四人个人结果见records、review和贡献表；三个其他成员的E9个人包已由组长电脑独立抽查，见 [抽查JSON](../E9/validation/peer-sample-audit.json)。公共lab.py未改变，个人历史测试数量与集成16项分别记录。当前仍待最终文档CI、共同分支至main整合PR、原始证据集中收齐和平台提交。E10的30行性能矩阵属于后续阶段，不将公共CI中的演示作为个人完成记录。
