# E3 组长独立复现检查

- 日期：2026-10-09。
- 执行人：刘馨雅；复核依据为其 Ubuntu 终端回传及已提交的原始证据。
- 工作分支：`a08/e3-baseline`；证据最晚提交：`c354dcb39afc0c2ff3f5486d053c369b3710da83`。
- 本记录汇总 E3 样本行为，不是 BuildChecker/EChecker 自动检测报告，也不是 B08 接口联调结果。

| 项目 | 固定输入及环境 | 实际结果 | 原始证据 |
|---|---|---|---|
| 固定 MD/RD | 样本提交 `8a9cfc46d854e697fd397c1f6c579014e219144b`；Ubuntu 24.04 宿主机 | `bash E3/scripts/run-md-rd.sh` 返回 `PASS`；18 条命令、14/14 项断言通过 | [observations.json](md-rd/20261009T031730569317Z/observations.json)、[commands.txt](md-rd/20261009T031730569317Z/commands.txt) |
| C0 | `e3-c0` = `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`；由标签导出的源码构建 Ubuntu 24.04.5 镜像 | Docker 构建完成；`./bin/demo --version` 为 `demo 1.0.0`，`./bin/demo` 为 `10` | [完整构建日志](environment/c0-replay-20261009T032247Z/docker-build.log)、[提交 SHA](environment/c0-replay-20261009T032247Z/commit.txt)、[环境](environment/c0-replay-20261009T032247Z/container-environment.txt)、[输出](environment/c0-replay-20261009T032247Z/output.txt) |
| C1→C2 | `e3-c1` = `4b70cabad1be8f6e98ee90ed9c5803b7aa793253`；`e3-c2` = `56deea9199679907893fa53add1d867ff62028e1`；同一 Ubuntu 24.04.5 容器 | `python3 E3/scripts/run_incremental.py --operator "刘馨雅"` 返回 `PASS`；37/37 项断言通过；C1 干净构建 12、C2 普通增量 12、C2 干净重建 19 | [运行说明](c2/20261009T111743059182+0800/README.md)、[observations.json](c2/20261009T111743059182+0800/observations.json)、[commands.txt](c2/20261009T111743059182+0800/commands.txt) |

C0 使用 `git archive e3-c0` 导出固定源码到临时目录，再从该目录执行
`docker build --no-cache --progress=plain -f "$SNAP/E3/fixtures/incremental/Dockerfile" -t a08-e3-c0:replay "$SNAP"`，
并以 `tee` 保存合并输出。本次镜像 ID 见
[image-id.txt](environment/c0-replay-20261009T032247Z/image-id.txt)；
它与 2026-10-05 首次构建的镜像 ID 不同。重新安装当前软件包后得到新镜像，
不能把两次构建的 ID 混写。C0 构建日志末尾为 `DONE`，但原始日志没有单独
保存 `docker build` 的数值退出码；成功判断还依据终端执行结果及随后成功的
容器运行。C0 其余运行命令的输出分文件保存，亦未单独记录退出码。

MD/RD 复现脚本的 `executor` 字段固定写为早期“Codex 代成员 2 执行”，
因此这次 observations.json 的该字段不能证明实际操作者。本次组长执行身份
依据其 Ubuntu 终端回传；不修改历史生成记录。C2 运行目录中“待成员 4 确认”
也是运行时快照，后续人工确认见[独立审阅记录](../oracle/incremental-review-20261009.md)。

## 检查结论与边界

上述三项由组长在本地 Ubuntu/Docker 环境独立复现，结果均符合 E3 人工 oracle；
不依赖 B08 尚未交付的运行产物。固定 MD/RD 的负责人确认见
[成员 2 审阅记录](md-rd/oracle-review-20261006-132502/REVIEW.md)。

剩余待办是形成跨提交稳定的团队 `configuration_id` 并按真实环境核对 C0、
C1、C2 和固定 MD/RD。现有 C1/C2 实测编号包含当次镜像 ID，仅标识对应运行；
C2 的 `-DMODE=7` 改变关键编译选项，不能将 C1→C2 行为对比冒充 E2 同配置
增量请求。处理原则见 [契约引用](../CONTRACT_REFERENCE.md)。
