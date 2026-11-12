# E7 专项审阅

审阅人：邱莉扉（241250097）。
日期：2026-11-12。
专项：声明路径归一化与 Make 数据库证据。

所用源码 SHA：
- 基线：3a0ae35b27e783c480f66412b3e4f53802c6be68
- 个人轮：c656363e41cf86c2579aa9e2b11b302dbe2e7011

以下证据路径相对于服务器仓库 `/root/241250097/buildchecker`。
基线证据目录：`work/e7-241250097-3ZXk0iRO`。
个人轮证据目录：`work/e7-241250097-WoT7AmkU`。

| 检查项 | 输入与预期 | 实际观察 | 代码位置与证据 | 判定 |
| --- | --- | --- | --- | --- |
| 声明目标路径归一化 | 人工数据库目标 ./build/../main.o 应归一化为 main.o | 新增测试断言目标集合精确为 main.o，通过 | services/buildchecker/buildchecker/fullcheck.py 的 project_path、declaration_graph；services/buildchecker/tests/test_e7_241250097.py；个人轮 personal-test.log | PASS |
| 普通依赖路径归一化 | ./src/../main.c、/course/project/include/../config.h、./unused.h 应归一化为 main.c、config.h、unused.h | 新增测试精确集合断言通过 | 同上；个人轮 build-console.log 和 full/gate/unit-tests/stdout.log | PASS |
| 原始声明证据保留 | 每条归一化依赖仍保留 source=make_database、artifact=make-db.txt、line=3 和完整原始声明 | 三条依赖的完整证据字典断言均通过 | fullcheck.py 的 declaration_graph；test_e7_241250097.py 的逐依赖 subTest；个人轮 personal-test.log | PASS |
| 真实 Make 数据库声明 | original 三次运行应声明 main.o: main.c unused.h | 两轮三次运行的 make-db.txt 第1053行均为该声明，与 findings 中的证据一致 | 两轮 full/gate/original-1、original-2、original-3 下的 evidence/make-db.txt 和 evidence/findings.json | PASS |
| 声明与实际读取对照 | config.h 被实际读取但未声明；unused.h 被声明但本次配方任务未观察到读取 | 两轮 original 的 trace 均显示 config.h 成功以 O_RDONLY 打开；报告精确检出对应 MD/RD | 两轮 original 场景的 evidence/trace/、evidence/findings.json 和 evidence/make-db.txt | PASS |
| 读取与输出创建区分 | 不将创建 main.o 的操作解释为读取 config.h | original-1 的 t.15 第579行为读取 config.h，t.16 第23行为创建 main.o；original-2、original-3 对应为 t.14 第579行和 t.15 第23行，两轮一致 | 两轮 original 场景 evidence/trace/ 中对应文件 | PASS |
| 修复输入与结果 | fixed 相比 original 仅 Makefile 输入哈希变化，findings 为空 | 两轮均符合；config.h、main.c、unused.h 哈希未变，状态 SUCCEEDED，工具退出0 | 两轮 full/gate/fixed/evidence/findings.json、original-1/evidence/findings.json 和 full/gate/results.csv | PASS |
| 新增测试集成 | 新镜像包含本人测试，定向测试及完整门禁通过 | 定向测试1项通过；服务测试由基线19项变为个人轮20项；两轮门禁均8/8，整体退出0 | 个人轮 personal-test.log、build-console.log、full/gate/unit-tests/stdout.log；两轮 gate-exit.txt 和 full/gate/results.csv | PASS |

待复核问题及对应日志：

本次已检查范围内未发现待修复问题。验证边界如下：
- 新增测试使用人工构造的小型 Make 数据库，验证声明解析及证据保留；
  未运行真实 Make 来生成这条含特殊路径的声明。
- RD 的结论限定于本次构建配置及配方任务中的读取观察，
  不表示 unused.h 在所有构建配置下均无用途。
- 未将本次结果扩展为对所有 Make 语法、符号链接或复杂路径场景的验证。
- 对应原始日志及数据库、trace 已列于上表；两轮原始证据已独立归档并下载，服务器与本地 SHA-256 校验均通过。归档名称、校验值和备份路径见[个人报告](../records/241250097.md)。
