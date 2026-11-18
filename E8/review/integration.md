# E8 专项：integration

负责人：刘馨雅 241250088。状态：参考基线、个人测试与扩展实验通过，两轮原包已核验；PR/CI 待验收。

## 问题与机制

参考 lab.py 的 fixture、scan、commit、buildchecker。scan 用预处理指令、源文件集合、配方和配置签名决定是否复用旧实际图；当前失效策略是全目标保守刷新。BuildChecker 实际图投影用于独立核对，不能把 GCC 依赖扫描称为增量 strace 归并。

## 独立预期与个人改动

新增 labs/e8e10/test_student_241250088.py 的 test_helper_indirect_include_invalidates_history。已有课程测试覆盖 main.c 直接新增 include，本用例改为 helper.c → bridge.h → extra.h，验证另一对象目标的两层包含。

先保存原 fixture 的基线，再新增 bridge.h 并修改 helper.c，创建真实内部提交。独立预期：helper.o 实际依赖精确为 bridge.h/extra.h/helper.c，声明仍仅 helper.c；新增两项 helper.o MD，原 main.o 的 MD/RD 保留；无消除项。签名变化后两个目标均刷新，增量与全量 actual/declared/findings 一致，传入旧报告保持不变。只增加测试，不改参考算法。

## 真实验证与证据

个人版本 `26f414168eacf7149be943238a8d1ac6ba85175b`，服务器定向 1 项、完整回归 8 项均 OK。持久化 OUT 为 work/e8-A-manual.iand6b：新增 helper.o 的 bridge.h/extra.h 两项 MD，两个目标刷新，原发现保留，增量与全量三集合一致，BuildChecker 动态投影核对通过。读取证据 t.48:101/102，目标写入 t.49:23，声明 make-db.txt:1187；下载原包已核验。

详见 [个人记录](../records/241250088.md) 和 [机器核验](../validation/personal-241250088-local-audit.json)。该用例验证受限 C/Make 配置下的保守刷新，不证明最小刷新集合或完整论文能力。服务器实验由本人执行，电脑仅审阅证据，未重跑实验。
