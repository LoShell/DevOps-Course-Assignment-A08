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

`configuration_id` 在服务器实际运行后，根据镜像、GCC 版本和架构填写，当前不
预先假设具体 GCC 版本。

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

样本源码、Makefile、Dockerfile、运行脚本和真实输出由成员在工作分支上按
[`WORKFLOW.md`](WORKFLOW.md) 分步提交。
