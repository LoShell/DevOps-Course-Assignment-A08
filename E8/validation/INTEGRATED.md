# E8 集成运行与原包核验

2026-11-18，源码 `04f386971d8f924cbdd85401c1f3583935c9b1c4`，用户在服务器执行，电脑只读核验，不代跑实验。

OUT为work/e8-A-manual.zTJjf8，共用回归目录work/e89-241250088-integrated-dmvueNDG，16项/3.582s/退出0。GCC基线、动态对象投影与精确MD/RD一致，未变输入复用两目标、无刷新，三集合与全量相同。输入哈希、读取trace、声明数据库与步骤日志核验通过。详细范围见 [审计JSON](integrated-local-audit.json)。

| 文件 | SHA-256 |
| --- | --- |
| student-source.tar | 6a224603a8ab44c5bb9ba106190e7d21d76b162b9d1112ca911390fe88e2f583 |
| E8-integrated-evidence.tar.gz | 69ab35bf2a213426d342fe297912af8974792811c6887708bf36ee30a35881a1 |

服务器：/root/devops-submissions/241250088/E8/integrated/run-AfCQY0fm。
电脑：D:\MYfile\3-1\Devops\Lab\241250088\E8\integrated。
双端与清单哈希一致。原始包留在仓库外，Git仅保存摘要和核验索引。
