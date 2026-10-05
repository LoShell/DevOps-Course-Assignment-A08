# 人工 Oracle

本目录保存人工确认的预期结果，不保存工具自动生成后未经核对的结论。

计划文件：

- `md-rd.expected.json`：固定 MD/RD 的目标、文件路径和判定依据。
- `incremental.expected.json`：C0/C1/C2 的 SHA、变更类型、预期报告和行为输出。

JSON 字段应尽量与 E2 契约一致，但所有仓库 URL、SHA 和配置标识必须替换为
E3 的真实值。负责人需在证据文件中解释每一条预期结果如何人工得出。
