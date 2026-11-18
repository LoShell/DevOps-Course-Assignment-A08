# E8 专项：include-invalidation

负责人：范从钰（241250071）。状态：已完成本人实测、原始证据归档与本地 SHA-256 校验；PR/CI 待后续提交。

## 问题与机制

负责范围是间接 include 导致的依赖变化与缓存失效。审阅代码位于 `labs/e8e10/lab.py` 的 `scan()`：缓存键包含项目中所有本地 `.c`、`.h` 文件的预处理指令行、Make 配方、编译 flags 和 GCC 版本；键相同才复用历史 `actual` 图，否则对 `main.o`、`helper.o` 重新使用 GCC `-MM` 扫描。

该教学实现为保守失效策略：任一本地预处理指令变化都会刷新两个对象，而不是根据 include 图仅刷新最小受影响目标。实际依赖由 GCC `-MM` 获得；真实动态交叉核对由 `buildchecker()` 调用 BuildChecker 的 strace 路径完成。该机制适用于本次小型、显式 Make 规则输入，不覆盖复杂 Make 语法、并行构建、符号链接或大型项目。

## 独立预期与个人改动

课程已有测试覆盖直接 include 新增、未变化输入复用和不支持配置拒绝；未单独覆盖“`config.h` 间接包含 `extra.h`”的变化。

本人新增测试文件：`labs/e8e10/test_student_241250071.py`。
E8 测试方法：`test_indirect_include_invalidates_cached_dependencies`。
个人测试源码提交：`9531e0d5aed286b61941955319b1149b52577de2`。

测试输入：C0 中 `main.c` 直接包含 `config.h`；随后 C1 将 `config.h` 改为 `#include "extra.h"` 后保留 `#define VALUE 1`。C0、C1 均通过内层 Git 真实提交固定。

独立预期：

1. `main.o` 的实际依赖从 `main.c`、`config.h` 增加为 `main.c`、`config.h`、`extra.h`。
2. 声明仍为 `main.c`、`unused.h`，因此新增且仅新增 MD(`main.o`, `extra.h`)；原 MD(`main.o`, `config.h`) 和 RD(`main.o`, `unused.h`) 保留。
3. 缓存键失效；参考实现保守刷新 `main.o`、`helper.o`，无 reused 目标。
4. 增量扫描与全量扫描的 actual、declared、findings 三个集合严格相同。

## 真实验证与证据

基线轮源码 SHA：`369a8c82b73e53fb220fca28b89f3fc786e386e3`；OUT：`work/e8-A-manual.N3T6Mn`。BuildChecker 基线实际图来自 `buildchecker/actual-graph.json`，精确检出 MD(`main.o`, `config.h`) 与 RD(`main.o`, `unused.h`)；`trace/t.15` 第 579 行成功读取 `config.h`，`make-db.txt` 第 1044 行声明 `main.o: main.c unused.h`。未变化输入的 `incremental.json` 显示两个对象均复用。

个人轮 OUT：`work/e8-A-manual.ilU2Fl`；镜像 ID：`sha256:ac9488455abe7567438f7ccfc4b826aef5021efece7be18cc8fc8022768969c7`。内层 C0 为 `c0ac49e07deb4711ffbbcb24d4cc3985acbbdf1d`，C1 为 `ea2296795b6087a62e7ca7f523138c76e643e46c`。

`P1.json` 的实际集合为 `main.o -> [config.h, extra.h, main.c]`、`helper.o -> [helper.c]`；`added` 精确为 `[[MISSING, main.o, extra.h]]`；`refreshed=[main.o, helper.o]`；`reused=[]`。`P1-full.json` 与 P1 的 actual、declared、findings 相同。`P1-buildchecker/findings.json` 的真实动态检查也与独立预期一致；`P1-build.log` 构建成功，程序输出文件 `P1-program-output.txt` 为 `1`；`personal-gate.json` 为 `passed=true`。

测试日志目录 `work/e89-241250071-tests-z4WYXC8O` 中，定向测试为 1 项通过、退出码 0；完整回归为 8 项通过、退出码 0。

E8 基线归档：`/root/devops-submissions/241250071/E8/baseline/run-m4qBiUsa`；个人归档：`/root/devops-submissions/241250071/E8/personal/run-zDx34xnH`。两轮均已下载到电脑并按 SHA-256 清单校验一致。
