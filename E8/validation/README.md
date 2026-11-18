# E8 验证证据索引

状态：2026-11-17 组长参考基线与个人扩展通过，两轮下载原包均已核验。其他成员、CI 与集成轮尚未验收。

| 轮次/成员 | 源码 SHA | 镜像 ID | OUT/归档位置 | 判定 | PR/CI |
| --- | --- | --- | --- | --- | --- |
| 组长参考基线 | 369a8c82b73e53fb220fca28b89f3fc786e386e3 | sha256:6b34d781ec37d2e6484f953587e022d5fef897ec9fd8b2b808898bf65a899d3f | /root/241250088/buildchecker/work/e8-A-manual.iz7oZm；归档见下文 | GCC/动态投影/未变复用及原包核验通过 | 共同分支已推送；CI待核对 |
| 088 个人轮 | 26f414168eacf7149be943238a8d1ac6ba85175b | 同基线镜像 | work/e8-A-manual.iand6b；归档见个人记录 | 定向1项、回归8项、扩展与原包核验通过 | PR/CI待核对 |
| 097/071/076 个人轮 | 各自记录 | 各自记录 | 各自记录 | 待执行 | 待提交 |
| 集成轮 | 待执行 | 待执行 | 待执行 | 待执行 | 待提交 |

原始 trace、Make 数据库、完整图与步骤日志留在 work，下载归档。此目录仅提交摘要、清单和审计记录。

组长基线已在服务器归档至 `/root/E8-241250088-baseline-MJZnwXqO`，下载至 `D:\MYfile\3-1\Devops\Lab\241250088\E8`。两项服务器与电脑哈希校验一致，源码版本、输入哈希、图与发现、五份步骤日志及原始证据核验通过。文件及 SHA-256 见 [个人记录](../records/241250088.md)，检查范围见 [机器核验记录](baseline-241250088-local-audit.json)。

个人轮归档为 `/root/devops-submissions/241250088/E8/personal/run-FERZKgqd`，电脑目录为上述 E8 目录的 personal 子目录；核验范围见 [个人轮机器记录](personal-241250088-local-audit.json)。后续归档统一使用 /root/devops-submissions/<学号>/<阶段>/<轮次>/；首轮旧归档尚未迁移。
