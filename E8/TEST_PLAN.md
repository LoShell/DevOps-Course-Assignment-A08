# E8—E9 测试计划

当前仅定义判定，尚未执行。服务器运行采用 Python unittest。课程原有 test_profile.py 七项保持不动；个人文件命名 test_student_<学号>.py，统一发现模式 test*.py。

## 基线验收

E8：actual(main.o) 精确等于 main.c/config.h；发现精确为 MD(main.o, config.h)、RD(main.o, unused.h)。真实 strace/Make 数据库结果按 main.o/helper.o 投影交叉核对；baseline.actual 来自真实 BuildChecker。未变输入 reused 两目标、refreshed 空，图和发现一致。

E9：C0 构建输出 1；C1 函数体变化仅复用依赖图，但 make 可重编译/链接；C2 新增 extra.h include 后新增 MD，参考实现保守刷新两个目标；C3 声明补 config.h/extra.h 后复用实际图、消除两项 MD，保留 RD unused.h。记录真实 C0—C3 提交与 C0/C1/C2 构建日志。

## 个人专项

| 学号 | 建议新增输入 | 独立预期 |
| --- | --- | --- |
| 088 | 与原用例不同的函数体变化，另补本人 E8 间接 include 用例 | 预处理/配方/配置未变时两图复用，actual/declared/findings 精确不变；全量扫描一致 |
| 097 | 基线仅添加 config.h 声明，随后在新增 include 状态补相应声明 | 实际图复用，MD 按预期消除，RD unused.h 不被删除；核对 added/resolved 的完整集合 |
| 071 | config.h 间接包含 extra.h，改变前后均有真实内部提交 | 旧签名失效，main.o 新增 extra.h 边与 MD；参考实现两个目标刷新，增量和全量三集合一致 |
| 076 | 从支持的 -O0 切换 -O1，并独立构造一个不支持配置 | 支持配置触发刷新且与全量一致；不支持配置明确抛 UNSUPPORTED_FLAGS；旧历史 JSON/已有证据不被覆盖 |

课程测试已覆盖直接 include 新增、未变输入复用、不支持配置拒绝等基础场景，个人用例要说明新增覆盖。此处是预期，成员可据实际问题调整输入并更新记录。E8 每人另有间接 include 自主任务，详见分工表。

阶段记录必须包括输入、预期、实际、日志位置、退出码；通过的精确集合不能仅用发现数量代替。测试和实验均在服务器执行，本地框架阶段只做语法及文档检查。
