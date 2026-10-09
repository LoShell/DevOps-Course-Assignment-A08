# C2 首次导出校验失败：Git for Windows 换行转换

本目录保留首次真实失败的 commands.txt 和 observations.json，未修改原始输出、
断言、执行时间或 runner_sha256。失败发生在 Docker 构建之前，因此本次没有
build.txt 或 image-inspect.json，也不能作为 C2 构建成功证据。

## 原因与处理

本机 Git 的 `core.autocrlf=true`。Git for Windows 的 `git archive` 也会应用
换行转换，将固定提交中的 LF 转成 CRLF；因此首次脚本中的 LF 精确替换校验
失败。Git blob 本身未变，C2 提交仍只有预定的 Makefile 单行变化。

复现脚本已改用 `git -c core.autocrlf=false -c core.eol=lf archive ...`，只对
这次导出禁用转换，不修改全局或仓库配置。后续在新目录重新运行；本次失败记录
保留用于解释修复过程。初次 Docker 服务连接错误在启动 Docker Desktop 后已恢复。

下方为首次运行自动生成的摘要，原始执行数据以 JSON 和命令记录为准。

- 执行时间：2026-10-08T19:44:15.817054+08:00。
- 执行者：Codex on behalf of member 4 (Yevhen277)；人工 oracle 状态：待成员 4 确认。
- 仓库：https://github.com/LoShell/DevOps-Course-Assignment-A08.git。
- C1：`4b70cabad1be8f6e98ee90ed9c5803b7aa793253`（输入 `e3-c1`）。
- C2：`56deea9199679907893fa53add1d867ff62028e1`（输入 `e3-c2`）。
- 镜像：`未生成`；标签 `a08-e3-c2:local-20261008-194415817054`。
- 实验工作目录：`/tmp/a08-e3-incremental`；镜像项目目录：`/workspace/E3/fixtures/incremental`。
- 结果：**FAIL**；6/7 项断言通过。

| 阶段 | 实测行为输出 |
|---|---|
| C1 干净构建 | `未执行` |
| 仅替换 C2 Makefile，普通增量构建 | `未执行` |
| 同一 C2 源码，干净构建 | `未执行` |

本次已从 Git 导出固定版本并确认只有 Makefile 不同，但 LF 精确替换校验失败。
预定的容器构建、仅替换 Makefile 后的增量构建和干净构建均未发生。

完整命令、原始合并输出和退出码见 [commands.txt](commands.txt)。本次在源码导出
校验阶段停止，未进行 Docker 构建或生成镜像元数据。
导出文件哈希、失败断言和错误原因见 [observations.json](observations.json)。
本次没有采集容器工具版本或生成产物快照。

## 配置编号与契约限制

- 本次 C1 配置：`未生成`。
- 本次 C2 配置：`未生成`。
- 本次在进入容器阶段之前失败，未生成配置编号和计算依据；后续成功运行的
  配置记录及契约限制见 [C2 证据索引](../../c2/README.md)。

## 结论边界

本次未通过，不作为成功验证证据。失败原因：C2 contains exactly the MODE=7 option change

本次没有创建或删除容器，也未构建镜像；临时 Git 导出目录已清理。
重复实验必须使用新的证据目录。
