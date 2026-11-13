# E7 提交检查表

## 已有材料和剩余项目

四人测试、个人报告、验收 CSV 和专项审阅已随 PR #16—#19 合并。基线服务 19 项、个人轮各 20 项、组长集成 23 项通过，各轮门禁回报均为 8/8。

- 088 基线与个人轮归档、SHA-256 及电脑备份路径仍需补录。
- 071、097、076 的个人报告已列两轮归档及哈希，组长收齐原包后核对哈希和报告索引。076 另有证据核验 JSON。
- 集成结果已记录，原始目录需下载核验，补录归档哈希。
- main 正常 CI、保护配置、失败 PR 拒绝日志、同一 PR 恢复和最终合并记录仍待完成。个人报告中引用该共享结果的 PENDING 项届时再更新。
- 模板内的空项用于后续填写，保留模板。历史 E5/E6 报告沿用其已有归档索引，本次收集 E7 的新增证据。

## 需要下载的服务器目录

| 所有人 | 仓库位置 | 完整运行目录，相对于该仓库 |
| --- | --- | --- |
| 088 基线 | /root/241250088/buildchecker | work/e7-241250088-baseline-nr4FTjkl |
| 088 个人 | /root/241250088/buildchecker | work/e7-241250088-personal-qfitdKaY |
| 088 集成 | /root/241250088/buildchecker | work/e7-241250088-integrated-GYJmGTi1 |
| 097 两轮 | /root/241250097/buildchecker | work/e7-241250097-3ZXk0iRO、work/e7-241250097-WoT7AmkU |
| 071 两轮 | /root/241250071/buildchecker | work/e7-241250071-X0ti8vqv、work/e7-241250071-GBno9AYS |
| 076 两轮 | /root/241250076/buildchecker | work/e7-241250076-baseline-0p7BTMgO、work/e7-241250076-personal-nBIdmim1 |

每轮保留整个目录，包含构建、镜像检查、单测、oracle、输入副本、trace、Make 数据库、JSON、CSV 和原始命令日志。已有归档直接下载原包及对应 .sha256，按个人报告中的哈希核对。071、097 的原包在其仓库 work/ 下，076 的原包在 /root/devops-submissions/241250076/ 下。

CI 完成后另外下载组长仓库的 work/ci-setup、work/ci-rejection、work/ci-recovery，以及 main 正常运行的 artifact 保存目录，按实际执行路径记录。保存三次运行的原始 artifact、运行链接、commit.txt、保护快照、拒绝日志及最终合并 JSON。

## 组长三轮证据打包命令

以下命令在 Ubuntu 执行，成功后通过 SFTP 下载打印出的归档和 .sha256。

```bash
(
  set -e
  cd /root/241250088/buildchecker
  mkdir -p /root/devops-submissions/241250088
  for RUN in \
    e7-241250088-baseline-nr4FTjkl \
    e7-241250088-personal-qfitdKaY \
    e7-241250088-integrated-GYJmGTi1
  do
    test -d "work/$RUN"
    ARCHIVE="/root/devops-submissions/241250088/A08-$RUN-$(date +%Y%m%d-%H%M%S).tar.gz"
    test ! -e "$ARCHIVE"
    tar -czf "$ARCHIVE" "work/$RUN"
    sha256sum "$ARCHIVE" > "$ARCHIVE.sha256"
    sha256sum -c "$ARCHIVE.sha256"
    printf '%s\n' "$ARCHIVE" "$ARCHIVE.sha256"
  done
)
```

## 最终包的组成

- 最终版本仓库源码、依赖锁文件、workflow、E7/ 和 docs/，附最终 SHA。
- 四人的两轮原始证据包，以及组长集成证据包。
- CI 正常、失败、恢复的 artifact 和合并门禁记录。
- 归档清单与 SHA-256，及 E5/E6 既有证据归档索引。

下载原包后在电脑用 PowerShell 的 Get-FileHash -Algorithm SHA256 校验，填写本地路径。最终源码包从收尾后的版本生成，报告源码版本与实际验证版本分别记录。

## 最终核对

- [ ] 个人报告、验收 CSV、个人 commit 和 PR 可相互追溯。
- [ ] 记录验证所用源码 SHA、服务镜像 ID、锁文件和环境。
- [ ] 保存独立判定、服务及新增测试日志，归档完整门禁 JSON、CSV 和逐场景原始证据。
- [ ] 填写正常、失败及恢复 CI 的运行链接、触发 SHA 和 artifact，保存保护快照、拒绝日志及最终合并记录。
- [ ] 汇总 E5/E6 证据索引和 E7 共同报告，核对本地备份路径与 SHA-256。
- [ ] 扫描提交内容。原始 `work/` 及 CI artifact 独立归档，排除认证文件和密钥。
