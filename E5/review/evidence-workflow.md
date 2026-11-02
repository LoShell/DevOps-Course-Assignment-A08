# E5 专项审阅：命令、退出码、证据完整性与备份

审阅人：叶原原（241250076）。

实验日期：2026-10-31；文档整理及本地复核日期：2026-11-03。

状态：已执行待审阅；本人实测与原始证据备份核验完成；全组原包抽查、最终提交包及平台验收未完成。

## 对象与审阅方式

- 完整运行 SHA：`25e57544fe7b98e496aeea8681e5cfaca128a255`。
- 个人分支：`a08/241250076/e5-e6`；服务器仓库：`/root/241250076/buildchecker`。
- 本人记录：[E5/records/241250076.md](../records/241250076.md)。文档正文提交 SHA：`7e34933595d8faea5c8b1ff1ac0b390f2bda7ec5`；个人 PR：[PR #8](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/8)，目标为 `a08/e5-e6`，待组长审阅。之后补充 PR 索引的提交与实验运行 SHA 分开记录。
- 自检目录：`work/e5-preflight-20261031-215818/`；构建目录：`work/e5-build-20261031-215818/`；E5 目录：`work/e5-run-20261031-215818/`。下文以这三个目录分别指代自检、构建和实验材料。
- 源码：运行基准中的 `scripts/course.py`、`scripts/lab_cloud.py`、`scripts/doctor.py`、服务 Dockerfile 和 `fixtures/md-rd/`。
- 原始测试前后工作区均干净。个人仓库初始仍在 E4，经本人确认后按指南同步指定基准，再开始测试；未改写样例 Makefile、源码或资源门槛。
- 2026-10-31 通过 Codex 辅助的 SSH 会话执行既有脚本并核对服务器证据；2026-11-03 在电脑保存的归档和解压副本上重新校验。此次补文档没有重新登录服务器、构建镜像或运行 E5/E6。
- 对其他成员仅只读查看了远端个人文档，不将文档回报等同于原包核验。

## 观察和结论

| 检查点 | 实际观察 | 文件或原始依据 | 结论或问题 |
| --- | --- | --- | --- |
| 身份与版本 | 学号 241250076；三个目录的 source-commit 均为统一 SHA | 各自 `source-commit.txt`；自检 `student-id.txt`、`student-email.txt`、`git-status.txt` | 本人目录与运行版本可追溯 |
| 个人自检 | 即时退出码 0，problems 为空，保留三项资源建议警告 | 自检 `doctor-console.log`、`exit-code.txt` | 满足统一基准的最低要求，未自行调整门槛 |
| 镜像构建 | 包装入口及 Docker 构建退出码均为 0 | 构建 `wrapper-exit-code.txt`、`build/exit-code.json`、完整构建日志 | 镜像构建成功 |
| 服务单测 | 退出码 0，实际日志为 `15 passed in 0.05s` | 构建 `unit-tests/exit-code.json`、`stdout.log`、`stderr.log` | 15 项单测通过，不以包装入口成功替代子步骤核验 |
| 镜像与工具链 | E5 inspect 的 ID 与构建保存的 ID 相同；宿主机与镜像工具版本分别记录 | 构建 `image/`、`image-id.txt`、`toolchain.lock`；E5 `service-image-inspect.json` | 运行镜像与本人的构建记录对应 |
| E5 执行 | 包装入口 0、runner 0、程序输出 1 | E5 `wrapper-exit-code.txt`、`runner/exit-code.json`、`evidence/program-output.txt` | 原始采集执行成功，不与 E6 检测结果混淆 |
| 实际输入 | 四个副本与基准样例一致；VALUE=1，声明仍为 main.c/unused.h | `evidence/main.c`、`config.h`、`unused.h`、`Makefile` | 未先修复依赖声明 |
| 原始采集 | 全部 7 个 trace、Make 数据库、程序输出和构建错误流均存在 | `evidence/trace/t.14` 至 `t.20`、`make-db.txt`、`program-output.txt`、`build-stderr.log` | 保留完整记录，未只保留 grep 截图 |
| 产物与空日志 | main.o、app 为 ELF；构建错误流及 runner 错误流长度为 0 | `evidence/main.o`、`app`、`build-stderr.log`；`runner/stderr.log` | 产物存在，空错误流不是缺失文件 |
| 调用关系 | 保存运行阶段、镜像、容器命令、容器 ID、源码 SHA 和同次证据目录 | `invocation.json`、`runner/command.json`、`service-container-id.txt`、`related-evidence.txt`；自检 `run-paths.json` | 命令、版本、构建和运行证据相互关联 |
| 原始文件校验 | 内部 SHA-256 清单覆盖 55 个证据文件 | E5 `file-checksums.sha256`；电脑归档及解压副本逐项复核 | 全部通过，未把目录及源码条目混算为证据文件数 |
| 归档与电脑备份 | 归档可读，96 个成员条目，服务器生成记录与电脑归档摘要一致 | 归档、`.contents.txt`、`.sha256`、`backup-verification.json` 及 2026-11-03 本地复核 | 原始证据快照已保留两份；本轮未重新检查服务器实时状态 |
| 报告覆盖范围 | 原包生成于报告补写前，未含本次两份文档 | 归档成员清单中没有 `E5/` 文档 | 不能称为已包含最终报告的提交包，定稿后仍需更新 |

### 命令与退出码保存

在个人仓库依次运行：

```bash
python3 scripts/course.py doctor
python3 scripts/course.py build --out work/e5-build-20261031-215818 --build-timeout 1200
python3 scripts/course.py e5 --out work/e5-run-20261031-215818
```

每一步结束后通过 `if command; then CODE=0; else CODE=$?; fi` 立即保存返回值，再执行后续命令。自检写入 `exit-code.txt`；构建与 E5 分别写入包装入口退出码，随后读取各子步骤 `exit-code.json`、完整 stdout/stderr。构建还核对实际 `15 passed` 文本，E5 核对程序输出，而非仅判断最外层返回 0。

三个输出目录采用同一时间戳，且创建前检查不存在，未覆盖旧记录。SHA、工作区、构建结果和镜像对应关系检查通过后才继续下一步。E5 保留的容器命令是禁网、SYS_PTRACE、user 0:0，并在独立输入副本上先 clean build 再采集。

### 原始证据能够支持的判定

本人编译链为 make（14）→ cc（15）→ cc1（16）和 as（17）；链接链为 make（14）→ cc（18）→ collect2（19）→ ld（20）。父子关系依据 `t.14:55,66`、`t.15:64,84`、`t.18:129`、`t.19:96`，并结合各进程成功 execve 核对。

| 判定 | 成功打开与声明依据 |
| --- | --- |
| main.o 的实际项目输入为 main.c、config.h | `t.16:67,580` 以 `O_RDONLY|O_NOCTTY` 成功打开，返回 3、4；同作业 `t.17:23` 创建 main.o |
| main.o 的 MD=config.h、RD=unused.h | `make-db.txt:1061` 为 `main.o: main.c unused.h`；unused.h 只在 `t.14:46` 命中状态检查，没有编译作业成功读取记录 |
| app 的实际与声明依赖一致 | `t.20:71` 创建 app，`t.20:82–83` 成功只读打开 main.o；`make-db.txt:609` 为 `app: main.o` |

本次 `%file,%process` 记录支持成功打开及目标归属，不包含逐字节的 read/write 跟踪。失败的 open、stat/access 和路径搜索不代替成功读取；系统头文件、工具链及编译临时文件不纳入项目输入集合。以上结论仅适用于本次样例和构建配置。

## 归档与备份核验

- 原始归档：`/root/devops-submissions/241250076/A08-241250076-E5-20261031-220102.tar.gz`，2026-10-31 22:01:02 生成（北京时间）。
- 归档 SHA-256：`caca6386ce36bd04eee43197a97319a3ac2cc3633179a8fa8f8a62b950f01e01`。
- 电脑当前目录：`D:\MyDocument\Download\DevOps-Course-Assignment-A08\work\E5-backup-241250076-20261031-215818\`。
- 备份包括原归档、`.contents.txt`、`.sha256`、`backup-verification.json` 和 `extracted/`；原始 work/ 不提交 Git。
- 原工作区从 `Download\devops-labs\DevOps-Course-Assignment-A08` 迁移到当前目录。保留原校验 JSON 的历史路径字段，文档列出实际可访问的新位置；2026-11-03 重新核验了归档及解压文件，未修改旧快照。

归档只包含本人本次自检、构建、E5 三个证据目录及必要源码。成员清单核对未包含其他成员 work/、认证目录、`.git`、真实 `.env` 或私钥，也未打包全部 `/root`。96 个条目包含目录和源码；内部清单覆盖的 55 个证据文件、7 个 trace 和两个 ELF 产物分别核对，统计口径不同。

2026-10-31 的备份核验包括：比较服务器生成的归档 SHA-256 与电脑文件；确认成员清单一致；读取压缩包内容；逐一校验内部清单；解压并再次校验 55 个文件；核对三个目录的基准 SHA、构建/单测/E5 退出码、15 passed、输出 1、镜像 ID、输入副本及关键 trace。2026-11-03 又在迁移后的本地目录重算归档摘要，并逐项检查归档与解压副本的 55 个文件。

**备份边界：**现有文件是原始证据快照，不含本次报告，也没有课程平台上传回执。文档定稿后应另建包含报告、必要源码和完整证据的最终包，保留旧快照；本次文档 PR 不重建服务器归档、不上传压缩包，也不声称 E5 已完成平台验收。

## 跨成员文档对照与后续事项

2026-11-03 只读查看以下远端个人记录及专项审阅，参考其结构并对照回报字段：

| 成员与参考版本 | 文档回报 | 本次核验级别 |
| --- | --- | --- |
| 范从钰 241250071，[PR #6](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/6)，参考分支提交 `6c89f21251aa189f55f7a1d075bc48ffb27c55dc` | 运行 SHA 相同，15 passed、E5 退出 0、输出 1；MD=config.h、RD=unused.h；cc1/as/ld 为 17/18/21 | 阅读其个人记录与 process-trace.md，未读取原始归档 |
| 邱莉扉 241250097，[PR #7](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/7)，参考分支提交 `d5b701c76675e52e6c57f44338e841be923345e2` | 运行 SHA 相同，15 passed、E5 退出 0、输出 1；MD=config.h、RD=unused.h；cc1/as/ld 为 16/17/20 | 阅读其个人记录与 sample-declarations.md，未读取原始归档 |

文档回报与本人实测结论一致，但不能据此替代全组同基准原包抽查，也未核验其他成员的归档哈希、下载文件或当前服务器状态。共同报告、贡献总表及整合审阅由组长维护。

AI 使用：Codex 协助执行既有课程脚本、读取和定位证据、计算校验值并整理两份文档；本人完成登录密码输入和 GitHub 网页授权。这里明确区分本人运行记录、保存材料的复核、远端文档参考与尚未开展的跨成员原包审阅。

后续事项：组长审阅个人 PR、全组原包抽查、定稿后更新最终归档及电脑备份、核对课程平台要求并确认上传状态。本次未开展 E6、增量构建、并行多目标或大规模项目验证。
