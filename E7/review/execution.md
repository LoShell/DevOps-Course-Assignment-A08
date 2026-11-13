# E7 专项审阅：跨行读取系统调用还原与 trace 证据

审阅人：范从钰（241250071）。
日期：2026-11-12。
专项：`execution_graph` 的跨行 `openat` 还原、项目依赖识别和 trace 证据保留。

所用源码 SHA：

- baseline：`3a0ae35b27e783c480f66412b3e4f53802c6be68`
- 个人轮：`9f11545d4c8a81b96090c7b27ed3fb41982dca9e`

证据目录相对于服务器仓库 `/root/241250071/buildchecker`：

- baseline：`work/e7-241250071-X0ti8vqv`
- personal：`work/e7-241250071-GBno9AYS`

| 检查项 | 输入与预期 | 实际观察 | 代码位置与证据 | 判定 |
| --- | --- | --- | --- | --- |
| 跨行系统调用还原 | 将读取 `needed.h` 的 `openat` 拆为 unfinished 与 resumed 两行 | 两行被还原为成功的 `openat` 事件 | `fullcheck.py` 的 `trace_events`；`test_e7_241250071.py` | PASS |
| 读取依赖识别 | `unit.o` 应依赖 `unit.c` 与 `needed.h` | 依赖集合精确为 `{"unit.c", "needed.h"}` | `execution_graph`；新增测试断言 | PASS |
| trace 证据回查 | `needed.h` 的证据应保留起始行，而不是 resumed 行 | 证据为 source=`system_call`、trace_file=`t.12`、line=3、pid=12、operation=`openat` | `test_e7_241250071.py` 的精确字典断言 | PASS |
| 输出目标识别 | as 创建 `unit.o` 后应识别唯一最终目标 | 目标集合仅为 `unit.o` | 新增测试；`execution_graph` 输出目标逻辑 | PASS |
| baseline 门禁 | 19 项服务测试、8 项门禁均通过 | 服务测试 19 passed；gate 退出 0；8 项均 passed=true | `work/e7-241250071-X0ti8vqv/build-console.log`；`full/gate/` | PASS |
| personal 门禁 | 新镜像包含新增测试，服务测试变为 20 项，定向测试和门禁通过 | 定向测试退出 0；服务测试 20 passed；gate 退出 0；8 项均 passed=true | `work/e7-241250071-GBno9AYS/personal-test.log`、`build-console.log`、`full/gate/` | PASS |
| 原始与修复场景 | original 检出 MD/RD；fixed findings 为空 | original-1、2、3 均为 SUCCEEDED / 1；fixed 为 SUCCEEDED / 0 | 两轮 `full/gate/results.csv`、各场景 `evidence/findings.json` | PASS |

待复核问题及对应日志：

本次已审阅范围内未发现待修复问题。新增测试使用人工构造的小型 trace，验证跨行 `openat` 的还原、依赖识别和证据行号保留；未覆盖所有系统调用格式、复杂并发进程树或所有 strace 输出变体。

RD 结论只适用于本次完整门禁的构建配置与配方任务读取观察，不表示 `unused.h` 在所有构建配置下均无用途。两轮原始证据已分别归档，归档路径和 SHA-256 见个人实验报告。
