# 固定 MD/RD 样本（成员 2）

此目录是独立故障样例，不修改 `fixtures/incremental/` 的 C0/C1/C2。
`src/main.c` 使用 common.h 和 config.h；Makefile 的 HEADERS 故意只声明
common.h 和 unused.h。因此 build/main.o 缺少 include/config.h（MD），
并多声明 include/unused.h（RD）。范围仅限当前配置下的项目头文件。

## 一键复现

在仓库根目录、Linux 环境中执行：

```sh
bash E3/scripts/run-md-rd.sh
```

需要 Python 3.8+、GCC、GNU Make。脚本在新的临时目录复制样例，测试后清理
临时副本，不修改源码。每次产生新的
`E3/evidence/md-rd/<UTC时间>/`，包含 commands.txt 和 observations.json。
失败返回非零退出码并保存已有记录。运行证据含工具版本、命令、退出码、断言、
文件 SHA-256 和已有基础提交。基础提交与样例版本分别记录。

## 手工复现

先复制本目录到自己的独立工作目录，再在副本中执行：

1. `make clean && make -j2`，`./bin/demo --version` 应为 demo 1.0.0，
   `./bin/demo` 应为 10。
2. `gcc -MM -Iinclude -MT build/main.o src/main.c`：项目头文件包含
   common.h、config.h，不含 unused.h；`make -pn` 可核对 Make 声明。
3. 等至少一秒，仅把 config.h 的 CONFIG_VALUE 从 4 改为 5。
   执行 `make -j2` 和 `./bin/demo`：对象文件不重建，仍输出 10。
4. `make clean && make -j2` 后运行：输出 11，证明相同源码的增量结果过时。
5. 等至少一秒，仅修改 unused.h 的注释。执行 `make -j2`：出现
   `-c src/main.c -o build/main.o` 编译命令，运行结果仍为 11。

步骤 3 和 5 不可先 clean。每条命令后记录退出码。脚本会检查时间戳，避免
头文件不够新导致错误结论。unused.h 必须存在，否则 make 会先报缺文件错误。

## 容器复现（需 Docker 服务可用）

从仓库根目录执行：

```sh
docker build -f E3/fixtures/md-rd/Dockerfile -t a08-e3-md-rd .
docker run --rm a08-e3-md-rd
docker run --rm a08-e3-md-rd ./bin/demo
# 一键测试并把证据保存到宿主机已有的 evidence/md-rd 目录
mkdir -p E3/evidence/md-rd
docker run --rm -v "$(pwd)/E3/evidence/md-rd:/workspace/E3/evidence/md-rd" a08-e3-md-rd bash /workspace/E3/scripts/run-md-rd.sh
```

Dockerfile 使用 Ubuntu 24.04。以上容器路径与本样例一致；容器构建是否已验证
以 evidence/md-rd/README.md 为准，不以 Dockerfile 存在作为运行成功证据。

## 标准答案与提交边界

`../../oracle/md-rd.expected.json` 是 AI 辅助起草、成员 2 已于 2026-10-06 审阅确认通过的 oracle，
不是 BuildChecker 输出。样例提交 SHA 为 `8a9cfc46d854e697fd397c1f6c579014e219144b`。
团队 configuration_id 暂留 null，按团队统一配置约定补齐。
测试阶段 CONFIG_VALUE=5 的变更仅发生在临时副本，交付样例始终为 4。
原始日志用 .txt 保存，避免仓库 *.log 忽略规则漏交证据。

容器镜像仅复制本样例、复现脚本和 oracle，由 Dockerfile.dockerignore 限制构建上下文，
不复制 .git 或其他实验。脚本可通过 --base-commit 传入已有基础提交，通过 --image-id
传入 docker image inspect 返回的真实镜像 ID。
例如容器测试命令末尾追加 `--base-commit <已有基础SHA> --image-id <实际镜像ID>`。
