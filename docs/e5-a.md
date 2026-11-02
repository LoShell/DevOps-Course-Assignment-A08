# A08 E5：原始证据与人工 MD/RD 分析

状态：报告整理中。四人已回报同基准 E5 成功，组长个人关键证据已核对；
组长原始快照已在服务器及电脑保存并核验；其他成员原始归档抽查、专项审阅、最终完整包及提交仍待完成。
仓库：<https://github.com/LoShell/DevOps-Course-Assignment-A08>。
轨道：A（BuildChecker）；共同分支：a08/e5-e6。
共同运行完整 SHA：`25e57544fe7b98e496aeea8681e5cfaca128a255`。
报告整理日期：2026-11-01。各人分别记录实际实验日期与文档提交 SHA。

本文件保留整理手册指定的报告入口，汇总各人结果；平台要求个人报告时，
按 [个人模板](../E5/records/TEMPLATE.md) 分别填写并独立归档。
入口见 [E5 README](../E5/README.md)。

## 1. 目标、来源和输入

采集教学样例的系统调用和 Make 数据库，人工比较实际与声明依赖。
参考代码由 PR #4 导入，资源适配后的共同运行基准见页首。
样例入口为 fixtures/md-rd/；088 本次镜像内样例复制到 work/e5-01/evidence/，
包内 main.c、config.h、unused.h、Makefile 已直接读取核对。
main.c 包含 config.h 并打印 VALUE，config.h 定义 VALUE=1，unused.h 未被包含。
Makefile 编译规则声明 main.c/unused.h，链接规则声明 main.o。

## 2. 环境与运行过程

完整命令、环境和版本边界见个人记录。088 本次实际调用
`python3 scripts/course.py e5 --out work/e5-01`，runner 保存的 Docker 命令已核对。
内部依次复制样例、make clean、
`strace -ff -s 4096 -o trace/t -e trace=%file,%process make -p app`，最后执行 app。
Make 数据库、构建错误流与程序输出分文件保存。

| 成员 | 运行完整 SHA / 工作区差异 | 镜像 ID / 构建证据 | E5 原始目录 | 实际退出码 / 程序输出 | 个人记录 |
| --- | --- | --- | --- | --- | --- |
| 刘馨雅 241250088 | E5 共同基准已核对 | work/build-02；历史构建镜像 sha256:c4324b296f07095287e2c6e4a1eea9e471ad362ebc7b30572b4ea50524a0523a；构建/单测均 0、15 passed | /root/241250088/buildchecker/work/e5-01；北京时间 2026-10-30 12:21:33 | 0 / 1，runner 0 | [个人记录](../E5/records/241250088.md)，已审阅 |
| 邱莉扉 241250097 | 自报共同基准；待抽查 | 自报 sha256:ed19a3c87c705cd740ad548b66ff71999db40abd126ca6b7a15e045a904385dc；构建 0、15 passed | /root/241250097/buildchecker/work/e5-run-20261031-134307 | 自报 0 / 1 | 本人称已完成，待 PR 与审阅 |
| 范从钰 241250071 | 自报共同基准；待抽查 | 自报 sha256:eca7a492b08860a6c2da212e0b1fb2b92b161e0fc559da753abf351495a5b186；构建 0、15 passed | /root/241250071/buildchecker/work/e5-run-20261031-162026 | 自报 0 / 1 | 本人称已完成，待 PR 与审阅 |
| 叶原原 241250076 | 自报共同基准及干净工作区；待抽查 | 自报 sha256:482f67c696d1d8ada7c4b7262ff13d6b7bf27aa40fdff97c59a29fc2359e7647；构建 0、15 passed | /root/241250076/buildchecker/work/e5-run-20261031-215818 | 自报 0 / 1，runner 0 | 按阶段安排待填写 |

## 3. 人工依赖结论与原始证据

下表结论已由组长本人的终端证据核对；其他三位回报一致，其原始文件仍待抽查。

| 目标 | 实际依赖 | Make 声明 | 人工判定 | 实际依据及结论 |
| --- | --- | --- | --- | --- |
| main.o | main.c、config.h | main.c、unused.h | MD config.h；RD unused.h | 088：t.16:67、580 成功读取；t.17:23 写出目标；make-db.txt:1061；unused.h 的打开检索无输出 |
| app | main.o | main.o | 无差异 | 088：t.20:71 写出 app、82–83 读取 main.o；make-db.txt:609 |

组长的 make（14）派生 cc（15），cc 派生 cc1（16）和 as（17）：
cc1 读取 main.c/config.h，as 写 main.o，归属于同一编译作业。
链接链路为 make（14）→ cc（18）→ collect2（19）→ ld（20）。
完整行号见 [组长个人记录](../E5/records/241250088.md)。
实际依赖依据成功只读打开及作业归属。
系统文件按项目根目录过滤；unused.h 的 RD 结论只适用于本次构建配置。

## 4. 与论文的对应及差异

已核对本地课程 BuildChecker 原文第 4–6 页的第 4 节、图 2、算法 1/2。
论文用动态构建执行与 GNU Make 数据库建立执行—声明模型，并按项目内依赖差异检测 MD/RD。
本次通过 strace 采集、人工还原进程作业和对照数据库，展示该思路。
原文以 ptrace 跟踪文件操作，本次使用 strace 输出。

论文评估 30 个项目；本次四人复现同一个简化 C/Make 样例，
重点核对固定配置下的原始证据、人工 MD/RD、15 项服务测试与程序输出。
完整依据、对应表和限制见 [论文对应与差异](../E5/PAPER_COMPARISON.md)。

## 5. 个人贡献和审阅

逐人责任、回报状态和未完成的提交/PR 见 [贡献表](../E5/CONTRIBUTIONS.md)。
组长已直接核对本人两份快照；其余三人回报同 SHA、构建与测试成功、
E5 输出 1 和一致的 MD/RD，原包抽查与专项文档审阅列入后续任务。
专项进度、版本缺项、问题与下一步见 [组长整合审阅](../E5/review/integration.md)。

## 6. 证据索引与提交

逐人列出输入、trace、数据库、程序输出、完整日志和版本文件，核对
[提交检查表](../E5/SUBMISSION.md)。

| 学号 | 服务器完整证据目录 | 归档文件 / 电脑备份 | 报告提交 SHA / 上传状态 |
| --- | --- | --- | --- |
| 241250088 | /root/241250088/buildchecker/work/e5-01；构建 work/build-02 | raw-20261101-164720 与 build-20261101-165437 两份快照均已下载至 D:\MYfile\3-1\Devops\Lab\241250088\，哈希及关键内容核对通过；完整名称与哈希见个人记录，最终报告包待制作 | 待完成 |
| 241250097 | /root/241250097/buildchecker/work/e5-run-20261031-134307 | 自报 /root/devops-submissions/241250097/A08-241250097-E5-20261031-153418.tar.gz；电脑 E:\大三上\DevOps\labs\lab5\ 同名包；组长待抽查 | 本人回报未 commit/push/上传；后续待确认 |
| 241250071 | /root/241250071/buildchecker/work/e5-run-20261031-162026 | 自报 /root/devops-submissions/241250071/A08-241250071-E5-20261031-165658.tar.gz；电脑 D:\My_Work\Homework\DevOps\lab5_7\E5备份；组长待抽查 | 本人回报 Git 提交及 PR 待安排 |
| 241250076 | /root/241250076/buildchecker/work/e5-run-20261031-215818 | 自报 /root/devops-submissions/241250076/A08-241250076-E5-20261031-220102.tar.gz；两端 SHA-256 一致、55 份证据及 7 份 trace 核验；电脑路径待补、组长待抽查 | 报告未填；回报未 commit/push/PR；最终包待更新 |

当前没有成员回报未解决的 E5 运行故障。未完成项是：个人及专项文档审阅、
另一成员原包抽查、个人 PR、最终报告包和平台要求核对及上传。
已有原始快照保持不改，最终包另命名。E6 报告与修复复检独立提交。
