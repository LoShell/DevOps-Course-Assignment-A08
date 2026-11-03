# E5 专项审阅：工具链、进程树与目标归属

审阅人：范从钰（241250071）  
日期：2026-10-31  
范围：工具链记录、E5 进程树、成功读写、编译/链接目标归属。  
状态：本人实测完成，归档与提交待后续安排。

## 对象

- 完整运行 SHA：`25e57544fe7b98e496aeea8681e5cfaca128a255`
- 个人分支：`a08/241250071/e5-e6`
- 运行前工作区：干净，无额外差异。
- 本人运行目录：
  - 自检：`work/e5-preflight-20261031-162026/`
  - 构建与单测：`work/e5-build-20261031-162026/`
  - E5 原始证据：`work/e5-run-20261031-162026/evidence/`
- 镜像：`course1027-buildchecker:241250071`
- 镜像 ID：`sha256:eca7a492b08860a6c2da212e0b1fb2b92b161e0fc559da753abf351495a5b186`

## 观察和结论

| 检查点 | 实际观察 | 文件 / PID / 行号等依据 | 结论或问题 |
| --- | --- | --- | --- |
| 工具链记录 | 镜像内记录 GCC 14.2.0、Make 4.4.1、strace 6.13、Git 2.47.3、Python 3.13.14、amd64，以及 pip 依赖版本。 | `work/e5-build-20261031-162026/toolchain.lock` | 通过。工具链和 Python 测试依赖的实际版本可追溯。 |
| 构建与测试 | 镜像构建退出码为 0，单测退出码为 0，结果为 `15 passed`。 | `work/e5-build-20261031-162026/build/exit-code.json`、`unit-tests/exit-code.json` 及测试日志 | 通过。 |
| Make 到编译进程链 | make（PID 15）派生编译 cc（PID 16），编译 cc 再派生 cc1（PID 17）与 as（PID 18）。 | `trace/t.15` 第 1、55 行；`trace/t.16` 第 1、64、84 行；`trace/t.17`、`t.18` 第 1 行 | 通过。`main.o` 读写可归属同一编译作业。 |
| `config.h` 成功读取 | cc1 成功以只读方式打开 `main.c` 与 `config.h`。 | `trace/t.17` 第 67 行：`main.c`；第 580 行：`openat(..., "config.h", O_RDONLY...) = 4` | 通过。该记录是成功打开，不是失败探测、stat 或 access。 |
| `main.o` 写入 | as 以创建、截断、读写方式打开 `main.o`。 | `trace/t.18` 第 23 行：`openat(..., "main.o", O_RDWR|O_CREAT|O_TRUNC, 0666) = 3` | 通过。`main.o` 写入归属汇编阶段。 |
| 链接进程链 | 链接 cc（PID 19）派生 collect2（PID 20），collect2 再派生 ld（PID 21）。 | `trace/t.19` 第 1、129 行；`trace/t.20` 第 1、96 行；`trace/t.21` 第 1 行 | 通过。最终目标归属可追溯到 ld。 |
| `app` 读取与写入 | ld 命令包含 `main.o` 和 `-o app`；随后只读打开 `main.o`，并创建/截断写入 `app`。 | `trace/t.21` 第 1 行、71 行、82–83 行 | 通过。`app` 的实际项目依赖为 `main.o`。 |
| Make 声明与 MD/RD | `main.o` 声明 `main.c unused.h`，但实际读取 `main.c config.h`；`app` 声明与实际均为 `main.o`。 | `make-db.txt` 第 1061 行：`main.o: main.c unused.h`；第 609 行：`app: main.o` | `main.o` 的 MD 为 `config.h`，RD 为 `unused.h`；`app` 一致。 |
| E5 运行结果 | runner 退出码为 0，程序输出为 `1`。 | `work/e5-run-20261031-162026/runner/exit-code.json`、`evidence/program-output.txt` | 通过。 |

本次审阅基于本人运行的原始 trace、Make 数据库和日志；未将 grep 的失败尝试或系统运行库误计为项目依赖。`clone3` 的 `ENOSYS` 后转为 `clone` 属于正常兼容回退，不构成运行失败。

未覆盖范围：本次只有单个 Make 进程、一个编译目标和一个链接目标，未验证多目标、增量构建、并行构建或大规模项目场景。组内其他成员的证据和统一对照由 `integration.md` 另行汇总。
