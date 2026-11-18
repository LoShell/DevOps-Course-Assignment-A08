# E8 专项：configuration-evidence

负责人：叶原原 241250076。状态：个人实现、服务器复验和原包核验通过，待组长审阅。

## 问题与机制

scan 的 key 包含项目内 C/H 文件预处理指令、配方、CFLAGS 和 GCC 版本。本用例改变 helper.c 的 include 并引入 bridge.h，当前全局 key 保守失效，因此连 main.o 也刷新。extra.h 被间接读取，不要求在 helper.c 直接出现。真实动态证据用 BuildChecker 的目标/作业归属投影核对。


没有修改核心 lab.py，也没有将白名单扩展成通用编译参数解析器；保持与公共框架的接口一致。

## 独立预期与新增覆盖

个人输入在 helper.c 添加 `#include "bridge.h"`，新建 bridge.h 包含 extra.h，helper 返回 EXTRA（仍输出 1）。独立预期：main.o 仍为 `[config.h,main.c]`；helper.o 精确为 `[bridge.h,extra.h,helper.c]`；声明不变；发现为 `{MD(main.o,config.h), RD(main.o,unused.h), MD(helper.o,bridge.h), MD(helper.o,extra.h)}`。

P1 两目标刷新、reused 为空，added 精确为 helper.o 的 bridge.h/extra.h 两条 MD，resolved 为空。增量与 P1-full 的 actual/declared/findings 三集合相同；`P1-buildchecker/` 的真实 strace 对象投影也一致。再次未变扫描两目标复用，新增/消除集合为空。旧 baseline 内存深拷贝和已有证据 SHA-256 不变；`personal-gate.json` passed=true。


已有测试仅覆盖直接 include、新旧图复用和无历史的不支持配置拒绝。个人三项测试增加 helper 目标的两层 include、支持配置失效、旧内存/磁盘证据保持、拒绝早于编译器及历史访问、恢复有效配置复用。

## 真实验证与证据

源码 `b0c8a2bcd2dd910ae480ffab84607ba00107fd89`；基线 `369a8c82b73e53fb220fca28b89f3fc786e386e3`。定向 `python3 -m unittest discover -s labs/e8e10 -p 'test_student_241250076.py' -v`：3 项 OK，退出 0；完整回归 `-p 'test*.py'`：10 项 OK，退出 0。均在服务器 `course-e8e10:241250076` 容器内执行，源码 `b0c8a2bcd2dd910ae480ffab84607ba00107fd89`，日志 `work/e89-241250076-tests-ae8tTaKa/personal-test.log`、`regression.log` 和对应 `*-exit.txt`。同一源码、同一套日志随两个个人包归档。

基线 OUT `work/e8-A-manual.0kRGs5`，个人 OUT `work/e8-A-manual.lH0ymS`；两轮完整提交、构建/扫描路径、trace 定位与哈希清单见 [个人记录](../records/241250076.md)。机器可读索引见 [evidence](../validation/241250076-evidence.json)。

## 代价与局限

全局 key 使未变化目标也可能刷新；只比较两对象目标，不能推断系统头、动态 include、条件构建和复杂 Make 的任意配置。SHA-256 保持证明本轮被纳入 snapshot 的旧证据未变，不代表框架自动提供不可变存储。snapshot 明确排除正在写入的步骤日志和受测项目。
