# E6 专项审阅：full_check、报告校验与证据完整性

审阅人：叶原原（241250076）；日期：2026-11-06（北京时间）。

状态：本人 baseline、personal 两轮实测与电脑原始证据复核完成，提交组长审阅。个人 PR：PR_LINK。

负责机制：`full_check` 的参数检查、采集流程及报告边界；验证精确发现、修复输入哈希和证据归档。

## 输入、实现和实际观察

| 输入/版本 | 函数及关键位置 | 实际观察 | 图/报告字段与原始证据 | 结论 |
| --- | --- | --- | --- | --- |
| baseline：`aff4eba7dca7a09a372d1264375d9fe9cd11354f` | `fullcheck.py:343`，`full_check` | 自检通过，构建、服务单测均 0；15 passed | `work/e6-baseline-20261106-002801/meta/`、`build/` | 符合固定基线 |
| personal：`bd00e74011c94d3fb0d3b300f17a35ca4d049564` | 同函数；本人新增测试 | 重建成功，16 passed，无跳过 | `work/e6-personal-20261106-002927/build/unit-tests/stdout.log` | 本人边界测试进入服务镜像并通过 |
| 两轮原始 fixtures | 参数校验后复制输入、clean、strace、analyze | status=SUCCEEDED，clean/build=0，入口1 | 两轮 `before/evidence/findings.json`、runner 退出码 | 依赖错误与采集失败可区分 |
| 两轮修复 fixtures | `scripts/lab_cloud.py` 的 e6 `--fixed` 分支 | 独立副本替换声明，findings=[]，入口0 | 两轮 `after/fixture/Makefile`、`after/evidence/` | 原始副本保留，修复不改生产源码 |
| 两轮报告 | `scripts/verify_e6_evidence.py:15` 起 | 精确两条发现、修复为空、输入集合一致且仅 Makefile 哈希变化 | 两轮 `meta/verification.json`，passed=true | 保存报告校验通过；原始记录另行核对 |

`full_check` 先拒绝非 POSIX 平台，再 resolve 路径并检查输入存在、输出不能位于输入内部、输出必须为空以及符号链接等边界。输入内输出检查位于创建证据目录、复制项目及 execute 调用之前。采集开始后按 clean、strace 构建、分析和写报告的顺序进行，只有成功完成才能标为 SUCCEEDED。

参数检查抛出的 ValueError 位于报告采集 try 块之前，嵌套输出路径应直接被拒绝，不应被视作“空 findings 的成功报告”。本人的测试同时检查异常与无副作用。

## 本人测试

- 文件：[test_e6_241250076.py](../../services/buildchecker/tests/test_e6_241250076.py)；个人代码 SHA：`bd00e74011c94d3fb0d3b300f17a35ca4d049564`。
- 输入：临时 fixture 内的 Makefile、unit.c；输出为 fixture/result。调用前计算所有输入文件的相对路径及 SHA-256。
- 执行：调用真实 full_check，仅 mock `buildchecker.fullcheck.execute`。
- 断言：ValueError 包含 `Output must be outside`，execute 未调用，输入清单和哈希不变，result 不存在。
- 实际结果：Linux 个人镜像重建后 `16 passed in 0.20s`。Windows 下跳过此项不计作正式通过，本次服务器测试没有跳过项。
- 贡献范围：一个新增测试文件，覆盖采集入口路径边界；没有修改参考实现、公共资源配置或其他成员测试。

## 原始与修复结果

两轮的实际图精确为 `{app→main.o, main.o→main.c, main.o→config.h}`。原始声明图精确为 `{app→main.o, main.o→main.c, main.o→unused.h}`，修复声明图与实际图一致。所有图均恰好三条边，observed_targets 为 `[app, main.o]`。

已分别核对两轮原包，以下行号在本次两轮中相同，均相对各轮 `before/evidence/`：

- `trace/t.14:67` 成功只读打开 main.c；`trace/t.14:579` 成功只读打开 config.h，返回 4。
- `trace/t.15:23` 创建 main.o，返回 3；进程 14、15 的父进程均为 13，job_pid 均为 13。创建记录为 `t.12:55`、`t.13:64,84`。`t.15:5` 为成功执行 as，前四条 execve 失败未当作成功。
- `make-db.txt:1053` 为 `main.o: main.c unused.h`；unused.h 在全部 trace 中只有 `t.12:46` 的 newfstatat，没有 openat，不能将状态查询当作读取。
- `trace/t.18:82` 成功只读打开 main.o；`make-db.txt:601` 声明 app: main.o；链接进程 16→17→18 的创建关系也已核对。
- 修复后的声明位于各轮 `after/evidence/make-db.txt:1045`；实际输入副本重新计算 SHA-256 后，仅 Makefile 改变，三份 C/头文件不变。

两轮 findings 中的 MD 证据将 cc1 的 config.h 打开与 as 的 main.o 输出联系到同一编译作业；RD 以声明和本次未观察到成功读取为依据。结论与本人 [E5 人工记录](../../E5/records/241250076.md) 一致，PID 和行号使用本次 E6 记录。

## 校验范围与证据完整性

`verify_e6_evidence.py` 检查保存报告的 status、clean/build、精确两条 findings、修复空结果及输入哈希变化。它不会独立验证 trace、图、进程列表或输入文件的实际字节。因此补充读取两轮原始文件，逐条核对图边证据行、成功返回值、进程创建关系及真实文件哈希；最终包保存 `validation/raw-evidence-audit.json` 和复核脚本。

两轮四份 source-commit 均与对应运行 SHA 一致，阶段间工作区干净。构建包装入口、底层构建和单测退出码均为0，before 的包装入口与 runner 为1，after 与报告校验为0。命令结束后立即保存退出码，完整空日志也按原样保留。

同名个人镜像的两轮 ID 不同，已分别保存 inspect 和工具链，并与对应构建输出比对；完整 ID 见 [个人报告](../records/241250076.md)。输入挂载只读，输出单独挂载，运行容器无网络。

原始快照在每轮校验通过后立即生成，下载包及其 .sha256 后本机计算一致：

| 轮次 | 服务器 `/root/devops-submissions/241250076/` 下文件名 | SHA-256 |
| --- | --- | --- |
| baseline | `A08-241250076-E6-baseline-20261106-002806.tar.gz` | `a62ff53cc297d2d9fe02c29abcd4d77287cde6a61acd2465103651429845f746` |
| personal | `A08-241250076-E6-personal-20261106-002930.tar.gz` | `a22a4808524ee4b89d35e6422499a951de98c4926acd7bd1fd393379600eb037` |

本机备份目录为 `D:\MyDocument\Download\DevOps-Course-Assignment-A08\work\E6-backup-241250076-20261106\`。定稿源码、报告、两轮证据及复核材料另收集为 `A08-241250076-E6-final-20261106.tar.gz`，最终文档 SHA、PR 和目录说明见包内 DELIVERY.md，最终哈希由配套 .sha256 提供。

## 同版本对照与交付边界

本次对照对象为本人两轮原包：baseline 使用组长固定 SHA，personal 只增加本人测试，实际/声明图、findings 及修复输入变化一致。没有将其他成员文档或 E5 旧记录作为本人的 E6 实测。

组长负责后续测试合并、集成 SHA 和集成复验；本次没有执行 integrated 轮，也没有完成其他成员原包抽查或课程平台上传。个人结果、验收表和专项审阅通过个人 PR 交付。

AI 协助代码阅读、测试编写、命令执行、原始证据复核及文字整理；本人提供 SSH 登录并确认服务器运行时段。
