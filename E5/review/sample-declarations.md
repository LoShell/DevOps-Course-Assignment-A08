# E5 专项审阅：样本与声明依赖

审阅人：邱莉扉，241250097。  
日期：2026-10-31。  
范围：样本与 E3 衔接、源码、Make 声明、人工 MD/RD。  
状态：本人样本、声明、人工 MD/RD 及 E3 衔接核对完成。

## 对象

- 完整运行 SHA：`25e57544fe7b98e496aeea8681e5cfaca128a255`。
- 本人仓库：`/root/241250097/buildchecker`。
- 分支：`a08/241250097/e5-e6`。
- 本次测试前后、填写文档前，工作区检查均无改动；本记录及个人记录在测试结束后填写，尚未提交。
- 已核对成员：本人 241250097；另只读核对了仓库保留的 E3 历史材料，尚未核对其他成员本次 E5 证据。
- E5 源码：统一版本的 `fixtures/md-rd/main.c`、`config.h`、`unused.h`、`Makefile`。
- E3 对照材料：`E3/fixtures/md-rd/`、`E3/oracle/md-rd.expected.json` 及其引用的历史实测与确认记录。
- 本人记录：`E5/records/241250097.md`。
- 本次实际运行目录：`work/e5-run-20261031-134307`。

## 观察和结论

下表 trace 和数据库路径均相对于本次运行目录的 `evidence/`。

| 检查点 | 实际观察 | 文件 / PID / 行号等依据 | 结论或问题 |
| --- | --- | --- | --- |
| 样本输入 | main.c 包含 config.h，VALUE=1；unused.h 未被 main.c 包含 | 本人查看四个输入文件；`fixtures/md-rd/main.c:2–3`、`config.h:1` | 样本符合本次指南描述 |
| main.o 声明 | main.o: main.c unused.h | `make-db.txt:1061`；源码 `fixtures/md-rd/Makefile:6` | 声明包含 main.c、unused.h，未包含 config.h |
| main.o 实际输入 | cc1 成功只读打开 main.c、config.h | PID 16，`t.16:67`、`t.16:580` | 两者均为实际项目输入 |
| 输入与目标归属 | make 派生编译驱动，编译驱动创建 cc1 和 as，as 创建 main.o | `t.14:55`、`t.15:1,64,84`、`t.17:23` | 输入与 main.o 属于同一次编译任务 |
| unused.h 的使用 | 仅发现 make 检查文件状态 | PID 14，`t.14:46`；本次完整 trace 的 unused.h 搜索结果 | 不将状态检查计为实际读取 |
| main.o 的 MD/RD | 实际输入与声明依赖不一致 | 上述 trace 与数据库 | MD=config.h，RD=unused.h |
| app 声明及实际依赖 | 声明依赖 main.o；ld 读取 main.o 并创建 app | `make-db.txt:609`；PID 20，`t.20:71,82–83` | 项目依赖一致，MD/RD 为空 |
| 程序结果 | 输出 1，E5 和 runner 退出码均为 0 | `program-output.txt`、runner 退出码及控制台记录 | 本次运行成功 |
| E3 衔接 | 已对照源码、声明、oracle 及引用的历史实测记录 | 见下文 E3 衔接核对 | 故障机制一致，样本源码、路径与输出不同 |
| 跨成员对照 | 尚未查看另一成员本次 E5 同基准的原始证据 | 待小组协调核对 | 不宣称已完成至少两人的结果对照 |

### 人工依赖集合差

| 目标 | 实际项目依赖 | Make 声明依赖 | MD：实际减声明 | RD：声明减实际 |
| --- | --- | --- | --- | --- |
| main.o | main.c、config.h | main.c、unused.h | config.h | unused.h |
| app | main.o | main.o | 无 | 无 |

成功打开的依据：

- `t.16:67`：`openat(AT_FDCWD, "main.c", O_RDONLY|O_NOCTTY) = 3`。
- `t.16:580`：`openat(AT_FDCWD, "config.h", O_RDONLY|O_NOCTTY) = 4`。
- `t.17:23`：`openat(AT_FDCWD, "main.o", O_RDWR|O_CREAT|O_TRUNC, 0666) = 3`。
- `t.20:71`：`openat(AT_FDCWD, "app", O_RDWR|O_CREAT|O_TRUNC, 0666) = 3`。
- `t.20:82–83`：两次只读打开 main.o，分别返回 7、8。

这些记录的返回值均为非负文件描述符。已查看关键原始 trace 上下文，不以 grep 命中、stat/access 或失败打开代替成功打开证据。本次跟踪类别为 `%file,%process`，不将上述记录描述为逐字节 read/write 跟踪。

编译进程关系为 make（PID 14）→ cc（PID 15）→ cc1（PID 16）及 as（PID 17）。因此，将 cc1 的源码和头文件输入，与 as 生成的 main.o 归属于同一次编译任务。

链接进程关系为 make（PID 14）→ cc（PID 18）→ collect2（PID 19）→ ld（PID 20）。ld 成功只读打开 main.o 并创建 app。

依赖表只保留项目文件。系统头文件、工具链文件及编译临时文件不纳入项目源码依赖集合。

## E3 样本衔接核对

### 材料与版本

本次只读核对了：

- `E3/fixtures/md-rd/README.md`
- `E3/fixtures/md-rd/src/main.c`
- `E3/fixtures/md-rd/include/common.h`
- `E3/fixtures/md-rd/include/config.h`
- `E3/fixtures/md-rd/include/unused.h`
- `E3/fixtures/md-rd/Makefile`
- `E3/oracle/md-rd.expected.json`
- `E3/evidence/md-rd/oracle-review-20261006-132502/REVIEW.md`
- `E3/evidence/md-rd/oracle-review-20261006-132502/run/observations.json`

E3 材料记录的样本提交为 `8a9cfc46d854e697fd397c1f6c579014e219144b`，历史运行的基础提交为 `60318cf03e7f988058160ccf422147cf2d424e04`。历史测试时样本处于未提交工作区，使用 source_sha256 记录测试文件，样本提交随后形成。

以上是历史材料的版本信息，不替代本次 E5 运行 SHA。本次未重新执行 E3。

### 源码和声明对照

| 项目 | E3 | 本次 E5 |
| --- | --- | --- |
| 对象目标 | build/main.o | main.o |
| 实际项目输入 | src/main.c、include/common.h、include/config.h | main.c、config.h |
| Make 声明输入 | src/main.c、include/common.h、include/unused.h | main.c、unused.h |
| MD | include/config.h | config.h |
| RD | include/unused.h | unused.h |
| 最终程序 | bin/demo | app |
| 初始输出 | 历史实测为 10 | 本次实测为 1 |

E3 的 `src/main.c:3–4` 包含 common.h 和 config.h，第 16 行使用 COMMON_VALUE 与 CONFIG_VALUE，初始值分别为 6 和 4。

E3 Makefile 第 5 行将 HEADERS 定义为 include/common.h、include/unused.h，第 14 行声明 `build/main.o: src/main.c $(HEADERS)`。因此遗漏实际使用的 config.h，同时多声明未使用的 unused.h。

E5 简化为平铺目录，移除 common.h，程序输出 VALUE=1。Makefile 第 6 行声明 `main.o: main.c unused.h`，仍保留“遗漏 config.h、多声明 unused.h”的故障设计。

结论：E5 延续 E3 的 MD/RD 故障机制，但不是原样复用 E3 源码，不能混用两次实验的路径、目标名称或输出值。

### E3 历史实测结果核对

已读取的 observations.json 状态为 PASS，14 项断言全部通过，18 条记录中的命令退出码均为 0。

| 场景 | 历史记录中的实际结果 | 支持的结论 |
| --- | --- | --- |
| 初始构建 | 程序输出 10，版本为 demo 1.0.0 | 初始样本可运行 |
| GCC 项目依赖 | 包含 src/main.c、include/common.h、include/config.h，不含 unused.h | 支持项目输入与 Make 声明对照 |
| CONFIG_VALUE 从 4 改为 5 后增量构建 | make 提示无需构建，对象未更新，输出仍为 10 | config.h 缺失声明导致过时产物 |
| 相同修改后干净重建 | 输出 11 | 证实前一步增量结果过时 |
| unused.h 仅修改注释 | 重新编译、链接，输出仍为 11 | unused.h 冗余声明导致不必要重建 |

历史实验由 Codex 执行，成员 2 随后确认人工 oracle。本次是对历史材料的只读核对，不声称本次亲手重新执行了 E3。

observations.json 中的 human review pending 是执行时快照，后续人工确认见 REVIEW.md；不改写历史记录。oracle 为人工预期结果，不是 BuildChecker 自动检测报告。

### 衔接结论及边界

E3 通过头文件变更后的增量构建、干净重建和编译行为，展示 MD/RD 的后果。本次 E5 通过 trace 的成功打开、进程归属和 Make 数据库，人工确认实际依赖与声明依赖的集合差。

两类证据支持相同的故障类型。本人已完成样本、源码、Make 声明、人工 MD/RD 及 E3 历史结果衔接核对。

本次未修改 E5 Makefile 或头文件，未验证 E5 修改头文件后的增量行为，未执行 E6。不能把 E3 的历史行为写成本次 E5 实测。

## 审阅范围、问题与后续事项

- 本记录区分了源码查看、本人 E5 实测及 E3 历史证据只读核对。
- 尚未核对另一成员本次 E5 同基准原始证据，E3 历史核对不能替代跨成员对照。
- 本次为小型、串行构建；未覆盖大型或并行构建场景。课程论文具体机制的完整对应尚未完成，不宣称完整复现论文。
- 原有归档早于 E3 衔接补充，更新后的文档及引用的 E3 必要材料需重新归档、下载备份。
- 组长 integration.md 的四人版本、依赖结论和归档整合由组长维护。
