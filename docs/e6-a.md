# A08 E6：自动依赖检测与修复复检

轨道：A（BuildChecker）；组长：刘馨雅（241250088）。
实验日期：2026-11-03 至 2026-11-06。
仓库：<https://github.com/LoShell/DevOps-Course-Assignment-A08>。

四人完成基线和个人新增测试后的两轮实验，个人成果通过 PR #11—#14 合入 `a08/e5-e6`。组长完成一次集成验证，19 项服务测试通过；原始检测精确发现两项依赖错误，修复后发现为空。

## 1. 输入与实现

样例为 `fixtures/md-rd/`，包含 Makefile、main.c、config.h、unused.h。main.c 包含 config.h，原声明为 `main.o: main.c unused.h`。修复副本将声明改为 `main.o: main.c config.h`。

核心实现位于 `services/buildchecker/buildchecker/fullcheck.py`：

| 函数 | 作用 |
| --- | --- |
| load_processes | 解析系统调用记录，建立进程关系 |
| execution_graph | 将同一构建作业的输入打开和输出产物归属到目标，生成实际图 |
| declaration_graph | 解析 Make 数据库、展开伪目标并检查依赖环，生成声明图 |
| analyze | 按目标计算实际依赖与声明依赖的集合差，生成 MD/RD 和证据索引 |
| full_check | 校验路径、复制输入、执行 clean 和 strace 构建、保存报告 |

E5 的[人工分析](e5-a.md)给出 main.o 缺失 config.h、冗余 unused.h，app 依赖 main.o。E6 自动检测得到相同结论，并完成修复复检。

## 2. 版本与分工

| 版本 | 完整 SHA | 用途 |
| --- | --- | --- |
| E6_BASE_SHA | aff4eba7dca7a09a372d1264375d9fe9cd11354f | 四人基线轮 |
| E6_FINAL_SHA | 9716ae3a20cae6ff8eda89d69733ab71d4a7b3e6 | 四项测试合并后的集成轮 |

| 成员 | 个人测试运行 SHA | 新增覆盖 | PR |
| --- | --- | --- | --- |
| 刘馨雅 241250088 | df409596099fc8f05d891c27e34bd230c7311335 | 依赖一致时发现为空，两图边集合精确一致 | [#14](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/14) |
| 邱莉扉 241250097 | 12f85dcbfc7ff58325f814c3c21c50962b0c6089 | 伪目标依赖环触发 Unsupported 及指定消息 | [#11](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/11) |
| 范从钰 241250071 | 005b2e0dd67bdb1bc54ac6187561c5ac43b30739 | temporary.o 重命名后只识别最终目标 unit.o | [#12](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/12) |
| 叶原原 241250076 | bd00e74011c94d3fb0d3b300f17a35ca4d049564 | 拒绝输入目录内的输出路径，执行次数为零，输入保持一致 | [#13](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/13) |

四项测试各放在 `services/buildchecker/tests/test_e6_学号.py`。各人基线轮 15 项、个人轮 16 项服务测试通过；集成轮 19 项通过。个人命令、镜像及证据目录见[贡献索引](../E6/CONTRIBUTIONS.md)。

## 3. 集成运行

执行目录：`/root/241250088/buildchecker`。
本轮 `R=work/e6-integrated-20261106-111142`。

服务器为 Ubuntu 22.04.5 LTS、x86_64、2 CPU、可见内存 1.7 GiB。自检 `problems=[]`，保留三项资源建议警告。沿用课程 2 GiB ECS 的最低可见内存 1.5 GiB 配置。

| 步骤 | 完整命令（R 为上述目录） | 实际结果 | 证据（相对 R） |
| --- | --- | --- | --- |
| 环境自检 | `python3 scripts/doctor.py --out "$R/meta/env.json"` | problems=[] | meta/env.json |
| 构建与服务测试 | `python3 scripts/course.py build --out "$R/build" --build-timeout 1200` | 入口、构建、单测均 0；19 passed in 0.25s | build/、meta/build-exit-code.txt |
| 原始检测 | `python3 scripts/course.py e6 --out "$R/before"` | 入口及 runner 为 1；SUCCEEDED；clean/build=0；精确两条发现 | before/、meta/before-exit-code.txt |
| 修复复检 | `python3 scripts/course.py e6 --fixed --out "$R/after"` | 入口及 runner 为 0；SUCCEEDED；findings=[] | after/、meta/after-exit-code.txt |
| 报告校验 | `python3 scripts/verify_e6_evidence.py --before "$R/before/evidence/findings.json" --after "$R/after/evidence/findings.json"` | 退出 0；passed=true；changed_inputs=[Makefile] | meta/verification.json、meta/verification-exit-code.txt |

集成镜像标签为 `course1027-buildchecker:241250088`，保存的完整 ID 为 `sha256:6ec1ac4b718c6362529a320aa2922f430985d2b8472844a73445d0cc90e66e1b`。构建输出与 meta 中的镜像 inspect 一致。meta、build、before、after 四处保存的源码 SHA 均为 E6_FINAL_SHA，构建前工作区干净。

## 4. 图、发现与修复

| 阶段 | main.o 实际依赖 | main.o 声明依赖 | app 依赖 | 发现 |
| --- | --- | --- | --- | --- |
| 原始 | main.c、config.h | main.c、unused.h | 实际与声明均为 main.o | MISSING(main.o, config.h)、REDUNDANT(main.o, unused.h) |
| 修复 | main.c、config.h | main.c、config.h | 实际与声明均为 main.o | 空 |

下表路径相对集成轮 `before/evidence/`：

| 关系 | 原始位置 | 说明 |
| --- | --- | --- |
| main.o→main.c | trace/t.14:67 | cc1 成功只读打开 main.c |
| main.o→config.h | trace/t.14:579；trace/t.15:23 | cc1 成功只读打开 config.h；同一编译作业的 as 创建 main.o |
| main.o 声明 | make-db.txt:1053 | main.o: main.c unused.h |
| app→main.o | trace/t.18:82；make-db.txt:601 | ld 成功只读打开 main.o，声明相同 |

编译作业为 PID 13，cc1 为 14、as 为 15；链接作业为 PID 16，collect2 为 17、ld 为 18。修复后 main.o 的正确声明位于 `after/evidence/make-db.txt:1045`。

Makefile 的 SHA-256 由 `fd1dcd76a0bd9678351a1503941a5a875351455d4a6879e76af0af0b6c64772f` 变为 `128069c949b0239e3377f320d51498c2b37a317c602d8755d573a283e1f400ae`。main.c、config.h、unused.h 保持一致，fixture 与 evidence/project 的实际字节均已核对。

原始 trace_id 为 `e6-b997540ba6294d1eb7e8dd88e406c469`，修复 trace_id 为 `e6-e643ecd4f97c4d39840ad57b72208f48`。

## 5. 原包核验与同基线对照

集成原包含 89 个文件，每次检测各含 7 份 trace。已重新分析 trace 与 Make 数据库，findings、实际图、声明图和进程记录均与保存文件一致。

另对照 088、097 两人的 E6_BASE_SHA 原包：四处源码 SHA 一致，测试均为 15 项通过；对应输入哈希、图边集合、精确 MD/RD 和修复结果一致。两人的原始记录重新分析均与各自报告一致。

| 原包 | SHA-256 |
| --- | --- |
| A08-241250088-E6-baseline-20261103-160245.tar.gz | 9e3d1afc347199d8ece8420cd354f08d04d65624a5aada94509bc8d2e8434870 |
| A08-241250097-E6-baseline-20261104-110114.tar.gz | 356fb57b2bc3dced1b28ed3df02d85bdf102e01c8a44acae5b25ecba8ae92a62 |
| A08-241250088-E6-integrated-20261106-111659.tar.gz | 5787c2ba5d5fdda31f2170e3cc77729c560f91fd0b82e511db5b5386da845505 |

原包及配套 .sha256 已下载到组长电脑 `Lab/学号/E6/`。核验摘要见 [集成核验](../E6/validation/integrated-audit-20261106.json)和[同基线对照](../E6/validation/baseline-comparison-20261106.json)。

## 6. 成果索引

- [四人报告、验收表与专项审阅](../E6/CONTRIBUTIONS.md)。
- [组长整合审阅](../E6/review/integration.md)、[集成验收表](../E6/records/integrated-验收记录.csv)。
- 源码：`services/buildchecker/buildchecker/fullcheck.py`；四项新增测试：`services/buildchecker/tests/test_e6_学号.py`。
- 完整原始证据：各人 baseline、personal 目录，以及组长 integrated 目录。
- [提交清单](../E6/SUBMISSION.md)、[AI 使用记录](../E6/AI_USAGE.md)。

剩余交付：提交收尾文档，创建 E6 阶段 PR 合入 main，制作独立提交包并上传课程平台。
