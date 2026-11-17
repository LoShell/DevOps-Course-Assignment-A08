# E9 验证证据索引

状态：组长参考基线与个人扩展通过，两轮原包及双端哈希核验通过；PR/CI、集成待验收。

组长源码 0c1e2c46eb788037f14ef7658926bbe63c8194cb，OUT work/e9-A-manual.eBhiYp，服务器归档 /root/devops-submissions/241250088/E9/baseline/run-jGmwm2Py。三个哈希、恢复的C0—C3历史、精确图与发现变化、构建及步骤日志已核验，见 [审计JSON](baseline-241250088-local-audit.json) 和 [个人记录](../records/241250088.md)。

组长个人版本71a4eda，OUT work/e9-A-manual.WzDiYf，定向2项、回归9项通过；P0—P2历史、图复用/失效、全量和动态对照已核验，见 [个人轮审计](personal-241250088-local-audit.json)。服务器归档 /root/devops-submissions/241250088/E9/personal/run-YD11gDYR，回传哈希与本地实际文件及下载清单一致。

待补：其他三人实验、PR/CI与最终集成轮。原始证据留在 work 并下载归档，不提交大批运行产物。

每份报告 commit 必须对应可恢复的 C0—C3 历史；不能用外层工具代码 SHA 替代。
