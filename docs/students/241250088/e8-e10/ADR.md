# 决策记录

负责人：刘馨雅 241250088。状态：E8 个人用例已验证；E9 决策待补。

背景与约束：受限 C/Make 教学样例，课程已有 main.c 直接 include 失效测试；需增加具有独立预期的个人覆盖。

选择与替代方案：选择 helper.c → bridge.h → extra.h 的间接包含，验证另一对象目标。保留参考全目标刷新策略；仅刷新受影响目标需另行设计并证明，不在此次修改中实现。

缓存何时失效、配置身份如何绑定：scan 比较项目预处理指令、源码/头文件集合、配方、CFLAGS 与编译器身份。新增桥接头与 helper.c 包含关系使 key 改变，两个对象目标均重新采集。外层源码 SHA、镜像 ID 与内部样例提交分别记录。

代价与覆盖范围：保守刷新安全但非最小范围；通过 gcc -MM 与真实 BuildChecker 动态路径核对当前配置，不证明完整论文覆盖。将个人测试分文件，避免四人修改课程同一测试文件。

验证命令与实际证据：服务器 unittest discover 定向 1 项、完整 8 项通过；独立个人 OUT 保存 baseline/incremental/full、personal-gate、动态 trace 和步骤日志，源码 26f4141。双端下载核验及原始行详见 E8/records/241250088.md 和 E8/validation/personal-241250088-local-audit.json。
