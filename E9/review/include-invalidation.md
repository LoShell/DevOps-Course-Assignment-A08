# E9 专项：include-invalidation

负责人：范从钰（241250071）。状态：已完成本人实测、原始证据归档与本地 SHA-256 校验；PR/CI 待后续提交。

## 问题与机制

本专项验证连续提交中的间接 include、间接头文件内容变化与缓存失效。审阅代码为 `labs/e8e10/lab.py` 的 `scan()`：缓存键由全部本地 `.c`/`.h` 文件的预处理指令、Make 配方、编译 flags 和 GCC 版本构成；键相同才复用历史 actual 图，否则保守刷新 `main.o`、`helper.o`。

本轮还区分两类行为：GCC `-MM`/BuildChecker 能观察到真实头文件读取关系；而 Make 只根据 Makefile 中显式声明决定是否重编译。未在声明中列出 `config.h`、`extra.h` 时，修改它们不会触发 Make 重建，但不代表实际依赖不存在。

## 独立预期与个人改动

课程 E9 基线覆盖 C0—C3 的直接 include、声明修复与图复用；本人新增连续间接包含场景。

新增测试文件：`labs/e8e10/test_student_241250071.py`。
E9 测试方法：`test_indirect_header_change_invalidates_cache_across_commits`。
个人测试提交：`e80d991142c5af8d33408b9e77177a670481b349`。

输入与独立预期：

1. P1 将 `config.h` 改为间接包含 `extra.h`。预期 `main.o` 新增实际边 `extra.h` 和 MD(`main.o`, `extra.h`)；两个对象刷新，无复用；增量和全量三集合相同。
2. P2 只将 `extra.h` 的 `#define EXTRA 0` 改为 `#define EXTRA 1`。预期边集合、findings、added、resolved 不变，但由于间接头文件预处理指令变化，缓存键失效，两个对象仍刷新、无复用；增量和全量三集合相同。
3. 因 Makefile 仍未声明 `config.h`、`extra.h`，P1/P2 的 `make app` 不应出现 gcc 重编译命令；真实 BuildChecker 动态检查仍应报告精确 MD/RD。

## 真实验证与证据

E9 基线 OUT：`work/e9-A-manual.XJ75E0`，外层源码 SHA：`9531e0d5aed286b61941955319b1149b52577de2`。内部 C0/C1/C2/C3 分别为：

- `7e1b1a004bb101ddcbd66f2c55dd9ea425453b44`
- `64f6f545a07aca8dce6628e5f7649b4970e1a7df`
- `cb0bcf8145f1b39fbcebf35cfbf3e3245bb6347d`
- `c43923793b2bcba635f0ce29978108ba36c936f3`

C1 普通函数体变化时 `C1.json` 复用两个目标；C2 直接 include 时 `C2.json` 新增 MD(`main.o`, `extra.h`) 并刷新两个目标；C3 补齐声明时 `C3.json` 复用 actual 图，resolved 精确为 config.h、extra.h 两项 MD，RD(`main.o`, `unused.h`) 保留。C2/C3 均与其 full JSON 的 actual、declared、findings 一致；`baseline-gate.json` 为 `passed=true`。

个人 OUT：`work/e9-A-manual.knagqu`；镜像 ID：`sha256:ac9488455abe7567438f7ccfc4b826aef5021efece7be18cc8fc8022768969c7`。内层 P0/P1/P2 分别为：

- `2cfb7064bb773b36809d5d5b05e44eae893f8004`
- `400311eaed71a58f537bc3ba7994bc38c2f02fac`
- `f1bb02b552f3fdc79d29f48e8f1ae632a8be6bc6`

P1 的 `P1.json` 显示 `main.o -> [config.h, extra.h, main.c]`，新增项精确为 `[[MISSING, main.o, extra.h]]`，两个目标刷新、无复用；`P1-full.json` 一致。`P1-build.log` 无 gcc 命令，说明显式 Make 声明未触发重建；`P1-buildchecker/findings.json` 的真实 strace 证据仍与预期 MD/RD 一致。

P2 的 `P2.json` 与 P1 的 actual/finding 相同，`added=[]`、`resolved=[]`，但 `refreshed=[main.o, helper.o]`、`reused=[]`；`P2-full.json` 一致。`P2-build.log` 同样无 gcc 命令；`P2-buildchecker/findings.json` 与 P1 相同，验证实际依赖关系没有因 Make 未重建而丢失。`personal-gate.json` 为 `passed=true`。

测试日志目录 `work/e89-241250071-tests-WtDsP00i`：定向测试 2 项通过、退出码 0；完整回归 9 项通过、退出码 0。

局限：本结论限定于本次单目录、小型显式 Make 输入与 GCC `-MM` 教学实现。缓存采取保守全目标刷新，未验证并行构建、多层目录、复杂宏展开、符号链接和最小化失效策略。
