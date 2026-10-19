# E4 容器构建与运行配置审阅记录

**审阅人：** 241250071  
**审阅范围：** Dockerfile 基础镜像 digest、Compose 资源限制与 `SYS_PTRACE`、`toolchain.lock`。  
**复现基准：** `4c1ff6caf40fc4f1d90b730cbc2477824a6d4576`  
**本次证据目录：** `~/241250071/buildchecker/work/20261018-150333`

## 总体结论

本次审阅未发现问题。Dockerfile 对基础镜像进行了不可变 digest 固定；Compose 对容器资源和权限均作了最小化约束；工具链及 Python 依赖的实际版本已记录在锁文件中，并与本次构建输出一致。

## 1. Dockerfile 基础镜像 digest

**检查位置：** `services/buildchecker/Dockerfile` 第 7–8 行。

```dockerfile
ARG BASE_IMAGE=docker.io/library/python@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74
FROM ${BASE_IMAGE}
```

**审阅结论：** 通过。基础镜像使用 `@sha256:...` digest 固定，而不是仅使用会变化的标签，因此同一基准下可以定位到同一份基础镜像内容，满足可复现构建要求。

**补充核对：** 本次构建生成的本地镜像为 `e4-buildchecker:241250071`，其本地镜像 ID 为：

```text
sha256:db5dcd85f9403de5e37c46fdb798ddf148d0938b204b44b8cacdb18f69068a76
```

该 ID 是本地构建产物标识；Dockerfile 第 7 行的 digest 才是固定基础镜像来源的依据。

## 2. Compose 资源与权限配置

**检查位置：** `compose.yaml` 第 9–16 行。

```yaml
network_mode: none
cpus: 2
mem_limit: 1g
pids_limit: 256
cap_add:
  - SYS_PTRACE
security_opt:
  - no-new-privileges:true
```

**资源限制结论：** 通过。服务设置了最多 2 个 CPU、1 GiB 内存和 256 个进程数上限，能够避免单次构建/测试无上限占用共享 ECS 的资源。

**`SYS_PTRACE` 结论：** 通过。该能力是执行 `strace` 所需的最小附加能力；配置未使用 `privileged: true`，同时启用了 `no-new-privileges:true`，没有给予容器不必要的全面特权。`network_mode: none` 也避免了该检测容器获得不需要的网络访问。

## 3. 工具链锁定

**检查位置：** `work/20261018-150333/toolchain.lock`，以及 Dockerfile 第 17–26 行。

锁文件记录了系统工具、运行环境和 Python 测试依赖的实际版本，包括：

```text
gcc=4:14.2.0-1
make=4.4.1-2
strace=6.13+ds-1
git=1:2.47.3-0+deb13u1
libc6-dev=2.41-12+deb13u4
python3=3.13.14
arch=amd64
pytest==8.4.2
```

**审阅结论：** 通过。Dockerfile 在安装系统依赖后通过 `dpkg-query` 写入 `/opt/toolchain.lock`，并在安装 Python 依赖后追加 `pip freeze` 结果；证据目录保留了该锁文件。构建输出显示 GNU Make 4.4.1、GCC 14.2.0、strace 6.13，与锁文件记录的工具主版本一致，可用于后续复现和问题定位。

## 4. 审阅结果汇总

| 检查项 | 结果 | 依据 |
| --- | --- | --- |
| Dockerfile 基础镜像 digest | 通过 | Dockerfile 第 7–8 行使用 `python@sha256:...` |
| Compose 资源限制 | 通过 | `cpus: 2`、`mem_limit: 1g`、`pids_limit: 256` |
| `SYS_PTRACE` 与权限收敛 | 通过 | 仅添加 `SYS_PTRACE`，未使用 `privileged`，并设置 `no-new-privileges` |
| 工具链锁定 | 通过 | `toolchain.lock` 记录系统工具、Python、架构和 pip 依赖版本 |

