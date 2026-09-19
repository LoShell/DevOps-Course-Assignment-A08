# A08 E2 工作流程与分工

## 一、协作方式

本轮只使用 `a08/e2-review` 一个工作分支。每位成员负责不同文件，避免
多人同时修改同一文件。

首次获取工作分支：

```bash
git clone https://github.com/LoShell/DevOps-Course-Assignment-A08.git
cd DevOps-Course-Assignment-A08
git fetch origin
git checkout a08/e2-review
```

每次开始工作前：

```bash
git checkout a08/e2-review
git pull --rebase origin a08/e2-review
```

完成个人工作后：

```bash
git status
git add E2
git commit -m "docs(e2): describe completed work"
git push origin a08/e2-review
```

协作规则：

1. 每个人使用自己的 GitHub 账号和 Git 身份提交。
2. 每人至少保留一个独立 Commit。
3. 每次修改前先拉取最新内容。
4. 只修改本人负责的文件；公共汇总文件按约定最后填写。
5. 禁止使用 `git push --force`。

## 二、四人分工

| 成员 | E2 负责内容 | 独立负责文件 |
|---|---|---|
| 成员1 | 联系 B08、记录配对讨论、汇总最终评审、创建 Issue/PR | `review/coordination.md`，最后填写 `A08_REVIEW.md` |
| 成员2 | 解释并评审 `FULL_CHECK` 的请求与结果样例 | `review/full-check-review.md` |
| 成员3 | 解释并评审 `INCREMENTAL_CHECK` 的请求与结果样例 | `review/incremental-check-review.md` |
| 成员4 | 整理 Backlog、设计记录、AI 使用和贡献追溯 | `BACKLOG.md`、`AI_USAGE.md`、`adr/0001-contract-review.md`，最后填写 `CONTRIBUTIONS.md` |

## 三、提交顺序

1. 成员2完成 `full-check-review.md` 并推送。
2. 成员3拉取最新内容，完成 `incremental-check-review.md` 并推送。
3. 成员4拉取最新内容，完成 Backlog、ADR 和 AI 使用记录并推送。
4. 成员1拉取全部内容，完成沟通记录和最终评审汇总并推送。
5. 成员4根据 Git 历史回填 `CONTRIBUTIONS.md` 中的 Commit SHA。
6. 汇总人检查材料后，将 `a08/e2-review` 合并到 `main`。

## 四、最终检查

- [ ] 双方能解释同一份请求和结果样例。
- [ ] A08 已记录接受、修改或待讨论的接口内容。
- [ ] Backlog 和设计记录完整。
- [ ] 四名成员均有独立 Commit。
- [ ] 仓库地址、评审 Commit 和 Issue/PR 链接已记录。
- [ ] E2 材料中没有把 E3 实现写成已完成。

