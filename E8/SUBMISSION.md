# E8—E9 交付清单

状态：准备中，下面是待办，不表示已通过。

## 每名成员

- [ ] 在个人服务器目录核对 origin、Git 本地学号/邮箱、认证与干净工作区。
- [ ] 记录共同基线 SHA，分别运行 E8/E9；每阶段使用新 OUT。
- [ ] E8 保存 baseline/incremental、完整 BuildChecker trace/数据库/图/报告、steps、结论、源码 SHA 与镜像 ID。
- [ ] E9 保存 baseline、C1/C2/C3、C0/C1/C2 构建日志、内部完整 Git 历史、steps、结论。
- [ ] 新增个人独立预期与测试，提交后固定源码版本，新 OUT 运行个人轮并保存 unittest 日志。
- [ ] 填写 E8/E9 records、验收 CSV、专项 review，以及个人报告、ADR、AI_USAGE。
- [ ] 创建个人 PR 至 a08/e8-e9，记录实际提交、PR、Checks 与归档 SHA-256。
- [ ] 原始 work 不进 Git，归档下载到电脑并抽查恢复。

## 组长集成

- [ ] 抽查个人证据与报告对应关系，合并四人贡献。
- [ ] 在服务器验证集成版本，记录源码 SHA、环境 ID、测试数量和实际结果。
- [ ] 原 E7 CI 与 e8e10-quality-gate 检查通过；记录 run URL/headSha/结论，下载 artifact（14 天）。
- [ ] 整合 PR 至 main，记录合并 SHA。
- [ ] 分别整理 E8/E9 交付，核对教师平台实际要求；材料未给出统一最终上传平台/截止日，按教师通知。

## 归档注意

通用 tar 排除 .git，而 E9 明确要求内部完整历史。额外用 git -C <E9_OUT>/project bundle create <仓库外路径>/E9-project.bundle --all 保存并 verify；恢复克隆时核对 C0—C3 和报告 commit 一致。归档包含 bundle、源码、run_lab.py、个人报告、实验 work 和 CI 下载证据。归档置于仓库外，记录 SHA-256，避免把压缩包自身打入包内。

区分外层学生源码 SHA、内部受测项目 commit、CI headSha、最终合并 SHA。仅有参考代码导入或绿色 CI 不代表个人实验已完成。
