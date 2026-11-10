# E7 专项审阅：CLI 退出策略与集成

审阅人刘馨雅（241250088）。

| 检查项 | 输入与预期 | 实际观察 | 代码位置与证据 | 判定 |
| --- | --- | --- | --- | --- |
| CLI 检测到 MD，省略门禁开关 | 成功报告含一条 MD，退出 0，JSON 保留报告 | 本地定向测试通过 | `services/buildchecker/buildchecker/cli.py` 的 `main` | PASS |
| CLI 检测到 MD，启用门禁开关 | 同一报告，退出 1，JSON 与前次相同 | 本地定向测试通过 | `services/buildchecker/tests/test_e7_241250088.py` | PASS |
| 个人版本镜像复验 | 镜像内定向测试通过，完整门禁八项通过 | 定向 1 项通过，服务 20 项通过，门禁退出 0 且八项通过 | `work/e7-241250088-personal-qfitdKaY/` 下的 `personal-test.log`、`build/unit-tests/stdout.log` 和 `full/gate/results.csv` | PASS |
| 集成与 CI | 核对整合版本的门禁，保留同一演示 PR 的失败、拒绝与恢复记录 | 待执行 | 见小组验证索引 | PENDING |
