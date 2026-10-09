# 成员 2 人工 Oracle 确认记录

- 日期：2026-10-06。
- 确认人：成员 2（用户）。
- 结论：人工 oracle 核对通过，状态为已完成。
- 确认方式：Codex 应用户要求重新执行 Ubuntu 24.04 容器实验，将各场景真实输出逐项反馈；用户阅读反馈后明确确认“人工oracle核对通过了”，并要求更新状态。
- 执行人与确认人区分：实际命令由 Codex 运行；成员 2 确认结果和判断，不声称其本人手动执行命令。

## 已确认内容

| 项目 | 实际观察 | 结论 |
|---|---|---|
| 初始构建 | 程序输出 10，版本 demo 1.0.0 | 样例可运行 |
| config.h：CONFIG_VALUE 4 改为 5 后增量构建 | make 提示无需构建，输出仍为 10，对象文件未变 | build/main.o 缺少 include/config.h 声明（MD） |
| 相同源码 clean 后重建 | 输出 11 | 上一步确实使用过时产物 |
| unused.h 只改注释 | 实际重新编译和链接，输出仍为 11 | build/main.o 冗余声明 include/unused.h（RD） |
| GCC 项目依赖输出 | 包含 common.h/config.h，不含 unused.h | 支持源码与声明的人工对照 |

证据：[原始日志](run/commands.txt)、[14 项通过断言及环境记录](run/observations.json)、[容器调用](invocation.json)。

## 状态更新与历史证据

此次只更新 oracle 的来源、审阅状态、确认人及说明，未修改 findings、expected_behavior、样例源码或测试逻辑。
历史 observations.json 中的 pending review 描述和 source_sha256 是执行时快照，保持原样。
当前 oracle 因增加人工确认元数据，其文件哈希与运行时草稿不同；不改写旧哈希，不冒充重新运行结果。

人工确认已完成。样例提交 SHA：`8a9cfc46d854e697fd397c1f6c579014e219144b`；团队 configuration_id 仍待补齐。

