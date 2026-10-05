# 固定 MD/RD 样本

本目录将保存一份可独立构建的 C + GNU Make 项目，用于同时提供一个固定 MD
和一个固定 RD。

计划状态：

- `src/main.c` 实际读取 `include/common.h` 和 `include/config.h`。
- Makefile 的 `HEADERS` 只声明 `include/common.h` 和 `include/unused.h`。
- MD：`build/main.o -> include/config.h`。
- RD：`build/main.o -> include/unused.h`。

源码、Makefile 和 Dockerfile 由负责人在 `a08/e3-baseline` 分支提交。本文件只
记录已共同确认的样本设计，不构成实验结果。
