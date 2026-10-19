# E4 A 组冒烟与 E3 样本衔接审阅

- 审阅人：邱莉扉（241250097）
- 审阅日期：2026-10-19
- 本次运行源码 SHA：`4c1ff6caf40fc4f1d90b730cbc2477824a6d4576`
- 个人运行证据目录：`/root/241250097/buildchecker/work/20261018-161219/`
- 审阅方式：AI 辅助阅读本地样本及脚本，并核对本人提供的服务器 `smoke.json`。本次审阅未重新运行实验；源码 SHA、证据目录及运行前工作区干净的状态沿用 `E4/CONTRIBUTIONS.md` 中的记录。

## 1. 检查范围

以下路径均相对于仓库根目录：

- E3：`E3/fixtures/md-rd/src/main.c`、`include/common.h`、`include/config.h`、`include/unused.h`（后三项位于 `E3/fixtures/md-rd/` 下）、`E3/fixtures/md-rd/Makefile`、`E3/fixtures/md-rd/README.md`、`E3/scripts/run_md_rd.py`。
- E4：`fixtures/md-rd/main.c`、`fixtures/md-rd/config.h`、`fixtures/md-rd/unused.h`、`fixtures/md-rd/Makefile`、`services/buildchecker/buildchecker/smoke.py`、`services/buildchecker/buildchecker/cli.py`。
- 运行证据：上述个人目录中的 `smoke.json`，以本人提供的内容为核查依据。

E4 使用仓库根目录的 `fixtures/md-rd/`，与 `E3/fixtures/md-rd/` 是两个独立目录。

## 2. 样本依赖关系对照

| 检查项 | E3 样本 | E4 样本 |
| --- | --- | --- |
| 对象文件 | `build/main.o` | `main.o` |
| 源码实际包含的项目头文件 | `common.h`、`config.h` | `config.h` |
| Makefile 声明的项目头文件依赖 | `include/common.h`、`include/unused.h` | `unused.h` |
| 缺失依赖（MD，Missing Dependency） | `include/config.h` | `config.h` |
| 冗余依赖（RD，Redundant Dependency） | `include/unused.h` | `unused.h` |
| 初始程序输出 | `COMMON_VALUE + CONFIG_VALUE`，即 `6 + 4 = 10` | `VALUE`，即 `1` |

两份样本都实际使用 `config.h`，但未在对应对象文件的构建规则中声明它；都声明了未被源代码包含的 `unused.h`。这是故意保留的实验故障结构，无需将其作为普通代码错误修复。E4 去掉了 E3 的 `common.h`、版本参数和部分目录结构，是具有相同依赖故障结构的简化样本。

## 3. 本次 E4 冒烟结果

| 字段 | 实际观察 | 核查结论 |
| --- | --- | --- |
| `fixture` | `fixtures/md-rd` | 使用了 E4 根目录样本 |
| `make_exit_code` | `0` | 构建成功 |
| `make_output` | `cc -c main.c -o main.o`；`cc main.o -o app` | 完成编译与链接 |
| `app_output` | `"1"` | 与 `config.h` 的 `VALUE 1` 一致 |
| `trace_lines` | `1206` | 已产生跟踪记录；行数无需固定 |
| `config_h_opened` | `15    openat(AT_FDCWD, "config.h", O_RDONLY\|O_NOCTTY) = 4` | 观察到成功打开 `config.h`；返回值 `4` 为文件描述符 |
| `unused_h_opened` | `[]` | 未匹配到打开 `unused.h` 的操作，符合预期 |
| `passed` | `true` | 冒烟脚本通过 |

工具版本为 GNU Make 4.4.1、GCC 14.2.0（Debian 14.2.0-19）、strace 6.13。本次只核对本人提供的结果，未独立读取其他成员的证据；跨成员版本及结果一致性以组长汇总记录为准。

`unused_h_opened` 为空仅说明未匹配到该文件的 `open/openat` 操作，不代表 Make 未查询其存在性或时间戳，也不能单凭此字段完成 RD 检测。

## 4. 验证方式与范围

E3 的 `run_md_rd.py` 在临时副本中检查初始输出为 `10`，并通过 `gcc -MM` 核对编译器依赖。随后将 `CONFIG_VALUE` 从 `4` 改为 `5`，检查增量构建未更新对象文件、输出仍为 `10`，而清理后重新构建输出为 `11`；再只修改 `unused.h` 注释，检查对象文件发生无必要的重新编译且输出仍为 `11`。脚本还检查原始样本文件未被修改。以上是本次阅读确认的脚本逻辑，本次未重新执行 E3。

E4 的 `smoke.py` 将样本复制到临时目录，用 `strace -f` 跟踪一次 `make`，随后运行 `./app`，记录头文件打开操作和程序输出。它不修改头文件，也不比较增量构建与干净构建，因此不能替代 E3 的 MD/RD 行为验证。

当前 E4 自动通过条件是 `code == 0 and bool(config)`，即构建成功且匹配到 `config.h` 的打开记录。匹配函数未检查该操作是否成功，自动通过条件也未检查程序输出、程序退出码或 `unused.h` 的打开情况。本次已额外人工核对 `config.h` 打开返回值为非负数、程序输出为 `1`、`unused_h_opened` 为空，均符合预期；程序退出码未单独保存在结果中。

## 5. 审阅结论

本次代码核查确认：E4 样本保留了与 E3 相同的 MD/RD 设计，两个样本目录相互独立。本人提供的 E4 冒烟结果符合预期，支持本次构建、程序运行和文件跟踪环境可用的结论。

本次核查未发现需要修改样本的事项。冒烟通过不表示已经实现 MD/RD 检测算法，也不表示本次已验证修改头文件后的增量构建行为；按进程归属分析文件访问、比较声明依赖等工作属于后续实验范围。
