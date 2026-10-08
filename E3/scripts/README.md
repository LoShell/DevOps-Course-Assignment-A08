# 复现脚本

本目录保存固定 MD/RD 与 C1/C2 的复现脚本。脚本使用项目自身的 Makefile 和
可执行文件，失败时返回非零退出码，记录版本、命令、原始输出和退出码。

## 已实现入口

- `run-md-rd.sh` / `run_md_rd.py`：Linux 上在临时副本中验证固定 MD/RD，
  需要 Python 3.8+、GCC 和 GNU Make；详见固定样例 README。
- `run_incremental.py`：宿主机运行，支持 Windows/Linux，需要 Python 3.12+、
  Git、Docker CLI 和运行中的 Docker Linux 引擎。容器不需要 Python。

在仓库根目录执行：

```sh
python E3/scripts/run_incremental.py --operator "填写实际执行人"
```

Linux 若命令名为 `python3`，相应替换。可选参数：`--c1-ref`、`--c2-ref`
（默认 `e3-c1`、`e3-c2`），`--output`（必须是新目录），`--image-tag`、`--operator`。
脚本打印固定提交 SHA、实测工具链和每条命令；默认写入
`E3/evidence/c2/<北京时间>/`，拒绝覆盖现有目录。

脚本逐字节检查两份样例仅有指定 Makefile 变化，从固定 C2 提交导出镜像构建
上下文；在同一容器中依次执行 C1 干净构建、仅替换 Makefile 后的 C2 增量构建、
C2 干净构建。源码与产物的 SHA-256、大小和纳秒精度修改时间均有记录。
Docker 构建日志即时保存，失败也保留已有记录；临时实验容器在收尾阶段删除，
镜像保留供复核。Git 导出临时禁用 CRLF 转换，不改变用户的 Git 配置。

配置 ID 按实测镜像、工具链和编译选项生成。C1/C2 因选项不同而采用不同 ID；
后续 E2 同配置接口策略仍待组长统一，不修改成员 3 的历史记录。

`capture-environment.sh` 尚未单独实现；本次 C2 环境采集由复现脚本完成。
