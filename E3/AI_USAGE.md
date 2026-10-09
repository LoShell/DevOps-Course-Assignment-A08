# A08 E3 AI 使用记录

| 日期 | 使用场景 | AI 建议 | 人工处理 | 关联文件 | 验证方式 |
|---|---|---|---|---|---|
| 2026-09-30 | E3 范围、项目结构和协作流程梳理 | 根据 E3 课件区分测试基线与后续工具实现，并起草单分支、分目录协作方案 | 人工对照课件和 E2 契约，修正项目来源、跨组依赖和 B08 示例含义后采用 | `README.md`、`WORKFLOW.md`、`adr/0001-baseline-project-design.md` | 对照 E3 课件、E2 评审记录和双方沟通结果 |
| 2026-10-05 | C0 项目与验证证据准备 | 起草 C 源码、Makefile、Dockerfile、样本说明和验证记录，并协助同步进度文档 | 刘馨雅确认项目约束，在 Ubuntu 24.04 宿主机和容器中执行构建、运行及依赖检查，提交 C0 并固定 `e3-c0` 标签；AI 未代替真实运行 | `fixtures/incremental/`、`evidence/environment/c0-ubuntu-24.04.md`、`README.md`、`BACKLOG.md`、`CONTRIBUTIONS.md` | `make clean && make -j2`、`./bin/demo --version`、`./bin/demo`、`gcc -MM`、`docker build`、`docker run`；输出见 C0 验证记录 |
| 2026-10-06 | 固定 MD/RD 基线与 oracle 验证 | 辅助编写样例、复现脚本和文档，并执行本地及容器测试 | 邱莉扉确认任务范围，审阅测试输出并核对 MD/RD 判定依据，确认 oracle 通过 | `fixtures/md-rd/`、`oracle/md-rd.expected.json`、`scripts/run-md-rd.sh`、`scripts/run_md_rd.py`、`evidence/md-rd/` | Ubuntu 24.04 环境验证通过；容器复核 14 项断言通过，记录见 `evidence/md-rd/oracle-review-20261006-132502/REVIEW.md` |
| 2026-10-07 | C1 新增头文件样本与增量证据 | 辅助构造 `feature.h` 缺失声明场景、起草 oracle 和证据，Codex 在授权工作区执行验证命令 | 范从钰提交 C1 源码与证据，并修订环境说明；人工 oracle 的确认由组长于 2026-10-09 转述，未把代理执行写为成员手动执行 | `fixtures/incremental/include/feature.h`、`fixtures/incremental/src/main.c`、`oracle/incremental.expected.json`、`evidence/c1/20261007T143349+0800/` | Ubuntu 20.04.6 WSL2：干净构建 12、改动头文件后增量 12、干净重建 13；命令及退出码见 C1 证据 |
| 2026-10-08 | 成员 4 C2 构造、容器实验、配置编号与交付文档 | 增加 `-DMODE=7`，编写宿主机 Python 复现脚本；根据真实日志起草 C2 oracle，记录不同配置编号和 E2 对接限制 | 叶原原确认实施方案、容器环境、分别记录配置编号及仅本地提交；Codex 实际执行命令，首次导出校验因 Git CRLF 转换失败后修复并重跑；未声称成员本人手动执行，C2 人工 oracle 确认仍待完成 | `fixtures/incremental/Makefile`、`scripts/run_incremental.py`、`oracle/incremental.expected.json`、`evidence/c2/`、`evidence/failures/`、进度与贡献文档 | Ubuntu 24.04 容器：`make clean`、`make -j2`、仅替换 Makefile 后 `make -j2`、再次干净重建、`./bin/demo`、`gcc -MM`、`make -pn`、`sha256sum`、`stat`；最终运行 48 条命令退出码均为 0，37 项断言通过，3 项异常处理检查通过；详见 `evidence/c2/20261008T201035798727+0800/` |
| 2026-10-09 | E3 文档收尾与贡献追溯 | 对照 Git 提交、三枚远端标签、oracle 和实验记录，起草状态更新与审阅元数据 | 组长确认两位负责人分别完成 C1/C2 人工 oracle 核对；保留历史日志的原始执行者和当时状态，综合复现及接口策略仍记为待办 | `README.md`、`BACKLOG.md`、`CONTRIBUTIONS.md`、`WORKFLOW.md`、`oracle/incremental.expected.json`、`oracle/incremental-review-20261009.md` | `git log`、`git show`、远端标签核对、JSON 解析、证据目录与文档交叉检查 |

后续使用 AI 生成或修改源码、Makefile、Dockerfile、oracle 或脚本时，应追加记录，
并写明人工验证命令和结果。AI 输出不能代替真实实验日志。
