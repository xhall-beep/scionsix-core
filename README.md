# SCION SIX Console

**Upgraded 2026-10-28.** SCION SIX was attempted twice and failed
twice. This repo now holds the honest merge of the two attempts into
one working core: `console.py` (verified, below), beside the original
Kivy prototype files (`main.py`, `logic/`, `buildozer.spec`), which
are superseded by it.

**Security note:** this upgrade removed `ori`, `ori-service`, and
`service.log` from the tree. The old `ori` script contained a
hardcoded GitHub credential; it was designed out of the rebuild and
never copied. The credential **remains in this repo's git history**
and must be considered compromised — revoking/rotating it (owner's
GitHub settings) is still required; removing the file from HEAD does
not purge history.

## What came from each repo

| Source | What it was | What survives here |
|---|---|---|
| **SCIONSIX-AI** | A stock Android/Gradle scaffold (`ai.scionsix.orchestrator`) with no feature code. Its one real artefact: `terminal_orchestrator.sh`, a Termux loop that builds and installs the APK on-device. | The **packaging route** (see below) and the product intent: an orchestrator that lives on the phone. No scaffold code is carried over — there was nothing in it to carry. |
| **scionsix-core** | A Kivy command console: type a command, the phone executes it, output streams back. The front-end idea was real; the orchestration half (`ori`, the "APEX 600" layer) was vaporous and contained a **hardcoded credential**. | The **console concept**: streamed command execution as the primary interface. The `ori` layer is **not** copied, read, or reused — its credential is compromised and the whole half is designed out. Orchestration here is real instead: the verified ApexYX bus. |

## What this build is

`console.py` (Python 3, standard library only, $0) has three layers:

1. **Streamed executor** — `run_streamed()` runs a shell command with
   stdout and stderr drained on separate reader threads, line by line as
   produced (not buffered-then-printed), capturing the real exit code
   and wall-clock duration.
2. **Safety layer** — an explicit blocklist checked *before* any process
   exists. A blocked command is refused with the rule named:
   `rm-recursive-force`, `mkfs-filesystem-format`, `dd-to-raw-device`,
   `power-control` (shutdown/reboot), `credential-file-access` (any
   touch of `.env`, `*credential*`, `*.pem`, `*.key`, key files,
   `.ssh/`…), `download-pipe-to-shell` (curl/wget piped to a shell),
   and `fork-bomb`. This is a guardrail for an agent-driven console,
   not a sandbox — it stops the known-catastrophic and
   known-credential shapes cold.
3. **Bus task mode** — on the verified ApexYX bus
   (the sibling ApexYX-Sovereign checkout's `mesh_bus/mesh_bus.py`, loaded
   directly; its exec tier is never invoked). `post_task()` safety-checks
   and posts a `cmd` row; `worker_once()` claims it (the bus's
   exactly-once handoff), executes it through the *same* streamed,
   safety-checked executor, posts the captured output as a sealed
   `result` row linked to the task, and closes the task. A blocked
   command that reaches the bus by another route is closed by the
   worker with the refusal as its stored result — never executed.
   `bus.verify()` walks the sha256 seal chain over all of it.

Bus data lives in `MESH_DIR` — by default a workspace-local `.mesh/`
inside this directory, never `~/.mesh`. The bus library is loaded from
a sibling checkout of the ApexYX-Sovereign repo (either
`apexyx-sovereign` or `ApexYX-Sovereign` capitalisation; override with
`APEX_BUS_PATH`).

## The vision build (2026-10-28)

The console above was the stated rebuild. The *envisioned* product —
per SCIONSIX-AI's own idea content — was a Six-Scion orchestrator
with a Naming Gate and an Agent Foundry. Those are now built, beside
the console, in the same style (stdlib only, fail-closed, refusals
that name their rule):

- **`scions.py`** — the six offices (Runner, Scout, Mason, Warden,
  Keeper, Herald), each chartered for its own kinds of work.
  `dispatch(work, command)` routes a unit of work to its owning
  scion and posts it to the bus; `work_once(scion_id)` claims only
  that office's rows (address + claim filter both enforced) and runs
  them through the console's streamed, blocklist-checked executor.
- **`naming_gate.py` + `name_registry.json`** — the Naming Gate as
  code. A proposed agent/product name is checked against the
  registry (seeded with the estate's real product/agent names and
  known external collisions) and rules NG-FORMAT / NG-COLLISION /
  NG-RESERVED / NG-GENERIC / NG-REGISTRY. It returns a pass or the
  specific violations; nothing registers without passing.
- **`foundry.py`** — the Agent Foundry. A definition from the
  template goes through the Gate; on a pass the agent is registered
  (registry entry + a bus announcement from the Keeper's office);
  on a failure the Foundry refuses, names the violations, and
  changes nothing.

Verify: `python3 test_vision.py` → 9/9 (roster partition, gate
accept/reject with named rules, Foundry end-to-end both ways, a
scion dispatch→claim→done round-trip on a temp bus). Full build
record: `BUILD-REPORT.md`.

## Usage

```sh
python3 console.py --cmd run  --text "echo hello; sleep 1; echo done"
python3 console.py --cmd task --text "echo hello from the bus"
python3 console.py --cmd verify
python3 console.py --cmd health
python3 console.py            # interactive: run / task / work / verify / health
python3 test_scion.py         # the verification suite (see TEST-OUTPUT.txt)
```

`--cmd run` exits with the command's real exit code (126 when blocked).

## Verification

`test_scion.py` proves: streamed arrival of 3 timed lines in order with
exit 0; a failing command's real non-zero exit and stderr; six blocked
patterns refused by name before execution (the `rm -rf` target verified
untouched afterwards); a full bus round-trip — post → claim → execute →
done, stored result containing the command's real output, seal chain
INTACT; a bus-injected blocked command refused by the worker; and a
no-secrets scan over the whole build directory. Verbatim output is in
`TEST-OUTPUT.txt`.

## Honest packaging note

The Android/Gradle APK and the on-device Termux build loop from
SCIONSIX-AI (`terminal_orchestrator.sh`) are the **phone-side packaging
step, not part of this verified core**. They are not rebuilt or verified
here. The Kivy shell from scionsix-core would wrap exactly the functions
in `console.py` (`run_streamed`, `post_task`, `worker_once`,
`verify_chain`, `bus_health`) — that wrapping, and an on-device build,
are future packaging work. What is claimed as done is the core: it
executes, streams, refuses, and orchestrates, with captured proof.
Nothing in this directory contains a secret, by construction and by
test.

## Latest verification

2026-10-28, in this repo, on the estate VM: `python3 test_scion.py`
→ **7/7 checks passed** (streamed execution, real exit/stderr capture,
six blocklist refusals, bus round-trip with seal chain INTACT,
bus-injected blocked command refused, no-secrets scan). One
portability fix ships with this upgrade: the bus library lookup now
accepts a sibling checkout named either `apexyx-sovereign` or
`ApexYX-Sovereign` (the canonical repo name).

## Continuous integration

CI is the **SCION SIX console CI** workflow (`.github/workflows/ci.yml`):
on every push it checks out this repo beside a sibling
`ApexYX-Sovereign` checkout (the layout `console.py` expects for the
bus library), compiles the Python sources, and runs the verification
suite (`python3 test_scion.py`).

The old **Build ORI SCION APK** workflow was retired on 2026-10-28. It
built an APK from the superseded Kivy prototype (`main.py`, via
Buildozer) and its runs fail — four of four on 2026-10-28, each dying
inside the Buildozer build with exit code 1. The prototype is not the
product anymore, so its build is not this repo's CI. APK packaging
lives in SCIONSIX-AI's Gradle pipeline, which passes.
