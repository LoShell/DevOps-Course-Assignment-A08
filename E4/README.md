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

## 组员连接服务器前：确认公网 IP

组员先连接**准备使用 SSH 的网络**，在自己的电脑上查询公网 IPv4。Windows
PowerShell 运行（不要在云服务器里运行）：

```powershell
curl.exe --noproxy "*" -4 https://api.ipify.org
curl.exe --noproxy "*" -4 https://ipv4.icanhazip.com
```

macOS/Linux 终端把 `curl.exe` 换成 `curl`。两次查询应得到同一个 IPv4；
把结果和当前使用的网络（校园网、宿舍网或手机热点）发给组长，**不要发送密码**。
电脑显示的 `10.x.x.x`、`172.16.x.x`～`172.31.x.x` 或 `192.168.x.x`
是内网地址，不能作为这里的公网来源地址。即使同在校园网，也要各自查询，
不能假定出口 IP 相同。

组长在**这台 ECS 实际关联的安全组**中，为每位组员的公网 IPv4 添加
入方向 `TCP 22`、来源 `<该 IPv4>/32` 的允许规则；若多人查到同一地址，
一条规则即可。不要为方便登录而长期把 SSH 来源设为 `0.0.0.0/0`。
组员切换 VPN、代理、手机热点、校园网/宿舍网，或后来无法连接时，先在
当前网络重新运行上述命令；公网出口可能改变，应由组长核对并更新安全组。
网页代理与 SSH 也可能使用不同出口；若地址看似正确仍连不上，联系组长
一起检查关联的安全组和服务器连接日志，不要反复猜测地址。

规则生效后，组员使用组长通过组内渠道提供的 ECS 公网 IP 和登录账号
执行 `ssh -l <账号> <ECS公网IP>`。首次连接会提示核对服务器主机指纹；
组长可在华为云远程控制台运行
`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`，组员核对一致后再输入
`yes`。登录密码仅在 SSH 提示中输入，不写进文档、命令或截图。

## 服务器上的运行顺序

组长先确认 Ubuntu 22.04、架构、Docker Engine、Compose、Buildx、Git、
Make 和 Python 3 可用。若 Docker 尚未安装，先核对系统，再由有管理员权限的
成员按课程实验包的 `setup/bootstrap_ubuntu.sh` 初始化一次。全组共用一台
2 GiB 服务器，组员依次构建，不同时执行 `make all`。

每位组员在服务器上用自己的学号建立目录，从 **A08 GitHub 仓库**克隆
`a08/e4-environment` 分支，在克隆根目录设置本地 Git 身份并运行：

```sh
mkdir -p /root/<学号>
cd /root/<学号>
git clone --branch a08/e4-environment https://github.com/LoShell/DevOps-Course-Assignment-A08.git buildchecker
cd buildchecker
git config --local user.name '<学号>'
git config --local user.email '<学号>@localhost'
git rev-parse HEAD
git status --short
make all
```

`<学号>` 必须替换为本人学号。不要在共享登录账号下设置全局 Git 身份。
个人运行不要求创建提交或推送。`.env` 由 `make` 从示例生成，A 组 E4
不需要填真实 API Key；`work/` 中的个人运行证据默认不进入 Git。

## 验收点

一次成功的 `make all` 应在同一个 `work/<时间>/` 中留下 `env.json`、
`build.log`、`image.json`、`toolchain.lock`、`test.log`、`smoke.json` 和
`secret-scan.txt`。A 组模板预期单测为 `3 passed`，冒烟应记录
`config.h` 被打开、程序输出 `1` 且 `passed: true`，密钥扫描应显示未发现问题。
另一名组员在自己的学号目录从同一源码 SHA 重跑，比较工具版本和结论。

当前服务器按课程安排购买为 **2 vCPU、2 GiB、Ubuntu 22.04、80 GiB 系统盘**。
当前仓库的最低可见内存门槛仍为 **3.5 GiB**，在本组服务器上实测
`make doctor` 因 `mem_gib=1.7` 失败。按助教认可的 2 GiB ECS 规格，
组长在个人克隆中**临时、未提交**地把门槛调为 **1.5 GiB**，重跑自检已通过，
低于建议内存仍有警告。是否正式修改模板，待完整 `make all` 的真实构建
结果和组内审阅确定；单独通过自检不等于 E4 验收通过。

进度、责任与真实验证记录见 [BACKLOG.md](BACKLOG.md)、
[WORKFLOW.md](WORKFLOW.md)、[CONTRIBUTIONS.md](CONTRIBUTIONS.md)。
