"""Run a live or fresh R10 arm with handshake, deadline, and preserved logs."""
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

p = argparse.ArgumentParser()
p.add_argument("mode", choices=("live", "fresh"))
p.add_argument("probe", type=Path)
p.add_argument("project_dll", type=Path)
p.add_argument("seed", type=Path)
p.add_argument("checkpoint", type=Path)
p.add_argument("output", type=Path)
p.add_argument("--gameplay-source", type=Path)
p.add_argument("--timeout", type=float, default=900)
a = p.parse_args()
probe, dll, seed = a.probe.resolve(strict=True), a.project_dll.resolve(strict=True), a.seed.resolve(strict=True)
checkpoint, output = a.checkpoint.resolve(), a.output.resolve()
if output.exists(): p.error("output must be new")
if a.mode == "live" and not a.gameplay_source: p.error("live mode requires --gameplay-source")
output.mkdir(parents=True)
probe_out = output / "probe"
cmd = ["dotnet", str(probe), a.mode, str(dll), str(seed), str(checkpoint), str(probe_out)]
rec = {"mode": a.mode, "command": cmd, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "timeout_seconds": a.timeout, "probe_sha256": sha(probe), "application_sha256": sha(dll), "timed_out": False}
start = time.monotonic()
with (output / "stdout.log").open("wb") as so, (output / "stderr.log").open("wb") as se:
    proc = subprocess.Popen(cmd, stdout=so, stderr=se, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    rec["pid"] = proc.pid
    if a.mode == "live":
        ready = probe_out / "ready.json"
        deadline = start + min(a.timeout * 0.6, 420)
        while not ready.exists() and proc.poll() is None and time.monotonic() < deadline:
            time.sleep(0.1)
        if ready.exists() and proc.poll() is None:
            src = a.gameplay_source.resolve(strict=True)
            old = src.read_text(encoding="utf-8-sig")
            old_literal = "static member BrickReward = 100"
            new_literal = "static member BrickReward = 200"
            if old.count(old_literal) != 1 or old.count(new_literal) != 0:
                rec["edit_error"] = "reward-100 source occurrence mismatch"
                proc.terminate()
            else:
                (output / "Gameplay.before.fs").write_text(old, encoding="utf-8", newline="")
                src.write_text(old.replace(old_literal, new_literal), encoding="utf-8", newline="")
                new = src.read_text(encoding="utf-8")
                (output / "Gameplay.after.fs").write_text(new, encoding="utf-8", newline="")
                edit = {"old_sha256": sha(output / "Gameplay.before.fs"), "new_sha256": sha(src),
                        "changed_occurrences": 1, "ready": json.loads(ready.read_text())}
                (output / "edit.json").write_text(json.dumps(edit, indent=2) + "\n")
                (probe_out / "go.signal").write_text(json.dumps(edit) + "\n")
        elif proc.poll() is None:
            rec["edit_error"] = "checkpoint-ready timeout"
            proc.terminate()
    try:
        remaining = max(1, a.timeout - (time.monotonic() - start))
        rec["exit_code"] = proc.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        rec["timed_out"] = True
        if os.name == "nt": subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=20)
        else: proc.kill()
        rec["exit_code"] = proc.wait(timeout=20)
rec["elapsed_seconds"] = time.monotonic() - start
(output / "process.json").write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
raise SystemExit(0 if rec.get("exit_code") == 0 and not rec["timed_out"] and "edit_error" not in rec else 1)
