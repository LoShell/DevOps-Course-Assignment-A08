# E6 专项审阅：实际图与进程归属

审阅人、学号、日期：范从钰，241250071，2026-11-04。
负责机制：`load_processes` 与 `execution_graph`；实际图、进程归属和 `rename` 最终产物识别。

| 输入/版本 | 函数及关键位置 | 实际观察 | 图/报告字段与原始证据 | 结论 |
| --- | --- | --- | --- | --- |
| baseline：`aff4eba7dca7a09a372d1264375d9fe9cd11354f` | `load_processes`；`execution_graph` | 原始样例构建成功，观测目标为 `main.o`、`app`。`main.o` 实际读取 `main.c`、`config.h`。 | `work/e6-baseline-20261104-184801/before/evidence/actual-graph.json`；`findings.json` 中 `config.h` 读取证据为 `trace/t.15` 第 579 行，`main.o` 输出证据为 `trace/t.16` 第 23 行。 | 通过。实际图能从成功读写的系统调用中识别项目内依赖和目标。 |
| baseline：`aff4eba7dca7a09a372d1264375d9fe9cd11354f` | `execution_graph` 与 `analyze` | Make 声明 `main.o: main.c unused.h`，与实际图对比后得到一项 MD 和一项 RD。 | `before/evidence/findings.json`；`make-db.txt` 第 1053 行；`meta/verification.json`。 | 通过。MD 为 `config.h`，RD 为 `unused.h`，发现项精确且数量为 2。 |
| 个人测试版本：`005b2e0dd67bdb1bc54ac6187561c5ac43b30739` | `execution_graph` 的 `rename` 分支 | 独立 trace 中，as 创建 `temporary.o`、读取该临时文件，再执行 `rename("temporary.o", "unit.o") = 0`。 | `services/buildchecker/tests/test_e6_241250071.py`。断言目标仅为 `unit.o`，依赖为 `unit.c`、`needed.h`，输出证据 `operation=rename`。 | 通过。临时产物被归属为同一作业的 produced 文件，不会作为最终目标的误报依赖。 |
| 个人测试版本：`005b2e0dd67bdb1bc54ac6187561c5ac43b30739` | `load_processes`、`execution_graph` | 新测试提交后重建服务镜像，完整测试通过。 | `work/e6-personal-20261104-190926/build/unit-tests/stdout.log`；结果为 `16 passed in 0.06s`。镜像 ID：`sha256:ac5d46bf8df652e59bdea7f0bdaf9559ab54f23a27be8e1d81861a8e93d2b02a`。 | 通过。新增测试已在服务镜像中实际执行。 |
| 个人测试版本：`005b2e0dd67bdb1bc54ac6187561c5ac43b30739` | `execution_graph`、修复复检 | 原始检测仍精确得到两项发现；修复副本复检后 findings 为空。 | `work/e6-personal-20261104-190926/before/evidence/findings.json`；`after/evidence/findings.json`；`meta/verification.json`。 | 通过。原始检测退出码为 1，修复复检退出码为 0，校验 `passed: true`。 |

## 本人测试

测试文件：`services/buildchecker/tests/test_e6_241250071.py`。
输入：独立的小型 syscall trace，包含 make → cc → cc1/as 的进程关系；cc1 成功读取 `unit.c`、`needed.h`；as 创建并读取 `temporary.o` 后将其重命名为 `unit.o`。
预期：只识别 `unit.o` 为最终目标；依赖精确为 `unit.c`、`needed.h`；输出操作标记为 `rename`；`temporary.o` 不会被作为依赖。
实际：单独单测通过；提交 SHA 为 `005b2e0dd67bdb1bc54ac6187561c5ac43b30739`；重建后服务测试 `16 passed in 0.06s`。
重建日志：`work/e6-personal-20261104-190926/build/`。

## 原始与修复结果

baseline 版本为 `aff4eba7dca7a09a372d1264375d9fe9cd11354f`，personal 版本为 `005b2e0dd67bdb1bc54ac6187561c5ac43b30739`。

两个版本的原始检测均显示：

- 实际图：`main.o` 读取 `main.c`、`config.h`；
- 声明图：`main.o` 声明 `main.c`、`unused.h`；
- 发现：`MISSING(main.o, config.h)` 与 `REDUNDANT(main.o, unused.h)`；
- 原始检测退出码：1。

两个版本的修复复检均显示：

- `findings` 为空；
- 校验 `passed: true`；
- `before_findings: 2`、`after_findings: 0`；
- `changed_inputs` 只有 `Makefile`；
- 修复复检退出码：0。

baseline 证据目录为 `work/e6-baseline-20261104-184801/`，personal 证据目录为 `work/e6-personal-20261104-190926/`。

## 同版本对照与待办

baseline 使用 15 项既有测试；个人版本新增本人测试后为 16 项测试，两种版本已分开保存运行证据和归档包。四人测试合并后的统一 E6_FINAL_SHA 验证、共同报告和整合审阅由组长后续安排。

个人归档：

- `/root/devops-submissions/241250071/A08-241250071-E6-baseline-20261104-185633.tar.gz`
- `/root/devops-submissions/241250071/A08-241250071-E6-personal-20261104-191510.tar.gz`
