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
| 刘馨雅 | C0 项目、环境验证与证据整理；最终整合待完成 | `fixtures/incremental/`、`evidence/environment/c0-ubuntu-24.04.md` | `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`、`aa28d53` | Ubuntu 24.04 宿主机与容器构建通过；`e3-c0` 指向 C0 提交，详见环境验证记录 |
| 邱莉扉 | 负责固定 MD/RD 样本、人工 oracle 与复现证据；实现和执行测试，审阅确认 oracle | `fixtures/md-rd/`、`oracle/md-rd.expected.json`、`scripts/run-md-rd.sh`、`scripts/run_md_rd.py`、`evidence/md-rd/` | `8a9cfc46d854e697fd397c1f6c579014e219144b` | Ubuntu 24.04 容器验证通过；Ubuntu 24.04 复核 18 条命令成功、14 项断言通过；2026-10-06 确认 oracle，见 `evidence/md-rd/oracle-review-20261006-132502/REVIEW.md` |
| 范从钰 | C1 新增头文件读取但遗漏声明；C1 人工 oracle 与复现实验证据 | `fixtures/incremental/include/feature.h`、`fixtures/incremental/src/main.c`、`oracle/incremental.expected.json`、`evidence/c1/20261007T143349+0800/` | `4b70cabad1be8f6e98ee90ed9c5803b7aa793253`（`e3-c1`） | Ubuntu 20.04.6 WSL2：干净构建输出 12；`feature.h` 仅改为 3 时增量输出仍为 12、干净重建为 13；Ubuntu 24.04/Docker 复验待完成 |
| 叶原原 | C2 编译命令变化与追溯材料 | 待填写 | 待填写 | 待填写 |

只记录成员实际完成并由 Git 历史支持的工作。B08 材料、AI 草稿和仅参与口头
讨论的内容不得计为个人代码贡献。
