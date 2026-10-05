# C0/C1/C2 增量样本

本目录是 C0/C1/C2 共用的 C + GNU Make 项目。当前源码为依赖声明正确的 C0；
后续状态在同一目录逐次修改，并由真实 Commit SHA 和注释标签固定。

从本目录构建和验证：

```sh
make clean && make -j2
./bin/demo --version
./bin/demo
```

C0 的版本输出为 `demo 1.0.0`，行为输出为 `10`。`build/main.o` 实际读取的
项目内头文件为 `include/common.h` 和 `include/config.h`，两者都通过
Makefile 中的 `HEADERS` 声明。C0 不应出现项目内的 MD 或 RD。

从仓库根目录构建容器：

```sh
docker build -f E3/fixtures/incremental/Dockerfile -t a08-e3-c0 .
docker run --rm a08-e3-c0
docker run --rm a08-e3-c0 ./bin/demo
```

Docker 构建上下文是整个仓库，容器工作目录为
`/workspace/E3/fixtures/incremental`；后续 DRAFT、FULL_CHECK 和
INCREMENTAL_CHECK 请求需使用与实际镜像一致的工作目录。

| 状态 | 计划变化 | 计划行为 |
|---|---|---|
| C0 | `common.h` 和 `config.h` 均被读取且正确声明 | 干净构建输出 `10` |
| C1 | 新增并读取 `feature.h`，但不在 Makefile 中声明 | 构建输出 `12`，预期发现新增 MD |
| C2 | 保持 C1 源码，只修改编译命令以加入模式宏 | 增量构建仍输出 `12`，干净构建输出 `19` |

公共约定见上级 `README.md`。C1 和 C2 的预期值仍需在对应提交和实验日志中
实际验证。
