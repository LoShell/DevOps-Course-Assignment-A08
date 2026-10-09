# C0/C1/C2 增量样本

本目录是 C0/C1/C2 共用的 C + GNU Make 项目。依赖声明正确的 C0 已由
`e3-c0` 标签固定在提交 `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`；
后续状态在同一目录逐次修改，并分别由真实 Commit SHA 和标签固定。
当前工作分支源码已演进到 C2；直接干净构建输出 `19`，版本仍为 `demo 1.0.0`。
C2 远端注释标签 `e3-c2` 固定在 `56deea9199679907893fa53add1d867ff62028e1`，
其独立提交只把 `CPPFLAGS := -Iinclude` 改为 `CPPFLAGS := -Iinclude -DMODE=7`。

从本目录构建和验证：

```sh
make clean && make -j2
./bin/demo --version
./bin/demo
```

C0 的版本输出为 `demo 1.0.0`，行为输出为 `10`。`build/main.o` 实际读取的
项目内头文件为 `include/common.h` 和 `include/config.h`，两者都通过
Makefile 中的 `HEADERS` 声明。C0 不应出现项目内的 MD 或 RD。
C0 的 Ubuntu 24.04 宿主机与容器验证结果见
[`../../evidence/environment/c0-ubuntu-24.04.md`](../../evidence/environment/c0-ubuntu-24.04.md)。

从仓库根目录构建容器：

```sh
docker build -f E3/fixtures/incremental/Dockerfile -t a08-e3-incremental .
docker run --rm a08-e3-incremental
docker run --rm a08-e3-incremental ./bin/demo
```

Docker 构建上下文是整个仓库，容器工作目录为
`/workspace/E3/fixtures/incremental`；后续 DRAFT、FULL_CHECK 和
INCREMENTAL_CHECK 请求需使用与实际镜像一致的工作目录。上述命令构建当前
工作区，不能仅凭镜像标签声称它是 C0；固定版本实验应使用 Git 导出或复现脚本。

| 状态 | 已构造变化 | 已验证行为 |
|---|---|---|
| C0 | `common.h` 和 `config.h` 均被读取且正确声明 | 干净构建输出 `10` |
| C1 | 新增并读取 `feature.h`，但不在 Makefile 中声明 | 构建输出 `12`，预期发现新增 MD |
| C2 | 保持 C1 源码，仅向 CPPFLAGS 加入 `-DMODE=7` | 保留 C1 产物后增量构建输出 `12`，同一 C2 源码干净构建输出 `19` |

公共约定见上级 `README.md`。C1 历史验证见
[`../../evidence/c1/20261007T143349+0800/README.md`](../../evidence/c1/20261007T143349+0800/README.md)，
C2 证据见 [`../../evidence/c2/README.md`](../../evidence/c2/README.md)。

在仓库根目录执行 `python E3/scripts/run_incremental.py` 可导出固定的 C1/C2
版本，在同一 Ubuntu 24.04 容器中重现上述对比。脚本仅在构建 C1 后替换
Makefile，保留源码、头文件和旧产物时间戳；增量阶段不能先 clean，也不能分别
启动两个干净镜像后将其结果当作增量比较。宿主机需 Python 3.12+、Git 和 Docker。

C1 的 `feature.h` 缺失声明在 C2 中继续保留。编译命令变化不会被额外记成头文件
MD。C1/C2 的人工 oracle 确认来源见
[`../../oracle/incremental-review-20261009.md`](../../oracle/incremental-review-20261009.md)。
C1/C2 实测配置编号不同，E2 同配置接口的后续处理仍待组长统一。
