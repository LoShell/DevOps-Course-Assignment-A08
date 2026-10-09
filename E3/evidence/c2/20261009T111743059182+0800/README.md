# C2 编译命令变化证据

- 执行时间：2026-10-09T11:17:43.059182+08:00。
- 执行者：刘馨雅；人工 oracle 状态：待成员 4 确认。
- 仓库：https://github.com/LoShell/DevOps-Course-Assignment-A08.git。
- C1：`4b70cabad1be8f6e98ee90ed9c5803b7aa793253`（输入 `e3-c1`）。
- C2：`56deea9199679907893fa53add1d867ff62028e1`（输入 `e3-c2`）。
- 镜像：`sha256:f9c6a090258dcebff09accf2be49de5e56ed3f285b51fdad36cb5eb46a951e85`；标签 `a08-e3-c2:local-20261009-111743059182`。
- 实验工作目录：`/tmp/a08-e3-incremental`；镜像项目目录：`/workspace/E3/fixtures/incremental`。
- 结果：**PASS**；37/37 项断言通过。

| 阶段 | 实测行为输出 |
|---|---|
| C1 干净构建 | `12` |
| 仅替换 C2 Makefile，普通增量构建 | `12` |
| 同一 C2 源码，干净构建 | `19` |

复现流程设计为：先从 Git 导出固定版本，检查 C2 独立提交仅修改 Makefile，并逐字节验证
`CPPFLAGS := -Iinclude` 只增加 `-DMODE=7`。在同一容器中先构建 C1，随后
只复制 C2 Makefile，不替换或触碰源码、头文件和已有产物，再执行 `make -j2`。
随后在同一工作目录执行 `make clean` 和 `make -j2`。实际执行到的阶段以
上方实测表格、status 和命令记录为准；失败时不会把未执行阶段当作成功结果。

本次实际生成的证据：[commands.txt](commands.txt)、[observations.json](observations.json)、[build.txt](build.txt)、[docker-version.txt](docker-version.txt)、[image-inspect.json](image-inspect.json)。
已执行命令的原始合并输出和退出码见 commands.txt。已采集的工具版本、阶段快照
和逐项断言见 observations.json；进入相应阶段后才会生成 Docker 构建日志、
镜像元数据及源码/产物哈希和修改时间。复现脚本使用宿主机 Python，不增加容器内依赖。

## 配置编号与契约限制

- 本次 C1 配置：`e3-incremental-68a30bdbb41fb730`。
- 本次 C2 配置：`e3-incremental-58ae69f36cba4c79`。
- 编号依据为实测 Ubuntu、GCC、Make、架构、镜像 ID 及编译选项；规范化 JSON
  和哈希算法在成功采集环境后保存在 observations.json 的 configurations/configuration_policy。
- C1 的重新验证仅使用本次容器，不覆盖成员 3 的 WSL 历史记录。
- 因编译选项不同，两个配置编号不同。本记录用于 E3 行为对比，不能直接声称
  满足 E2 同配置增量请求；后续由组长统一对接策略。

## 结论边界

C2 增量构建保留 C1 产物，而干净构建应用 MODE=7 后输出 19，证明编译命令变化未触发普通 Make 重建。feature.h 仍被 GCC 列为读取依赖，Make 仍未声明它，因此 C1 的既有 MD 保持不变；命令变化不新增头文件 MD。本记录不是 BuildChecker/EChecker 自动检测报告。

脚本仅在已创建临时实验容器时执行删除，结果以收尾命令和断言为准；已生成的
镜像保留供复核。重复实验必须使用新的证据目录。
