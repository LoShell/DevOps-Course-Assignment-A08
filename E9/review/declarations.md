# E9 声明依赖专项

负责人：邱莉扉 241250097。独立测试和服务器复验均完成。

## 机制

参考 `labs/e8e10/lab.py` 的 declarations 每次解析当前 Makefile；scan 缓存 key 包含本地 C/H 预处理行、配方、CFLAGS和编译器版本。纯声明变化不改变 key，所以 actual 可复用，但 declared 必须重新读取。findings 分别计算 actual-declared（MD）和 declared-actual（RD），added/resolved 再比较新旧发现。声明增加不应顺带删除冗余项。

## 独立输入与结果

基线 C0 程序输出1；C1只改表达式，实际 make 重编 main.o 并链接 app，但依赖图复用；C2新增 extra.h include，保守刷新两目标，added仅 MD(main.o,extra.h)；C3只补 config.h/extra.h 声明，复用实际图，resolved精确为两项MD，只剩RD(main.o,unused.h)。个人 P1先只补config.h，resolved仅该MD且保留RD；P2新增并使用extra.h，added仅该MD；P3只补extra.h，resolved仅该MD，RD继续保留。P1/P3不变key、actual与配方，declared发生变化；每步增量与GCC全量一致，P1/P3另经真实动态核对。P2构建采用make -B app规避时间戳粒度影响，该日志不用于声称普通增量构建行为。

## 个人贡献

新增 `labs/e8e10/test_student_241250097.py` 的 run_e8/run_e9 和两个 unittest。现有参考测试有直接 include 失效与 patch 保留RD，但没有 helper 的两层间接 include，也没有先后补两项声明时各步完整 added/resolved、declared、实际图复用核对。本次未修改 lab.py，无需协调公共函数归属。场景同用于临时测试与新 OUT 持久化，只有成功断言后写 personal-gate。动态检查在持久化阶段通过带 SYS_PTRACE 的 lab_python 实际执行。

## 证据与局限

- baseline：源码 `ecc8ff3a199b72abfa49b78bf9ff8667fc371968`，OUT `work/e9-A-manual.sdtYRl`，服务器包 `/root/devops-submissions/241250097/E9/baseline/run-ut7eZreE`，电脑SHA-256全部一致。
- personal：源码 `8c4b9e2bdc21574cf1fa42df3834aad971056c08`，OUT `work/e9-A-manual.JTpb4b`，服务器包 `/root/devops-submissions/241250097/E9/personal/run-9fAmRHCz`，电脑SHA-256全部一致。

完整报告、实际集合、日志、trace定位和哈希见本阶段 records/241250097.md 与验收CSV。GCC依赖扫描只覆盖允许配置下本地头文件；缓存对预处理变化保守刷新全部两个目标，不是精细到单目标的最优失效策略。E9参考路线仅GCC全量，个人P1/P3另有真实动态核对；不以未执行检查冒充动态通过。E10个人验收未开展。
