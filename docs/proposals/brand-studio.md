# MVP proposal: Brand Studio Crew

Sources: `../brand-studio/` (working bridge: `adapters/`, `bridge/`, `tests/`, `tasks/`); `../ambitious-plan.md` sections 3, 4b; `../agent-pr-bottleneck-diagrams.md` Idea 10; Brand Studio Crew concept (pasted by user, not re-read here).
Status: bridge partly built (see below). No publishing. Nothing posted.

## Scenario and first customer

- Problem: a one-person brand edits each photo by hand until it "looks on-brand". Slow, inconsistent.
- First customer: the owner's own brand. No brand guide exists yet (ambitious-plan 4b); writing it is task 1.
- Output: a folder of on-brand, human-approved images + captions, ready for the owner to post by hand.
- What exists today in `../brand-studio/` (read 2026-11-19):
  - `bridge/tasks.py`: `claim_task` (atomic rename inbox -> claimed) and `finish_task` (claimed -> done with result).
  - `adapters/base.py`: `EditorAdapter` protocol, one method `apply_recipe(src, dst, recipe)`.
  - `adapters/pillow_adapter.py`: recipe keys `crop`, `brightness`, `saturation`; rejects unknown keys and out-of-bounds crops.
  - `adapters/mock_adapter.py`: copies source, writes recipe JSON beside it.
  - `tests/`: 3 tests (claim-edit-finish flow with double-claim guard; crop guard; unknown-key guard). Pass status not re-run here.
- Caution: the diagram artifact's audit scored the brand-critic loop 12/25 and recommended dropping it; no study tested a vision critic against human reviewers (Idea 10 source note).

## MVP scope (in) and out-of-scope

| In | Out |
|---|---|
| 1-page brand guide (colors, tone, do/don't), human-approved | Social posting (needs business accounts + app review) |
| Photo edits via recipe JSON through the adapter layer | Lightroom automation (no tool found) |
| Pillow adapter as the working default | Adobe MCP / Express API (not verified) |
| Critic with deterministic checks + LLM notes | Image generation (check API terms and cost first) |
| Human veto before anything leaves `approved/` | Publisher, ops monitor, analytics roles |
| Captions in brand tone | Website upload (first real target, v2) |

## Agent roles and the review loop

Five roles; exact role names from the pasted concept were not in the files read, so this list follows ambitious-plan section 3 trimmed to 5 (guess on match).

| # | Role | One line |
|---|---|---|
| 1 | Coordinator (brand strategist) | Turns the owner's brief into task JSON in `tasks/inbox/`; only agent the owner talks to |
| 2 | Creative director | Writes and maintains the brand guide as `brand.yaml` (machine checks) + `brand.md` (tone) |
| 3 | Asset producer | Picks a recipe per photo, runs it through the adapter, writes captions |
| 4 | Brand critic (reviewer) | Runs deterministic checks, then LLM review; passes or sends back with reasons |
| 5 | Packager | Copies passed assets + captions + critic report to `approved/` for human veto; never publishes |

Review loop:
1. Critic deterministic checks (code, no LLM): size/aspect ratio per channel, brightness and saturation within `brand.yaml` ranges, dominant colors within a distance of the palette, caption length, banned words.
2. Any fail -> task back to `tasks/inbox/` with `round += 1` and machine-readable reasons -> producer adjusts recipe.
3. Max 3 rounds, then human queue.
4. Pass -> LLM critic note on tone/composition (advisory only, cannot override a failed check).
5. Human veto on every asset before it leaves `approved/`. Only the critic can move an asset forward; packager never reads raw drafts.

## Architecture (components, data flow)

```
owner brief -> Coordinator -> tasks/inbox/T-*.json {src, dst, recipe, round}
  -> worker: claim_task() (atomic rename)        [exists]
  -> adapter.apply_recipe(src, dst, recipe)        [exists: Pillow, Mock]
  -> finish_task() -> tasks/done/                  [exists]
  -> critic.py (deterministic) + LLM note         [to build]
  -> pass: approved/<id>/ ; fail: new inbox task with reasons
  -> owner reviews approved/ and posts by hand
```

- Adapter layer: `get_adapter(name)` picks Pillow by default. A future `AdobeAdapter` or `PhotoshopScriptAdapter` implements the same `apply_recipe` only after the tool is verified (ambitious-plan 4b options: folder bridge first, local scripting second, MCP last).
- Agents run as Claude Code and Codex in Herdr panes (per class constraints); file polling only.

## Storage (what is stored, where, retention)

| Data | Where | Retention |
|---|---|---|
| Source photos | `assets/src/`, local, gitignored | Owner keeps; never deleted by agents |
| Edited drafts | `assets/out/` | Delete failed drafts after 14 days (guess) |
| Task JSON (inbox/claimed/done) | `tasks/` | Keep `done/` for eval and audit trail |
| Brand guide | `brand.yaml`, `brand.md`, in git | Versioned |
| Critic reports | `approved/<id>/critic.json` | Kept with the asset |
| Approved assets | `approved/` | Owner's call |

Photos may show people: get consent before sending faces to an LLM vendor (vendor terms unverified).

## Deployment and runtime (where it runs, cost order of magnitude marked as guess)

- Local only (WSL/Linux), Python 3.12, Pillow. No server, no cloud storage.
- Cost: Pillow edits are free; LLM calls for captions and critic notes, cents per asset (guess). Vision calls for the LLM critic cost more per image than text (guess).

## CI/CD (pipeline stages, gates, what blocks a merge)

| Stage | Blocks merge if |
|---|---|
| 1. Lint (`ruff`) | fail |
| 2. `pytest tests/` (existing 3 tests + critic tests) | any fail |
| 3. Critic check tests: over-bright image fails, off-palette image fails, on-brand fixture passes | any fail |
| 4. Adapter contract test: every adapter rejects unknown recipe keys | any adapter accepts one |
| 5. No-publish guard: run the end-to-end test with network disabled | network call attempted |

## Installation package (what a user installs and runs, one command per step)

1. Enter folder: `cd brand-studio`
2. Install: `pip install pillow pytest` (move to `pip install -e .` once a `pyproject.toml` exists)
3. Check: `pytest -q tests/`
4. Add photos: `cp ~/Pictures/shoot/*.jpg assets/src/`
5. Queue a job: `python -m bridge.enqueue assets/src --brief "spring launch"` (to build)
6. Run worker: `python -m bridge.worker --adapter pillow` (to build)
7. Review: open `approved/` and veto or keep

## Eval: baseline arm vs team, metric, pass threshold

- Dataset: 20 owner photos + the approved brand guide.
- Arm 1: one AI, one prompt: "edit these to match this brand guide and write captions" (same Pillow tool access).
- Arm 2: the team with critic loop.
- Metrics:
  - Deterministic pass rate on the critic's checks (first round and final).
  - Owner veto rate (blind: owner sees both arms' outputs shuffled).
  - Owner minutes per approved asset.
- Pass threshold (guess, owner to set): team veto rate < Arm 1 veto rate, and team final check pass rate >= 90%.
- Report at least one place the team did worse (cost or time).

## Milestones (weeks, max 6 rows)

| Week | Deliverable |
|---|---|
| 0 (done) | Bridge, adapter protocol, Pillow + Mock adapters, 3 tests |
| 1 | Brand guide v1 (`brand.yaml` + `brand.md`), owner-approved |
| 2 | `critic.py` deterministic checks + tests |
| 3 | Worker loop + enqueue CLI + send-back with reasons |
| 4 | Captions + LLM critic note; human veto folder |
| 5 | Arm 1 vs team eval on 20 photos; demo video |

## Risks (max 5), each with a mitigation

| Risk | Mitigation |
|---|---|
| Vision critic disagrees with the owner's taste (no study supports it) | Deterministic checks gate; LLM note is advisory; owner veto measured |
| Adobe MCP / Lightroom never become usable | Pillow adapter is the product for v1; adapters are swappable behind one protocol |
| Pillow edits too basic for "on-brand" looks | Add recipe keys only as needed (contrast, white balance, overlay logo), each with a guard test |
| Accidental publishing | No posting code; packager writes to a local folder only; network-off test |
| No brand guide means nothing to check against | Week 1 blocks everything else until the guide is approved |

## Open questions (max 5)

1. Exact 5 roles in the pasted concept: do they match the table above?
2. Which installed Photoshop/Lightroom versions, and do they expose scripting (ExtendScript/UXP, Lua SDK)? (unverified)
3. Does an Adobe MCP server exist and work with the owner's account? (not verified)
4. Which channels (and sizes) does the brand target first?
5. Is image generation in scope at all, or edits of owner photos only?
