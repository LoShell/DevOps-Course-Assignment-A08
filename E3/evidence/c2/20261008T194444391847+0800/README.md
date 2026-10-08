# C2 编译命令变化证据

- 执行时间：2026-10-08T19:44:44.391847+08:00。
- 执行者：Codex on behalf of member 4 (Yevhen277)；人工 oracle 状态：待成员 4 确认。
- 仓库：https://github.com/LoShell/DevOps-Course-Assignment-A08.git。
- C1：`4b70cabad1be8f6e98ee90ed9c5803b7aa793253`（输入 `e3-c1`）。
- C2：`56deea9199679907893fa53add1d867ff62028e1`（输入 `e3-c2`）。
- 镜像：`sha256:7ab01a1cc4a4d3ad195d9776bcb16ab19b181d22a4b8e4ff261d60af6a8e0538`；标签 `a08-e3-c2:local-20261008-194444391847`。
- 实验工作目录：`/tmp/a08-e3-incremental`；镜像项目目录：`/workspace/E3/fixtures/incremental`。
- 结果：**PASS**；37/37 项断言通过。

| 阶段 | 实测行为输出 |
|---|---|
| C1 干净构建 | `12` |
| 仅替换 C2 Makefile，普通增量构建 | `12` |
| 同一 C2 源码，干净构建 | `19` |

实验先从 Git 导出固定版本，检查 C2 独立提交仅修改 Makefile，并逐字节验证
`CPPFLAGS := -Iinclude` 只增加 `-DMODE=7`。在同一容器中先构建 C1，随后
只复制 C2 Makefile，不替换或触碰源码、头文件和已有产物，再执行 `make -j2`。
随后在同一工作目录执行 `make clean` 和 `make -j2`。

完整命令、原始合并输出和退出码见 [commands.txt](commands.txt)，完整 Docker
构建记录见 [build.txt](build.txt)，镜像元数据见 [image-inspect.json](image-inspect.json)。
工具版本、各阶段源码及产物哈希、纳秒精度修改时间和逐项断言见
[observations.json](observations.json)。复现脚本使用宿主机 Python，不增加容器内依赖。

## 配置编号与契约限制

- 本次 C1 配置：`e3-incremental-24eda91c0bd7bb04`。
- 本次 C2 配置：`e3-incremental-85db7a8030c5d6ab`。
- 编号依据为实测 Ubuntu、GCC、Make、架构、镜像 ID 及编译选项；规范化 JSON
  和哈希算法保存在 observations.json 的 configurations/configuration_policy。
- 本次 C1 是在当前容器中重新验证，不覆盖成员 3 的 WSL 历史记录。
- 因编译选项不同，两个配置编号不同。本记录用于 E3 行为对比，不能直接声称
  满足 E2 同配置增量请求；后续由组长统一对接策略。

## 结论边界

C2 增量构建保留 C1 产物，而干净构建应用 MODE=7 后输出 19，证明编译命令变化未触发普通 Make 重建。feature.h 仍被 GCC 列为读取依赖，Make 仍未声明它，因此 C1 的既有 MD 保持不变；命令变化不新增头文件 MD。本记录不是 BuildChecker/EChecker 自动检测报告。

容器已在脚本收尾阶段尝试删除；镜像保留供复核。重复实验必须使用新的证据目录。
