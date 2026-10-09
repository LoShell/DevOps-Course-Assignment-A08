# E3 C1 Missing Header Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and document the C1 revision that reads `include/feature.h` without declaring it in the incremental sample Makefile.

**Architecture:** Keep the C0 Makefile dependency declaration unchanged and make the smallest source-level change: add one project header and consume its constant in `src/main.c`. Pin source state with `e3-c1`; keep mutation-based stale-build proof in an isolated evidence copy so it does not alter C1.

**Tech Stack:** C, GNU Make, GCC, Docker/Ubuntu 24.04, Git, JSON, Markdown.

## Global Constraints

- Start C1 from tag `e3-c0` (`88ffce8aeaa9172fc724130d5796ad18ca1ab9e4`).
- C1 changes only the new header and necessary source inclusion/use; `E3/fixtures/incremental/Makefile` remains byte-for-byte C0.
- C1 clean build must print `12`; an isolated `feature.h: 2 -> 3` mutation must leave incremental output at `12` and make clean output `13`.
- Record real SHA, environment, commands, exit codes, outputs, and manual conclusion. Do not commit build products or container images.
- Do not introduce the C2 `MODE` compiler-option change.

---

### Task 1: Establish the executable C1 contract

**Files:**
- Create: `E3/fixtures/incremental/include/feature.h`
- Modify: `E3/fixtures/incremental/src/main.c`
- Test: Docker build and runtime commands from `E3/fixtures/incremental/Dockerfile`

**Interfaces:**
- Consumes: `COMMON_VALUE`, `CONFIG_VALUE`, and C0 Makefile `HEADERS` declaration.
- Produces: `FEATURE_VALUE` equal to `2`, included by `src/main.c`; C1 program behavior equal to `6 + 4 + 2 + MODE`.

- [ ] **Step 1: Run the C0 build/behavior baseline in the Ubuntu container**

Run: `docker build -f E3/fixtures/incremental/Dockerfile -t a08-e3-c1-baseline .` followed by `docker run --rm a08-e3-c1-baseline ./bin/demo`

Expected: exit code `0` and output `10`.

- [ ] **Step 2: Create the failing C1 behavior probe**

Run the pre-change container command expecting C1 behavior: `docker run --rm a08-e3-c1-baseline ./bin/demo`.

Expected: it returns `10`, not the C1-required `12`; this is the red observation before C1 source changes.

- [ ] **Step 3: Add the minimal C1 source changes**

Create `E3/fixtures/incremental/include/feature.h`:

```c
#ifndef DEMO_FEATURE_H
#define DEMO_FEATURE_H

#define FEATURE_VALUE 2

#endif
```

In `src/main.c`, add `#include "feature.h"` after `#include "config.h"` and change the final expression to:

```c
printf("%d\\n", COMMON_VALUE + CONFIG_VALUE + FEATURE_VALUE + MODE);
```

Do not modify `Makefile`; `feature.h` must not occur in `HEADERS`.

- [ ] **Step 4: Run the C1 clean-build and behavior checks**

Run: `docker build -f E3/fixtures/incremental/Dockerfile -t a08-e3-c1 .`, `docker run --rm a08-e3-c1`, and `docker run --rm a08-e3-c1 ./bin/demo`.

Expected: exit code `0`; outputs `demo 1.0.0` and `12`.

- [ ] **Step 5: Commit and tag the C1 source state**

Run: `git add E3/fixtures/incremental/include/feature.h E3/fixtures/incremental/src/main.c && git commit -m "feat(e3): add C1 missing feature header scenario"`, then create annotated tag `e3-c1` on that commit.

Expected: one source-only C1 commit and tag, both resolving to the same source commit.

### Task 2: Capture reproducible C1 oracle and stale-build evidence

**Files:**
- Create: `E3/oracle/incremental.expected.json`
- Create: `E3/evidence/c1/<timestamp>/commands.txt`
- Create: `E3/evidence/c1/<timestamp>/observations.json`
- Create: `E3/evidence/c1/<timestamp>/README.md`
- Modify: `E3/CONTRIBUTIONS.md`
- Test: evidence commands replayed in an isolated C1 source archive/container.

**Interfaces:**
- Consumes: tagged C1 source SHA and C0 SHA, C1 Docker image, and compiler dependency output.
- Produces: one `MISSING` expectation for `build/main.o -> include/feature.h`, plus command-level proof that stale incremental behavior differs from a clean rebuild.

- [ ] **Step 1: Create a C1-only temporary copy and record the clean build**

Export the `e3-c1` tree to a unique temporary directory, run `make clean && make -j2`, `./bin/demo --version`, `./bin/demo`, and `gcc -Iinclude -MM src/main.c` inside the Ubuntu 24.04 container.

Expected: outputs `demo 1.0.0`, `12`, and a dependency list containing `include/feature.h`; all commands exit `0`.

- [ ] **Step 2: Create the stale-build proof in that temporary copy**

Change only `#define FEATURE_VALUE 2` to `#define FEATURE_VALUE 3`, run `make -j2` and `./bin/demo`; then run `make clean && make -j2` and `./bin/demo`.

Expected: ordinary make does not recompile `build/main.o` and behavior remains `12`; clean rebuild behavior is `13`.

- [ ] **Step 3: Write the human oracle**

Store actual repository URL, C0 SHA, C1 SHA, image/workdir/configuration identifier, C1 behavior, and one finding:

```json
{"type":"MISSING","target":"build/main.o","dependency":"include/feature.h"}
```

State that the source include/compiler dependency output proves actual reading while unchanged `HEADERS` proves missing declaration.

- [ ] **Step 4: Write raw evidence metadata and readable conclusion**

Preserve exact commands, exit codes, raw key output, actual timestamps and source SHA. Explain the isolated mutation, its ordinary-build result, its clean-build result, and why the mutation is not part of C1.

- [ ] **Step 5: Update the member 3 contribution row and commit the evidence/oracle**

Replace member 3 placeholders with the C1 source commit, files, and evidence path. Commit only member-3 oracle/evidence/contribution files.

### Task 3: Final compliance verification

**Files:**
- Verify: `E3/fixtures/incremental/Makefile`
- Verify: `E3/fixtures/incremental/src/main.c`
- Verify: `E3/fixtures/incremental/include/feature.h`
- Verify: `E3/oracle/incremental.expected.json`
- Verify: `E3/evidence/c1/`
- Verify: `E3/CONTRIBUTIONS.md`

**Interfaces:**
- Consumes: complete tagged C1 source and evidence commit.
- Produces: evidence-backed confirmation of the member 3 deliverables and a list of remaining handoff work.

- [ ] **Step 1: Verify the Makefile did not change from `e3-c0`**

Run: `git diff e3-c0 e3-c1 -- E3/fixtures/incremental/Makefile`.

Expected: no output.

- [ ] **Step 2: Verify source/tag identity and clean C1 behavior**

Run: `git rev-parse e3-c1^{}` and rebuild/run the image from the tagged tree.

Expected: tag resolves to the recorded source commit; behavior output is `12`.

- [ ] **Step 3: Validate traceability and repository hygiene**

Run: inspect oracle/evidence values, `git status --short`, and search changed files for `feature.h`, `MODE=7`, `build/`, and `bin/`.

Expected: C1 identity and evidence values agree; no C2 compiler-mode change or tracked generated products; worktree is clean after committing.
