# A08-B08 配对沟通记录

## 基本信息

| 项目 | 内容 |
|---|---|
| 配对小组 | `A08-B08` |
| A08 仓库 | `https://github.com/LoShell/DevOps-Course-Assignment-A08` |
| B08 仓库 | `https://github.com/Delario17/DevOps-Course-Assignment` |
| 沟通日期 | `2026-9-20` |
| 沟通方式 | `线上沟通` |

## 沟通目的

本次沟通用于确认 A08 与 B08 是否对同一版本的请求和结果样例具有一致理解，
并固定 E3 后续实现所依据的契约版本。E2 阶段只确认接口和交接方式，不部署
HTTP 服务，也不实现 BuildChecker、EChecker、DRAFT 或 MDFixer。

## A08 已完成的分项评审

| 评审对象 | A08 负责人 | 结论 | 详细记录 |
|---|---|---|---|
| BuildChecker（契约任务名 `FULL_CHECK`） | 范从钰 | 通过，无必须修改项 | [`full-check-review.md`](full-check-review.md) |
| EChecker（契约任务名 `INCREMENTAL_CHECK`） | 邱莉扉 | 通过，无必须修改项 | [`incremental-check-review.md`](incremental-check-review.md) |


## 组间交接理解

| 交接环节 | B08 当前书面方案 | A08 评审意见 | 配对状态 |
|---|---|---|---|
| DRAFT → BuildChecker | B08 提供与目标仓库、commit 和构建配置绑定的容器镜像、工作目录和构建信息 | 输入能够支持后续 BuildChecker 全量检查 | 待 B08 正式确认 |
| BuildChecker → EChecker | FULL_CHECK 返回实际依赖图、声明依赖图和统一错误报告；实际依赖图可作为增量检查基线 | 基线来源和版本约束清楚，可以接受 | 待 B08 正式确认 |
| BuildChecker/EChecker → MDFixer | 检测报告通过 ArtifactRef 交付，`MISSING` 发现可供 MDFixer 后续使用 | 报告格式和版本追溯方式可以接受 | 待 B08 正式确认 |
| 产物读取 | Job 响应返回 ArtifactRef，调用方通过 `GET /v1/artifacts/{artifact_id}/content` 获取正文 | 适合传递依赖图、报告等较大产物 | 待 B08 正式确认 |

## 双方需要确认的共同语义

### 请求和版本

- 请求使用 `repository_url + commit + configuration_id` 标识被处理的源码版本和构建配置。
- DRAFT 产物、检测基线和检测结果应与对应请求的版本信息一致。
- A08 本次评审基于固定 Commit，不直接以持续变化的 `main` 分支作为最终契约。

### 结果和错误

- 检测到 MD/RD 表示检测任务正常完成，任务状态仍为 `SUCCEEDED`。
- MD/RD 记录在检测报告的 `findings` 中；没有发现时可使用空数组。
- 输入不合法、环境不可用、构建失败、超时或检测器异常等情况才写入 `job.error`。

### E2 与 E3 边界

- 当前 JSON、依赖图和报告均为 E2 静态接口样例。
- E2 评审通过不表示 A08 已实现 BuildChecker 或 EChecker。
- 真实项目、C0/C1/C2、运行产物和组间服务联调在 E3 开展。