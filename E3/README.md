# A08 E3：并行测试基线

本目录保存 A08 的 E3 测试基线。E3 的目标是准备可复现输入和人工预期结果，
不是实现 BuildChecker 或 EChecker。

## 验收范围

| 基线 | A08 需要准备的内容 |
|---|---|
| 固定 MD | 源文件实际读取一个未在 Makefile 中声明的头文件，并给出人工判定依据 |
| 固定 RD | Makefile 声明一个构建过程中未实际读取的头文件，并给出人工判定依据 |
| C0 | 依赖声明正确的初始提交、构建配置和干净构建结果 |
| C1 | 在 C0 上新增头文件读取但遗漏依赖声明，记录增量检查预期 |
| C2 | 在 C1 上只修改编译命令，记录增量构建与干净构建的行为差异 |

每项基线必须保存真实 Commit SHA、环境信息、执行命令、输出、预期报告和失败
记录。E3 期间 A08 与 B08 独立产出各自基线，后续阶段再接入对方真实数据。

## 当前进展

| 基线 | 状态 | 版本与证据 |
|---|---|---|
| 固定 MD/RD | 实现、测试及人工 oracle 确认完成 | `fixtures/md-rd/`、`oracle/md-rd.expected.json`、[确认记录](evidence/md-rd/oracle-review-20261006-132502/REVIEW.md) |
| C0 | 已验证 | 提交 `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`，注释标签 `e3-c0`；[`环境与构建验证`](evidence/environment/c0-ubuntu-24.04.md) |
| C1 | 实现与实验完成，人工 oracle 待成员 3 确认 | 提交 `4b70cabad1be8f6e98ee90ed9c5803b7aa793253`、`e3-c1`；[历史证据](evidence/c1/20261007T143349+0800/README.md) |
| C2 | 实现与容器实验完成，人工 oracle 待成员 4 确认 | 提交 `56deea9199679907893fa53add1d867ff62028e1`、本地注释标签 `e3-c2`；[最终脚本运行证据](evidence/c2/20261008T201035798727+0800/README.md)，未推送 |

C0 在 Ubuntu 24.04 宿主机与容器中均完成干净构建；`./bin/demo --version`
输出 `demo 1.0.0`，`./bin/demo` 输出 `10`。GCC 列出的项目内头文件与
Makefile 声明一致。完整 Docker 构建原始日志仍待保存。

C2 在 Ubuntu 24.04.5 容器中验证通过：先构建 C1 输出 `12`，仅替换 C2
Makefile 后增量构建仍为 `12`，相同 C2 源码干净重建后为 `19`。增量阶段对象和
可执行文件的哈希及时间戳均不变；37 项实验断言与 3 项脚本异常检查通过。
命令由 Codex 代成员 4 执行，人工 oracle 审阅状态单独记录。

## 已确定约定

- 项目类型：Linux 下的 C + GNU Make 小型项目。
- 容器基线：`ubuntu:24.04`。
- 构建命令：`make clean && make -j2`。
- 可执行文件：`bin/demo`。
- DRAFT 验证命令：`./bin/demo --version`。
- 行为验证命令：`./bin/demo`。
- 对象文件：`build/main.o`。
- 依赖声明使用 `HEADERS` 变量，便于构造并修复 MD/RD。
- E3 工作分支：`a08/e3-baseline`。

C0 实测为 Ubuntu 24.04、GCC 13.3.0、GNU Make 4.3、x86_64。
C2 实测工具链为 Ubuntu 24.04.5、GCC 13.3.0、GNU Make 4.3、x86_64。
本次同一容器中的 C1/C2 配置编号分别为 `e3-incremental-2d73359c5ff8dc5d`
和 `e3-incremental-589dbd0022ee0df7`，计算依据和算法见原始证据。
编译选项变化使配置编号不同，本次 E3 对比不能直接作为 E2 同配置增量请求；
组长仍需统一接口对接策略、C0/固定 MD/RD 的团队配置及最终汇总。
成员 3 的历史 WSL 配置记录保持原样。

从仓库根目录复现 C2（宿主机 Python 3.12+、Git、运行中的 Docker）：

```sh
python E3/scripts/run_incremental.py --operator "填写实际执行人"
```

脚本导出 `e3-c1`、`e3-c2` 的固定版本，每次生成新的证据目录，拒绝覆盖旧记录。

## 目录

```text
E3/
├── README.md
├── WORKFLOW.md
├── BACKLOG.md
├── CONTRIBUTIONS.md
├── AI_USAGE.md
├── CONTRACT_REFERENCE.md
├── coordination.md
├── fixtures/
│   ├── md-rd/
│   └── incremental/
├── oracle/
├── evidence/
├── scripts/
└── adr/
    └── 0001-baseline-project-design.md
```

后续样本、运行脚本和真实输出由成员在工作分支上按
[`WORKFLOW.md`](WORKFLOW.md) 分步提交。
