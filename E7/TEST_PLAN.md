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
