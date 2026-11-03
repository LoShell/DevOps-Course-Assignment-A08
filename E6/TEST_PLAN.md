# E6 新增测试分配

以下四项是代码阅读后的选题，尚未编写或执行。现有参考测试为 15 项，各人独立新增一个文件，避免修改同一测试文件。
四项场景已用临时独立输入完成离线可行性检查，预期与现有实现吻合；正式个人测试由各成员编写并在服务镜像中验证。

## 088：实际与声明完全一致

- 文件：services/buildchecker/tests/test_e6_241250088.py。
- 机制：analyze 的两项集合差与输出图。
- 输入：独立小型 trace：make 派生编译作业，成功读取 unit.c、needed.h，生成 unit.o；数据库声明 unit.o: unit.c needed.h。
- 预期：findings=[]，observed_targets=[unit.o]；实际图和声明图均精确包含 unit.o→unit.c、unit.o→needed.h。
- 与现有覆盖的区别：现有 analyze 测试针对一条缺失、一条冗余；新增验证零差异的正例及两图边集合。

## 097：伪目标依赖环

- 文件：services/buildchecker/tests/test_e6_241250097.py。
- 机制：declaration_graph 的递归展开与环检查。
- 输入：# Files 区段，.PHONY: prepare loop，prepare: loop，loop: prepare，unit.o: unit.c prepare，末尾带 files hash-table stats。
- 预期：抛出 Unsupported，包含 Cycle in phony prerequisites；由循环输入触发，正常无环展开继续由既有测试覆盖。
- 与现有覆盖的区别：现有用例只验证无环伪目标展开与 order-only 字段。

## 071：临时产物重命名

- 文件：services/buildchecker/tests/test_e6_241250071.py。
- 机制：execution_graph 的 rename 分支、produced 集合和最终目标归属。
- 输入：独立 make→编译作业 trace；读取 unit.c、needed.h；创建 temporary.o，rename("temporary.o", "unit.o")=0。
- 预期：目标集合只有 unit.o，依赖为 unit.c、needed.h；输出证据 operation=rename；temporary.o 属本作业产物。
- 与现有覆盖的区别：既有测试覆盖 unlink 清理，新增覆盖 rename 最终输出。

## 076：输出目录位于输入目录内

- 文件：services/buildchecker/tests/test_e6_241250076.py。
- 机制：full_check 输入/输出路径检查。
- 输入：临时 fixture 目录内放置小文件，将输出设置为 fixture/result；记录输入哈希，mock execute 观察调用情况。
- 预期：在 Linux 服务测试环境抛出 ValueError，消息包含 Output must be outside；execute 调用次数为 0，输入哈希保持一致。
- 与现有覆盖的区别：已有测试主要检查离线图分析，新增覆盖实际采集入口的参数检查。

## 实施规则

每个文件只放本人用例，使用独立可读的小型输入和精确断言。直接调用负责函数即可，单元测试无需真实 Docker 构建。
076 的入口检查在 Linux 服务镜像中运行；本地 Windows 的 os.name 检查与之不同。
测试发现实现问题时保留失败日志并说明预期，按小组协商安排源码修改。
新增后先形成个人提交，再重建服务镜像、记录完整测试输出，并用新目录运行 E6 原始检测、修复复检和报告校验。
