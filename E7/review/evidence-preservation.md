# E7 专项审阅：旧证据保留

审阅人：叶原原（241250076）；日期：2026-11-13（北京时间）。

基线 SHA：`3a0ae35b27e783c480f66412b3e4f53802c6be68`；个人测试 SHA：`eef6c4a0ec5da3d4b02995ef21eb7b3a283b6479`。生产实现两轮相同，代码位置为 `services/buildchecker/buildchecker/fullcheck.py` 的 `full_check`（第 343 行起）。

| 检查项 | 输入与预期 | 实际观察 | 代码位置与证据 | 判定 |
| --- | --- | --- | --- | --- |
| 已有非空输出拒绝 | 有效 fixture 外的输出目录含旧日志；拒绝复用 | 抛出 ValueError，消息包含 fresh empty output directory | `fullcheck.py:351`；个人测试 | PASS |
| 外部命令零调用 | mock execute；预期不执行 clean 或 traced build | assert_not_called 通过 | `test_e7_241250076.py`；个人轮 `personal-test.log` | PASS |
| 旧证据原样保留 | 含 CRLF、NUL、非 UTF-8 的 clean.log、旧 findings、嵌套 trace 和空目录 | 所有相对路径、类型和文件原始字节前后完全相同；输出根目录仍存在 | 个人测试递归快照断言 | PASS |
| 拒绝发生在副作用之前 | 非空检查应早于 mkdir、copytree 和执行函数 | 第 351 行检查并抛出，第 360 行后才创建输出及采集 | `fullcheck.py:351`、`:360`、`:369` | PASS |
| 补充原有覆盖 | E6 覆盖输出位于 fixture 内部；E7 覆盖 fixture 外的已有证据目录 | 使用有效独立 fixture，命中非空检查；生产代码无修改 | `test_e6_241250076.py`、`test_e7_241250076.py` | PASS |
| 版本及镜像 | 两轮分别记录 SHA、干净状态、镜像 ID 和依赖锁 | 两轮开始及结束状态均为空，镜像 ID 与各轮 inspect 一致 | 各轮 source-commit、source-status、image-id、toolchain.lock | PASS |
| 实际容器验证 | 基线 19 项；个人轮增加 1 项；独立判定及完整门禁通过 | 19→20，个人定向退出 0；两轮 oracle 6/6，gate 8/8、退出 0 | build/unit-tests、personal-test.log、full/gate | PASS |
| 原始证据回查 | findings、图边引用可回查，修复仅改变 Makefile | 两轮各自原始三次及 fixed 的引用逐行核对；fixture 哈希与报告一致 | [复核摘要](../validation/241250076-evidence-audit.json) | PASS |
| 故障场景语义 | 编译失败、不支持和超时均应以工具退出 1 明确报告 | CHECK_FAILED、UNSUPPORTED、TIMEOUT 符合预期，门禁三项通过 | 各轮 full/gate 下对应 findings、command 和日志 | PASS |
| 独立归档及本地校验 | 两轮分别归档并下载，电脑 SHA-256 等于服务器校验值 | 两个原始包校验一致，解压与内容复核通过 | [报告归档表](../records/241250076.md)、复核摘要 | PASS |

服务器证据目录为 `/root/241250076/buildchecker/work/e7-241250076-baseline-0p7BTMgO/` 与 `work/e7-241250076-personal-nBIdmim1/`（后者同仓库根目录）。电脑备份位于 `work/E7-backup-241250076-20261113/`，原始文件不进入 Git。

待复核问题：本专项未发现阻碍个人交付的问题。测试验证当前非空目录的一次调用，未覆盖并发竞争、符号链接输出或权限异常。小组集成和 CI 门禁闭环由组长后续审阅执行。
