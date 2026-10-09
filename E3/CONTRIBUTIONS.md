# A08 E3 个人贡献与版本追溯记录

## 成员信息

| GitHub 用户名 | 姓名 | 学号 |
|---|---|---|
| `LoShell` | 刘馨雅 | 241250088 |
| `autumn123321` | 邱莉扉 | 241250097 |
| `FanCongyu` | 范从钰 | 241250071 |
| `Yevhen277` | 叶原原 | 241250076 |

## 贡献记录

| 姓名 | 负责内容 | 关联文件 | Commit SHA | 验证记录 |
|---|---|---|---|---|
| 刘馨雅 | E3 骨架与分工、C0 项目、环境验证和进度文档；最终综合检查待完成 | `README.md`、`WORKFLOW.md`、`fixtures/incremental/` 的 C0 部分、`evidence/environment/c0-ubuntu-24.04.md` | 骨架 `ae42159001fc4a289e10785a4c7e172ced89ecdf`；分工 `e717c3737773071e527593e2446707396adf90e1`；C0 `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`（`e3-c0`）；证据 `aa28d538e3fbd14d8e58fadefe31e6fdcd1ea049`；进度 `60318cf03e7f988058160ccf422147cf2d424e04` | Ubuntu 24.04 宿主机与容器构建通过；`e3-c0` 指向 C0 提交，见 `evidence/environment/c0-ubuntu-24.04.md` |
| 邱莉扉 | 固定 MD/RD 样本、复现脚本与证据、人工 oracle 审阅 | `fixtures/md-rd/`、`oracle/md-rd.expected.json`、`scripts/run-md-rd.sh`、`scripts/run_md_rd.py`、`evidence/md-rd/` | 实现与证据 `8a9cfc46d854e697fd397c1f6c579014e219144b`；样例 SHA 补录 `2246d962fd76841ae556fd11e7cb0c8da241044f` | Ubuntu 24.04 容器复核 18 条命令、14 项断言通过；2026-10-06 确认 oracle，见 `evidence/md-rd/oracle-review-20261006-132502/REVIEW.md` |
| 范从钰 | C1 新增 `feature.h` 读取但遗漏 Make 声明，整理实验与 oracle；验证命令由 Codex 代执行 | `fixtures/incremental/include/feature.h`、`fixtures/incremental/src/main.c`、`oracle/incremental.expected.json` 的 C1 部分、`evidence/c1/20261007T143349+0800/` | 源码 `4b70cabad1be8f6e98ee90ed9c5803b7aa793253`（`e3-c1`）；证据 `c3ed2ff2a3d82481b2c1c2e39ba851d84238ef8e`；说明修订 `90ace4c0d930c5c587f337b27db7e2a0107ba089` | Ubuntu 20.04.6 WSL2：干净构建 12、修改 `feature.h` 后增量 12、干净重建 13；人工确认由组长于 2026-10-09 转述，见 `oracle/incremental-review-20261009.md` |
| 叶原原 | C2 编译选项变化、复现脚本、容器实验与证据；Codex 代执行命令 | `fixtures/incremental/Makefile`、`scripts/run_incremental.py`、`oracle/incremental.expected.json` 的 C2 部分、`evidence/c2/`、`evidence/failures/` | 源码 `56deea9199679907893fa53add1d867ff62028e1`（`e3-c2`）；脚本 `03c0d28d0645699966c150fee90c4405b84947a3`；修订 `ae86618b602a08ce4d893b396dde6b6f75e3fccc`；证据 `1a7630f7c55327e58caba2945f6635bb99bc0383` | Ubuntu 24.04.5 容器：12/12/19，37 项实验断言与 3 项脚本异常检查通过；人工确认由组长于 2026-10-09 转述，见 `oracle/incremental-review-20261009.md` |

上述 Commit SHA 对应各成员在 Git 历史中的提交；标签 `e3-c0`、`e3-c1`、
`e3-c2` 均已在远端核对。提交作者、实际执行人和 oracle 审阅人分别记录，
不把 AI 执行的命令写成成员亲自执行。B08 材料及仅有口头讨论、无 Git 记录的
内容不计为代码贡献。本次文档收尾提交尚未产生，完成后再补录其 SHA。
