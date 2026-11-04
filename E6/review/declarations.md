# E6 专项审阅

审阅人、学号、日期：邱莉扉，241250097，2026-11-04。
负责机制：declaration_graph；声明图解析、伪目标递归展开与环检查。

## 机制审阅

实现文件：services/buildchecker/buildchecker/fullcheck.py。
declaration_graph 从第237行开始；本次查看的版本中，伪目标环异常位于第289行。位置以对应运行 SHA 的源码为准。

函数读取 Make 数据库的 # Files 区段，在 # files hash-table stats 处结束区段解析。它收集目标、普通依赖、order-only 依赖及 .PHONY 声明，对项目路径归一化后建立声明关系。

内部 expand 函数递归展开伪目标：
- 非伪目标作为叶子依赖返回。
- 伪目标递归展开为其依赖。
- trail 保存当前递归路径；再次遇到路径中的伪目标时，抛出 Unsupported("Cycle in phony prerequisites")。
- 返回声明图时过滤伪目标本身。
- order-only 字段单独保存，不混入普通依赖集合。

| 输入/版本 | 函数及关键位置 | 实际观察 | 图/报告字段与原始证据 | 结论 |
| --- | --- | --- | --- | --- |
| 基线 aff4eba7dca7a09a372d1264375d9fe9cd11354f；原始样例 | declaration_graph；Files区段解析、声明依赖收集 | main.o 声明 main.c、unused.h；app 声明 main.o | work/e6-baseline-20261104-104839/before/evidence/declared-graph.json；make-db.txt:1053 和图中引用的 make-db.txt:601 | 声明图包含三条预期边 |
| 个人版本 12f85dcbfc7ff58325f814c3c21c50962b0c6089；原始样例 | declaration_graph；同一解析逻辑 | 声明图边集合与基线相同 | work/e6-personal-20261104-113209/before/evidence/declared-graph.json；make-db.txt:1053 和图中引用的 make-db.txt:601 | 新增测试后，原始样例声明图结果保持一致 |
| 个人测试；独立临时 Make 数据库 | declaration_graph 内部 expand；递归路径环检查 | prepare 与 loop 相互依赖，断言 Unsupported 及指定消息 | services/buildchecker/tests/test_e6_241250097.py；个人轮 build/unit-tests/stdout.log，16 passed | 循环输入按预期触发明确异常 |
| 两轮修复副本 | declaration_graph 的输入声明；检测报告与校验 | main.o 声明改为 main.c、config.h；修复后 findings=[] | 各轮 after/fixture/Makefile、after/evidence/findings.json、meta/verification.json | 修复声明后发现消除，仅 Makefile 输入哈希变化 |

## 本人测试

测试文件：
services/buildchecker/tests/test_e6_241250097.py

测试方法：
TestPhonyCycle241250097.test_phony_prerequisite_cycle_raises_unsupported

个人代码提交及运行 SHA：
12f85dcbfc7ff58325f814c3c21c50962b0c6089

输入：
使用 TemporaryDirectory 创建独立 make-db.txt，内容如下。

```text
# Files
.PHONY: prepare loop
prepare: loop
loop: prepare
unit.o: unit.c prepare
# files hash-table stats:
```

预期：
直接调用 declaration_graph(database, "/course/project")，抛出 Unsupported，消息包含 Cycle in phony prerequisites。

断言：
assertRaisesRegex(Unsupported, "Cycle in phony prerequisites")，同时检查异常类型与消息。

输入包含合法的 Files 区段、区段结束标记和目标声明，因此预期异常来自伪目标递归环，而不是缺少 Files 区段等输入格式错误。该测试不以宽泛的 ValueError 或任意异常作为通过条件。

实际：
新增一个独立测试文件，未修改核心实现。先提交测试代码，再重建个人服务镜像；构建入口、构建子步骤和单测子步骤退出码均为0，服务测试由15项增加为16项。

重建日志：
- work/e6-personal-20261104-113209/build/build/
- work/e6-personal-20261104-113209/build/unit-tests/stdout.log
- work/e6-personal-20261104-113209/build/unit-tests/exit-code.json
- work/e6-personal-20261104-113209/meta/build-exit-code.txt

实际单测结果：
16 passed in 0.05s。

覆盖区别：
既有 test_phony_expands_to_real_files_and_order_only_is_separate 覆盖正常无环展开和 order-only 分离；本人新增测试覆盖伪目标依赖环。未声称覆盖全部 Make 语法、所有环形拓扑或大型构建场景。

## 原始与修复结果

### 两轮输入与运行版本

| 轮次 | 运行 SHA | 证据根目录 |
| --- | --- | --- |
| baseline | aff4eba7dca7a09a372d1264375d9fe9cd11354f | work/e6-baseline-20261104-104839 |
| personal | 12f85dcbfc7ff58325f814c3c21c50962b0c6089 | work/e6-personal-20261104-113209 |

各轮 before/fixture/ 和 after/fixture/ 分别保存原始与修复输入；before/evidence/ 和 after/evidence/ 保存报告、两图、进程、Make 数据库及 trace。

### 图边与发现

两轮原始实际图边集合相同：
- app→main.o
- main.o→main.c
- main.o→config.h

两轮原始声明图边集合相同：
- app→main.o
- main.o→main.c
- main.o→unused.h

两轮均精确报告：
- MISSING(main.o, config.h)
- REDUNDANT(main.o, unused.h)

原始报告 status=SUCCEEDED、clean_exit_code=0、build_exit_code=0，入口退出码1。

### 原始证据追溯

以下文件位置分别相对于各轮 before/evidence/。

基线：
- t.15:579 成功只读打开 config.h。
- t.16:23 创建 main.o。
- processes.json 显示 PID 15、16 的 job_pid 均为14，将输入读取与产物创建归入同一编译作业。
- make-db.txt:1053 声明 main.o: main.c unused.h。

个人轮：
- t.14:579 成功只读打开 config.h。
- t.15:23 创建 main.o。
- processes.json 显示 PID 14、15 的 job_pid 均为13。
- make-db.txt:1053 声明 main.o: main.c unused.h。

上述关键原始行及上下文已在服务器查看。创建 main.o 的记录是产物证据，不是读取 config.h 的记录。

unused.h 在声明中存在，在本次实际依赖图中不存在。冗余结论限于本次构建配置和相应作业的观测范围。

### 修复与校验

两轮均在独立副本中将：

```make
main.o: main.c unused.h
```

改为：

```make
main.o: main.c config.h
```

两轮修复后均为 status=SUCCEEDED、findings=[]、clean_exit_code=0、build_exit_code=0、入口退出码0。

两轮校验均为：
- 校验退出码0。
- passed=true。
- before_findings=2。
- after_findings=0。
- changed_inputs=["Makefile"]。

Makefile 修复前 SHA-256：
fd1dcd76a0bd9678351a1503941a5a875351455d4a6879e76af0af0b6c64772f

Makefile 修复后 SHA-256：
128069c949b0239e3377f320d51498c2b37a317c602d8755d573a283e1f400ae

其余输入哈希保持一致，完整值见个人报告第3节及两轮 findings.json。

校验输出：
- work/e6-baseline-20261104-104839/meta/verification.json
- work/e6-personal-20261104-113209/meta/verification.json

校验器检查保存报告的断言，未独立重新验证全部 trace；本审阅另行查看了上述关键原始记录。

### 与 E5 人工结论对照

E5/records/241250097.md 的人工结论同样为 main.o 缺失 config.h、冗余 unused.h，app 的实际与声明依赖均为 main.o，与本次两轮 E6 原始结果一致。

E5 与 E6 的 trace 文件名、PID 和行号按各次运行分别引用。E5 当时未执行修复复检，本次 E6 补充了该验证。

## 同版本对照与待办

本人 baseline 使用组长公布的 E6_BASE_SHA；personal 使用本人的测试提交 SHA。两轮版本不同，不将它们称为同版本跨成员对照。

尚未完成至少两人的同集成版本证据对照。等待组长合并四项测试、公布 E6_FINAL_SHA 并安排集成结果与跨成员证据审阅。

两轮原始证据已在服务器归档，并下载到电脑 E:\大三上\DevOps\labs\lab6，完整 SHA-256 一致，关键报告可读取：

- baseline：A08-241250097-E6-baseline-20261104-110114.tar.gz
- SHA-256：356fb57b2bc3dced1b28ed3df02d85bdf102e01c8a44acae5b25ecba8ae92a62
- personal：A08-241250097-E6-personal-20261104-114817.tar.gz
- SHA-256：41d41eca37132ad00664897ef5307195fee5e339751dbc0b619cc66566995d33

构建后的镜像 ID 已保存于各轮 meta/service-image-inspect.json。运行命令记录镜像标签与容器 ID，未独立保存运行容器的不可变镜像 ID；这一证据边界见个人报告第2节。

待完成：
- 三份个人文档均已填写；下一步审阅变更并提交文档。
- 推送个人分支并提 PR 到 a08/e5-e6。
- 制作并核对包含源码、定稿报告、E5 必要引用和原始证据的最终包。
- 由组长完成集成审阅、跨成员同版本对照及共同成果汇总。

AI 使用：Codex 辅助阅读实现、生成测试和文档、解释与核对证据；本人在服务器执行命令，实际结论以保存的日志和原始记录为依据。
