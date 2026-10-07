# C1 新增头文件缺失声明证据

本记录对应 `e3-c1` / `4b70cabad1be8f6e98ee90ed9c5803b7aa793253`，并以
`e3-c0` / `88ffce8aeaa9172fc724130d5796ad18ca1ab9e4` 为基线。C1 仅新增
`include/feature.h`，并让 `src/main.c` 读取 `FEATURE_VALUE`；Makefile 的
`HEADERS` 仍只声明 `common.h` 和 `config.h`。

`gcc -MM` 显示 `main.o` 实际读取 `include/feature.h`。C1 干净构建后程序输出
`12`。在独立的验证性修改中，仅把 `FEATURE_VALUE` 从 `2` 改为 `3`：普通增量
`make` 不重编译且程序仍输出 `12`；同一源码经 `make clean && make -j2` 后输出
`13`。这同时证明了遗漏声明及其漏重建后果。验证性修改已经恢复，不属于 C1 提交。

完整命令、关键原始输出和退出码见 [commands.txt](commands.txt)，结构化观察见
[observations.json](observations.json)。本次成功验证环境为 Ubuntu 20.04.6 WSL2。
