# E7 验证计划

独立判定测试 6 项应全部通过。完整门禁应有 8 项 `passed=true`，整体退出 0。逐场景区分工具状态、工具退出码和门禁判定。

| 场景 | 预期结果 | 证据 |
| --- | --- | --- |
| unit-tests | 当前服务测试全部通过，退出 0 | pytest 日志 |
| original-1、original-2、original-3 | 各为 SUCCEEDED / 1，三次精确检出 MD(main.o, config.h) 与 RD(main.o, unused.h) | 各次 findings、trace_id、读取 trace 和 Make 数据库声明 |
| fixed | SUCCEEDED / 0，findings 为空，仅 Makefile 输入哈希变化 | findings、输入哈希 |
| build-failed | FAILED / 1，CHECK_FAILED，真实编译失败 | findings、构建日志 |
| unsupported | FAILED / 1，UNSUPPORTED，构建成功 | findings、构建日志、输入副本 |
| timeout | TIMED_OUT / 1，TIMEOUT | findings、预算和超时日志 |

每人另补至少一项测试，写明现有覆盖、测试输入、预期和实际。重建包含该测试的镜像，保存定向测试与完整门禁结果。服务测试数量按实际版本填写。

## 个人测试题目

| 学号 | 新增输入 | 预期断言 |
| --- | --- | --- |
| 241250088 | 调用 CLI，通过 mock 返回同一份含一条 MD 的 `SUCCEEDED` 报告，分别传入和省略 `--fail-on-findings` | 启用开关返回 1，省略返回 0。两次标准输出均保留相同的状态和 findings |
| 241250097 | 给 `declaration_graph` 一段带行号的 Make 数据库，规则含 `./unit.o: src/../needed.h` | 目标和依赖分别归一为 `unit.o` 和 `needed.h`。断言证据的文件名、行号和原声明 |
| 241250071 | 给 `execution_graph` 一组微型进程 trace，将成功读取 `needed.h` 的 `openat` 拆成 unfinished/resumed 两行 | 仍识别该读取，`unit.o` 的依赖集合精确等于 `unit.c` 和 `needed.h`，证据可回查该读取 |
| 241250076 | 给 `full_check` 一个已含旧日志的输出目录，mock 执行函数监测调用 | 拒绝复用该目录，命令执行次数为零，旧日志的字节及输出目录内容一致 |
