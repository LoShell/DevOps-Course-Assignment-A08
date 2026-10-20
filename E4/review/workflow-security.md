# E4 一键命令、自检与密钥扫描审阅

- 审阅人：叶原原（241250076）
- 审阅日期：2026-10-20
- 个人复跑源码 SHA：`4c1ff6caf40fc4f1d90b730cbc2477824a6d4576`
- 个人复跑证据目录：`/root/241250076/buildchecker/work/20261018-152841/`
- 本次本地审阅提交：`ce27f2a603876146178aa827478c6936d75f507a`
- 审阅方式：AI 辅助源码核查、本地命令预演和隔离测试；服务器结果引用 [服务器基线](../SERVER_BASELINE.md) 与 [贡献记录](../CONTRIBUTIONS.md)。本次未连接 ECS，未重新读取个人原始证据，也未重新执行服务器 `make all`。

## 1. 检查范围与结论

检查根目录 `Makefile`、`scripts/doctor.py`、`scripts/secret_scan.py`、
`.gitignore`、`.dockerignore`，并核对 `compose.yaml` 的镜像命名和环境配置。
上述文件在本次审阅提交与个人复跑 SHA 之间没有差异，因此源码核查适用于
已记录的复跑版本。

按现有服务器记录，个人复跑的七个证据文件齐全，测试、冒烟与扫描符合 E4
预期；1.5 GiB 可见内存门槛保留了建议资源警告，并已有 2 GiB ECS 的完整
运行结果支持。专项审阅完成，同时发现部分管道未检查上游退出码、扫描范围
有限等边界，详见下文。不能把扫描通过解释为所有文件和镜像层均无密钥。

## 2. 一键命令与失败处理

`all: doctor build test smoke scan` 在默认串行 `make all` 下依次执行五步。
`STAMP := ...`、`RUN := work/$(STAMP)` 在同一次 Make 调用内只求值一次，
各步骤共用一个目录；单独执行 `make doctor` 或 `make scan` 会重新计算时间，
不能把不同调用的目录拼成一次完整运行。

| 入口 | 核查结果 |
| --- | --- |
| `doctor` | 创建证据目录，直接执行 Python 自检；必需项失败会阻止串行 `all` 继续 |
| `build` | 必要时从示例复制 `.env` 并设置权限 `600`；构建输出保存到 `build.log`，随后导出镜像元数据和工具链 |
| `test` / `smoke` | 在容器内运行，使用 `-T --interactive=false`，外层 `timeout 600` 限时 |
| `scan` | 扫描已跟踪文件、Git 历史、当前学号镜像的历史命令与环境变量 |
| 镜像命名 | `e4-buildchecker:$(STUDENT_ID)` 与 Compose 一致；应先设置本仓库的学号身份，避免回退到全局身份或 `local` |

构建、测试、冒烟、扫描的主命令使用 `PIPESTATUS[0]`，避免 `tee` 成功掩盖
上游失败。脚本扫描发现匹配时退出 `1`，镜像检查命令失败时退出 `2`；GNU Make
遇到配方错误通常自身退出 `2`，不能将它误记为扫描脚本的退出码。

以下限制需保留在复跑约定中：

- `docker image inspect ... | tee image.json` 和工具链导出的管道没有同样的
  退出码检查，也未启用 `pipefail`。上游失败可能被 `tee` 掩盖，所以必须另查
  `image.json` 是否有效、`toolchain.lock` 是否非空，不能只看最后的目录提示。
- 五个目标之间没有显式依赖链。不要使用 `make -j all` 或带并行参数的
  `MAKEFLAGS`；共享服务器还应按工作流程依次构建。
- 时间戳精度为秒；在同一秒启动的多次 Make 调用可能复用目录。现有记录中
  的成功目录不同；执行时仍应避免同目录并发运行。

这些事项作为审阅发现记录；本次未修改公共 Makefile，保留同 SHA 复跑依据。

## 3. 环境自检与 2 GiB 差异

`doctor.py` 检查 Linux、可见 CPU/内存、Docker 所在文件系统的可用磁盘、
Docker Engine、Compose、Git、Make、Python 和本仓库 Git 身份；Buildx
为建议项。`env.json` 即使在自检失败时也会写出，不能以文件存在判断通过，
还要核对退出码与 `problems`。

| 项目 | 最低值 | 建议值 | 审阅观察 |
| --- | --- | --- | --- |
| 可见 CPU | 2 | 4 | ECS 的 2 核达到最低值，低于建议值时警告 |
| 可见内存 | 1.5 GiB | 8 GiB | 原门槛为 3.5 GiB；实测约 1.7 GiB 的 2 GiB ECS 改为通过并保留警告 |
| 可用磁盘 | 40 GiB | 100 GiB | 检查剩余空间，不是购买磁盘总容量；原自检记录约 70.3 GiB |

服务器基线记录原门槛下自检失败，调整后 `problems` 为空，随后组长及三名
组员在干净的 `4c1ff6c` 完成 `make all`。这支持本组 E4 模板的资源适配，
不能推断后续真实项目也能在相同资源下构建。

本地隔离测试确认：模拟 2 核、1.7 GiB、70.3 GiB 时通过并保留三项资源
警告；内存 1.4 GiB、单核、磁盘 39 GiB、Docker/Compose 不可用、缺少
本地身份或非 Linux 均被拒绝；缺少 Buildx 仅警告。测试使用模拟数据，
不构成新的 ECS 实测。

另有边界：内存读取失败返回 `None` 时会跳过内存门槛，当前不会记入
`problems`。`env.json` 也不自动记录源码 SHA 或工作区状态，因此必须另行
保存 `git rev-parse HEAD` 和 `git status --short` 的结果。

## 4. 七份证据与现有记录

以下路径均相对于个人复跑目录，完整性结论来自现有服务器记录；本次没有
直接读取 ECS 上的七份原始文件。

| 文件 | 用途与核查要点 | 现有记录支持的结论 |
| --- | --- | --- |
| `env.json` | 系统、资源、工具、本地身份、`problems` 与 `warnings` | 文件存在；个人文件的完整字段未在仓库展开，不补写未见数值 |
| `build.log` | Docker 构建过程及错误 | 文件存在；原记录为完整 `make all` 成功，未逐行复查个人日志 |
| `image.json` | 镜像名称、ID、架构、创建时间 | 文件存在；未从其他成员记录推定个人镜像 ID |
| `toolchain.lock` | 实际工具链与 Python 包版本 | 四份 SHA-256 均为 `bc70f4e9e436d2567c88588171d7fd4575a614c442874baa089407106bbf9358` |
| `test.log` | 单测结果 | 四份尾行均为 `3 passed in 0.01s` |
| `smoke.json` | 构建、程序输出及文件打开情况 | 同 SHA 对照为 `make_exit_code: 0`、输出 `1`、`config_h_opened` 非空、`unused_h_opened` 为空、`passed: true` |
| `secret-scan.txt` | 工作区、历史和个人镜像的扫描输出 | 文件存在，个人运行终端记录显示未发现问题；本次未独立检查服务器镜像 |

`.gitignore` 忽略 `.env`、个人 `work/` 和私钥扩展名；`.dockerignore`
同时排除 `.env*`、`work`、`.git`、私钥文件及 E2/E3/E4 文档。Compose
没有 `env_file`，A 组本阶段不需要填写真实 API Key。本地
`git ls-files work .env` 无输出，`git check-ignore` 确认两类路径受忽略。

## 5. 密钥扫描与负向验证

扫描器覆盖 API Key、私钥头、GitHub Token 和常见密钥赋值模式；输出仅保留
匹配值前四位。它另外拒绝 Git 跟踪的 `.env`/非示例环境配置文件，并在
POSIX 系统检查现有 `.env` 的权限，不读取该文件中的密钥内容。

组长已有真实服务器负向记录：暂存假 Key 文件后，
`work/20261018-163542/secret-scan.txt` 报告两种模式匹配，`make scan`
退出 `2`；移除暂存并删除文件后，`work/20261018-163607/` 的扫描退出
`0`，工作区干净且 `.env` 未被跟踪。这是组长的验证，不记为本人新执行。

本次在系统临时目录内建立独立 Git 仓库，用纯合成假值验证：干净仓库通过；
暂存假值后脚本退出 `1`、报告两处且完整假值未出现在输出；提交假值再删除
后，普通扫描通过而 `--history` 仍检出；跟踪空 `.env` 被拒绝。另通过模拟
Docker 命令失败确认镜像检查退出 `2`。测试未改动课程仓库的暂存区或历史，
临时仓库已自动清理。

扫描范围有以下边界：

- Git 仓库使用 `git ls-files`，未跟踪或已忽略的文件不在扫描列表内；本地
  负向测试确认未暂存的假值文件会被跳过。非 Git 目录才使用递归遍历。
- 工作区扫描跳过大于 2,000,000 字节的文件和无法读取的文件；正则只覆盖
  已列模式，不能证明没有其他形式的凭据。
- `--history` 使用本地 `git log --all -p`，只涉及本地可见历史；Git 历史
  命令的返回码未显式检查，失败不能当作已完成历史审阅。
- `--image` 读取 `docker history --no-trunc` 与镜像 `Config.Env`，没有
  导出或逐层扫描镜像文件系统。经 `COPY` 写入镜像文件的秘密可能漏检。

## 6. 本次本地验证与交付

本地共完成 21 项核查，均得到预期结果（其中部分用于确认已知限制，并不表示
这些限制已修复）。使用 Python 3.13.5 运行隔离核查，并在 WSL Ubuntu 使用 GNU Make
预演 `make -n all STUDENT_ID=241250076 STAMP=review-dry-run`，确认五步
顺序与同一目录下七个输出路径。Bash 对照实验确认主命令的 `PIPESTATUS`
能保留失败，普通管道则会掩盖失败。这些检查不调用 Docker 构建。

本地执行 `python -X utf8 scripts/secret_scan.py . --history` 返回 `0`，
扫描当前已跟踪文件及全部已获取的本地分支历史，未发现问题。本机 Docker
守护进程不可连接，所以没有执行本地镜像扫描、容器测试或完整 `make all`。

本地核查脚本、结果与命令预演保留在被忽略的
`work/20261020-workflow-security-review/`（`verify_review.py`、`checks.json`、
`make-dry-run.txt`、`secret-scan.txt`），与 ECS 的七份运行证据分别记录。
后续若修订公共脚本，应由组内确定负责人，并以新提交重新运行完整流程。
