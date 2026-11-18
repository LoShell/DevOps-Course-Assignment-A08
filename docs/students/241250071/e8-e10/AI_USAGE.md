# AI 使用记录

负责人：范从钰 241250071。

共同框架由组长使用 Codex 辅助整理，参考实现来源见 `course-support/e8e9/README.md`；此说明不代表本人已经调用 AI 或完成实验。

## 本人使用工具、日期与范围

本人于 2026-11-18 使用 ChatGPT/Codex 对话式辅助完成 E8/E9 实验过程解释、个人测试设计建议、命令顺序核对，以及实验记录和专项审阅的初稿整理。

## 输入上下文与问题

本人向 AI 提供了课程操作文档、`E8/TEST_PLAN.md`、`labs/e8e10/lab.py` 的相关内容，以及服务器实际运行输出。主要问题包括：

- 如何为“间接 include、依赖变化与缓存失效”设计独立测试；
- 如何区分 Make 的声明依赖、GCC `-MM` 实际依赖与 BuildChecker 的 strace 动态证据；
- 如何按阶段保存 OUT、测试日志、内部提交、归档包和 SHA-256 校验信息；
- 如何根据本人实际输出填写记录、CSV、专项审阅和 ADR。

## 建议及采纳/拒绝理由

采纳的建议包括：新增 `test_indirect_include_invalidates_cached_dependencies` 和 `test_indirect_header_change_invalidates_cache_across_commits`；对每次个人轮使用新的 OUT；保存增量和全量 JSON；保存真实 BuildChecker 证据；在归档前执行定向测试和完整回归；下载后在 Windows PowerShell 复算 SHA-256。

未将 AI 建议直接视为结论。所有 MD/RD、reused/refreshed、测试数量、退出码、内部提交 SHA、镜像 ID 和归档 SHA-256，均以本人服务器实际输出和下载后的本地校验为准。

## 人工修改与实际验证

本人手动在服务器创建并保存个人测试文件、运行命令、检查输出、提交 Git、下载证据包并执行本地 SHA-256 校验。本人没有向 AI 提供 GitHub 密码、2FA 验证码或其他凭据。

实际验证结果：

- E8 定向测试 1 项通过，完整回归 8 项通过；
- E9 定向测试 2 项通过，完整回归 9 项通过；
- E8/E9 的基线轮和个人轮均已在服务器归档，并在本地与 `SHA256SUMS.txt` 核对一致；
- E8/E9 个人轮的 `personal-gate.json` 均为 `passed=true`。

PR、CI 运行链接、artifact 与最终合入结论将在推送文档并获得实际结果后补充。
