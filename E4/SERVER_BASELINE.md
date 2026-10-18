# A08 E4 服务器环境基线

以下是 2026-10-17 组长通过 SSH 在新购 ECS 上运行命令后提供的原始结果摘要；
表中 Docker 状态为首次检查时的状态，后续安装和首次 `make all` 结果见下文。
不将购买规格或模板预期当成实测结果。

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

以上只确认守护进程和插件可用；后续镜像拉取、构建、测试和扫描结果见下文。

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
`BASE_IMAGE` 改用 Docker Hub 原站名称，并保留相同摘要；实际构建结果见下文。

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
Docker Hub 原站名称，以便利用 ECS 已配置的 SWR 加速器。个人克隆中的
临时修改当时没有提交；门槛调整当时也尚未纳入远端分支。

## 首次完整运行结果与待解决的复现差异

首次构建从 `deb.debian.org` 下载 Debian trixie 的软件包索引时长时间停在
`trixie/main amd64 Packages`。组长确认华为云 Debian 镜像的
`trixie/InRelease` 返回 HTTP 200 后，在服务器个人克隆的 Dockerfile 中
**临时、未提交**地把 Debian APT 源从 `http://deb.debian.org/debian`
替换为 `https://mirrors.huaweicloud.com/debian`，再运行 `make all`。

组长提供的运行输出显示，本次证据目录为 `work/20261017-151409/`；
个人克隆的源码提交为 `d26609c5f2653464a5770edf68bc143f8ab5a1f6`
（当时远端 `a08/e4-environment` 的提交），运行时 `git status --short`
另有 `scripts/doctor.py` 和 `services/buildchecker/Dockerfile` 两个未提交改动。
证据目录内已确认存在 `build.log`、`env.json`、`image.json`、
`toolchain.lock`、`test.log`、`smoke.json`、`secret-scan.txt` 七个文件。
`pytest` 为 `3 passed`，冒烟结果 `passed: true`、程序输出 `1`，并记录
`config.h` 被打开、`unused.h` 未被打开；密钥扫描报告未发现问题。
工具链输出包含 Debian trixie 的 `libc6-dev=2.41-12+deb13u4`、
`make=4.4.1-2`、`strace=6.13+ds-1`、`python3=3.13.14` 和 `arch=amd64`。
`make all` 打印了证据目录，表明本次运行完成；尚需审阅完整构建日志和
镜像信息，再供其他组员复跑。

本次成功依赖服务器个人克隆中的三处临时改动：可见内存最低门槛
`3.5 → 1.5 GiB`、基础镜像地址改用 Docker Hub 原站名称、APT 源改用
华为云镜像。审阅后，本分支已纳入这三处改动；但上述试验仍是带未提交改动
的旧 SHA，不能充当新提交的复现证据。下一步让组员从更新后的同一源码 SHA
各自干净克隆并运行 `make all`，记录新的证据目录和对照结论。

## 更新分支后的组长复跑

组长在新目录 `buildchecker-clean` 运行更新后的分支，提供的 `make all` 尾部
输出显示证据目录为 `work/20261017-152852/`。构建得到 `amd64` 镜像，
镜像 ID 为 `sha256:beda061d0cac2c35db18809455be549d2b834b32ad20f32ebd9f4133351b00e0`；
`toolchain.lock` 中包含 `gcc=4:14.2.0-1`、`git=1:2.47.3-0+deb13u1`、
`libc6-dev=2.41-12+deb13u4`、`make=4.4.1-2`、`strace=6.13+ds-1`、
`python3=3.13.14` 和 `arch=amd64`。测试为 `3 passed`；冒烟的
`make_exit_code: 0`、`app_output: "1"`、`passed: true`，且 `config.h`
被打开、`unused.h` 未被打开；密钥扫描未发现问题。

组长随后在同一 `buildchecker-clean` 目录核对：
`git rev-parse HEAD` 为 `4c1ff6caf40fc4f1d90b730cbc2477824a6d4576`，
`git status --short` 无输出。因此本次是更新后源码提交的干净工作区
`make all` 成功运行。

## 2026-10-18 组员独立复跑进度

组长在三名组员各自的克隆中核对 `git rev-parse HEAD`，均为
`4c1ff6caf40fc4f1d90b730cbc2477824a6d4576`；当时
`git status --short` 均无输出。每人随后在自己的 `work/` 生成目录：

| 学号 | 证据目录 | 已核对内容 |
| --- | --- | --- |
| 241250071 | `/root/241250071/buildchecker/work/20261018-150333/` | 七个预期文件齐全；`test.log` 为 `3 passed` |
| 241250076 | `/root/241250076/buildchecker/work/20261018-152841/` | 七个预期文件齐全；终端显示冒烟 `passed: true`、输出 `1`，密钥扫描未发现问题 |
| 241250097 | `/root/241250097/buildchecker/work/20261018-161219/` | 组长报告 `make all` 完成；七个预期文件齐全，文件内容待核对 |

证据文件存在不等于内容已经全部审阅。三名组员还需分别核对本人负责的内容，
组长需比较 `toolchain.lock`、`test.log` 和 `smoke.json` 的结论并记录差异。
个人 `work/` 默认留在 ECS，不进入 Git 提交。
