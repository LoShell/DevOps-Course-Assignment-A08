# INCREMENTAL_CHECK 请求与结果样例评审

## 评审依据

| 项目 | 内容 |
|---|---|
| 配对小组 | `A08-B08` |
| B08 仓库 | `https://github.com/Delario17/DevOps-Course-Assignment` |
| B08 初始评审基准 | `309237a12aaeb0dba6f03228c0542e3f9385dd9e` |
| 本次实际评审 Commit | `2c1b15332456410b74679d479094406fb7e183aa` |
| 接口定义 | `E2/openapi.yaml` 中的 `POST /v1/incremental-check-jobs` |
| 请求 Schema | `E2/contracts/create-request.schema.json` 中的 `IncrementalCheckInput` |
| 结果 Schema | `E2/contracts/task.schema.json` 中的 `IncrementalCheckOutput` |
| 请求样例 | `E2/examples/valid/incremental-check.request.json` |
| 成功结果样例 | `E2/examples/valid/incremental-check.succeeded.json` |
| 静态产物样例 | `E2/examples/artifacts/a08-b08/incremental-001/` |

本报告评审 B08 在上述固定 Commit 中的契约和静态 JSON 样例。E2 阶段不要求部署 HTTP 服务，也不要求实际实现 EChecker 或执行真实增量构建。

## 请求说明

- 发起方：调用 EChecker 的流程；通常在新的源代码提交需要与已完成全量检测的基线比较时发起。
- 接收方：A08 后续实现的 EChecker。
- 请求目的：在当前提交的构建环境中执行增量构建，将观察到的当前实际依赖图与指定基线的实际依赖图比较，识别本次变更引入、消除或保持的依赖问题。
- 基线信息：基线不是虚构的 C0/C1/C2 项目，而是调用方提供的、已完成 FULL_CHECK 的提交版本和其 `ACTUAL_GRAPH` 产物引用；当前样例以提交 `aaaaaaaa...` 为基线、以提交 `bbbbbbbb...` 为待检版本。

### 公共请求字段

| 字段 | 作用 | 评审结果 |
|---|---|---|
| `schema_version` | 标识契约版本，当前为 `1.0.0` | 接受 |
| `trace_id` | 串联 DRAFT、FULL_CHECK、INCREMENTAL_CHECK 和 REPAIR | 接受 |
| `pair_id` | 标识配对小组，当前为 `A08-B08` | 接受 |
| `idempotency_key` | 防止同一请求被重复创建 | 接受 |
| `job_type` | 增量检测请求固定为 `INCREMENTAL_CHECK` | 接受 |

OpenAPI 要求请求头携带 `Idempotency-Key`，其值与请求体中的 `idempotency_key` 相同；同键且相同请求应复用既有 Job，同键但内容不同应返回 HTTP `409` 和 `CONTRACT_2001`。

### INCREMENTAL_CHECK 输入字段

| 字段 | 作用 | 评审结果 |
|---|---|---|
| `input.subject` | 指定当前待检测仓库、40 位提交 SHA 和构建配置 | 接受 |
| `input.environment.container_image` | 引用由 DRAFT 生成、且 `subject` 与当前版本一致的容器镜像 | 接受 |
| `input.environment.working_directory` | 指定容器内源代码所在的绝对路径 | 接受 |
| `input.baseline.base_commit` | 指定用于比较的基线提交 | 接受 |
| `input.baseline.configuration_id` | 指定基线构建配置，并要求与当前配置一致 | 接受 |
| `input.baseline.actual_graph` | 引用基线 FULL_CHECK 产生的 `ACTUAL_GRAPH`，携带来源任务、版本和校验摘要 | 接受 |
| `input.incremental_build_command` | 指定当前版本执行的增量构建命令 | 接受 |

校验逻辑要求基线图的仓库与当前 `subject.repository_url` 一致、基线图提交等于 `base_commit`，并要求基线配置、图配置和当前配置相同；因此不会误用其他仓库、提交或构建配置的图。仓库同时提供了缺少基线和跨仓库基线的无效请求样例。

## 结果说明

INCREMENTAL_CHECK 使用异步 Job。创建请求被受理时，状态为 `QUEUED` 或 `RUNNING`，此时 `output` 和 `error` 均为 `null`。成功完成时状态为 `SUCCEEDED`，必须提供 `output` 且 `error` 为 `null`。

成功输出包含：

| 字段 | 内容 | 后续用途 |
|---|---|---|
| `updated_actual_graph` | 当前提交在增量构建中观察到的实际依赖图 | 作为本次变更的依赖事实，也可成为后续检测基线 |
| `error_report` | 本次增量检测发现的 MD/RD 及其证据 | 供调用方查看或交给后续 REPAIR 流程 |
| `delta.added` | 相对基线新增的发现数 | 快速了解新引入的问题 |
| `delta.resolved` | 相对基线已消除的发现数 | 跟踪修复效果 |
| `delta.unchanged` | 相对基线仍存在的发现数 | 跟踪遗留问题 |

每项输出产物均以 ArtifactRef 返回，包含 `artifact_id`、`type`、`uri`、`media_type`、`producer_job_id`、`subject` 和可选的 `sha256`。调用方可通过 `GET /v1/artifacts/{artifact_id}/content` 读取产物正文；产物应由当前 Job 产生，且其 `subject` 应与当前检测版本一致。

MD/RD 是检测成功发现的结果，不是任务执行错误；此时任务仍应为 `SUCCEEDED`，发现记录在 `error_report.findings` 中。输入不合法、幂等键冲突、基线不匹配、镜像或环境不可用、增量构建失败、超时或检测器异常，才属于任务错误，此时使用 `FAILED`、`TIMED_OUT` 或 `CANCELLED`，并令 `output` 为 `null`、错误原因写入 `job.error`。

## 静态样例一致性检查

对 B08 提供的 INCREMENTAL_CHECK 请求、成功响应和两个主要产物逐项核对，结果如下：

1. 请求样例的当前 `subject`、容器镜像 `subject`、工作目录和增量构建命令齐全，仓库、提交和配置编号一致。
2. 基线信息引用 `actual-graph-c0`，其 `subject.commit` 与 `base_commit` 都为 `aaaaaaaa...`，仓库和配置与当前任务一致。
3. 成功响应的任务类型为 `INCREMENTAL_CHECK`、状态为 `SUCCEEDED`，`error` 为 `null`。
4. 成功响应返回 `ACTUAL_GRAPH` 和 `ERROR_REPORT` 两类产物；两者的 `producer_job_id` 都是 `job-incremental-001`，且 `subject` 与当前任务一致。
5. `updated-actual.json` 显示 `build/main.o` 在本次增量构建中新增读取 `include/feature.h`，同时保留对 `src/main.c` 和 `include/config.h` 的读取。
6. `error-report.json` 因此记录一条 `MISSING` 发现：`build/main.o` 缺少对 `include/feature.h` 的声明，并附有增量跟踪与当前 Make 声明两条证据。
7. 成功响应中的差异统计为 `added: 1`、`resolved: 0`、`unchanged: 0`，与该样例新增的一条发现相符。
8. `validate.py` 对请求 Schema、Job 状态、输入基线的一致性、输出产物类型与来源，以及缺少基线和跨仓库基线等无效样例进行校验。

## A08 评审意见

| 项目 | 记录 |
|---|---|
| 可以接受的设计 | 接受异步 Job 模型；接受以 `base_commit + configuration_id + ACTUAL_GRAPH` 明确固定增量比较基线；接受对基线仓库、提交和配置的交叉校验；接受输出更新后的实际图、统一 ERROR_REPORT 和新增/消除/未变化统计；接受以 ArtifactRef 追溯产物来源和版本。 |
| 存在疑问的设计 | 无阻塞双方对接的问题。`delta` 是对发现数量的摘要，具体发现及证据仍以 `error_report` 为准；E3 实现时应确保统计由同一比较过程生成，避免摘要与报告不一致。 |
| 建议修改的内容 | 无必须修改项。当前请求、响应、基线约束和静态产物样例已满足 E2 增量检查接口契约评审要求。 |

## 评审结论

`通过`

当前 INCREMENTAL_CHECK 请求明确给出了当前源代码版本、构建环境、增量构建命令以及可追溯的 FULL_CHECK 基线；结果可返回当前实际依赖图、发现报告和相对基线的变化摘要。基线图与当前任务之间的仓库、提交和配置约束清晰，样例中的任务和产物来源也可追溯。现有设计满足 E2 阶段的静态接口契约与组间交接要求，可作为后续 E3 实现和联调的依据。
