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
模板 `scripts/doctor.py` 的最低可见内存仍为 **3.5 GiB**，因此原样执行
`make all` 会在 `doctor` 步骤失败。这里如实保留该差异；先记录服务器
`/proc/meminfo`、Docker 和实际构建结果，再按助教确认的课程标准修订
自检门槛并重新运行完整流程。不能把单独通过的后续步骤当成 `make all` 通过。

进度、责任与真实验证记录见 [BACKLOG.md](BACKLOG.md)、
[WORKFLOW.md](WORKFLOW.md)、[CONTRIBUTIONS.md](CONTRIBUTIONS.md)。
