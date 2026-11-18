# E8 声明依赖专项

负责人：邱莉扉 241250097。独立测试和服务器复验均完成。

## 机制

参考 `labs/e8e10/lab.py` 的 declarations 每次解析当前 Makefile；scan 缓存 key 包含本地 C/H 预处理行、配方、CFLAGS和编译器版本。纯声明变化不改变 key，所以 actual 可复用，但 declared 必须重新读取。findings 分别计算 actual-declared（MD）和 declared-actual（RD），added/resolved 再比较新旧发现。声明增加不应顺带删除冗余项。

## 独立输入与结果

基线精确为 MD(main.o,config.h)、RD(main.o,unused.h)。个人输入在 helper.c 引入 shared.h，shared.h 间接包含 extra.h，helper 返回 EXTRA；main.c 仍直接包含 config.h。独立实际图 main.o=[config.h,main.c]，helper.o=[extra.h,helper.c,shared.h]；声明 helper.o=[helper.c]。个人发现精确为原两项加 MD(helper.o,shared.h)、MD(helper.o,extra.h)。未变输入复用两目标，added/resolved 均空，增量与全量一致。baseline.actual 来自本轮真实 BuildChecker 对象投影。

## 个人贡献

新增 `labs/e8e10/test_student_241250097.py` 的 run_e8/run_e9 和两个 unittest。现有参考测试有直接 include 失效与 patch 保留RD，但没有 helper 的两层间接 include，也没有先后补两项声明时各步完整 added/resolved、declared、实际图复用核对。本次未修改 lab.py，无需协调公共函数归属。场景同用于临时测试与新 OUT 持久化，只有成功断言后写 personal-gate。动态检查在持久化阶段通过带 SYS_PTRACE 的 lab_python 实际执行。

## 证据与局限

- baseline：源码 `369a8c82b73e53fb220fca28b89f3fc786e386e3`，OUT `work/e8-A-manual.UDAQ79`，服务器包 `/root/devops-submissions/241250097/E8/baseline/run-xjN3g98o`，电脑SHA-256全部一致。
- personal：源码 `f7757f2d45d0dd73487c67cda7a4409c4b1396f4`，OUT `work/e8-A-manual.hWDQak`，服务器包 `/root/devops-submissions/241250097/E8/personal/run-RWhoKtWs`，电脑SHA-256全部一致。

完整报告、实际集合、日志、trace定位和哈希见本阶段 records/241250097.md 与验收CSV。GCC依赖扫描只覆盖允许配置下本地头文件；缓存对预处理变化保守刷新全部两个目标，不是精细到单目标的最优失效策略。E9参考路线仅GCC全量，个人P1/P3另有真实动态核对；不以未执行检查冒充动态通过。E10个人验收未开展。
