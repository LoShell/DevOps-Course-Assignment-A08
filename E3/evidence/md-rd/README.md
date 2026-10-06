# 成员 2 MD/RD 本地验证记录

最新进展：Ubuntu 24.04 容器实验已通过，详见 [容器实验记录](docker-ubuntu24-20261006/README.md)。下方保留此前 WSL Ubuntu 22.04 的历史验证及环境障碍，容器状态以最新记录为准。

- 日期：2026-10-06
- 执行：进行本地开发与真实测试；成员 2 已于 2026-10-06 基于后续复核的真实输出确认 oracle 通过。
- 最终运行目录：[20261006T033800321061Z](20261006T033800321061Z/observations.json)
- 原始命令、输出和退出码：[commands.txt](20261006T033800321061Z/commands.txt)
- 环境：WSL Ubuntu 22.04.5 LTS、x86_64、GCC 11.4.0、GNU Make 4.3。
- 运行入口：仓库根目录执行 `bash E3/scripts/run-md-rd.sh`。
- 结果：PASS；18 条外部命令退出码均为 0，14 项断言全部通过。

| 场景 | 实际结果 |
|---|---|
| 初始干净构建 | demo 1.0.0；行为输出 10 |
| config.h 的 CONFIG_VALUE 从 4 改为 5，普通 make | 对象文件时间戳和哈希不变，仍输出 10 |
| 相同源码 clean 后重新构建 | 输出 11 |
| 只修改 unused.h 注释 | 实际重新编译，对象文件时间戳更新，输出仍为 11 |
| GCC 项目依赖 | common.h、config.h；不含 unused.h |
| 测试前后源码 | 文件哈希一致，测试修改只发生于临时副本 |

## 版本和证据边界

基础提交为 60318cf03e7f988058160ccf422147cf2d424e04。
observations.json 的 source_sha256 标识本次实际测试的样例、脚本和 oracle。
不得把基础提交误写为新样例提交 SHA。

局部配置标识为 local-md-rd-0a2e1a7a3e9c85e8，计算依据见脚本，
仅用于区分本地证据，不冒充团队 configuration_id。

这是故障样本的行为验证和人工依据，不是 BuildChecker 的自动检测报告。
Oracle 由 AI 辅助起草，成员 2 已确认通过；见 [人工确认记录](oracle-review-20261006-132502/REVIEW.md)。没有生成 Linux strace 跟踪。

## 首次 WSL 验证时的环境障碍（历史记录，Docker 已恢复可用）

本机默认 Docker 端点检查失败：docker version 返回 1，提示无法连接
npipe:////./pipe/docker_engine，且沙箱不能读取用户 Docker 配置。
这不证明其他 Docker context 一定不可用；本次未启动服务、安装软件或修改系统配置。
Ubuntu 24.04 Dockerfile 已编写，但未构建或运行验证，也没有镜像 ID。
Ubuntu 22.04 的验证不能替代组长 Ubuntu 24.04 容器环境的复核。

WSL 在默认沙箱下枚举发行版报 E_ACCESSDENIED，经执行权限审核后可运行。
首次测试已通过，随后隔离子进程环境（只传 PATH/LANG/LC_ALL），避免 make -pn
夹带用户环境变量，再次测试通过；最终保留的是上述第二次证据。

## 待补信息

- 已完成：成员 2 根据真实复核输出确认 oracle 的两条判断和运行证据。
- 已补齐 Ubuntu 24.04 容器验证及镜像 ID，见上方最新记录。
- 与组长确认团队 configuration_id。
- 记录样例的真实 SHA，补齐 oracle 和个人贡献记录。
- 汇总负责人同步 BACKLOG、CONTRIBUTIONS 与公共进度。
