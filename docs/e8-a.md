# A08 E8：EChecker 基线复现

状态：2026-11-17 组长参考基线通过，原包已下载并核验；个人扩展及集成待完成。共同分支 a08/e8-e9。

## 目标与范围

保留 E7 BuildChecker 成果，建立真实对象目标历史图并验证未变化输入复用。受限 C/Make 教学配置，gcc -MM 路径与 BuildChecker 动态路径交叉核对；不宣称复现完整论文。

## 实际版本与证据

源码 SHA 为 `369a8c82b73e53fb220fca28b89f3fc786e386e3`；组长个人分支运行目录 `/root/241250088/buildchecker/work/e8-A-manual.iz7oZm`。镜像及详细判定见 [组长记录](../E8/records/241250088.md)。

GCC 与真实 BuildChecker 对象投影核对一致，精确检出 MD(main.o, config.h)、RD(main.o, unused.h)。原始读取证据 t.15:579，声明证据 make-db.txt:1044。未变化输入复用两个目标、无刷新，actual/declared/findings 三集合不变；终端步骤退出 0。
归档位于服务器 `/root/E8-241250088-baseline-MJZnwXqO` 与电脑 `D:\MYfile\3-1\Devops\Lab\241250088\E8`。双端哈希及原包内容核验通过，详见 [核验记录](../E8/validation/baseline-241250088-local-audit.json)。个人与集成测试、PR/CI 待填写。

## 贡献与结论

分工见 [E8/CONTRIBUTIONS.md](../E8/CONTRIBUTIONS.md)，实际记录见各成员 records 和 review。当前组长参考基线与证据归档核验通过；未完成项为个人扩展、其他成员实验及最终提交验收。
