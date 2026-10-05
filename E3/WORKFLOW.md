# A08 E3 工作流程与分工

## 一、分支方式

`main` 只保存共同确认的 E3 骨架。实际实验统一在
`a08/e3-baseline` 分支完成，不再为每名成员建立额外工作分支或 worktree。

首次进入工作分支：

```bash
git checkout main
git pull --rebase origin main
git checkout -b a08/e3-baseline
git push -u origin a08/e3-baseline
```

若远端工作分支已经由组长建立，其他成员使用：

```bash
git fetch origin
git checkout -b a08/e3-baseline origin/a08/e3-baseline
```

每次工作前执行：

```bash
git checkout a08/e3-baseline
git pull --rebase origin a08/e3-baseline
```

## 二、四人分工

| 成员 | 主要任务 | 主要责任目录或文件 |
|---|---|---|
| 刘馨雅 | 建立可运行基础项目和 C0；整合环境证据与最终检查 | `fixtures/incremental/`、`evidence/environment/`、公共汇总 |
| 邱莉扉 | 构造固定 MD/RD 样本；编写人工 oracle 与复现证据 | `fixtures/md-rd/`、`oracle/md-rd.expected.json`、对应证据 |
| 范从钰 | 在 C0 后构造 C1 新增头文件场景；记录预期与证据 | C1 源码提交、`oracle/incremental.expected.json` 的 C1 部分、对应证据 |
| 叶原原 | 在 C1 后构造 C2 编译命令变化；对比增量与干净构建 | C2 Makefile 提交、C2 证据、`BACKLOG.md`、`AI_USAGE.md`、`CONTRIBUTIONS.md` |

分工中的“证据”包括本人执行的命令、原始输出、结果解释和关联 Commit SHA，
不把成员工作缩减为只写文档。

## 三、提交顺序

1. 完成并验证 C0，推送后记录真实 SHA，并创建注释标签 `e3-c0`。
2. 可独立完成固定 MD/RD 样本，不依赖 C1/C2。
3. 从已推送的 C0 继续构造 C1，验证后创建标签 `e3-c1`。
4. 从已推送的 C1 继续构造 C2，验证后创建标签 `e3-c2`。
5. 全员补齐证据和 oracle，组长进行最终复现与汇总。

C0、C1、C2 必须依次完成；不得并行修改同一份增量样本。固定 MD/RD 可与
增量链并行，但开始和推送前均需先执行 `git pull --rebase`。

## 四、提交规则

1. 每名成员使用自己的 GitHub 账号和 Git 身份提交。
2. 每名成员至少保留一个独立、可解释的 Commit，不进行 squash。
3. Commit 只包含当前任务相关文件，不提交编译产物和临时日志。
4. 不使用 `git push --force`，不移动已经共享的 C0/C1/C2 标签。
5. 原始实验日志放入 `evidence/`，并在文件中标明命令、退出码和对应 SHA。
6. `configuration_id` 必须根据真实服务器环境生成，不能沿用 E2 示例值。

## 五、最终检查

- [ ] 固定 MD 和 RD 均可从干净环境复现，人工依据明确。
- [ ] C0、C1、C2 对应三个真实 Commit 和三个固定标签。
- [ ] C1 只引入预定的新头文件读取及必要代码变化。
- [ ] C2 只修改预定的编译命令或编译选项。
- [ ] C2 的增量构建和干净构建输出符合 oracle。
- [ ] Docker 镜像、编译器、Make 和架构版本已记录。
- [ ] 每名成员的贡献与 Commit SHA 可追溯。
- [ ] A08 独立复现通过，不依赖 B08 尚未交付的运行产物。
