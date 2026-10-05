# 复现脚本

本目录将保存固定 MD/RD 和 C0/C1/C2 的复现脚本。脚本必须在失败时返回非零
退出码，并打印当前 Commit SHA、工具版本和实际执行的命令。

计划文件：

- `run-md-rd.sh`
- `run-incremental.sh`
- `capture-environment.sh`

脚本应调用项目自身的 Makefile 和可执行文件，不在脚本中重新实现构建逻辑。
