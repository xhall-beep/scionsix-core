# BUILD REPORT — SCION SIX vision build (Six-Scion orchestrator + Naming Gate + Agent Foundry)

**Built:** 2026-10-28 (owner directive: "Greatly improve repos. Build
what's envisioned rather than what's stated.")
**Where:** `scionsix-core` (primary), synced to `SCIONSIX-AI`.
**Not done:** no GitHub push, no `.github/workflows` changes, nothing
deleted, $0 spent, Python 3 stdlib only, zero new dependencies.

---

## 1. The vision, per the docs

What the sources actually say:

- **audit-cluster-a.md §5–§6** (goal `every-failed-app-rebuilt-
  fully-functional`): SCIONSIX-AI was meant to be a native Android
  **orchestrator** app (`ai.scionsix.orchestrator`); scionsix-core a
  "ORI SCION Sovereign Node" console backed by an "APEX 600"
  orchestration layer that never existed as working code.
- **The rebuild program's audit summary** (estate log, 2026-10-28)
  records SCIONSIX-AI as *"the idea CONTENT source: Six-Scion
  orchestrator + Naming Gate + Agent Foundry"* — the three envisioned
  pieces. The merged console build (Q4) delivered none of the three:
  it built the executor, the safety layer, and a generic bus worker.
- **In-repo taxonomy:** `segment2.sh` ("SCIONSIX CONTROL PLANE")
  decomposes work into read-only queries (battery / location /
  network / sms / call / whoami / file) and change actions (update /
  install / uninstall / exec); `console.py` added streamed execution,
  seal-chain verification, and bus tasks. The six scion charters are
  that taxonomy, grouped.
- **Governance pattern:** sovereign-vault's `policy.py`/`policy.json`
  is the estate's rules-as-code canon on disk — named rules
  (SV-*), fail-closed default, every refusal names its rule. The
  Naming Gate is built in exactly that shape (NG-*).

### Two honest gaps in the sources (read this before the code)

1. **No standalone "Naming Gate canon" file exists in any local
   copy.** The audit summary says sovereign-vault "holds the Naming
   Gate canon", but the local sovereign-vault contains only its six
   original configs plus the Reech concierge code — no naming rules,
   no name registry. Exhaustive search (both SCION repos, the vault,
   both audits, the rebuilds, the capability stack, full-workspace
   text search) found the *concept* attested only in that one audit
   line. So the gate below implements the vault's governance
   *pattern* (named rules, fail-closed) with name rules derived from
   the estate's own on-disk naming practice, and its registry is
   seeded from names verifiably in use on disk. If the owner has a
   fuller canon elsewhere, the rules live in one small module and
   can be re-cut to match it.
2. **The six scions are never named in any doc.** The docs name
   their *work* (above), not the six. The roster names below are
   therefore defined by this build as the founding offices and are
   registered in the registry as grandfathered entries; dispatch and
   claiming key off work kinds and scion ids, so renaming an office
   later is a registry edit, not a code change.

### Flagged anomaly (for the parent agent)

During research, one search result listed a set of files under
`ApexYX-Sovereign/assets/PyCode/` (including a supposed
"naming-gate" file) that **do not exist on disk** — verified twice
by direct listing and a workspace-wide find. No such directory
exists anywhere under `~/workspace`. Those paths were treated as
phantom and were NOT followed or used. The only genuine attestation
of the Naming Gate concept is the audit line quoted above.

---

## 2. What was built

### `scions.py` — the Six-Scion orchestrator

Six offices, each chartered for its own kinds of work; the 13
chartered kinds are partitioned (each kind has exactly one owner —
asserted by test):

| # | Scion | Node | Chartered work kinds | Mandate |
|---|-------|------|----------------------|---------|
| I | Runner | `scion-runner` | cmd, exec | General command execution |
| II | Scout | `scion-scout` | recon, scan | Read-only discovery queries |
| III | Mason | `scion-mason` | build, install, update | Build / package / system work |
| IV | Warden | `scion-warden` | verify, audit | Seal-chain verification, health, safety audits |
| V | Keeper | `scion-keeper` | registry, state | Registry upkeep, state, registrations |
| VI | Herald | `scion-herald` | announce, notify | Announcements and reports |

- `dispatch(work, command)` — the orchestrator: routes by work kind
  to the owning scion, runs the console's blocklist check BEFORE
  posting (blocked ⇒ refused, never posted), then posts a bus row of
  kind `scion-task`, tgt = scion id, text = JSON envelope
  `{"work", "command", "via"}`. An unowned work kind is refused —
  no generic queue.
- `dispatch_to(scion_id, work, command)` — refuses work outside the
  named scion's charter.
- `work_once(scion_id)` — claim filter enforced twice: the row must
  be addressed to this scion AND its work kind must be inside the
  scion's charter; anything else is left pending for its owner.
  Claiming is the bus's exactly-once claim; execution is the
  console's same streamed, safety-checked executor; output returns
  as a sealed `result` row and the task is closed. A blocklisted
  command injected onto the bus by another tool is closed with the
  refusal as its result — never executed (the console's rule, kept).
- `pending()` / `roster()` — queue view and the six offices.

### `naming_gate.py` — the Naming Gate, enforced as code

`check_name(name, kind)` returns a pass or the specific violations,
each naming its rule:

- **NG-REGISTRY** — registry file missing ⇒ fail closed (collisions
  cannot be checked, so nothing passes).
- **NG-FORMAT** — 3–40 chars, letters/digits/spaces/hyphens,
  starting with a letter.
- **NG-COLLISION** — identical (after normalization) to a registered
  name, or sharing a contained word-set with one in either
  direction ("hook forge" collides with HookForge; "Dark Vault"
  would collide with Dark Vault Bundle).
- **NG-RESERVED** — contains a reserved root (scion, sovereign,
  apexyx, ori): those lines' names belong to their registered
  entries; new ones are the owner's word, not the gate's.
- **NG-GENERIC** — a bare category word (Agent, Bot, Orchestrator,
  …) is not a name.

The gate is a pure check: it registers nothing and writes nothing.

### `name_registry.json` — the registry

40 entries, seeded from on-disk estate records: SCION SIX, the six
founding offices, the estate agents (Weave, Apex, Acore, Argon,
Reech), and the product names from the storefront sku-map
(HookForge … Pedal Compendium), all status `approved`; plus
"Void and Vessel" as status `taken` (the US Class-21 registration
that is NOT the owner's). Grandfathered entries that predate the
gate are marked by their `origin`. The Foundry appends; no code
path edits or removes an entry.

### `foundry.py` — the Agent Foundry

- `new_definition(name, role, work_kinds)` fills the TEMPLATE.
- `forge(definition, registry_path, mesh_dir_arg)`:
  1. **Template check (FD-TEMPLATE)** — a name, a stated role, and at
     least one chartered work kind are required, and every kind must
     be owned by a scion office (the Foundry mints no agents for
     unowned work).
  2. **Naming Gate** — a failing name is refused with the gate's
     named violations.
  3. **Register + announce (pass only)** — the registry gains an
     `approved` entry (origin `foundry`, role and work kinds
     recorded, bus node `agent-<slug>`), and a bus row of kind
     `announce` is posted from the Keeper's office (registry work is
     Keeper's charter) so the estate can see the new agent exists.
  On any failure: the registry file is byte-identical afterwards
  and nothing is posted — proven by test.

### `test_vision.py` — hermetic suite for the three pieces

Temp bus + temp registry throughout; the shipped registry is only
read. 9 checks (evidence in §4).

### README.md (scionsix-core only)

Gained a "vision build" section describing the three modules and
how to verify them.

---

## 3. File list

**New in scionsix-core** (all synced to SCIONSIX-AI, md5-identical):

| File | Bytes | Purpose |
|------|------:|---------|
| `scions.py` | 11,468 | Six-Scion orchestrator |
| `naming_gate.py` | 7,678 | Naming Gate |
| `foundry.py` | 5,015 | Agent Foundry |
| `name_registry.json` | 3,735 | Gate registry (seed) |
| `test_vision.py` | 9,003 | Vision suite, 9 checks |

**Changed in scionsix-core only:** `README.md` (vision-build
section added). `console.py` and `test_scion.py` are unchanged.

**Deliberately NOT synced to SCIONSIX-AI:**
- `BUILD-REPORT.md` — the deliverable lives in the primary repo, per
  the assignment.
- `README.md` — the two repos carry different READMEs by design;
  SCIONSIX-AI's already defers to scionsix-core as the core's
  primary home and notes the same files are included there for
  convenience. Its copy of the vision modules follows that pattern.
- The Android scaffold (`app/`, `build.gradle`, `gradlew`,
  `settings.gradle`) and `scripts/terminal_orchestrator.sh` in
  SCIONSIX-AI were not touched at all.

---

## 4. Test evidence (verbatim)

### scionsix-core — `python3 test_vision.py` → 9/9, exit 0

```
PASS: roster: six offices, claim filters partition the work kinds — 13 kinds, each owned exactly once
PASS: gate accepts a compliant name — violations=[]
PASS: gate rejects violations with the rule named — HookForge->NG-COLLISION; hook forge->NG-COLLISION; Agent->NG-GENERIC; Scion Prime->NG-RESERVED; 9!!->NG-FORMAT
PASS: foundry: gate failure registers nothing (registry untouched, no announcement)
PASS: foundry: malformed definition refused by template check
PASS: foundry: pass registers the agent + posts the bus announcement (chain INTACT) — announce #1
PASS: scion dispatch routes by kind; claim filter honoured (Runner completes only its own)
PASS: scion round-trip completes (Warden's task done, result stored, chain INTACT)
PASS: dispatch refuses unowned kinds, cross-charter work, and blocklisted commands — unowned kind; cross-charter; blocklisted pre-post
SUMMARY: 9/9 checks passed
```

### scionsix-core — `python3 test_scion.py` → 7/7, exit 0 (unchanged suite, still green with the new files in the tree — its no-secrets scan covers them)

```
PASS: streamed execution (3 lines, in order, over time, exit 0) — spread=0.40s duration=0.61s
PASS: failing command captures real exit + stderr — exit=2 stderr="ls: cannot access '/nonexistent-xyz-scion': No such file or directory"
PASS: blocklist refuses >=3 patterns by name before execution — refused: rm-recursive-force, credential-file-access, download-pipe-to-shell, mkfs-filesystem-format, dd-to-raw-device, power-control
PASS: blocked rm -rf left its target untouched
PASS: bus round-trip (post -> claim -> execute -> done, result stored, chain INTACT) — task #1 result_id=2
PASS: worker refuses a bus-injected blocked command (refusal is the stored result)
PASS: no credential-shaped strings anywhere in the build dir — scan clean
SUMMARY: 7/7 checks passed
```

### SCIONSIX-AI — `python3 test_vision.py` → 9/9, exit 0

```
PASS: roster: six offices, claim filters partition the work kinds — 13 kinds, each owned exactly once
PASS: gate accepts a compliant name — violations=[]
PASS: gate rejects violations with the rule named — HookForge->NG-COLLISION; hook forge->NG-COLLISION; Agent->NG-GENERIC; Scion Prime->NG-RESERVED; 9!!->NG-FORMAT
PASS: foundry: gate failure registers nothing (registry untouched, no announcement)
PASS: foundry: malformed definition refused by template check
PASS: foundry: pass registers the agent + posts the bus announcement (chain INTACT) — announce #1
PASS: scion dispatch routes by kind; claim filter honoured (Runner completes only its own)
PASS: scion round-trip completes (Warden's task done, result stored, chain INTACT)
PASS: dispatch refuses unowned kinds, cross-charter work, and blocklisted commands — unowned kind; cross-charter; blocklisted pre-post
SUMMARY: 9/9 checks passed
```

### SCIONSIX-AI — `python3 test_scion.py` → 7/7, exit 0

```
PASS: streamed execution (3 lines, in order, over time, exit 0) — spread=0.41s duration=0.61s
PASS: failing command captures real exit + stderr — exit=2 stderr="ls: cannot access '/nonexistent-xyz-scion': No such file or directory"
PASS: blocklist refuses >=3 patterns by name before execution — refused: rm-recursive-force, credential-file-access, download-pipe-to-shell, mkfs-filesystem-format, dd-to-raw-device, power-control
PASS: blocked rm -rf left its target untouched
PASS: bus round-trip (post -> claim -> execute -> done, result stored, chain INTACT) — task #1 result_id=2
PASS: worker refuses a bus-injected blocked command (refusal is the stored result)
PASS: no credential-shaped strings anywhere in the build dir — scan clean
SUMMARY: 7/7 checks passed
```

Sync integrity: the five synced files are md5-identical across the
two repos (scions.py `fef5a988…`, naming_gate.py `ee0852ed…`,
foundry.py `0c73acaa…`, test_vision.py `391dcb6f…`,
name_registry.json `096e8a9d…` — the registry md5 is unchanged after
all test runs, i.e. the suites never mutated the shipped registry).

---

## 5. Still missing, with why

- **The original Naming Gate canon** — if it exists beyond the
  audit's one-line attestation, it was not in any local copy (see
  §1). The gate's rules are therefore this build's codification of
  the estate's practice, in the vault's named-rule style. Swapping
  in a recovered canon is a one-module change.
- **A long-running scion daemon** — `work_once` is a single duty
  cycle, exactly like the console's worker. A persistent loop
  (the estate's hub workers already poll this way) is a deployment
  choice, not missing logic; none was started, per the $0/local
  scope of this build.
- **Interactive/CLI front-end for the three modules** — the console's
  interactive shell still exposes only its original commands
  (run / task / work / verify / health). The vision modules are
  library-shaped, like the Q3/Q4 cores; wiring `scion`, `gate`, and
  `forge` verbs into the interactive shell is small follow-up work,
  deliberately left out so the verified core stays untouched.
- **Phone packaging** — unchanged from the Q4 note: the Android app
  that would host the orchestrator on-device remains the scaffold +
  Termux build loop in SCIONSIX-AI, unverified as an APK. The
  orchestrator built here is host-side Python, same as the console
  it extends.
- **GitHub push** — not performed, per instructions. The new files
  sit in the two sync directories ready for the parent agent's
  review and the usual snapshot-push route. Note for that push:
  scionsix-core's CI (once the staged `ci.yml` lands) runs
  `test_scion.py`; adding `test_vision.py` to it is a one-line
  follow-up the parent may want.
