# C0 环境与构建验证

- 日期：2026-10-05
- 执行人：刘馨雅
- 仓库：`https://github.com/LoShell/DevOps-Course-Assignment-A08.git`
- 分支：`a08/e3-baseline`
- C0 Commit：`88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`
- 宿主环境：Ubuntu 24.04 LTS、x86_64、GCC 13.3.0、GNU Make 4.3、Docker 29.6.1
- 容器环境：`ubuntu:24.04`、x86_64、GCC 13.3.0、GNU Make 4.3
- 容器镜像标签：`a08-e3-c0:latest`
- 容器镜像 ID：`sha256:2e8bf64b77d8cff4e17f6bf39d453759f24457d9c71fec85a361d9b402458828`
- 项目工作目录：宿主机 `E3/fixtures/incremental`；容器内 `/workspace/E3/fixtures/incremental`

以下结果由执行人从 Ubuntu 终端提供；Docker 构建记录是终端摘录，尚未保存完整原始日志。

## 宿主机构建与行为

```sh
make clean && make -j2
./bin/demo --version
./bin/demo
gcc -MM -Iinclude -MT build/main.o src/main.c
```

```text
rm -rf build bin
mkdir -p build
gcc -Iinclude -Wall -Wextra -O2 -c src/main.c -o build/main.o
mkdir -p bin
gcc -Wall -Wextra -O2 build/main.o -o bin/demo
demo 1.0.0
10
build/main.o: src/main.c include/common.h include/config.h
```

上述命令均继续执行并产生预期输出；终端记录未单独打印各命令的退出码。
Makefile 中 `build/main.o` 的项目内依赖为 `src/main.c`、`include/common.h`、
`include/config.h`，与 GCC 列出的项目内读取文件一致。

## Docker 构建与行为

从仓库根目录执行：

```sh
docker build -f E3/fixtures/incremental/Dockerfile -t a08-e3-c0 .
docker run --rm a08-e3-c0
docker run --rm a08-e3-c0 ./bin/demo
docker run --rm --entrypoint sh a08-e3-c0 -c 'gcc --version | head -n 1; make --version | head -n 1; uname -m'
docker image inspect a08-e3-c0 --format '{{.Id}}'
```

构建摘录：`Building 393.2s (10/10) FINISHED`，其中 `RUN make clean && make -j2`
完成。容器运行和镜像检查的输出依次为：

```text
demo 1.0.0
10
gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
GNU Make 4.3
x86_64
sha256:2e8bf64b77d8cff4e17f6bf39d453759f24457d9c71fec85a361d9b402458828
```

## 结论与待补证据

C0 在 Ubuntu 24.04 宿主机和 Ubuntu 24.04 容器中均完成构建与行为验证；
项目内头文件依赖无预期 MD/RD。该结论基于人工对照和 GCC 依赖输出，
尚不是 BuildChecker 自动检测报告。

- 待保存供他人复核的 Docker 构建原始日志。
- 已核对远端注释标签 `e3-c0`，其目标提交为上述 C0 Commit。
- `configuration_id` 在确认 C0/C1/C2 的配置标识策略后填写。
