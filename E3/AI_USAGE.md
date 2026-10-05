# A08 E3 AI 使用记录

| 日期 | 使用场景 | AI 建议 | 人工处理 | 关联文件 | 验证方式 |
|---|---|---|---|---|---|
| 2026-09-30 | E3 范围、项目结构和协作流程梳理 | 根据 E3 课件区分测试基线与后续工具实现，并起草单分支、分目录协作方案 | 人工对照课件和 E2 契约，修正项目来源、跨组依赖和 B08 示例含义后采用 | `README.md`、`WORKFLOW.md`、`adr/0001-baseline-project-design.md` | 对照 E3 课件、E2 评审记录和双方沟通结果 |
| 2026-10-05 | C0 项目与验证证据准备 | 起草 C 源码、Makefile、Dockerfile、样本说明和验证记录，并协助同步进度文档 | 刘馨雅确认项目约束，在 Ubuntu 24.04 宿主机和容器中执行构建、运行及依赖检查，提交 C0 并固定 `e3-c0` 标签；AI 未代替真实运行 | `fixtures/incremental/`、`evidence/environment/c0-ubuntu-24.04.md`、`README.md`、`BACKLOG.md`、`CONTRIBUTIONS.md` | `make clean && make -j2`、`./bin/demo --version`、`./bin/demo`、`gcc -MM`、`docker build`、`docker run`；输出见 C0 验证记录 |

后续使用 AI 生成或修改源码、Makefile、Dockerfile、oracle 或脚本时，应追加记录，
并写明人工验证命令和结果。AI 输出不能代替真实实验日志。
