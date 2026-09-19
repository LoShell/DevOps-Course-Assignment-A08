# FULL_CHECK 请求与结果样例评审

## 评审依据

| 项目 | 内容 |
|---|---|
| 配对小组 | `A08-B08` |
| B08 仓库 | `https://github.com/Delario17/DevOps-Course-Assignment` |
| B08 初始评审基准 | `309237a12aaeb0dba6f03228c0542e3f9385dd9e` |
| 本次实际评审 Commit | `2c1b15332456410b74679d479094406fb7e183aa` |
| 接口定义 | `E2/openapi.yaml` 中的 `POST /v1/full-check-jobs` |
| 请求 Schema | `E2/contracts/create-request.schema.json` 中的 `FullCheckInput` |
| 结果 Schema | `E2/contracts/task.schema.json` 中的 `FullCheckOutput` |
| 请求样例 | `E2/examples/valid/full-check.request.json` |
| 成功结果样例 | `E2/examples/valid/full-check.succeeded.json` |
| 静态产物样例 | `E2/examples/artifacts/a08-b08/full-001/` |

本报告评审的是 B08 当前契约及静态 JSON 样例。E2 阶段不要求部署 HTTP 服务，也不要求实际实现 BuildChecker。

## 请求说明

- 发起方：B08 的 DRAFT 流程或双方约定的流水线调用方。
- 接收方：A08 后续实现的 BuildChecker。
- 请求目的：在指定源码版本、构建配置和容器环境中执行 clean build，生成实际依赖图和声明依赖图，并比较两者以发现缺失依赖（MD）与冗余依赖（RD）。
- 调用方式：向 `POST /v1/full-check-jobs` 提交请求。服务受理后返回 HTTP `202`，调用方再通过 `GET /v1/jobs/{job_id}` 查询状态和结果。

### 公共请求字段

| 字段 | 作用 | 评审结果 |
|---|---|---|
| `schema_version` | 标识契约版本，当前为 `1.0.0` | 接受 |
| `trace_id` | 串联 DRAFT、FULL_CHECK、INCREMENTAL_CHECK 和 REPAIR | 接受 |
| `pair_id` | 标识配对小组，当前固定为 `A08-B08` | 接受 |
| `idempotency_key` | 防止同一请求被重复创建 | 接受 |
| `job_type` | FULL_CHECK 请求固定为 `FULL_CHECK` | 接受 |

OpenAPI 还要求请求头携带 `Idempotency-Key`，其值应与请求体中的 `idempotency_key` 相同。同一个键和相同请求应复用原 Job；同一个键对应不同内容时返回 HTTP `409` 和 `CONTRACT_2001`。

### FULL_CHECK 输入字段

| 字段 | 作用 | 评审结果 |
|---|---|---|
| `input.subject.repository_url` | 指定被检测源码仓库 | 接受 |
| `input.subject.commit` | 固定被检测的源码版本，Schema 要求为 40 位完整 SHA | 接受 |
| `input.subject.configuration_id` | 标识操作系统、编译器及关键构建选项 | 接受 |
| `input.environment.container_image` | 引用 B08 DRAFT 生成的构建镜像 | 接受 |
| `input.environment.working_directory` | 指定容器内源码所在的绝对路径 | 接受 |
| `input.clean_build_command` | 指定全量干净构建命令 | 接受 |

`container_image` 使用完整 ArtifactRef，包含产物编号、类型、URI、生产任务和自己的 `subject`。校验逻辑要求镜像的 `subject` 与 FULL_CHECK 请求的 `subject` 完全相同，并要求镜像 URI 使用 `docker://`。这可以防止 A08 错用另一个仓库、commit 或构建配置生成的镜像。

经检查，上述字段足以表达 E2 阶段 BuildChecker 执行一次全量依赖检测所需的基本输入。

## 结果说明

FULL_CHECK 采用异步 Job。创建请求被接受时，状态为 `QUEUED` 或 `RUNNING`，此时 `output` 和 `error` 都应为 `null`。分析正常完成时状态为 `SUCCEEDED`，此时必须有 `output`，并且 `error` 为 `null`。

成功输出包含：

| 字段 | 内容 | 后续用途 |
|---|---|---|
| `actual_graph` | clean build 中实际观察到的依赖图 | 可作为 EChecker 后续增量检测的基线 |
| `declared_graph` | Makefile 等构建文件声明的依赖图 | 与实际依赖图进行比较 |
| `error_report` | MD/RD 发现及其证据 | MISSING 发现可交给 B08 的 MDFixer |
| `summary.missing` | 缺失依赖数量 | 快速查看检测结果 |
| `summary.redundant` | 冗余依赖数量 | 快速查看检测结果 |

每个输出产物都通过 ArtifactRef 返回，包含：

- `artifact_id`
- `type`
- `uri`
- `media_type`
- `producer_job_id`
- `subject`
- 可选的 `sha256`

调用方使用 `GET /v1/artifacts/{artifact_id}/content` 获取产物正文，内容响应使用 SHA-256 作为 ETag。校验器还要求输出产物的 `producer_job_id` 等于当前 FULL_CHECK 的 `job_id`，并要求产物 `subject` 等于任务输入 `subject`。

## 状态和错误语义

- 检测到 MD 或 RD 表示 BuildChecker 正常完成了分析，因此任务仍应是 `SUCCEEDED`，发现记录在 `error_report.findings` 中。
- 没有发现问题时，`findings` 可以为空数组，任务仍应是 `SUCCEEDED`。
- 输入字段不合法、幂等键冲突、镜像或运行环境不可用、构建失败、任务超时、检测器异常等情况才属于任务错误。
- 错误任务使用 `FAILED`、`TIMED_OUT` 或 `CANCELLED`，此时 `output` 应为 `null`，具体原因写入 `job.error`。

这种设计能够区分“检测器成功发现了依赖问题”和“检测器本身没有正常运行”，语义合理。

## 静态样例一致性检查

对 B08 提供的 FULL_CHECK 请求、成功响应和三个主要产物逐项核对，结果如下：

1. `full-check.request.json` 的 `subject`、容器镜像 `subject`、工作目录和 clean build 命令齐全，仓库、commit 和配置编号一致。
2. `full-check.succeeded.json` 的任务类型为 `FULL_CHECK`，状态为 `SUCCEEDED`，`error` 为 `null`。
3. 成功响应返回 `ACTUAL_GRAPH`、`DECLARED_GRAPH` 和 `ERROR_REPORT` 三类产物，三者的 `producer_job_id` 都是 `job-full-001`，并与当前任务的 `subject` 一致。
4. `actual.json` 表示 `build/main.o` 在实际构建中读取了 `src/main.c` 和 `include/config.h`。
5. `declared.json` 表示 Makefile 只为 `build/main.o` 声明了 `src/main.c`，没有声明 `include/config.h`。
6. `error-report.json` 因此产生一条 `MISSING` 发现，指出 `build/main.o` 缺少对 `include/config.h` 的声明，并给出了构建跟踪和声明解析两条证据。
7. 成功响应中的统计为 `missing: 1`、`redundant: 0`，与所引用报告的 findings 数量一致。
8. 仓库还提供了 `redundant-report.json`，用于说明统一的 ERROR_REPORT 同样可以表达 `REDUNDANT` 发现。
9. `validate.py` 会验证 FULL_CHECK 请求 Schema、Job 状态、产物类型、subject、生产任务、产物 URI、SHA-256，以及 `summary` 与 ERROR_REPORT findings 的数量是否一致。

## A08 评审意见

| 项目 | 记录 |
|---|---|
| 可以接受的设计 | 接受异步 Job 模型；接受 `repository_url + commit + configuration_id` 的版本绑定；接受由 DRAFT 提供完整容器镜像 ArtifactRef；接受 FULL_CHECK 输出实际图、声明图、统一 ERROR_REPORT 和数量统计；接受通过 ArtifactRef 与下载端点读取较大产物；接受 MD/RD 属于正常检测结果而不是系统错误。 |
| 存在疑问的设计 | 无阻塞双方对接的问题。`error-report.json` 中的 `detector: INSTRUCTOR_ORACLE` 可理解为 E2 静态样例使用的人工真值；E3 实际运行 BuildChecker 后，真实报告应按生产者填写为 `BUILDCHECKER`。 |
| 建议修改的内容 | 无必须修改项。当前请求、响应、状态、错误和产物样例已经满足 E2 接口契约评审要求。 |

## 评审结论

`通过`

当前 FULL_CHECK 请求已经包含 BuildChecker 所需的源码版本、构建配置、容器环境、工作目录和 clean build 命令；成功结果可以返回实际依赖图、声明依赖图、检测报告及统计信息；任务和各项产物能够追溯到对应仓库、commit、配置和生产 Job。现有设计满足 E2 阶段的静态接口契约与组间交接要求，可以作为后续 E3 实现和联调的依据。
