# 决策记录

负责人：范从钰 241250071。状态：已验证；PR [#26](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/26) 已创建，提交 `7a864f40f57fee2628ed5c706502b81694e4b6a2` 的 PR/push CI 均成功；最终合入待组长审核。

## 背景与约束

本次 E8/E9 要在连续源码变化中复用或刷新历史依赖图，并区分 Make 声明依赖和编译器实际读取依赖。输入是单目录 C/Make 教学项目，目标为 `main.o`、`helper.o`；实际依赖通过 GCC `-MM` 获取，并由 BuildChecker 的 strace 路径交叉核对。

## 选择与替代方案

采用 `scan()` 现有的保守缓存策略：缓存键包含全部本地 `.c`、`.h` 文件的预处理指令、Make 配方、编译 flags 和 GCC 版本。键完全一致时复用历史 actual 图；任一键字段变化时刷新 `main.o`、`helper.o` 两个对象。

未采用“仅根据 Makefile 声明判断是否刷新”，因为 `config.h`、`extra.h` 可以被编译器实际读取却未在 Makefile 中声明。未实现按 include 图仅刷新最小受影响目标，因为本轮教学实现以正确性和可审计性优先，尚未建立适用于复杂项目的完整反向依赖索引。

## 缓存何时失效、配置身份如何绑定

未变化输入时，E8 基线的 `incremental.json` 复用两个目标。E9 C1 只改变普通函数体，不改变预处理指令、配方、flags 或编译器身份，因此依赖图复用。

以下变化都会使缓存键失效并保守刷新两个目标：

- 新增直接或间接 include；
- 修改本地头文件中的预处理指令；
- 修改 Make 配方；
- 修改支持范围内的编译 flags；
- GCC 版本变化。

本人 E8/E9 测试验证了 `config.h` 间接包含 `extra.h`，以及只修改 `extra.h` 的 `#define` 指令；两种情况均刷新两个目标。P2 中实际边和 findings 未改变，仍失效是预期的保守行为。

## 代价与覆盖范围

优点是不会因为间接头文件或配置身份变化而错误复用旧依赖图，且增量扫描与全量扫描结果可直接对照。代价是与最小失效相比会多刷新未受影响的 `helper.o`，并增加 GCC 扫描开销。

本结论覆盖小型、单目录、显式 Make 规则和 GCC `-MM` 教学输入；不覆盖并行 Make、复杂宏规则、多目录、符号链接、跨工具链或大型项目的最小刷新优化。

## 验证命令与实际证据

E8 个人轮源码 SHA 为 `9531e0d5aed286b61941955319b1149b52577de2`，OUT 为 `work/e8-A-manual.ilU2Fl`。C1 间接 include 后，`P1.json` 显示新增 MD(`main.o`, `extra.h`)、两个目标刷新、无复用；`P1-full.json` 与增量三集合一致；`P1-buildchecker/` 为真实动态交叉核对。

E9 个人轮源码 SHA 为 `e80d991142c5af8d33408b9e77177a670481b349`，OUT 为 `work/e9-A-manual.knagqu`。P1 的间接 include 与 P2 的 `extra.h` 指令变化均刷新两个目标；P1/P2 各自与 full JSON 一致，`P1-buildchecker/`、`P2-buildchecker/` 通过真实 BuildChecker 核对。定向测试 2 项、完整回归 9 项均通过。
