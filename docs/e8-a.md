# A08 E8：EChecker 基线复现

状态：2026-11-18 四人个人PR已合入a08/e8-e9，集成测试、服务器E8实验与下载原包核验通过。整合PR、最终CI归档及平台交付待完成。

## 目标与范围

保留 E7 BuildChecker 成果，建立真实对象目标历史图并验证未变化输入复用。受限 C/Make 教学配置，gcc -MM 路径与 BuildChecker 动态路径交叉核对；不宣称复现完整论文。

## 小组集成结果

实验源码为 `04f386971d8f924cbdd85401c1f3583935c9b1c4`，包含个人PR #23—#26；后续报告提交不替代实验版本。镜像course-e8e10:241250088，ID `sha256:6b34d781ec37d2e6484f953587e022d5fef897ec9fd8b2b808898bf65a899d3f`。

集成OUT为 `/root/241250088/buildchecker/work/e8-A-manual.zTJjf8`，回归目录work/e89-241250088-integrated-dmvueNDG。16项/3.582s/退出0，覆盖课程7项、071两项、076三项、088两项、097两项；已逐项核对日志与源码中的测试方法。

GCC基线实际图main.o→config.h/main.c、helper.o→helper.c，精确发现MD(main.o, config.h)、RD(main.o, unused.h)。真实BuildChecker对象投影一致，SUCCEEDED、clean/build退出0。用本次动态实际图建立历史后，未变输入两个目标复用、无刷新，无新增/消除，actual/declared/findings与基线和全量一致。

内部样例提交63bb4cdf1ceac6f98ae9e52f9f515a26ff67ab2c；trace_id e6-d5a01fb3af92401885fbd2d3af29b154。原始输入、图、trace读取行、Make数据库声明及步骤日志已核验，见 [集成记录](../E8/validation/INTEGRATED.md) 与 [审计JSON](../E8/validation/integrated-local-audit.json)。

## 组长个人轮历史版本与证据

源码 SHA 为 `369a8c82b73e53fb220fca28b89f3fc786e386e3`；组长个人分支运行目录 `/root/241250088/buildchecker/work/e8-A-manual.iz7oZm`。镜像及详细判定见 [组长记录](../E8/records/241250088.md)。

GCC 与真实 BuildChecker 对象投影核对一致，精确检出 MD(main.o, config.h)、RD(main.o, unused.h)。原始读取证据 t.15:579，声明证据 make-db.txt:1044。未变化输入复用两个目标、无刷新，actual/declared/findings 三集合不变；终端步骤退出 0。
个人基线归档位于服务器 `/root/E8-241250088-baseline-MJZnwXqO` 与电脑 `D:\MYfile\3-1\Devops\Lab\241250088\E8`。双端哈希及原包内容核验通过，详见 [核验记录](../E8/validation/baseline-241250088-local-audit.json)。后续集成结果在上文单独列出，不混用两轮运行身份。

## 贡献与结论

组长个人版本 `26f4141` 新增 helper.c → bridge.h → extra.h 用例，定向 1 项与回归 8 项通过，个人 OUT work/e8-A-manual.iand6b 检出两项新增 MD、保守刷新两个目标，与全量及动态投影一致。个人归档已双端哈希及内容核验，见 [个人轮审计](../E8/validation/personal-241250088-local-audit.json)。

分工见 [E8/CONTRIBUTIONS.md](../E8/CONTRIBUTIONS.md)，实际记录见各成员records和review。四人个人PR已合并；组长本人四轮原包已核验，其他三人的E9个人包已独立抽查，见 [抽查JSON](../E9/validation/peer-sample-audit.json)。此抽查不扩称其他成员所有E8/基线原包均已逐包核验。

本轮未修改公共lab.py，仍是两对象目标、全目标保守刷新教学配置，不宣称完整论文增量系统调用归并或大型项目性能。最终文档CI、整合PR至main、原始证据集中收齐与平台交付仍待完成。
