"""Replay the tagged C1 -> C2 experiment using host Python, Git and Docker."""

import argparse
import contextlib
import datetime as dt
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import tempfile
import uuid


E3 = Path(__file__).resolve().parents[1]
REPO = E3.parent
FIXTURE = Path("E3/fixtures/incremental")
WORKDIR = "/tmp/a08-e3-incremental"
SOURCE_FILES = [
    "src/main.c", "include/common.h", "include/config.h", "include/feature.h"
]
ARTIFACT_FILES = ["build/main.o", "bin/demo"]
SHANGHAI = dt.timezone(dt.timedelta(hours=8))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(directory):
    return {
        p.relative_to(directory).as_posix(): digest(p)
        for p in sorted(directory.rglob("*")) if p.is_file()
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c1-ref", default="e3-c1")
    parser.add_argument("--c2-ref", default="e3-c2")
    parser.add_argument("--output", type=Path, help="New evidence directory; never overwritten")
    parser.add_argument("--image-tag", help="Local image tag for this run")
    parser.add_argument("--operator", default="script operator (identity not supplied)")
    args = parser.parse_args()
    started = dt.datetime.now(SHANGHAI)
    stamp = started.strftime("%Y%m%dT%H%M%S%f%z")
    output = (args.output or E3 / "evidence/c2" / stamp).resolve()
    if output.exists():
        parser.error(f"Evidence directory already exists: {output}")
    output.mkdir(parents=True, exist_ok=False)
    image_tag = args.image_tag or "a08-e3-c2:local-" + started.strftime("%Y%m%d-%H%M%S%f")
    container = "a08-e3-c2-" + uuid.uuid4().hex[:12]
    record = {
        "recorded_at": started.isoformat(),
        "operator": args.operator,
        "repository": "https://github.com/LoShell/DevOps-Course-Assignment-A08.git",
        "provenance": "REAL_BUILD_EXECUTION_NOT_A_DETECTOR_REPORT",
        "review_status": "pending_member_4_confirmation",
        "runner_sha256": digest(Path(__file__)),
        "runner_source_state": "Host working-tree script identified by SHA-256; fixture inputs are fixed Git commits",
        "host_python": sys.version,
        "container_working_directory": WORKDIR,
        "image_tag": image_tag,
        "commands": [], "assertions": [], "stages": {}, "status": "RUNNING",
    }
    transcript = output / "commands.txt"
    transcript.write_text("# C1 -> C2 real command transcript\n", encoding="utf-8")
    container_started = False
    tracked_before = None

    def run(argv, *, log_file=None, check=True):
        argv = [str(part) for part in argv]
        print("$ " + shlex.join(argv), flush=True)
        entry = {"argv": argv, "cwd": str(REPO), "exit_code": None, "output": ""}
        record["commands"].append(entry)
        header = (
            f"$ cwd: {REPO}\n$ argv: {json.dumps(argv, ensure_ascii=False)}\n"
            f"$ {shlex.join(argv)}\n"
        )
        # Persist output as it arrives, including long or failed Docker builds.
        with contextlib.ExitStack() as stack:
            streams = [stack.enter_context(transcript.open("a", encoding="utf-8"))]
            if log_file:
                streams.append(stack.enter_context((output / log_file).open("w", encoding="utf-8")))

            def emit(text):
                for stream in streams:
                    stream.write(text)
                    stream.flush()

            emit(header)
            lines = []
            try:
                with subprocess.Popen(
                    argv, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    encoding="utf-8", errors="replace",
                ) as process:
                    for line in process.stdout:
                        lines.append(line)
                        emit(line)
                    entry.update(exit_code=process.wait(), output="".join(lines))
            except OSError as exc:
                entry.update(output="".join(lines), error=str(exc))
                emit("error=" + str(exc) + "\n")
            emit(f"\nexit_code={entry['exit_code']}\n\n")
        if check and entry["exit_code"] != 0:
            raise RuntimeError(f"Command failed: {shlex.join(argv)}; {entry.get('error', entry['exit_code'])}")
        return entry

    def check(name, condition):
        record["assertions"].append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    def inside(argv):
        return run(["docker", "exec", "--workdir", WORKDIR, container, *argv])["output"]

    def snapshot():
        files = SOURCE_FILES + ARTIFACT_FILES
        hashes = inside(["sha256sum", *files])
        stats = inside(["stat", "--format=%n|%s|%y", *files])
        result = {}
        for line in hashes.splitlines():
            value, name = line.split("  ", 1)
            result[name] = {"sha256": value}
        for line in stats.splitlines():
            name, size, modified = line.split("|", 2)
            result[name].update(size_bytes=int(size), mtime=modified)
        check("snapshot contains every source and artifact", set(result) == set(files))
        return result

    def stage(name, build_output):
        result = {
            "build_output": build_output,
            "version_output": inside(["./bin/demo", "--version"]).strip(),
            "behavior_output": inside(["./bin/demo"]).strip(),
            "files": snapshot(),
            "makefile_sha256": inside(["sha256sum", "Makefile"]).split()[0],
        }
        record["stages"][name] = result
        check(name + " version", result["version_output"] == "demo 1.0.0")
        return result

    try:
        tracked_before = run(["git", "status", "--porcelain", "--untracked-files=no"])["output"]
        record["workspace_commit"] = run(["git", "rev-parse", "HEAD"])["output"].strip()
        record["host_git"] = run(["git", "--version"])["output"].strip()
        for label, ref in [("c1", args.c1_ref), ("c2", args.c2_ref)]:
            sha = run(["git", "rev-parse", "--verify", "--end-of-options", ref + "^{commit}"])["output"].strip()
            check(label + " resolves to full commit SHA", len(sha) == 40 and all(c in "0123456789abcdef" for c in sha))
            record[label] = {"ref": ref, "commit": sha}
            print(label.upper() + "_COMMIT=" + sha, flush=True)
        run(["git", "merge-base", "--is-ancestor", record["c1"]["commit"], record["c2"]["commit"]])
        changed = run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", record["c2"]["commit"]])["output"].splitlines()
        check("C2 commit changes only the incremental Makefile", changed == [(FIXTURE / "Makefile").as_posix()])
        with tempfile.TemporaryDirectory(prefix="a08-e3-c2-") as temp:
            temp = Path(temp)
            trees = {}
            for label in ["c1", "c2"]:
                archive = temp / (label + ".tar")
                # Git for Windows also applies checkout conversion to archives.
                # Export Git's LF bytes without changing the user's Git config.
                run(["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf", "archive", "--format=tar", "--output=" + str(archive), record[label]["commit"], FIXTURE.as_posix()])
                tree = temp / label
                tree.mkdir()
                with tarfile.open(archive) as source:
                    source.extractall(tree, filter="data")
                trees[label] = tree
                record[label]["fixture_sha256"] = manifest(tree / FIXTURE)
            before = record["c1"]["fixture_sha256"]
            after = record["c2"]["fixture_sha256"]
            check("C1 and C2 fixture file sets match", before.keys() == after.keys())
            check("Only Makefile bytes differ between C1 and C2", [p for p in before if before[p] != after[p]] == ["Makefile"])
            old = (trees["c1"] / FIXTURE / "Makefile").read_bytes()
            new = (trees["c2"] / FIXTURE / "Makefile").read_bytes()
            check("C2 contains exactly the MODE=7 option change", old.count(b"CPPFLAGS := -Iinclude\n") == 1 and new == old.replace(b"CPPFLAGS := -Iinclude\n", b"CPPFLAGS := -Iinclude -DMODE=7\n"))

            run(["docker", "version"], log_file="docker-version.txt")
            print("Building the tagged C2 Ubuntu 24.04 image...", flush=True)
            run(["docker", "build", "--progress=plain", "--file", trees["c2"] / FIXTURE / "Dockerfile", "--tag", image_tag, trees["c2"]], log_file="build.txt")
            inspection = run(["docker", "image", "inspect", image_tag])["output"]
            (output / "image-inspect.json").write_text(inspection, encoding="utf-8")
            image_id = json.loads(inspection)[0]["Id"]
            record["container_image_id"] = image_id
            check("Docker reports an actual image SHA-256", image_id.startswith("sha256:") and len(image_id) == 71)
            check("C2 image default version", run(["docker", "run", "--rm", "--network", "none", image_id])["output"].strip() == "demo 1.0.0")
            check("C2 image clean behavior", run(["docker", "run", "--rm", "--network", "none", image_id, "./bin/demo"])["output"].strip() == "19")
            run(["docker", "run", "--detach", "--network", "none", "--name", container, "--entrypoint", "sleep", image_id, "infinity"])
            container_started = True
            run(["docker", "exec", container, "mkdir", "-p", WORKDIR])
            run(["docker", "cp", str(trees["c1"] / FIXTURE) + "/.", container + ":" + WORKDIR])
            os_release = inside(["cat", "/etc/os-release"])
            os_fields = dict(line.split("=", 1) for line in os_release.splitlines() if "=" in line)
            environment = {
                "os": os_fields["PRETTY_NAME"].strip('"'),
                "os_version_id": os_fields["VERSION_ID"].strip('"'),
                "architecture": inside(["uname", "-m"]).strip(),
                "gcc": inside(["gcc", "--version"]).splitlines()[0],
                "make": inside(["make", "--version"]).splitlines()[0],
                "image_id": image_id,
            }
            record["environment"] = environment
            print("ENVIRONMENT=" + json.dumps(environment, ensure_ascii=False), flush=True)
            check("Container is Ubuntu 24.04", os_fields["ID"].strip('"') == "ubuntu" and environment["os_version_id"] == "24.04")
            record["configurations"] = {}
            for label, cppflags in [("c1", ["-Iinclude"]), ("c2", ["-Iinclude", "-DMODE=7"])]:
                basis = {
                    "environment": environment,
                    "cc": "gcc", "cppflags": cppflags,
                    "cflags": ["-Wall", "-Wextra", "-O2"],
                    "clean_build_command": "make clean && make -j2",
                }
                canonical = json.dumps(basis, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
                identifier = "e3-incremental-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
                record["configurations"][label] = {"configuration_id": identifier, "basis": basis}
            record["configuration_policy"] = {
                "algorithm": "e3-incremental- + first 16 hex characters of SHA-256 of basis JSON (sort_keys=True, ensure_ascii=True, separators=(',', ':')), UTF-8",
                "e2_same_configuration_compatible": False,
                "note": "Actual compile options differ, so configuration IDs differ. This E3 behavioral comparison must not be represented as an E2 same-configuration incremental request; team lead must resolve integration semantics. Historical C1 WSL evidence is unchanged.",
            }
            check("C1 and C2 configuration IDs differ", record["configurations"]["c1"]["configuration_id"] != record["configurations"]["c2"]["configuration_id"])

            print("Replaying C1 clean, C2 incremental and C2 clean builds...", flush=True)
            inside(["make", "clean"])
            baseline = stage("c1_clean", inside(["make", "-j2"]))
            check("C1 clean output 12", baseline["behavior_output"] == "12")
            check("C1 Makefile matches tagged bytes", baseline["makefile_sha256"] == before["Makefile"])
            check("C1 sources match tagged bytes", all(baseline["files"][p]["sha256"] == before[p] for p in SOURCE_FILES))
            run(["docker", "cp", trees["c2"] / FIXTURE / "Makefile", container + ":" + WORKDIR + "/Makefile"])
            record["c2_dry_run"] = inside(["make", "--always-make", "--dry-run"])
            check("C2 dry run includes MODE=7", "-DMODE=7" in record["c2_dry_run"])
            incremental = stage("c2_incremental", inside(["make", "-j2"]))
            check("C2 incremental output remains 12", incremental["behavior_output"] == "12")
            check("C2 incremental executes no compile or link command", "gcc" not in incremental["build_output"] and "Nothing to be done" in incremental["build_output"])
            check("C2 incremental preserves all source hashes and timestamps", all(incremental["files"][p] == baseline["files"][p] for p in SOURCE_FILES))
            check("C2 incremental preserves object and binary hashes and timestamps", all(incremental["files"][p] == baseline["files"][p] for p in ARTIFACT_FILES))
            check("C2 Makefile matches tagged bytes", incremental["makefile_sha256"] == after["Makefile"])
            inside(["make", "clean"])
            clean = stage("c2_clean", inside(["make", "-j2"]))
            check("C2 clean compiler executes MODE=7", "gcc -Iinclude -DMODE=7 -Wall -Wextra -O2 -c src/main.c -o build/main.o" in clean["build_output"])
            check("C2 clean output 19", clean["behavior_output"] == "19")
            check("C2 clean preserves all source hashes and timestamps", all(clean["files"][p] == baseline["files"][p] for p in SOURCE_FILES))
            check("C2 clean uses identical C2 Makefile", clean["makefile_sha256"] == incremental["makefile_sha256"])
            check("C2 clean changes object and binary hashes", all(clean["files"][p]["sha256"] != baseline["files"][p]["sha256"] for p in ARTIFACT_FILES))
            dependencies = inside(["gcc", "-MM", "-Iinclude", "-DMODE=7", "-MT", "build/main.o", "src/main.c"])
            make_database = inside(["make", "-pn"])
            declaration = next(line for line in make_database.splitlines() if line.startswith("build/main.o:"))
            record["dependencies"] = {"gcc_output": dependencies, "make_declaration": declaration}
            check("GCC still reads feature.h", "include/feature.h" in dependencies)
            check("Make still omits feature.h", "include/feature.h" not in declaration and "include/common.h" in declaration and "include/config.h" in declaration)
            check("Independent image source is still C2", run(["docker", "exec", container, "/workspace/E3/fixtures/incremental/bin/demo"])["output"].strip() == "19")
            check("Host exported fixture files unchanged", all(manifest(trees[label] / FIXTURE) == record[label]["fixture_sha256"] for label in ["c1", "c2"]))
        record["status"] = "PASS"
    except (Exception, KeyboardInterrupt) as exc:
        record.update(status="FAIL", error=str(exc))
    finally:
        if container_started:
            try:
                cleanup = run(["docker", "rm", "--force", container], check=False)
                check("Temporary experiment container removed", cleanup["exit_code"] == 0)
            except Exception as exc:
                record.update(status="FAIL", cleanup_error=str(exc))
        if tracked_before is not None:
            try:
                current = run(["git", "status", "--porcelain", "--untracked-files=no"])["output"]
                check("Tracked working tree status unchanged", current == tracked_before)
            except Exception as exc:
                record.update(status="FAIL", integrity_error=str(exc))
        record["finished_at"] = dt.datetime.now(SHANGHAI).isoformat()
        (output / "observations.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        passed = sum(item["passed"] for item in record["assertions"])
        configs = record.get("configurations", {})
        stages = record["stages"]
        evidence_links = "、".join(
            f"[{name}]({name})" for name in
            ["commands.txt", "observations.json", "build.txt", "docker-version.txt", "image-inspect.json"]
            if (output / name).exists()
        )
        readme = f"""# C2 编译命令变化证据

- 执行时间：{record['recorded_at']}。
- 执行者：{args.operator}；人工 oracle 状态：待成员 4 确认。
- 仓库：{record['repository']}。
- C1：`{record.get('c1', {}).get('commit', '未解析')}`（输入 `{args.c1_ref}`）。
- C2：`{record.get('c2', {}).get('commit', '未解析')}`（输入 `{args.c2_ref}`）。
- 镜像：`{record.get('container_image_id', '未生成')}`；标签 `{image_tag}`。
- 实验工作目录：`{WORKDIR}`；镜像项目目录：`/workspace/E3/fixtures/incremental`。
- 结果：**{record['status']}**；{passed}/{len(record['assertions'])} 项断言通过。

| 阶段 | 实测行为输出 |
|---|---|
| C1 干净构建 | `{stages.get('c1_clean', {}).get('behavior_output', '未执行')}` |
| 仅替换 C2 Makefile，普通增量构建 | `{stages.get('c2_incremental', {}).get('behavior_output', '未执行')}` |
| 同一 C2 源码，干净构建 | `{stages.get('c2_clean', {}).get('behavior_output', '未执行')}` |

复现流程设计为：先从 Git 导出固定版本，检查 C2 独立提交仅修改 Makefile，并逐字节验证
`CPPFLAGS := -Iinclude` 只增加 `-DMODE=7`。在同一容器中先构建 C1，随后
只复制 C2 Makefile，不替换或触碰源码、头文件和已有产物，再执行 `make -j2`。
随后在同一工作目录执行 `make clean` 和 `make -j2`。实际执行到的阶段以
上方实测表格、status 和命令记录为准；失败时不会把未执行阶段当作成功结果。

本次实际生成的证据：{evidence_links}。
已执行命令的原始合并输出和退出码见 commands.txt。已采集的工具版本、阶段快照
和逐项断言见 observations.json；进入相应阶段后才会生成 Docker 构建日志、
镜像元数据及源码/产物哈希和修改时间。复现脚本使用宿主机 Python，不增加容器内依赖。

## 配置编号与契约限制

- 本次 C1 配置：`{configs.get('c1', {}).get('configuration_id', '未生成')}`。
- 本次 C2 配置：`{configs.get('c2', {}).get('configuration_id', '未生成')}`。
- 编号依据为实测 Ubuntu、GCC、Make、架构、镜像 ID 及编译选项；规范化 JSON
  和哈希算法在成功采集环境后保存在 observations.json 的 configurations/configuration_policy。
- C1 的重新验证仅使用本次容器，不覆盖成员 3 的 WSL 历史记录。
- 因编译选项不同，两个配置编号不同。本记录用于 E3 行为对比，不能直接声称
  满足 E2 同配置增量请求；后续由组长统一对接策略。

## 结论边界

{('C2 增量构建保留 C1 产物，而干净构建应用 MODE=7 后输出 19，证明编译命令变化未触发普通 Make 重建。feature.h 仍被 GCC 列为读取依赖，Make 仍未声明它，因此 C1 的既有 MD 保持不变；命令变化不新增头文件 MD。本记录不是 BuildChecker/EChecker 自动检测报告。' if record['status'] == 'PASS' else '本次未通过，不作为成功验证证据。失败原因：' + record.get('error', record.get('cleanup_error', record.get('integrity_error', '见逐项断言'))))}

脚本仅在已创建临时实验容器时执行删除，结果以收尾命令和断言为准；已生成的
镜像保留供复核。重复实验必须使用新的证据目录。
"""
        (output / "README.md").write_text(readme, encoding="utf-8")
    print(f"{record['status']}\nEVIDENCE_DIR={output}\nASSERTIONS={passed}/{len(record['assertions'])}")
    if record["status"] != "PASS":
        print(record.get("error", record.get("cleanup_error", record.get("integrity_error", "See observations.json"))))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
