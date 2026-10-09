"""Reproduce MD/RD in a disposable copy; never run Git or change source fixtures."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import tempfile
import time

E3 = Path(__file__).resolve().parents[1]
SOURCE = E3 / "fixtures/md-rd"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New evidence directory (must not exist)")
    parser.add_argument("--base-commit", help="Existing base SHA; not the uncommitted sample SHA")
    parser.add_argument("--image-id", default="none; local Linux execution", help="Actual Docker image ID when running in a container")
    args = parser.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = args.output or E3 / "evidence/md-rd" / stamp
    output.mkdir(parents=True, exist_ok=False)
    files = sorted(p for p in SOURCE.rglob("*") if p.is_file() and not any(x in {"build", "bin"} for x in p.relative_to(SOURCE).parts))
    manifest = {str(p.relative_to(E3)): digest(p) for p in files}
    for p in [Path(__file__), E3 / "scripts/run-md-rd.sh", E3 / "oracle/md-rd.expected.json"]:
        manifest[str(p.relative_to(E3))] = digest(p)
    record = {"timestamp_utc": stamp, "executor": "Codex local execution on behalf of member 2; human review pending", "source_state": "uncommitted working tree; hashes identify tested files", "platform": platform.platform(), "architecture": platform.machine(), "commands": [], "assertions": [], "source_sha256": manifest, "status": "RUNNING"}
    # Read existing metadata only. No Git commands, commits or index changes.
    gitdir = E3.parent / ".git"
    head = (gitdir / "HEAD").read_text().strip() if (gitdir / "HEAD").exists() else "unavailable (no Git metadata in image)"
    ref = gitdir / head[5:] if head.startswith("ref: ") else None
    record["base_commit"] = args.base_commit or (ref.read_text().strip() if ref and ref.exists() else (head if ref is None else "unresolved"))
    record["container_image_id"] = args.image_id
    transcript = []

    def run(argv, cwd):
        result = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"PATH": os.defpath, "LANG": "C", "LC_ALL": "C"})
        entry = {"argv": argv, "cwd": str(cwd), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        record["commands"].append(entry)
        transcript.append(f"$ cd {shlex.quote(str(cwd))}\n$ {shlex.join(argv)}\n{result.stdout}{result.stderr}\nexit_code={result.returncode}\n")
        if result.returncode:
            raise RuntimeError(f"Command failed: {shlex.join(argv)}")
        return result.stdout

    def check(name, condition):
        record["assertions"].append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    def edit_later(path, old, new, obj):
        # Wait past the object's timestamp, avoiding coarse filesystem timestamps.
        time.sleep(max(0, obj.stat().st_mtime + 1.1 - time.time()))
        text = path.read_text()
        check("edit token exists: " + old, old in text)
        path.write_text(text.replace(old, new))
        check("edited header is newer than object", path.stat().st_mtime_ns > obj.stat().st_mtime_ns)
        record.setdefault("edits", []).append({"file": str(path.name), "before": old, "after": new})
        transcript.append(f"EDIT {path.name}: {old!r} -> {new!r}\n")

    try:
        for command in [["gcc", "--version"], ["make", "--version"], ["python3", "--version"], ["uname", "-a"], ["cat", "/etc/os-release"]]:
            run(command, E3)
        environment = {"platform": record["platform"], "gcc": record["commands"][0]["stdout"], "make": record["commands"][1]["stdout"], "flags": "-Iinclude -Wall -Wextra -O2", "image": args.image_id}
        record["local_configuration_id"] = "local-md-rd-" + hashlib.sha256(json.dumps(environment, sort_keys=True).encode()).hexdigest()[:16]
        record["configuration_note"] = "Local evidence identifier only; team configuration_id pending confirmation."
        with tempfile.TemporaryDirectory(prefix="a08-md-rd-") as tmp:
            work = Path(tmp) / "sample"
            shutil.copytree(SOURCE, work, ignore=shutil.ignore_patterns("build", "bin"))
            record["temporary_workdir"] = str(work)
            run(["make", "clean"], work)
            run(["make", "-j2"], work)
            check("version", run(["./bin/demo", "--version"], work).strip() == "demo 1.0.0")
            check("initial output 10", run(["./bin/demo"], work).strip() == "10")
            dependencies = run(["gcc", "-MM", "-Iinclude", "-MT", "build/main.o", "src/main.c"], work)
            check("compiler dependencies", "include/config.h" in dependencies and "include/common.h" in dependencies and "include/unused.h" not in dependencies)
            run(["make", "-pn"], work)
            obj = work / "build/main.o"
            before = (obj.stat().st_mtime_ns, digest(obj))
            edit_later(work / "include/config.h", "CONFIG_VALUE 4", "CONFIG_VALUE 5", obj)
            run(["make", "-j2"], work)
            check("MD object unchanged", before == (obj.stat().st_mtime_ns, digest(obj)))
            check("MD incremental output 10", run(["./bin/demo"], work).strip() == "10")
            run(["make", "clean"], work)
            run(["make", "-j2"], work)
            check("MD clean output 11", run(["./bin/demo"], work).strip() == "11")
            before = obj.stat().st_mtime_ns
            edit_later(work / "include/unused.h", "/* Deliberately", "/* Edited comment. Deliberately", obj)
            build = run(["make", "-j2"], work)
            check("RD compile command executed", "-c src/main.c -o build/main.o" in build)
            check("RD object rebuilt", obj.stat().st_mtime_ns > before)
            check("RD output unchanged 11", run(["./bin/demo"], work).strip() == "11")
        check("source fixture unchanged", all(digest(E3 / p) == h for p, h in manifest.items()))
        record["status"] = "PASS"
    except Exception as exc:
        record["status"] = "FAIL"
        record["error"] = str(exc)
    finally:
        (output / "observations.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        (output / "commands.txt").write_text("\n".join(transcript))
    print(f"{record['status']}\nEVIDENCE_DIR={output}")
    if record["status"] != "PASS":
        print(record.get("error", "unknown error"))
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
