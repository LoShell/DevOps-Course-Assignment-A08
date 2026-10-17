# A08 E4 服务器环境基线

以下是 2026-10-17 组长通过 SSH 在新购 ECS 上运行命令后提供的原始结果摘要；
表中 Docker 状态为首次检查时的状态，后续安装结果见下文。`make all`
尚未验证，不将购买规格或模板预期当成实测结果。

| 检查项 | 服务器输出 |
| --- | --- |
| 系统 | `Ubuntu 22.04.5 LTS` |
| 架构 | `x86_64` |
| 可用 CPU 数 | `nproc` 为 `2` |
| 内存 | `free -h`：总量 `1.7Gi`，当时可用 `1.2Gi` |
| Swap | `0B` |
| 根文件系统 | `/dev/vda1`：`79G`，已用 `4.5G`，可用 `71G` |
| Docker / Compose / Buildx（首次检查） | `docker` 命令不存在 |
| Git | `2.34.1` |
| GNU Make | `4.3` |
| Python | `3.10.12` |

服务器购买规格为 2 vCPU / 2 GiB，但 Ubuntu 报告的可见内存约 1.7 GiB。
模板 `scripts/doctor.py` 原来的 `MIN["mem_gib"]` 为 3.5，因此原样运行
`make doctor` 会将内存不足记为 `problems`。实际结果与临时试验见下文。

## Docker 安装后复核

同日组长执行 `systemctl enable --now docker` 后报告：

| 检查项 | 服务器输出 |
| --- | --- |
| Docker Client / Engine | `29.1.3` / `29.1.3`，`linux/amd64` |
| Docker Compose | `2.40.3+ds1-0ubuntu1~22.04.1` |
| Docker Buildx | `0.30.1-0ubuntu1~22.04.1` |

以上只确认守护进程和插件可用；后续镜像拉取结果见下文，构建、测试和扫描仍待实测。

## 基础镜像可达性首次检查

组长在服务器执行 `docker buildx imagetools inspect`，目标为 Dockerfile 中的
`m.daocloud.io/docker.io/library/python@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74`。
镜像站对清单的 `HEAD` 请求返回 `502 Bad Gateway`。该结果只说明此次
镜像站请求失败，尚不能判定摘要错误或 Docker 安装异常；待核对 Docker Hub
原始地址和再次重试结果。

随后用相同摘要检查 `docker.io/library/python` 原站，`registry-1.docker.io`
连接解析得到的 `31.13.91.33:443` 超时（`i/o timeout`）。两条镜像路径均
未取得清单，尚未进入构建；下一步检查 ECS 的 DNS 和华为云 SWR 镜像加速器。

组长随后报告 `resolvectl dns` 的 `eth0` 使用华北-北京四内网 DNS
`100.125.1.250`，`getent ahostsv4 registry-1.docker.io` 仅返回
`31.13.91.33`。DNS 服务器地址符合华为云该区域文档，但原站连接仍超时；
尚未修改 ECS DNS 或 Docker 配置。下一步查看 SWR 控制台提供的镜像加速器地址。

## 华为云 SWR 加速器验证

组长从北京四区域 SWR 控制台获取本账号的镜像加速器地址，在 ECS 的
`/etc/docker/daemon.json` 中配置 `registry-mirrors` 并重启 Docker。
`docker info` 已显示该地址；加速器的账号专用 URL 不记录在仓库中。

随后执行 `docker pull --platform linux/amd64` 拉取
`docker.io/library/python@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74`，
各层完成下载，输出 `Digest: sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74`。
因此服务器可通过 SWR 加速器获取模板固定的原始摘要。Dockerfile 中的
`BASE_IMAGE` 改用 Docker Hub 原站名称，并保留相同摘要；实际构建仍待验证。

## 原模板环境自检实测与临时门槛试验

组长在个人克隆中运行原模板 `make doctor`，生成
`work/20261017-145604/env.json`；运行时间为 2026-10-17 06:56:04 UTC。
自检报告 `cpus=2`、`mem_gib=1.7`、`disk_gib=70.3`，Docker、Compose、
Buildx、Git、Make、Python 均可用。唯一的 `problems` 为
`mem_gib=1.7 低于最低要求 3.5`；CPU 低于建议 4、磁盘低于建议 100
只列入 `warnings`。`make doctor` 因这 1 个必需项不满足而退出码为 1。

助教认可购买 2 GiB ECS；本组实测该规格对系统可见约 1.7 GiB。
因此组长在个人克隆的 `scripts/doctor.py` 中临时将最低**可见**内存改为
1.5 GiB，保留低于建议值的警告，CPU 与磁盘最低门槛不变。这项修改
尚未提交；其目的只是试验规格与自检条件的冲突，不能代替后续构建和
完整 `make all` 验证。

组长在服务器个人克隆中临时修改自检门槛（不提交），重跑 `make doctor`，
生成 `work/20261017-145950/env.json`，运行时间为
2026-10-17 06:59:50 UTC。报告的资源和工具版本与上次相同，
`problems` 为空；CPU、内存、磁盘低于建议值各有一条 `warnings`，
结论为“环境自检：通过”。Dockerfile 也在该个人克隆中临时改为相同摘要的
Docker Hub 原站名称，以便利用 ECS 已配置的 SWR 加速器；完整 `make all`
仍待实测。个人克隆中的临时修改没有提交；门槛调整也未纳入远端分支。
