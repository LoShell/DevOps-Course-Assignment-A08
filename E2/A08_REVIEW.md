# A08 对 B08 E2 接口契约的评审结论

## 基本信息

| 项目 | 内容 |
|---|---|
| 配对小组 | `A08-B08` |
| A08 仓库 | `https://github.com/LoShell/DevOps-Course-Assignment-A08` |
| B08 仓库 | `https://github.com/Delario17/DevOps-Course-Assignment` |
| 评审日期 | `2026-09-20` |

## 评审范围

A08 对 B08 提供的以下 E2 接口材料进行了阅读和评审：

- BuildChecker 请求与结果样例，契约任务名为 `FULL_CHECK`；
- EChecker 请求与结果样例，契约任务名为 `INCREMENTAL_CHECK`；
- DRAFT、BuildChecker、EChecker 和 MDFixer 之间的交接方式；
- 异步任务状态、正常检测结果和系统执行错误的表达方式；
- 依赖图、检测报告等产物的引用和获取方式。

## 分项评审结果

### BuildChecker 接口

BuildChecker 请求已经包含源码仓库、提交版本、构建配置、容器环境、工作
目录和构建命令。成功结果能够返回实际依赖图、声明依赖图、MD/RD 报告及
数量统计，满足后续完整依赖检查的接口需要。

评审结论：**通过，无必须修改项。**

详细记录见 [`review/full-check-review.md`](review/full-check-review.md)。

### EChecker 接口

EChecker 请求已经包含当前源码版本、构建环境、增量构建命令以及可追溯的
检测基线。成功结果能够返回更新后的实际依赖图、检测报告和相对基线的变化
摘要，满足后续增量依赖检查的接口需要。

评审结论：**通过，无必须修改项。**

详细记录见 [`review/incremental-check-review.md`](review/incremental-check-review.md)。

## 共同理解

- B08 的 DRAFT 向 A08 的 BuildChecker 提供构建环境和相关构建信息。
- BuildChecker 输出实际依赖图、声明依赖图和 MD/RD 检测报告。
- EChecker 使用已有检测结果作为基线，返回更新后的依赖图和发现变化。
- A08 输出的检测报告可以交给 B08 的 MDFixer 作为后续修复输入。
- 检测到 MD/RD 表示检测正常完成，发现记录在报告中，不等同于系统执行失败。
- 输入无效、环境不可用、构建失败、超时或程序异常等情况才作为任务错误处理。

配对沟通记录见 [`review/coordination.md`](review/coordination.md)。

## E2 工作边界

本次评审针对 B08 提供的静态接口定义和请求、结果样例。评审通过表示双方
能够解释并接受当前接口交接方式，不表示 A08 已经实现 BuildChecker 或
EChecker，也不表示已经生成真实 MD/RD 检测结果。

真实项目选择、C0/C1/C2、检测程序实现和微服务联调属于 E3 后续工作。

## 最终结论

经过分项检查，A08 认为 B08 当前提供的 BuildChecker 和 EChecker 请求、
结果及组间交接设计内容完整、语义清楚，能够满足 E2“需求与接口契约”的
课堂检查要求。

**A08 本次评审结论：通过，无必须修改项。**

后续实现过程中如发现接口细节需要调整，A08 与 B08 再根据实际开发情况
沟通修改。
