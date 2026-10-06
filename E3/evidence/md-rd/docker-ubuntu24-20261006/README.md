# Ubuntu 24.04 容器实验（成员 2）

## 实际结果

2026-10-06，在本机 Docker Desktop 的 desktop-linux context
构建并运行 Ubuntu 24.04 容器。构建退出码 0，三项容器检查与完整实验退出码均为 0。
实验包含 18 条命令、14 项断言，全部通过。运行使用 --network none 和 --rm，
证据保存至宿主机，临时容器已自动删除，本地镜像保留供重跑。

| 场景 | 实际观察 |
|---|---|
| 默认版本命令 | demo 1.0.0 |
| 初始构建行为 | 10 |
| config.h 的 CONFIG_VALUE 从 4 改为 5，普通 make | 对象时间戳和 SHA-256 不变，输出仍为 10 |
| 相同源码 clean 后重建 | 输出 11 |
| unused.h 仅改注释 | 出现真实编译命令，对象时间戳更新，输出仍为 11 |
| GCC 依赖对照 | 包含 common.h/config.h，不含 unused.h |
| 源码完整性 | 测试前后源文件哈希一致，临时副本中的修改未带回样例 |
| 镜像内容 | 不包含 /workspace/.git 或 /workspace/E2 |

## 环境与版本

- OS 实测：Ubuntu 24.04.5 LTS，VERSION_ID=24.04，x86_64。
- GCC：13.3.0（Ubuntu 13.3.0-6ubuntu2~24.04.1）。
- GNU Make：4.3。
- Python：3.12.3。
- Docker Engine：29.4.3，Docker Desktop 4.74.0。
- 镜像标签：a08-e3-md-rd:local-20261006。
- docker image inspect 返回的镜像 ID：sha256:93a41bef5c15dfbcead963a13a5bae5ca37682504e98a020e7b25c08b349fef6。
- Ubuntu 基础镜像摘要（构建日志）：sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55。
- 容器工作目录：/workspace/E3/fixtures/md-rd。
- 基础仓库提交：60318cf03e7f988058160ccf422147cf2d424e04。
- run/observations.json 的 source_sha256 标识实际测试内容。
- 本次局部配置 ID：local-md-rd-fe579904174d88c9，不替代尚未统一的团队 configuration_id。

容器使用 Docker/WSL2 提供的 Linux 内核，Ubuntu 24.04 指的是容器内用户空间，


## 证据文件

- [build.txt](build.txt)：完整 Docker 构建日志与退出码。
- [image-inspect.json](image-inspect.json)：实际镜像元数据。
- [docker-version.txt](docker-version.txt)：Docker 客户端和服务端版本。
- [docker-commands.json](docker-commands.json)：容器调用参数、结果和退出码。
- [run-console.txt](run-console.txt)：实验入口输出。
- [run/commands.txt](run/commands.txt)：容器内命令、工作目录、原始输出和退出码。
- [run/observations.json](run/observations.json)：14 项断言、环境、镜像 ID、源文件哈希。

构建调用（仓库根目录）：

```sh
docker build --progress=plain -f E3/fixtures/md-rd/Dockerfile -t a08-e3-md-rd:local-20261006 .
```

精确的容器运行参数见 docker-commands.json。日志中的 /evidence 是绑定到本目录的
宿主机证据目录，/tmp/a08-md-rd-* 是已清理的临时测试副本。
重复实验请用新的证据输出目录，脚本不会覆盖旧记录。

## 边界

- 本次只验证固定 MD/RD 基线，不是 BuildChecker 检测结果。
- Oracle 已由成员 2 于 2026-10-06 确认通过，见 ../oracle-review-20261006-132502/REVIEW.md；团队配置标识仍待组长统一。

- Dockerfile 使用可更新的 ubuntu:24.04 标签；未来重新构建可能得到不同包版本。
  本次具体版本、基础摘要和最终镜像 ID 已记录，不声称今后构建必然位级一致。
