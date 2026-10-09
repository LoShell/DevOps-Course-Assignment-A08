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

以下结果由执行人从 Ubuntu 终端提供；本节 Docker 构建记录为 2026-10-05 的
终端摘录。2026-10-09 的固定版本完整重建日志已另行保存，见文末链接。

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

- 已补录固定 `e3-c0` 标签的[完整 Docker 构建原始日志](c0-replay-20261009T032247Z/docker-build.log)、
  [环境](c0-replay-20261009T032247Z/container-environment.txt)和
  [运行输出](c0-replay-20261009T032247Z/output.txt)；补录提交为 `c354dcb39afc0c2ff3f5486d053c369b3710da83`。
- 已核对远端注释标签 `e3-c0`，其目标提交为上述 C0 Commit。
- `configuration_id` 在按真实环境确认跨提交的团队配置标识后填写；
  2026-10-09 重建镜像 ID 与上方首次镜像 ID 不同，分别保留。
