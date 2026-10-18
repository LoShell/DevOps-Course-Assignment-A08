# A08 E4：可重复工程环境

本阶段把 BuildChecker 骨架接入 A08 仓库，使组员在同一台 Ubuntu 服务器上
从同一源码提交运行 `make all`，分别得到可对照的环境、构建、测试和扫描证据。
E4 只验证工程环境，不实现后续实验的检测算法。

## 仓库结构

E4 运行入口放在**仓库根目录**：`Makefile`、`compose.yaml`、
`requirements-dev.in`、`requirements-dev.lock`、`services/buildchecker/`、
`fixtures/md-rd/` 与 `scripts/`。原有 `E2/`、`E3/` 保留；
`fixtures/md-rd/` 是 E4 模板自带的冒烟样本，不覆盖 `E3/fixtures/md-rd/`。
Docker 构建上下文排除 E2、E3、E4 文档和证据。
基础镜像在 Dockerfile 中按 Docker Hub 摘要固定；本组 ECS 因原站超时，
在服务器的 Docker 守护进程中配置华为云 SWR 镜像加速器。加速器地址只保留
在服务器配置中，不写进仓库；组员共用这台服务器，无需各自重复配置。

## 组员连接服务器

本组实测校园网公网出口会变化，因此组长邀请组员加入同一 Tailscale 私有网络；
组员在自己的电脑连接 Tailscale 后，使用组内单独提供的 ECS 私有地址和登录账号
执行 `ssh -l <账号> <ECS的Tailscale地址>`。这是通过 Tailscale 网络连接
普通 OpenSSH。已有组员通过不同网络成功登录，不必为每次校园网出口变化修改
华为云公网 SSH 安全组规则。首次连接应核对服务器的 ED25519 主机指纹；
组长可在华为云远程控制台运行
`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` 提供核对值。密码只在
SSH 提示中输入，不写入文档或截图。

若 Tailscale 暂不可用，公网 SSH 可作为备用：组员在当前网络查自己的公网
IPv4，由组长仅对该地址的 `/32` 开放入方向 TCP 22，并在网络变化后重新
核对；不要把 SSH 来源长期设为 `0.0.0.0/0`。华为云 VNC 控制台仍是
服务器故障排查入口。

## 服务器上的运行顺序

组长先确认 Ubuntu 22.04、架构、Docker Engine、Compose、Buildx、Git、
Make 和 Python 3 可用。若 Docker 尚未安装，先核对系统，再由有管理员权限的
成员按课程实验包的 `setup/bootstrap_ubuntu.sh` 初始化一次。全组共用一台
2 GiB 服务器，组员依次构建，不同时执行 `make all`。

每位组员在服务器上用自己的学号建立目录，优先从 **A08 GitHub 仓库**
克隆 `a08/e4-environment` 分支，在克隆根目录设置本地 Git 身份：

```sh
mkdir -p /root/<学号>
cd /root/<学号>
git clone --branch a08/e4-environment https://github.com/LoShell/DevOps-Course-Assignment-A08.git buildchecker
cd buildchecker
git config --local user.name '<学号>'
git config --local user.email '<学号>@localhost'
git rev-parse HEAD
git status --short
```

本组实测 ECS 到 GitHub 的 HTTPS 连接偶发超时，而其他站点可达。若直连
GitHub 失败，可在组长确认 `/root/241250088/buildchecker-clean` 的 HEAD
正是下述基准 SHA 且工作区干净后，改从该服务器副本独立克隆：

```sh
cd /root/<学号>
git clone --no-local --branch a08/e4-environment /root/241250088/buildchecker-clean buildchecker
cd buildchecker
git remote set-url origin https://github.com/LoShell/DevOps-Course-Assignment-A08.git
git config --local user.name '<学号>'
git config --local user.email '<学号>@localhost'
git rev-parse HEAD
git status --short
```

若失败的直连克隆已创建 `buildchecker` 目录，先检查该目录，不要直接覆盖；
备用命令需要空的目标路径。采用备用方式时，在个人记录中注明实际克隆来源；
设置 `origin` 只保留远端地址，不表示当时成功从 GitHub 下载。

`<学号>` 必须替换为本人学号。不要在共享登录账号下设置全局 Git 身份。
本轮同版本复跑以 `4c1ff6caf40fc4f1d90b730cbc2477824a6d4576` 为基准：
运行 `make all` 前，`git rev-parse HEAD` 必须得到该值，`git status --short`
必须无输出；若分支已更新到其他提交，先停下并联系组长确认版本。
SSH 容易断开时，可在 `make all` 前进入以自己学号命名的 `tmux` 会话：

```sh
tmux new -s "e4-$(git config --local user.name)"
```

断线重连后用 `tmux attach -t e4-<学号>` 回到会话；若已在 `tmux` 内，
无需再新建。服务器只有 2 GiB 内存，组员依次运行，不并行构建。
确认轮到自己后，在克隆根目录运行：

```sh
make all
```

个人运行不要求创建提交或推送。`.env` 由 `make` 从示例生成，A 组 E4
不需要填真实 API Key；`work/` 中的个人运行证据默认不进入 Git。

## 验收点

一次成功的 `make all` 应在同一个 `work/<时间>/` 中留下 `env.json`、
`build.log`、`image.json`、`toolchain.lock`、`test.log`、`smoke.json` 和
`secret-scan.txt`。A 组模板预期单测为 `3 passed`，冒烟应记录
`config.h` 被打开、程序输出 `1` 且 `passed: true`，密钥扫描应显示未发现问题。
截至 2026-10-18，组长和三名组员均使用
`4c1ff6caf40fc4f1d90b730cbc2477824a6d4576`；071、076、097
各自的 `work/` 中均已确认七个预期文件。组员分别核对工具版本、测试与
冒烟结论，审阅结果和跨成员对照仍需记录，见贡献记录。

当前服务器按课程安排购买为 **2 vCPU、2 GiB、Ubuntu 22.04、80 GiB 系统盘**。
原模板的最低可见内存门槛为 **3.5 GiB**，在本组服务器上实测
`make doctor` 因 `mem_gib=1.7` 失败。按助教认可的 2 GiB ECS 规格，
本分支将最低可见内存调整为 **1.5 GiB**，保留低于建议值的警告；
Dockerfile 也改用已在本组 ECS 验证的基础镜像和 Debian APT 下载路径。
此前组长用个人克隆中的临时改动完成了一次 `make all`，证据目录为
`work/20261017-151409/`。该次运行不能代替更新后提交的干净克隆验证；
组长随后在干净克隆的 `4c1ff6c` 上再次运行成功，证据目录为
`work/20261017-152852/`。三名组员已在相同 SHA 的独立目录生成证据；
逐项结果与审阅结论仍需对照，详见服务器基线。

进度、责任与真实验证记录见 [BACKLOG.md](BACKLOG.md)、
[WORKFLOW.md](WORKFLOW.md)、[CONTRIBUTIONS.md](CONTRIBUTIONS.md)。
