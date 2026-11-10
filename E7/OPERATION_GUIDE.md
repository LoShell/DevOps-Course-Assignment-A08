# A08 E7 操作指南

在 Ubuntu 云服务器原有的个人仓库 `/root/<学号>/buildchecker` 执行。沿用各自的 Git 本地作者和镜像标签。2 GiB 共享服务器上的构建和完整门禁依次执行。

## 1. 组长确认基线

从已经推送的共同分支选定完整 SHA，确认该提交的工作区干净，在自己的服务器目录执行第 3 节。记录服务单测数量、独立判定结果和八项门禁结果。基线通过后，把 SHA、指南和分工一起发给组员。

## 2. 组员建立个人分支

收到组长发布的 SHA 后执行。先确认工作区干净，`origin` 指向 A08 仓库。

```bash
git status --short
git remote -v
SID=$(git config --local user.name)
git config --local user.email
git fetch origin
read -r -p "组长发布的 E7 基线 SHA: " E7_BASE_SHA
git merge-base --is-ancestor "$E7_BASE_SHA" origin/a08/e7-validation &&
  git switch -c "a08/$SID/e7-validation" "$E7_BASE_SHA"
git rev-parse HEAD
```

确认 `SID` 是本人的数字学号，`HEAD` 与发布的 SHA 一致，再做基线验证。

## 3. 每轮构建与完整门禁

基线和个人改动后的验证各运行一次。个人轮先提交测试代码以固定源码版本。执行下方命令前确认 `git status --short` 为空。

```bash
SID=$(git config --local user.name)
IMAGE="course1027-buildchecker:$SID"
mkdir -p work
RUN=$(mktemp -d "work/e7-$SID-XXXXXXXX")
git rev-parse HEAD > "$RUN/source-commit.txt"
git status --porcelain > "$RUN/source-status.txt"
docker version > "$RUN/docker-version.txt"
printf '证据目录 %s\n' "$RUN"
```

随后执行自检、判定和构建。任何一步非零，先查日志再继续。

```bash
(
  set -eo pipefail
  python3 scripts/course.py doctor 2>&1 | tee "$RUN/doctor.log"
  python3 -m unittest discover -s tests/e7 -v 2>&1 | tee "$RUN/oracle.log"
  python3 scripts/course.py build --out "$RUN/build" 2>&1 | tee "$RUN/build-console.log"
  docker image inspect "$IMAGE" --format '{{.Id}}' > "$RUN/image-id.txt"
)
```

个人轮在完整门禁前执行定向测试。文件名以分工表为准。

```bash
(
  set -o pipefail
  docker run --rm --network none "$IMAGE" \
    pytest -q "tests/test_e7_${SID}.py" 2>&1 | tee "$RUN/personal-test.log"
)
```

基线轮在构建通过后直接执行完整门禁。个人轮确认定向测试通过后执行。

```bash
python3 scripts/course.py gate --out "$RUN/full"
GATE_EXIT=$?
printf '%s\n' "$GATE_EXIT" | tee "$RUN/gate-exit.txt"
cat "$RUN/full/gate/results.csv"
python3 -m json.tool "$RUN/full/gate/gate-result.json"
```

预期独立判定 6 项通过，门禁 8 项均为 `passed=true`、整体退出 0。按 [测试计划](TEST_PLAN.md) 抽查逐场景 `command.json`、日志、findings、trace 和 Make 数据库。失败时查看 `$RUN/full/driver/` 和对应 case，再使用新的运行目录重试。

## 4. 整理个人交付

1. 汇总新增测试的原有覆盖、输入、预期和实际。
2. 按 [个人记录说明](records/TEMPLATE.md) 填写报告、验收 CSV 和 [专项审阅](review/TEMPLATE.md)。分别列出基线和个人轮的源码 SHA、镜像 ID、日志及运行目录。
3. 独立归档两轮原始证据，下载后校验 SHA-256。参照 [提交检查表](SUBMISSION.md)。
4. 提交本人测试和记录，推送个人分支并向 `a08/e7-validation` 提 PR。组长审阅后汇总，并在合入全部个人改动的版本上再执行第 3 节的构建和完整门禁。

## 5. 组长完成 CI 与合并门禁

1. 共同分支集成验证通过后，提交阶段 PR 合入 `main`。确认 `main` 对应提交的 `e7-a-quality-gate` 成功，下载 artifact 并记录运行链接与 SHA。
2. 从该提交的 check runs 核对 `e7-a-quality-gate` 的实际 App ID，读取当前保护配置，核对必需检查、`strict=true` 和管理员约束。如需配置，以仓库的 [A 轨道保护模板](../course-support/ci/A-main-protection.json) 为参考，保留现有的其他保护条款。保存实际生效的快照。
3. 从此时的 `main` 建立独立演示分支 `a08/e7-gate-reject-demo`，将 [失败测试](../course-support/ci/rejection-demo/A/test_ci_reject_demo.py) 复制到 `services/buildchecker/tests/test_ci_reject_demo.py`，提交并向 `main` 提 PR。
4. 等待该 PR 检查因故意写错的断言失败，保存失败日志和 artifact。执行一次普通 `gh pr merge <PR号> --merge`，保存实际拒绝日志、退出码和 PR 的 `OPEN / BLOCKED` 状态。
5. 在同一 PR 用 [修复版测试](../course-support/ci/rejection-demo/A/fixed/test_ci_reject_demo.py) 覆盖失败测试，提交并推送。核对通过的检查对应 PR 最新提交，下载 artifact，再普通合并并保存 `MERGED`、`mergeCommit` 与 `mergedAt`。

用 [证据索引](validation/README.md) 汇总正常、失败和恢复三次运行。工作流的 artifact 保留 14 天，及时下载备份。
