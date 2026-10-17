# A08 E4 服务器环境基线

以下是 2026-10-17 组长通过 SSH 在新购 ECS 上运行命令后提供的原始结果摘要；
Docker 安装及 `make all` 尚未验证，不将购买规格或模板预期当成实测结果。

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
模板 `scripts/doctor.py` 的 `MIN["mem_gib"]` 为 3.5，因此按当前模板运行
`make doctor` 会将内存不足记为 `problems`。下一步仍须记录实际
`env.json` 和运行结果，再依据助教确认的课程标准处理这一差异。

## Docker 安装后复核

同日组长执行 `systemctl enable --now docker` 后报告：

| 检查项 | 服务器输出 |
| --- | --- |
| Docker Client / Engine | `29.1.3` / `29.1.3`，`linux/amd64` |
| Docker Compose | `2.40.3+ds1-0ubuntu1~22.04.1` |
| Docker Buildx | `0.30.1-0ubuntu1~22.04.1` |

以上只确认守护进程和插件可用；基础镜像可达性、构建、测试和扫描仍待实测。

## 基础镜像可达性首次检查

组长在服务器执行 `docker buildx imagetools inspect`，目标为 Dockerfile 中的
`m.daocloud.io/docker.io/library/python@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74`。
镜像站对清单的 `HEAD` 请求返回 `502 Bad Gateway`。该结果只说明此次
镜像站请求失败，尚不能判定摘要错误或 Docker 安装异常；待核对 Docker Hub
原始地址和再次重试结果。

随后用相同摘要检查 `docker.io/library/python` 原站，`registry-1.docker.io`
连接解析得到的 `31.13.91.33:443` 超时（`i/o timeout`）。两条镜像路径均
未取得清单，尚未进入构建；下一步检查 ECS 的 DNS 和华为云 SWR 镜像加速器。
