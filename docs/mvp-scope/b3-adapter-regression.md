# B3: UXP adapter regression plan

Date: 2026-11-20. Blocking item B3 (`scope.md` section 12), due week 2. Owner: the developer (one-person company).
Scope change 2026-11-20 (coordinator): the browser adapter is out of the MVP (Adobe General Terms 6.6 and 6.18 bar
automated browser access and scraping). This plan covers the UXP plugin only: Photoshop first, Premiere second.
Read: `scope.md` sections 4, 5, 5a, 5b, 10, 11, 12 (revision with the B4 layer map and the 17(B) logging scope);
`../brand-studio/adapters/`, `../brand-studio/bridge/`, `../brand-studio/tests/`.
Marks follow `scope.md`: (verified), (unverified), (guess). No UXP code exists yet, so every plugin behaviour below
stays (unverified) until the week 1 spike.

Code today: `EditorAdapter.apply_recipe(src, dst, recipe)` covers 3 pixel ops (crop, brightness, saturation) and
fails loudly on a bad recipe (`tests/test_adapter_guard.py`). Slot ops (open, place, set text, snapshot) do not exist.
The suite targets the `ps.*` binding ops, not `apply_recipe`. Pillow stays as the CI adapter and the pixel oracle.

## 0. Decisions

1. Every write op reads back what it changed, then checks pixels without a golden: the preview diff is non-zero
   inside the target layer's bounds and within tolerance outside them. Silent drift is the failure that reaches
   customer files; a thrown error is the easy case.
2. Untested Photoshop build: the adapter stays off until a dry-run preflight passes. The owner clicks "Check
   compatibility"; the companion runs the golden ops on a bundled fixture, never on customer documents.
3. All or nothing per (bundle version, host build). No per-op disabling: the golden ops chain on one document, so
   one failure cascades, and planning around a missing op is the agent workaround decision 4 bans.
4. Outcome unknown (`TIMEOUT`, socket drop mid-op): never re-send. On resume, run that op's readback first.
5. One golden set, recorded on the reference build (Photoshop 2026 here). Every later build and every preflight
   compares against it, so pixel changes between builds show up.
6. Live runs on triggers (Photoshop build change, plugin op change, release tag), not on a daily clock.

## 1. Failure modes (Photoshop UXP plugin)

| # | Failure | Customer sees (plugin panel + local page) | Companion detects |
|---|---|---|---|
| F1 | API drift, loud: an API call or batchPlay descriptor throws or is gone after an update | Step N red, package paused: "Photoshop refused step N (set headline). Take control, skip asset, or abort." | Plugin returns `OP_ERROR` with the exception text |
| F2 | API drift, silent: op returns OK, effect wrong (text unset, wrong or hidden layer, other resample) | Same pause: "Photoshop did step N differently than expected", before/after previews | Readback (layer names, text, bounds in pixels, doc size) plus the pixel postcondition (decision 1); place also vs Pillow's resize of the source the companion holds -> `POSTCONDITION_FAILED` |
| F3 | Photoshop build changed (auto-update) | "Photoshop updated to <build>. Brand Studio is off until you click Check compatibility (about 2 min, guess)" | Handshake `host_version` not in `adapters.lock.json` -> `HOST_UNTESTED` |
| F4 | Plugin and companion versions differ | Pairing refused: "Update the Brand Studio plugin: double-click <path>.ccx" | Handshake plugin version is not the one the companion ships with -> `PROTOCOL_MISMATCH` |
| F5 | UXP runtime change: plugin fails to load, manifest field or localhost permission changed | "Photoshop plugin not connected", checklist (Photoshop open? Plugins > Brand Studio listed?) | No connection 30 s (guess) after `studio pair` -> `NOT_CONNECTED`; the panel shows its own socket error if it loads |
| F6 | Pairing: token expired after companion restart; mirrored networking broken by a Windows or WSL update | "Pair again: type the code shown in the companion" | Bad token or refused connection -> `AUTH_FAILED` / `NOT_CONNECTED`; `studio doctor` checks 127.0.0.1 reachability |
| F7 | Socket drops mid-op | "Lost Photoshop connection, reconnecting", pause after 10 s (guess) | Outcome unknown (decision 4); replies carry the request id; a late reply for a closed step is dropped and logged |
| F8 | Modal dialog blocks Photoshop (missing font, colour profile mismatch, update prompt) | "Photoshop may be showing a dialog. Answer it, then Resume." | Per-op timeout 30 s (guess) -> `TIMEOUT`, outcome unknown (decision 4) |
| F9 | Owner edits the document while an agent runs | "Document changed outside Brand Studio", paused | Plugin changed/unchanged flag (scope 5a item 5) -> `DOC_CHANGED` |

- Every code is a step-log field and triggers auto-pause. Only `OP_ERROR` and `POSTCONDITION_FAILED` that reproduce on
  the fixture turn the adapter off (section 4); `TIMEOUT`, `NOT_CONNECTED`, `AUTH_FAILED`, `DOC_CHANGED` never do.
- Text compare: after NFC and newline normalisation (how UXP returns line breaks: unverified).
- Logging scope (scope 5a item 6): transcripts and step logs hold only our op requests and results, never UI content.
- Premiere (scope question 2): F1-F9 apply. Not installed (verified), so `pr.*` bindings are hidden from `search`.
- Gap for B2, not B3: scope 5b uses a random port, and the plugin cannot read files outside its data folder, so how
  the plugin finds the port is unspecified. F6 depends on that answer.

## 2. Contract tests

Fixtures (no customer data; brand files stay outside the repo, scope section 2): `tests/contract/fixtures/template.psd`,
a synthetic PSD built once by hand in Photoshop 2026: 1080 x 1350 (guess), RGB 8-bit sRGB, slots `photo`, `headline`
(text, Arial so Windows shows no missing-font dialog, guess), `logo`, plus its layer map. The `photo` placeholder colour
is far from the source mean. `source.png` is written by a Pillow script: asymmetric colour blocks, so a mirrored or
shifted place fails.

Golden ops, Photoshop. All run on a copy in the plugin's data folder; the companion targets the document by the id G1
returns, asserts its path is inside the data folder before every write, and closes it without saving.

| Op | Does | Structure check (exact unless marked) | Pixel check (thresholds guess) |
|---|---|---|---|
| G1 open | Opens a copy of the fixture, lists layers | 3 slots: names, kinds, order; 1080 x 1350, RGB, 8-bit; host build and doc id recorded | none |
| G2 place | Places `source.png` into `photo`, fit to frame | `photo` bounds = frame bounds within 1 px (guess); layer count unchanged | 8 x 8 (guess) grid-cell means within 3/255 of Pillow's resize of the source |
| G3 set text | Sets `headline` to `Café – 50%` + line break + `off` | Readback equal after normalisation; font unchanged | Postcondition only (decision 1) |
| G4 adjust + preview | Fixed test values: brightness +20, saturation -30 (guess); full-size preview | Adjustment values read back (which API: unverified) | Vs golden, text region masked: mean abs diff at most 2/255 per channel; at most 1% of pixels off by more than 16 |
| G5 export crop | Exports a 1080 x 1080 (guess) PNG crop | Exact size, PNG, no alpha, sRGB tag (unverified) | Vs Pillow crop of the G4 preview (geometry oracle) and vs golden: G4 thresholds |
| G6 snapshot | Hand-back snapshot (scope 5a item 3) | Layer names equal the G5 state; preview hash of decoded pixels, computed in the companion, equal across 5 calls (guess) | If hashes differ, switch to the G4 tolerance compare |
| G7 refuse | Sends a made-up op `ps.__not_allowed__` | Plugin refuses; document unchanged | none |

- Pass rule: an op passes only if every structure check holds and every pixel check is within threshold. Panel
  screenshots are never a check. G7 never sends a real destructive op to a signed-in Photoshop; real denied op names
  stay in the plugin unit test against the mocked `photoshop` module (scope 10 step 7).
- Goldens: `tests/contract/golden/ps/` (`G4.png`, `G5.png`, `structure.json`), recorded once on the reference build
  after the structure checks and Pillow oracles pass and a human has viewed them. A per-build override needs a human
  commit that names the build and the reason, after viewing the diff image.
- Thresholds: the numbers above are starting guesses. Week 2 sets them from 5 repeat runs (guess) on the reference
  build: noise floor plus margin. They are not a kill gate.
- Code home: golden ops and checks live in `studio/regress.py` (shipped); pytest wraps it; `studio regress --real` and
  the customer preflight call the same function.

| Layer | Runs | Proves |
|---|---|---|
| Replay, CI per PR | Companion side against JSON-RPC transcripts recorded from live runs; the transcript replayer is the mock plugin | Handshake parsing, readback and pixel checks, error codes, auto-pause; no Adobe needed |
| Drift fixtures, CI per PR | Mutated transcripts: layer renamed (`OP_ERROR` on place), op throws (`OP_ERROR`), OK with wrong text readback (`POSTCONDITION_FAILED`) | Each must fail with its code; one passing = detection broken, blocks merge |
| Live, owner's machine | Golden ops on real Photoshop | The plugin works on this build; refreshes transcripts |
| Plugin unit (scope 10 step 7) | Op allowlist vs mocked `photoshop` module | Allowlist only, not drift |

Transcripts are scrubbed before commit: session token and pairing code removed, image payloads stored as sha256.
Run time: G1-G7 under 3 min per build (guess).

Premiere: no golden ops until it is installed (scope question 2); default is ffmpeg (scope 5 item 5). If installed,
the same pattern: open a project copy, import an ffmpeg-made clip, set a title, export frames at 2 fixed timecodes.

## 3. Version matrix

| Target | Builds tested | Count |
|---|---|---|
| Photoshop, MVP | Photoshop 2026 as installed here, exact build from G1 (the reference build) | 1 |
| Photoshop canary | Photoshop (Beta) on the same host, if Creative Cloud offers it (unverified). Advisory only | +1 |
| Photoshop, after MVP | Current major N and N-1, latest build each; needs a second Windows machine or VM (side-by-side install unverified) | 2 (guess) |
| Premiere | None until installed; then the installed build only | 0-1 |
| UXP runtime | Bundled with the host build; recorded by G1, not tested separately | - |

`adapters.lock.json` ships with the companion: plugin version, protocol version, host builds that passed, date.

Untested build on a customer machine. Options: refuse, warn, dry-run. **Default: refuse until a dry-run passes.**

1. Handshake reports a build not in the lock file. The adapter is off; the panel shows "Check compatibility".
2. The owner clicks it. The companion runs G1-G6 on the fixture (about 2 min, guess), compared to the shipped goldens.
3. Pass: the build is added to this machine's lock entry for this bundle; the first package on it runs in step mode
   (scope 5a item 2) with an "untested Photoshop build" banner (guess: one package).
4. Fail: the adapter stays off for this build. Packages run takeover-only, with Pillow previews, until a bundle
   whose suite passes on this build is installed.

Not plain refuse: it would stop the customer on every Photoshop update. Not plain warn: F2 would reach customer files.
Owner click, not automatic: the preflight opens a document in the customer's live Photoshop session.

## 4. Canary, pinning, rollback, takeover fallback

Canary for a new Adobe build:

1. The test host runs the live suite on the Photoshop release and, if available, on Beta. Beta red = start the fix
   before the release ships (lead time unverified). Beta never blocks our release.
2. Install docs ask customers to turn off Photoshop auto-update in Creative Cloud (setting: unverified). Where they
   do not, the preflight (section 3) is the local canary.

Pinning and our own releases:

- Companion, plugin `.ccx` and `adapters.lock.json` ship as one versioned bundle. The handshake requires the exact
  plugin version the companion ships with (MVP); relax to protocol major after MVP.
- The plugin manifest declares the minimum host version (field semantics unverified).
- Rollback of our bundle: keep the previous signed bundle; reinstall it. `project.json` carries `schema_version`; an
  older companion refuses a newer schema with a message instead of misreading it.
- Rollback of an Adobe build: Creative Cloud can install earlier versions (unverified). Docs only, not automated.

Fallback when an op fails mid-package:

1. Auto-pause. The step log records code, request, readback and before/after previews (our op results only).
2. Outcome unknown (`TIMEOUT`, drop mid-op): on Resume or reconnect, run that op's readback. Pass = step done.
   Fail = stay paused. Never re-send.
3. The owner picks Take control, Skip asset or Abort (scope 5a).
4. Take control: the owner does the failed op by hand; the local page states it in plain words ("Set layer
   `headline` to ..."). Hand back: plugin snapshot (G6). If the plugin is down, the owner uploads an exported PNG on
   the local page; it becomes that asset's render, the companion records a `human_edit` step, the critic re-runs, and
   the asset goes to review like any other. No further agent ops on that asset.
5. After an `OP_ERROR` or `POSTCONDITION_FAILED`, the owner is offered the fixture check (same as preflight). Fixture
   red = drift: adapter off for this build. Fixture green = document-specific (font, odd PSD): adapter stays on.

## 5. Test environment

| Machine | Runs | State | Set up first |
|---|---|---|---|
| Windows host (this machine) | Photoshop 2026 with the plugin; live suite | Photoshop 2026 (verified). UXP Developer Tool, plugin load, localhost WebSocket (unverified, week 1 spike) | UDT, plugin loaded, owner signed in to Creative Cloud, fixture PSD |
| WSL2 (this machine) | Companion, `studio regress --real`, replay suite | Pillow 13.0.0 present (verified 2026-11-20); mirrored networking (verified), plugin reachability (unverified); venv and `pyproject.toml` are week 1 | venv, `pip install -e .[dev]` |
| GitHub Actions, Linux (scope 10, guess) | Replay, drift fixtures, plugin unit, per PR | Not set up | CI steps 1-2, week 1 |
| Self-hosted Windows runner | Nothing in MVP | Scope 10 suggests one (guess); on a personal machine it would run PR code next to the owner's signed-in Adobe apps | Not used |

- Playwright: not installed (verified; cached Chromium builds in `~/.cache/ms-playwright`). Not needed for UXP-only B3.
- Live runs are owner-started, so pairing stays as scope 5b (code typed, per-session token). Triggers:
  1. Photoshop build change on the owner's machine (`HOST_UNTESTED` on the owner's own companion).
  2. Before merging a change to a plugin op.
  3. Before each release tag. From week 6 this run installs the `.ccx` built from the tag commit, not the UDT-loaded
     dev plugin.
- Exit codes: 0 pass; 1 adapter failure; 2 environment not ready (Photoshop not running, not paired, signed out,
  dialog). Only 1 counts toward release blocks and kill criteria.
- Results: `regress/<date>.json` (host build, bundle sha, op, check, value, threshold, code) and diff images for failed
  pixel checks. The release script checks that the newest result matches the current host build and bundle sha.

## 6. Ownership and cadence

| What | Who | When |
|---|---|---|
| Replay, drift fixtures, plugin unit | CI | Every PR; red blocks merge |
| Live suite, Photoshop release | Owner's machine | The 3 triggers in section 5 |
| Live suite, Photoshop Beta | Owner's machine | When Creative Cloud updates Beta; advisory |
| Triage a red run | Developer | Next working day (guess); build-time agents may draft a fix, a human merges |
| Re-baseline goldens | Developer | Only after viewing the diff; commit names build and reason |
| Customer preflight | Customer, one click | Each new host build on that machine |

A release is blocked by any of:

1. Replay or drift suite red, or a drift fixture passing (detection broken).
2. The newest live result does not match the current release host build and the bundle sha.
3. A red live op on the release build. Beta results never block.

## 7. Kill criteria

| Adapter | Cut from MVP when any holds | Then |
|---|---|---|
| Photoshop UXP | Week 1 spike cannot pair over 127.0.0.1 or fill the mapped slots, and 1 extra week (guess) does not fix it; B1 bars UXP automation; G1-G3 structure checks not green live on Photoshop 2026 by end of week 2; at end of week 4 (guess), a 1-package dry run hits an `OP_ERROR` or `POSTCONDITION_FAILED` that reproduces on the fixture and is not fixed within 3 days (guess) | MVP becomes takeover-only: the owner drives Photoshop; agents plan, write copy, critique and package; Pillow renders previews. Eval arms then compare copy and critic only (scope 11 runs have no takeovers) |
| Premiere UXP | Not installed by the week 6 decision (scope 12) | ffmpeg on owned footage (scope 5 item 5) |
| Any adapter, after launch | Repairs over 4 h a week (guess) for 2 weeks (guess); hours logged as a `Repair-Hours:` trailer on fix commits | Takeover-only. Separately, the adapter is off on any build whose suite is red (lock file) |

Scope 11 lists "plugin op failures per 100 steps" as a diagnostic, not a gate; this plan keeps it that way.

## 8. Week 2 plan (B3)

Precondition: the week 1 spike paired and filled the mapped slots. If not, section 7 applies.

1. Commit the synthetic fixture PSD (not the owner's brand PSD), its layer map, and the Pillow script for `source.png`.
2. Implement `ps.open`, `ps.place`, `ps.set_text` with readbacks, pixel postconditions and request ids (G1-G3).
3. Add `studio regress --real` (`studio/regress.py`): run G1-G3 live 5 times (guess); save scrubbed transcripts,
   goldens, thresholds and `regress/<date>.json`.
4. Add replay to CI from those transcripts, plus the 3 drift transcripts with their named codes.
5. Live break-it: rename `headline` in a fixture copy (expect G1 fail and `OP_ERROR`), run G3 with a wrong expected
   text (expect `POSTCONDITION_FAILED`), run G2 against a different source (expect pixel fail). Hand the output to
   the `scope.md` owner to close B3.

Later: G4-G7 with their ops (weeks 3-4, guess); preflight button, outcome-unknown resume and the post-error fixture
check with the week 3 takeover states.

For the `scope.md` owner (not edited here):

1. Section 10 "Nightly ... self-hosted Windows runner" and "A failing plugin op is pulled": live run on build change
   and before each release tag, on the owner's machine; adapter off per build, not per op.
2. B3 row: "nightly run against the real app after each Adobe update" -> "live run after each Photoshop update and
   before each release tag".
3. Section 5 Premiere row says "question 1"; Premiere is question 2.
4. B2: port discovery (random port, plugin confined to its data folder).

## Review disputes

Fable 5.2 review (one run, on the draft). 10 issues: 8 applied in full (1, 2, 4, 5, 6, 7, 8, 9), 2 in part (3, 10).
Applied: one golden set across builds (1); live break-it with named codes (2); golden-free pixel postcondition, text
normalisation (3); outcome-unknown resume and request ids (4); all-or-nothing per build, owner-clicked preflight,
shipped `studio/regress.py` (5); made-up G7 op, grid-cell G2, decoded-pixel hashes, fixed G4 values (6); week 2
reorder and transcript scrubbing (7); kill gates moved off guessed thresholds and the scope 11 diagnostic (8);
trigger-based runs, no exit code 3, Beta advisory, no B2 token ask (9); unmarked numbers, stale `brand.yaml` reference removed, question 2 (10).

1. Issue 3, fix 4 (G1 records UI language, ruler units, colour working space): disputed. Reading app preferences
   conflicts with the plugin allowlist (no preference ops, scope 5b) and the 17(B) logging scope (scope 5a item 6).
   Instead every readback requests pixel units explicitly (API support unverified, week 1 spike); a units mismatch
   then fails G1 or G2.
2. Issue 10, fix 4 (delete speculative items), in part: deleted the 3-day soak and Premiere P1-P4; "keep 2 bundles"
   is now "keep the previous one". Kept one "after MVP" matrix row (the brief asks how many versions) and a 2-line
   Premiere note (scope names Premiere second).
