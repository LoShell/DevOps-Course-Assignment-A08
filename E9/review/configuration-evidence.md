# E9 专项：configuration-evidence

负责人：叶原原 241250076。状态：个人实现、服务器复验和原包核验通过，待组长审阅。

## 问题与机制

declarations 读取 CFLAGS 后，scan 首先验证精确白名单 `-O0`、`-O1`、`-O0 -DMODE=1`，再读取历史 key 和调用 GCC。flags 是 key 的一部分，故 -O0→-O1 必须刷新实际图，即使最终依赖集合相同。拒绝时 scan 不负责覆盖任何 JSON；个人运行器只在成功返回后另存新报告。恢复 -O1 可以复用最近有效 P1 历史。


没有修改核心 lab.py，也没有将白名单扩展成通用编译参数解析器；保持与公共框架的接口一致。

## 独立预期与新增覆盖

| 步骤 | 输入与独立预期 | 实际 |
| --- | --- | --- |
| P0 | CFLAGS=-O0，基础两项 MD/RD | 与独立基线精确集合一致，程序输出 1 |
| P1 | 仅 CFLAGS 改 -O1；key 改变、两目标刷新，依赖和发现不变 | refreshed 两目标、reused 空；added/resolved 均空；与 P1-full 三集合一致；真实 strace 投影一致；clean build 输出 1 |
| P2 | 仅 CFLAGS 改 -O2；不支持，增量和无历史扫描均应拒绝 | 两次均精确抛 UNSUPPORTED_FLAGS，无 P2 成功报告；旧历史内存对象及既有报告/构建日志/动态证据逐文件 SHA-256 不变 |
| P3 | 恢复 -O1，使用 P1 历史 | 两目标复用、刷新空；三集合与全量一致，added/resolved 空，commit 指向新 P3；clean build 输出 1 |

P2 的 `P2-rejected.json` 是拒绝记录，保存真实提交、错误和拒绝前逐文件哈希，不冒充成功扫描。snapshot 排除正在写入的 steps 日志和主动修改的 project；旧 baseline/P1/完整 buildchecker 都受校验。恢复阶段再次核对旧证据，`personal-gate.json` passed=true。

额外边界测试对 `-O2` 和 `-O1 -include extra.h`，分别以无历史、有效历史、畸形历史调用 scan；均先拒绝配置，mock 断言没有调用编译器/其他外部命令。编译器本身可支持这些选项，拒绝来自本教学 profile 的白名单。


已有测试仅覆盖直接 include、新旧图复用和无历史的不支持配置拒绝。个人三项测试增加 helper 目标的两层 include、支持配置失效、旧内存/磁盘证据保持、拒绝早于编译器及历史访问、恢复有效配置复用。

## 真实验证与证据

源码 `b0c8a2bcd2dd910ae480ffab84607ba00107fd89`；基线 `369a8c82b73e53fb220fca28b89f3fc786e386e3`。定向 `python3 -m unittest discover -s labs/e8e10 -p 'test_student_241250076.py' -v`：3 项 OK，退出 0；完整回归 `-p 'test*.py'`：10 项 OK，退出 0。均在服务器 `course-e8e10:241250076` 容器内执行，源码 `b0c8a2bcd2dd910ae480ffab84607ba00107fd89`，日志 `work/e89-241250076-tests-ae8tTaKa/personal-test.log`、`regression.log` 和对应 `*-exit.txt`。同一源码、同一套日志随两个个人包归档。

基线 OUT `work/e9-A-manual.1H0Y4P`，个人 OUT `work/e9-A-manual.FkC1SM`；两轮完整提交、构建/扫描路径、trace 定位与哈希清单见 [个人记录](../records/241250076.md)。机器可读索引见 [evidence](../validation/241250076-evidence.json)。

## 代价与局限

全局 key 使未变化目标也可能刷新；只比较两对象目标，不能推断系统头、动态 include、条件构建和复杂 Make 的任意配置。SHA-256 保持证明本轮被纳入 snapshot 的旧证据未变，不代表框架自动提供不可变存储。snapshot 明确排除正在写入的步骤日志和受测项目。
