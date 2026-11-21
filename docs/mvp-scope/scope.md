# Brand Studio: MVP scope (companion app)

Date: 2026-11-21, revision 15 (Phase 2 PhotoCraft adapter noted; rev 14: Adobe clause record; rev 13: hint rule; rev 8: team, routing).
Detail files: `model-routing.md` (prices, per-task routing), `b3-adapter-regression.md` (UXP regression), `legal/adobe.md` (Adobe clause record, B1). Supersedes `../proposals/brand-studio.md`.
Read: `../brand-studio/` (3/3 tests pass), `../ambitious-plan.md` 3, 4b, 4d, `../diagrams/brand-studio.html`, `../CS4680 Assignment 5 - Your One-Person Company.md`, DIGITAL files cited in section 6.
Installed (verified 2026-11-20): Deno 2.9.8 (`~/.deno/bin`, not on PATH), Herdr 0.9.5 (Apache 2.0), `.venv` (pillow 13.0.0,
mcp 2.3.0, pytest 9.2.0, ruff 0.17.6), bwrap 0.9.0, ffmpeg 6.1.1 (`--enable-gpl`), WSL2 2.6.2.0 mirrored. Photoshop 2026:
launches (user-confirmed); exact path verified at the week 1 spike. Not installed: Premiere (user installs), UXP Developer
Tool (Adobe login), CapCut (manual use only), Playwright (out of MVP). No NVIDIA GPU.
Marks: (verified) = checked locally or on a primary page; (unverified) = not checked; (guess) = estimate; (user Qn) = user answer.

## Conflicts for the user (nothing silently picked; each shows its working reading)

1. **Photoshop install: resolved.** User confirmed it launches. The two path checks disagreed; the week 1 spike records the path.
2. **DIGITAL brand: closed.** The owner owns DIGITAL and gave full authorization (2026-11-20); recorded in the profile as
   a consent record (section 6), scope: demo use and the MVP. No org letter needed.
3. **Posting (later phase) vs no publishing.** The MVP ends at the approved folder. Working reading for the later phase:
   YouTube Data API and Instagram Graph API, one owner approval click per post (YouTube Developer Policies I.2), under
   the section 7 conditions, after B5. Instagram needs a public media host (section 8; question 7).
4. **Judge vendor: closed, approved pending B6** (owner, 2026-11-20). Codex is primary (WSL2, bwrap). When Codex is down
   and the customer has a Google key, Gemini is the fallback judge; Gemini runtime use stays off until B6 passes for
   Google. Until then, or without a Google key: Claude, logged as same-vendor.
5. **Adobe AI/ML clause (Developer Terms 6.16): closed, option B** (owner, 2026-11-21). Adobe-touched assets (any
   Photoshop or Premiere render, any Adobe-only effect) go to human review only: no stage 2 AI judge, no previews of Adobe
   output to any vendor, at runtime or in eval. Non-Adobe assets and copy keep the full pipeline (stage 1, stage 2 per
   conflict 4, vendor previews where the consent record allows). **Hint rule** (owner, 2026-11-21): on Adobe-touched assets,
   stage 1 `critic.py` (local code, no AI) may attach its findings to the human review as hints; hints never enter the judge path (no stage 2, no model, no vendor).
6. **A5 repo vs Developer Terms 5.1: open, owner to confirm.** Working reading: `plugin/` stays out of any public repo; the
   grader gets a private invite. Supported by 4.1(A) (licence covers own development and testing) and 5.1 (shipping needs Adobe approval); record in `legal/adobe.md`. No repo exists yet; the owner decides it.
7. **Antigravity: settled, verification pending.** Excluded from every MVP runtime path, including model routing and any
   multi-model agent (owner decision). Build-time use only by the owner directly, as their own tool, and only after its
   terms clause 6 is read verbatim (so far a research summary: bars "using third party software, tools, or services to access the Service").

## 1. Product and first customer

**Brand Studio:** a local companion app that drives the customer's own logged-in Adobe desktop apps (Photoshop, then Premiere) through a
UXP plugin, turning owned photos and footage plus a one-paragraph brief into on-brand Instagram posts and Reels with scripts, captions and
alt text. A team of 7 agents does the work; the customer can pause or take over at any step and approves everything before export. No customer Adobe credentials leave the machine.

- First profile: **DIGITAL**, the non-commercial student-run venture studio at Cal Poly Pomona (user Q4; owner-authorized 2026-11-20). Second: the owner's portfolio.
- Formats (user Q5): Instagram post 4:5 at 1080x1350; Instagram Reels 9:16 at 1080x1920. Publishing stays a later phase.
- A5 demo mode is the MVP runtime: each LLM role in its own Herdr pane (section 3).
- Customers bring their own keys and budget (default $10 per package, user Q2). No hosted proxy.

## 2. Harness hierarchy

Deterministic code (the companion) owns apps, files, network, policy, routing and the step log. LLM harnesses decide.
Every harness reaches tools only through `studio-mcp` (section 4); all CLIs here expose MCP config (verified in `--help`).

**Runtime providers:** Anthropic and OpenAI required (customer keys); Google optional (fallback judge if B6 passes, eval); Grok out until its terms are read (403).
**Fallback: single-provider mode**: if one provider is down or its key is missing, every role runs on the other, and the step log marks same-vendor judging (user Q5).

| Tier | Harness | Owns | Capability needed (flag seen in `--help`) |
|---|---|---|---|
| 0 | Owner | Profile, budget, consent per image, mode, takeover, approval | Only actor that can approve export |
| 1 | `studio companion` + router | Plugin socket, policy, budget ledger, step log, packager, routed single calls (9a) | Existing atomic claim, `../brand-studio/bridge/tasks.py` |
| 1 | Herdr 0.9.5 (verified) | 7 panes, one per LLM role | Pane CLI usage: (unverified), week 4 |
| 2 | `claude` 2.1.329 | The team: Studio Lead; stills (Asset Editor, Copywriter); video (Script Generator, Director); Brand | `--strict-mcp-config`, `--tools`, `--json-schema`, `--max-budget-usd`, `--output-format`, `--fallback-model`. Image input with built-in tools removed: (unverified), week 1 |
| 3 | `codex` 0.169.0 in WSL2 | Brand Critic stage 2, primary judge | `exec -i`, `--output-schema`, `-s read-only`, `-C`, `--ephemeral`, `--ignore-user-config`, `--json`; under bwrap 0.9.0. The Codex desktop app may run too; the pipeline uses only `codex exec` |
| 3 | `gemini` 0.32.1 | Fallback judge (approved; off until B6 passes for Google, conflict 4); eval judge (processes video) | `-p`, `-o json`, `--approval-mode plan`. Image and video input not in `--help`: (unverified) |
| 5 | `cursor-agent` 2026.11.11 | Build time only, owner-driven: plan review, worktree implementer | `--mode plan`, `--model`, `-w`. Cursor AUP reportedly bars automated access (unverified) |
| 5 | `devin` 3000.12.57, `codex review` | Build time: long code tasks in cloud sessions; pre-merge review | `--cloud`, `--export`; `review` |
| 5 | Antigravity | Excluded from every runtime path (routing, multi-model agents); owner's own direct tool only, after clause 6 is read verbatim (conflict 7) | - |

- Build-time harnesses see the code repo only; profiles, assets and keys live outside it. `plugin/` stays out of Devin
  cloud sessions and any public repo until B1 passes. Meta MUSE: off until its ToS and AUP are read. Not used: `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` (absent in 2.1.329).

## 3. Agent roster: a team of 7 agents plus code

Each LLM role runs in its own Herdr pane with `roles/<role>.md` (job, inputs, outputs, quality bar), as A5 requires.
The owner types only in the Studio Lead pane; takeover controls are buttons, not chat. Models are starting points; the
router (9a) may move routed subtasks to cheaper models.

| # | Team | Role | Job | Inputs | Outputs | Quality bar | Runs on |
|---|---|---|---|---|---|---|---|
| 1 | Lead | Studio Lead | Brief -> package plan (posts and Reels), one task file per role | Brief, profile, asset index (hash, usable, people, consent) | `tasks/inbox/T-*.json`, schema-checked | 100% schema-valid; owned sources only; plan under budget | `claude`, Opus 5.5 |
| 2 | Stills | Asset Editor | Photoshop ops for posts; Premiere ops for Reels from the Director's plan; non-generative by default | Task, PSD + layer map or sequence plan, EXIF-stripped sources, critic reasons | Working copy, preview, `project.json` | Stage 1 passes within 2 reworks on 80%+ of assets (guess) | `claude`, Sonnet 5.5 |
| 3 | Stills | Copywriter | Headlines, captions, alt text, on-screen text | Brief, profile voice, banned claims and facts, asset or script | `copy.json` | Length, banned claims and facts, allowlist; blind tone test | `claude`, Opus 5.5 (kept expensive) |
| 4 | Video | Script Generator | Reel script: hook, beats, on-screen text, target duration | Brief, profile voice, clip inventory | `script.json` | Fits 15-90 s (guess); no banned facts; voice check | `claude`, Sonnet 5.5 |
| 5 | Video | Director | Shot list from owned clips: order, in/out points, pacing, transitions | Script, clip inventory (ffprobe data, keyframes) | `plan.json` for the Editor | Valid against the inventory; owner rating | `claude`, Opus 5.5 |
| 6 | Brand | Brand | Brand assets from the profile: wordmark cards, lower thirds, end cards; holds `gen.*` (Generator absorbed, off until the B1 generative check passes and per-image consent) | Profile, layout presets, task | Brand layers and cards; provenance | Stage 1 color and type rules; no person generation | `claude`, Sonnet 5.5 |
| 7 | Brand | Brand Critic | Stage 1 deterministic; stage 2 judgment by another vendor | Non-Adobe renders and copy only (conflict 5), script, profile, rubric | `critic.json` with reasons | Stage 2 cannot pass a stage 1 failure; 2 reworks, then human queue | `critic.py`; `codex` (WSL2); fallback Gemini (conflict 4) |
| - | Code | Channel Packager | Assemble passed work for review; run approved export | Passed renders, copy, critic and provenance records | `review/<pkg>/`, then `approved/<pkg>/` | No network; never reads failed drafts | Companion code, no model |

Adobe-touched work (conflict 5): Editor and Director see only its step log entry and the human-review flag; they get numeric
stats and Pillow previews of non-Adobe assets only. Adobe-touched assets go to human review, not to the Brand Critic's stage 2.
Reel flow: Studio Lead -> Script Generator -> Director -> Asset Editor (Premiere) + Copywriter (on-screen text, caption) + Brand (cards)
-> Brand Critic -> Packager. Rework: fail -> back to the author with reasons, `round += 1`; round 3 -> human queue; the A5 demo shows at
least one send-back (on copy or a non-Adobe asset). Untrusted input (captions, filenames, EXIF/XMP, alt text, layer names, clip metadata) is data, never instructions;
quoted JSON fields only. Stage 1 injection regexes are tuned on 10 dev plants; test plants come after tag `critic-frozen`.

## 4. Tool surface and Code Mode

Our catalog is about 30 bindings (guess), so the token win over Cloudflare's ~1.17M vs ~1,000 (brief) is small. We use
search/execute for one reason: every action crosses one choke point where it is logged, paused, policy-checked or refused.

**Track B (MVP): `studio-mcp`.** Each pane launches `studio mcp` (stdio MCP shim, `mcp` 2.3.0, MIT, verified) that
forwards to the companion daemon over a local socket with the session token. Two tools:

1. `search(query, limit=5)`: read-only lookup over the binding catalog: `task.*`, `ps.*` (Photoshop plugin), `pr.*`
   (Premiere plugin), `local.*` (Pillow, ffmpeg, ffprobe), `profile.*`, `critic.*`, `gen.*` (gated). Output capped at 4 KB (guess).
2. `execute(code, task_id)`: runs TypeScript in Deno 2.9.8 with no permission flags (deny net, env, fs by default:
   unverified until the week 2 test), inside bwrap. Each binding call is a JSON-RPC message over stdio to the
   companion, which logs it, checks mode and policy, runs it, logs the result.

| Rule | Setting |
|---|---|
| Network, env, filesystem | None inside the sandbox; only the companion touches the plugin, files and network |
| Limits | 60 s wall clock, 512 MB, 50 binding calls per `execute` (all guess) |
| Output | 16 KB cap (guess); images return as handles, previews as MCP image content (unverified in Claude Code) |
| Logging | Code saved to `runs/<pkg>/<task>/code/NNN.ts` with sha256, role, time, before it runs |

Policy on every binding call: role allowlist (only Brand calls `gen.*`; only Packager calls `export.*`), budget ledger,
consent check, mode (5a), approval-required list (5b). There is no publish, share or upload binding in MVP.

**Track C (later, cut from MVP).** If the companion calls the Claude API directly: bindings as custom tools with `allowed_callers: ["code_execution_20260120"]`; not compatible with MCP tools, `strict: true` or forced `tool_choice`.

## 5. Media pipeline

Design base: pyCapCut's pattern (a project-file model written by an edit layer, applied by adapters), re-implemented
from our own spec; no pyCapCut code.

| Adapter | How | Status |
|---|---|---|
| UXP plugin in Photoshop (MVP, first): IG posts | Plugin panel connects as a WebSocket client to the companion on 127.0.0.1 with a per-session token; named ops only | Photoshop launches (user-confirmed). UXP Developer Tool needs the user's Adobe login. Ops, WebSocket, localhost permission: (unverified), week 1 |
| UXP plugin in Premiere (MVP, second): IG Reels | Same pattern; runs the Director's plan | User installs Premiere (user Q3) |
| Local Pillow / ffmpeg / ffprobe | Renders for eval and for stage 2 on non-Adobe assets (conflict 5), clip inventory, CI, Reels fallback | Pillow adapter works; ffmpeg 6.1.1 present |
| Firefly Services API, Higgsfield | Generation only; customer's own credentials and terms; Brand role only | Off by default in the MVP; PSLT §6.2 and §7 (Firefly API) stay dormant until Firefly is turned on; then B1 generative check + consent (user Q6) |
| CapCut | **No binding in any plan.** CapCut terms (section 5) bar automated scripts and reverse engineering (user Q3) | Manual only; its exports can be ingested as owned sources |
| PhotoCraft (storytold/photocraft): **Phase 2 only, not MVP** | For customers without Adobe: Apache-2.0, self-declared clean-room Rust editor. FilmCraft optional for video, same gate. Adobe stays the primary path on the owner's machine | Gate: (a) clean-room process and AGENTS.md read; (b) a CLI or API we can drive (none verified; the README describes a GUI); (c) security review and sandbox run before any of its code executes |

**Later, legal sign-off required (not in MVP):** browser automation of web Adobe apps; General Terms 6.6, 6.7, 6.18 plausibly bar it. Needs Adobe's written authorization (6.6) plus counsel review. Desktop UI automation: out, not designed for.

1. **Ingest.** `studio ingest <dir> --rights rights.csv`: one row per file (source, owner, license, people y/n). No row,
   no ingest. Per-image consent for `people=y` (5b). EXIF/XMP stripped from the working copy; ffprobe builds the clip inventory.
2. **Profile-driven edits.** Works with any customer PSD. The layer map names the slots (`photo`, `headline`, `logo`);
   found by name, otherwise mapped once in the wizard (section 6). Ops: open a copy, place image, set text, apply a
   layout preset (4:5 or 9:16), set adjustments within profile ranges, render preview. Non-generative by default.
3. **Project model.** `project.json` per asset: canvas, materials (sha256, usable, people and consent flags inherited by
   every derived render), tracks, segments, ops, `human_edit` steps; also the replay log that makes edits revertible (5a).
4. **File transfer.** Bytes over the socket; the plugin works in its own data folder. No shared folder.
5. **Reels.** Script -> Director plan -> Premiere plugin places owned clips on a 1080x1920 sequence, trims, adds on-screen
   text and brand cards. Fallback: ffmpeg on owned footage. CapCut: owner's hand edits only.
6. **Generation, off by default** (Brand role). Options: Photoshop generative fill, Firefly Services API (plus the
   customer's Firefly agreement), Higgsfield (Soul 2 still $0.0032-$0.0057, unverified as API price). Wan 2.2 rejected
   (about 80 GB VRAM; no GPU). Text-to-image subjects: background, texture, pattern, empty scene.
7. **Brand critic.** Stage 1 `critic.py`: aspect and size per format, palette distance, profile rules (DIGITAL: red
   `#d8412f` a mark only; banned facts; no commercial claims), brightness and saturation, caption and script rules,
   provenance, people and consent flags. Stage 2 judge (tone, composition, wordmark placement, pacing,
   person without a consent record) runs on non-Adobe assets and copy. Adobe-touched assets go to human review only (conflict 5); by the hint
   rule, stage 1 findings attach to that review as hints and never enter the judge path.

## 5a. Modes, takeover and step log

Takeover needs no automation of Adobe: the customer drives the live app by hand; the companion pauses and resumes its
own calls around that. Modes (user Q1):

| Mode | Runs without a click | Stops and asks |
|---|---|---|
| Default (new customers) | Edit ops on the working copy (revertible) | Everything else: vendor sends, generation, export, deletes, spend over budget |
| Auto (like Claude Code's auto mode) | Everything except the approval-required list | The 5b approval-required list |

1. Revertible: every edit lands on a copy; revert to step N reopens the original copy and replays the first N ops from
   `project.json`. Reverting past a `human_edit` step discards that hand edit (the log warns first).
2. States in both modes: Running, Paused (current call finishes, no new call), Human control (bindings locked; plugin
   shows "You have control"), Aborted (nothing exported; app left as is).
3. Every binding call is one step. Before it runs, the log shows role, binding, argument summary, target document,
   expected effect, model, cost estimate. After: operation result, duration, preview hash, error if any.
4. Hand back: the plugin returns a snapshot of the customer's own document (layer names, preview hash); the companion
   records a `human_edit` step; the agent re-reads state; the asset is flagged for human review (conflict 5).
5. Auto-pause: approval-required action, round 3, adapter error, or the document's history state differs from the one
   our last op left (changed/unchanged flag only; no notification listener; API unverified, else the snapshot hash).
6. **Recording scope (General Terms 17(B) guard):** every recording surface (step log, B3 transcripts and goldens, CI
   mocks, eval data) holds only our own protocol messages, operation results, and renders or hashes of the customer's
   or our fixture's document. No Adobe UI content, panels, telemetry, raw descriptors or event payloads. Use: audit and
   compatibility tests of our plugin; never to model, reproduce, benchmark or test Adobe software or AI systems.
7. Surfaces: local page on 127.0.0.1 (same token) with log, mode switch, 4 buttons; Pause and Take control in the plugin panel; `studio log --follow` in a Herdr pane. Storage: `runs/<pkg>/steps.jsonl`, append-only.

## 5b. Security model for the companion

| Threat | Control |
|---|---|
| Another local process drives the plugin | Companion binds 127.0.0.1 only on a free port it writes to the pairing file; plugin pairs with a 6-digit code the owner types; per-session token; Origin check; schema-validated messages; rate limit 20 ops/s (guess) |
| Agent asks the app for something harmful | Plugin exposes named, typed ops only: open copy, list layers, place image, set text, apply preset, set adjustment, render preview, snapshot, export (Premiere: place clip, trim, add text, add card). No generic descriptor or script passthrough. Local documents in the plugin data folder only: no cloud documents, Libraries, Stock, Fonts activation, share, publish, account or preference ops. Adobe dialogs never suppressed; a plan or credit refusal is reported, never retried another way (6.7). Manifest: network to 127.0.0.1 only (exact keys: week 1) |
| Credential theft | Agents never see or type Adobe credentials; the owner logs in by hand; the companion never reads Adobe tokens or app storage |
| Generated code escapes | Deno with no permissions inside bwrap; 50-call cap; code logged before running |
| Prompt injection | Untrusted fields quoted as data; stage 1 checks; no publish binding exists to abuse |
| Judge reads secrets | `codex exec --ephemeral --ignore-user-config --skip-git-repo-check -C <scratch> -s read-only --json --output-schema rubric.schema.json -i <render>` in WSL2 inside bwrap (`--unshare-all --share-net --clearenv`) binding only the Codex binary, its auth and `<scratch>`; env holds the OpenAI key only; 120 s and 15 calls per package (guess). Nested sandbox: unverified. Fallback judges get the same scratch-only inputs |
| Real people | Non-generative edits are the default. Per-image consent: the customer confirms consent for each `people=y` image; the log records who, when, sha256, and the ops and vendors covered. With it: non-Adobe renders may go to those vendors (after B6 passes for each) and generative edits are allowed once B1's generative check passes. Without it: hard deny on generative ops, no pixels to any vendor (numeric stats only). No text-to-image people ever |
| Key leaks | Each harness and router call gets only its own vendor key; logs redact key patterns; startup fails if a key file is world-readable |

Approval-required list (stops in both modes): spend beyond the budget, deleting anything under the source folder, final export, enabling generation.

## 6. Brand profiles (onboarding wizard)

No PSD templates exist. Week 1 builds `studio profile new`, a wizard that works with any PSD the customer already uses. Every role reads the profile; `critic.py` checks against it; nothing runs until the owner signs it off.

| Profile part | Wizard does |
|---|---|
| Palette, color rules | Imports tokens from the owner's design files or proposes from on-brand images; owner confirms |
| Fonts | Lists fonts in PSDs and design files; flags Adobe Fonts (agent-set text only after the B1 fonts check; owned or OFL otherwise) |
| Logo or wordmark | Owned SVG or PNG, light and dark; until a logo exists, a text wordmark |
| Voice, mission | Studio Lead drafts `voice.md` from allowed sources; owner edits |
| Claims and facts | Banned claims; banned-as-fact list; held-until-confirmed list; allowlisted handles, hashtags, URLs |
| Layout presets | IG post 4:5 1080x1350 and Reels 9:16 1080x1920 (user Q5), safe margins, wordmark position, text area |
| Layer map, ranges, references, people | Slots by name or one-time mapping; brightness and saturation ranges; 10-20 on-brand and 5 off-brand images; consent per people image |

**Profile 1: DIGITAL** (`/mnt/c/Users/DangT/Documents/GitHub/DIGITAL_WebsiteV1`, read 2026-11-20, verified):

- Palette (`DESIGN.md:95-109`), light / dark: ground `#ffffff` / `#000000`; raised `#f5f5f7` / `#161617`; ink `#1d1d1f` /
  `#f5f5f7`; ink-2 `#6e6e73` / `#a1a1a6`; hairline `#d2d2d7` / `#424245`. "The one red" `#d8412f`: a mark, never body
  text, never a fill behind content; red text `#b3321f` / `#ef6a55`. Group colors (`DESIGN.md:281-283`): `#60c2ff`, `#b28fef`, `#68d7a1`.
- Fonts (`app/(apple)/_system/fonts/index.ts`), SIL OFL 1.1: Geist, Geist Mono (shipped), Hubot Sans, Mona Sans,
  Monaspace Krypton, Atkinson Hyperlegible Next. Photoshop needs desktop font files from upstream (OFL allows; guess).
- Wordmark: text "DIGITAL" (`DESIGN.md:298`: 21px, weight 600) for the whole MVP (owner). Later: add a logo (not blocking).
- Authorization (consent record): `authorized_by` = the owner (full name entered at wizard sign-off), date 2026-11-20,
  scope = demo use and the MVP; stored in `profile.yaml` and `consent.jsonl`. Use outside that scope needs a new record.
- Mission (user Q2): "Make something worth putting your name on."
- Voice sources (allowed, user Q2): description (`lib/data/siteConfig.ts:6`: "A student-run venture studio at Cal Poly
  Pomona. Pick one part of a real build and own it."); beliefs (`app/(apple)/_content/about.ts:24-29`: "Ideas aren't
  accomplishments. Making them real is." / "The problem picks the team." / "Reality grades the work." / "Sign your work.").
- Facts: the fact is 3 two-layer boards. "6 layers" (`app/(apple)/_content/sidekick.ts:170`) is a UI visual direction,
  banned in generated copy as a fact; the critic checks. Schedule: no club-wide meeting; work happens in sub-teams only
  (owner). The critic holds any meeting-schedule claim for human review.
- Non-profit student org (terms page section 1, `app/(apple)/terms/page.tsx:27`). Campaign restriction waived for the MVP
  (owner). Copy must not make commercial claims about DIGITAL unless the owner says so; the critic checks. LICENSE:
  none (verified).

**Profile 2: Portfolio** (`/mnt/c/Users/DangT/Documents/GitHub/PortfolioWebsiteV1`): owner's own brand; wizard extracts facts (not read here); second profile for the eval and demo.

## 7. Publishing: ends at a human-approved folder

- MVP: no posting, scheduling, sharing or platform credentials. The plugin allowlist has no share or publish op.
- Gate: critic pass -> Packager writes `review/<pkg>/` (previews at most 1024 px long edge, guess; copy; critic and
  provenance records). Owner approves with `studio approve <pkg>` or the local page. Only then does the Packager ask
  the plugin to export full-size files from the approved document state into `approved/<pkg>/`, with
  `approval.json` (who, when, sha256 of every file). If the document changed after approval, export stops and asks again.
- The owner posts by hand. `manifest.json` carries `ai_generated` and provider per asset for platform AI labels.
- **Later phase posting (conflict 3, working reading):** no posting code before B5. Conditions per coordinator research 2026-11-20:

| Platform | Conditions | Unverified |
|---|---|---|
| YouTube Data API | Each upload triggered by the owner's specific, express consent (Developer Policies I.2) = one approval click per upload; one API project per client; stay within quota (`videos.insert` 1 unit per Google's page; third-party "1,600" unconfirmed: verify in Cloud Console); quota extension needs a Google audit, only if needed; AI disclosure of realistic or altered content set in the manifest until the API field is confirmed | Whether the API exposes Studio's "AI use" field; current `videos.insert` page says unverified projects are NOT restricted to private: confirm in Cloud Console before designing around it |
| Instagram Graph API | Professional account (Business or Creator); owner completes Page publishing authorization; media on a public URL at publish time (section 8 host); 100 API posts per 24 h (verify with `GET /{IG_ID}/content_publishing_limit`; the page also says 50 in a carousel section); containers expire after 24 h; app access level confirmed in the dashboard; one approval click per post | App review requirement, Reels format specs, AI-label rule |

## 8. Storage: local-first

Retention guesses accepted by the user (Q10).

| Data | Where | Retention | Syncs to cloud |
|---|---|---|---|
| Source media + `rights.csv` | `~/BrandStudioData/<profile>/src/` (outside the code repo) | Owner's; deletes need approval | Never |
| Brand profile (`profile.yaml`, `voice.md`, layer maps, wordmark or logo) | `.../<profile>/profile/`, its own local git repo | Versioned | Optional, opt-in |
| Consent records (people images; brand authorization) | `.../consent.jsonl` and the step log | Life of the asset or profile (guess) | Never |
| Working copies, renders, scripts, plans | `.../work/<task>/` and the plugin data folder | Failed drafts 14 days (guess) | Never |
| Tasks, step logs, generated code | `.../tasks/`, `.../runs/` | 90 days (guess) | Never |
| Briefs | `.../briefs/` | Kept | Optional brief intake |
| Review and approved packages | `.../review/`, `.../approved/` | Owner's call | Never |
| Ledger, routing measurements, eval metrics | `.../runs/ledger.jsonl`, `.../runs/routing.json` | Kept | Optional, aggregates only |
| Public media host (later phase, Instagram only) | Owner's choice (question 7) | Upload only after the post's approval click; random unguessable names (guess); delete as soon as publish succeeds or the 24 h container expires | Public by design: anyone with the URL can read it. Never `people=y` media unless its consent record covers public posting |

Secrets: the customer's keys stay on their machine. Dev: `~/.config/brand-studio/env` on the WSL ext4 home, mode 600,
never under `/mnt/c` (drvfs shows files as 777); `studio doctor` fails otherwise. Customer Windows: Credential Manager
(unverified). No Adobe credentials stored. Plugin session token in memory only.

## 9. Deployment, runtime and cost

- MVP: this machine. WSL2 runs the companion, router, harnesses, Herdr panes and the Codex judge; Windows runs Photoshop
  and Premiere with the plugin; mirrored networking should share 127.0.0.1 (configured, verified; plugin reachability unverified).
- Product: Windows installer (companion, Deno, plugin `.ccx`, only after B1 5.1 passes); macOS later. Optional cloud
  after MVP: brief intake, profile store, aggregate analytics; public media host for Instagram (later phase, section 8).
- Budget (user Q2): default $10 per package; `studio budget set <usd>`; enforced by the ledger plus `--max-budget-usd` per call; hitting it pauses the package (approval-required).

Cost per package (guess), before routing. Post package = 5 posts + 5 captions; up to 3 passes; output includes thinking.
Prices in `model-routing.md` (Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, verified per coordinator research).

| Item | Typical | Worst (3 passes, all assets) |
|---|---|---|
| Studio Lead (Opus): ~40k in, 8k out | $0.30 | $0.80 |
| Asset Editor (Sonnet): 5 x passes x ~25k in, 4k out | $0.70 | $1.40-$3.00 |
| Copywriter (Opus): ~30k in, 6k out per pass | $0.25 | $0.75 |
| Critic stage 2 (Codex; fallback Gemini or Claude): 5-15 calls | $0.15-$0.50 | $1.50 |
| Harness overhead | $0.30 | $1.00 |
| **Post package total** | **$1.50-$3** | **$6-$10** |
| Reel add-on: Script (Sonnet), Director (Opus, keyframes), Brand cards (Sonnet), Editor, copy, judge | +$1-$2.50 | +$5 |

- A post package plus a Reel can exceed the $10 default in the worst case; the budget pause then asks the owner.
- Eval, one-off: 60 packages (4 arms x 3 runs x 5 briefs), $90-$750 (guess). Fixed: Adobe seats (customer's own);
  code signing $100-$400 a year (guess); build-time tools (unverified).

## 9a. Model routing (measured, per task)

Full price data and the per-task table: `model-routing.md` (draft until the week 5 eval measures each cell).

1. Deterministic code first; then the cheapest model that passes the subtask's check; a failed check escalates one tier;
   the step log records tier, model and cost.
2. Two axes: difficulty (easy, medium, hard) and speed need (interactive: the owner is waiting; batch: Auto runs, eval).
3. Routed subtasks are single calls by the companion's router with the customer's keys; role work stays in the panes.
4. Measured on fixtures and Pillow renders only (Developer Terms 6.16; conflict 5); re-measured on any model, price or check change and before
   retirements (Opus 5.5 Sep 22 2027, Sonnet 5.5 Sep 28 2027, Haiku 5.5 Oct 7 2027).

| Tier | Anthropic | OpenAI | Google (fallback judge if B6 passes; eval) |
|---|---|---|---|
| Easy | Haiku 5.5 $0.10/$0.50 (to 100K input; $0.50/$2.50 above) | gpt-6-luna $0.10/$0.50 | gemini-2.5-flash-lite $0.10/$0.40 |
| Medium | Sonnet 5.5 $2/$10 | gpt-6.1-terra $1/$5 (vision); gpt-6.2-sol $2/$10 | gemini-3.5-flash-lite $0.30/$2.50 (video) |
| Hard | Opus 5.5 $4/$20; Fable 5.2 $8/$40 | gpt-6.2-astra $8/$40 (context 272K vs 1.05M: verify) | gemini-4-carbon $2/$10, **$4/$20 from Dec 1 2026** |

- Kept on the expensive tier: Copywriter (Opus 5.5) and stage 2 judgment (Codex; fallback Gemini). Director starts hard.
- OpenAI prices rise above 272K input; gemini-3.8-flash rises Jan 1 2027; Google reroutes 2.5 Pro and 2.5 Flash on Dec 1 2026.
- Grok: out of runtime until its terms are read (403); grok-4.1-fast's $0.20/$0.50 is secondary-source only. Antigravity: never a routing target (conflict 7).

## 10. CI/CD and install package

Dev install: venv, deps, Deno, Herdr, bwrap, ffmpeg done (header). Remaining steps, one command each:

1. `export PATH="$HOME/.deno/bin:$PATH"` (Deno is installed but not on PATH; add to `~/.bashrc`)
2. `pip install -e .[dev]` (after `pyproject.toml` lands in week 1)
3. `studio doctor` (bwrap, ffmpeg, Deno, Herdr, key file mode, harness versions, plugin reachable)
4. Install UXP Developer Tool on Windows and sign in to Adobe (user; read the PSLT §9 new developer tools terms first, B1)
5. Load `plugin/manifest.json` in UXP Developer Tool
6. `studio pair` (prints the code to type in the plugin panel)
7. `studio profile new --from /mnt/c/Users/DangT/Documents/GitHub/DIGITAL_WebsiteV1`

Customer install (Windows, week 6, only after B1 5.1 passes): signed `BrandStudio-Setup.exe`; `brand-studio.ccx`; `studio keys set anthropic`; `studio keys set openai`; `studio budget set <usd>`; `studio pair`; `studio profile new`.

CI (GitHub Actions, guess; no repo exists yet: the owner decides it). Any failure blocks merge; no paid calls; mock plugin only:

1. `ruff check .`
2. `pytest -q tests`
3. `pytest -q tests/test_sandbox.py` (Deno denies net, env, fs; bwrap wrap; call cap; code logged; judge confined to scratch)
4. `pytest -q tests/test_socket.py` (no token, bad token, wrong Origin, non-allowlisted op: all refused; port file written)
5. `pytest -q tests/test_policy.py` (generative op without consent denied; `gen.*` off until both gates; budget pause; no publish binding; Adobe-touched assets and their stage 1 hints never reach stage 2, a model or a vendor)
6. `pytest -q tests/test_modes.py` (Default asks for non-edit actions; Auto stops at the approval list; revert replays N ops; log holds no UI content)
7. `pytest -q tests/test_router.py` (escalates one tier on a failed check; logs tier and cost; never routes to Grok or an unkeyed provider)
8. `npm test --prefix plugin` (plugin op allowlist against mocked `photoshop` and `premierepro` modules)
9. `pytest -q tests/test_plugin_secrets.py` (scans `plugin/` for API key and credential patterns; any hit fails; PSLT §6.6(A))
10. `python -m studio.eval --smoke` (planted violations through Pillow renders; any escape fails)

Not per PR, not nightly: live UXP regression runs (B3, `b3-adapter-regression.md`) on a Photoshop update, a plugin op
change or a release tag, started by hand on the owner's machine. A failing plugin op is pulled from the runtime path.

## 11. Evaluation

No Adobe output is used anywhere in the eval (Developer Terms 6.16; conflict 5): arms render with Pillow (posts) and ffmpeg (Reels).
Dataset: 20 owned photos and 5 owned clips, approved profile, 5 briefs (guess). Plants: 20 deterministic (off-palette, red used as a fill,
over-bright, wrong aspect, banned claim, "6 layers" stated as fact, commercial claim for DIGITAL, meeting-schedule claim, handle off the allowlist,
missing rights row, injection string in EXIF, filename or layer name), 10 judgment-only (off-tone caption with no banned word, claim
reworded outside the profile, wordmark off the layout preset, off-brand composition, Reel pacing off the script, person visible in a
generated image), 3 people-rule plants (text-to-image person prompt, `people=y` photo routed to generative fill without consent, `people=y`
render sent to a vendor without consent).

Arms (same bindings, adapter, profile and budget; no takeovers during runs):

- A, baseline (A5): one Opus 5.5 session, one prompt.
- A+: one Opus 5.5 session behind the same `critic.py` gate, failures back to the same session, 2 reworks.
- B: team with stage 1 critic only (does the LLM judge earn its cost?).
- C: full team. Team claim = B and C against A+. A vs A+ = value of the gate alone.

| Metric | Definition | Pass (guess) |
|---|---|---|
| Escape rate | Input-planted violations found in `review/` / input-planted. Post-producer plants are a separate critic-only result for B and C | C below A+ with non-overlapping 95% Clopper-Pearson intervals; no percent target below what n supports |
| False-reject rate | Clean assets failed by the critic that the owner marks "would post as-is" / clean assets | At most 15% |
| Yield | Assets in `review/` within 2 reworks / assets requested; human-queue items count as failures | C at least 80% |
| Owner minutes | Per requested asset, human-queue assets at full manual time; 1 run per arm per brief, order counterbalanced | C at most 50% of A+ |
| Cost | USD per package from usage logs and receipts, typical and worst | Within the budget and at most 3x A+ |

- Blind: one script exports render + caption pairs (and Reels) to neutral filenames, without critic, provenance or
  manifest files; the owner marks "would post as-is" (y/n) per asset.
- Judges: Codex (OpenAI, WSL2), Gemini (video-capable; CLI video input unverified) and Claude score all owner-rated
  assets (self-preference). Fallback judge in runtime: Gemini (conflict 4). Copywriter Opus vs Sonnet, blind (tone).
  Each 9a cell vs its escalation tier. Swap a default only if agreement intervals do not overlap. Meta MUSE: off.
- Diagnostics, not gates: takeovers per package, plugin op failures per 100 steps, fallback-judge share, escalation
  rate per routed task. Any missed threshold is reported as "not demonstrated" with the number, plus one place the team did worse.

## 12. Milestones, blocking items, cuts

Done 2026-11-20 (header list). User to install: UXP Developer Tool (Adobe login), Premiere, CapCut (manual only).

| Week | Deliverable |
|---|---|
| 1 | Read the PSLT §9 new developer tools terms and confirm the Developer Terms are current, before accepting them in UXP Developer Tool (B1). DIGITAL profile via the wizard (B4: wordmark, fact rules, authorization record). UXP spike in Photoshop: record the path, pair over 127.0.0.1, fill mapped slots, return a preview. `pyproject.toml`, CI 1-2 |
| 2 | Deno sandbox test + `studio-mcp`; UXP regression suite skeleton for Photoshop (B3) |
| 3 | Step log with the 17(B) recording scope, Default and Auto modes, revert by replay, takeover, local page, socket and policy tests (B2). CI 3-6 |
| 4 | `project.json`, `critic.py` stage 1, `roles/*.md` for all 7 roles, Herdr panes; router with `test_router.py`; IG post 4:5 end to end; approve -> export |
| 5 | Codex stage 2 in WSL2 on Pillow renders (after B6 for OpenAI); measured `routing.json` (9a); eval arms A, A+, B, C; A5 demo video (DIGITAL, owner-authorized) |
| 6 | Reels 9:16: Script -> Director -> Premiere plugin (or ffmpeg); Windows installer and signing (after B1 5.1); `gen.*` only after the B1 generative pass |

Blocking items (no build past the week named until closed):

| # | Item | Closes when | By |
|---|---|---|---|
| B1 | Adobe terms; clause record in `legal/adobe.md` (Developer Terms 2024, PSLT 2026v2, developer tools addendum 2026v1). **Partly closed:** own machine, own use allowed (4.1(A)). **Open:** PSLT §9 new developer tools terms (adobe.com/go/new-developer-tools-terms, NOT READ: the plugin's B1 gap); distribution (5.1, 5.2, 6.8, 6.10, 6.15, 14.2, 14.3); AI/ML 6.16 handled by conflict 5 option B (recheck against current terms); Adobe Fonts, unattended runs, generative ops | `legal/adobe.md` records pass, fail or ask-Adobe per check with source and date; a fail keeps the feature off. Still needed: the §9 terms text; Adobe's current Developer Terms. No Adobe request drafted (user Q11) | §9 terms and current-version check: week 1, before accepting in UXP Developer Tool. Distribution: before any `.ccx` leaves this machine. Generative and unattended checks: before those features |
| B2 | Credential isolation: port discovery (free 127.0.0.1 port written to the pairing file), socket pairing and token, plugin allowlist, per-vendor keys for harnesses and router, Codex judge confined in WSL2 | `test_socket.py`, `test_policy.py`, `test_sandbox.py` pass | Week 3 |
| B3 | UXP-only regression suite; fixtures hold our protocol messages only; runs are started by hand on the owner's machine (on a Photoshop update, a plugin op change, or a release tag) | Suite fails on a broken op or API change; mock written from our spec; Photoshop first, Premiere when installed | Week 2 |
| B4 | DIGITAL profile: palette, fonts, voice and mission, banned and held facts, no-commercial-claims rule, layout presets, layer map; wordmark "DIGITAL" for the whole MVP (logo later, not blocking) | Owner signs off `profile.yaml` and `voice.md`; one PSD mapped; authorization record stored | Week 1 |
| B5 | Posting terms (later phase). YouTube API Services and Google APIs: consent per upload, one project per client, quota (`videos.insert` units), audit, AI disclosure field, unverified-project status. Instagram Graph API: professional account, Page authorization, public URL, posting limit, container expiry, access level, app review, Reels specs, AI-label rule | Each condition quoted with URL and date; quota and limits checked in Cloud Console and via `content_publishing_limit`; pass, fail or ask per check | Before any posting work (not MVP) |
| B6 | Vendor input-data terms: OpenAI (judge, router), Google (fallback judge at runtime, eval), xAI Grok (terms returned 403), Meta (MUSE ToS and AUP; Instagram data terms if posting starts) | Terms read; training, retention, region recorded per vendor; a fail keeps that vendor off | OpenAI before week 5; Google before runtime fallback or the eval; Grok and Meta before any use |

Shippable before B1 passes: the companion with Pillow and ffmpeg adapters only. No plugin, no `.ccx`, no customer install.

Cut: posting and scheduling (later phase, conflict 3); browser automation and web Adobe apps (later, legal sign-off required); desktop UI
automation; any CapCut binding; Lightroom; video generation; self-hosted models (Wan 2.2, FLUX, SD 3.5); Grok at runtime until B6; Antigravity
in any runtime path; hosted LLM proxy and Track C; cloud sync (designed, not built); macOS installer; PhotoCraft and FilmCraft adapters (Phase 2, section 5; not in the MVP milestones); multi-customer billing; any web UI beyond the
local page (open-higgsfield: UI reference only). Never: text-to-image or video of people; generative edits on people without a consent record.

## 13. Legal and terms

Status: B1 partly closed; clause record in `legal/adobe.md`. Own use allowed (Developer Terms 4.1(A)). Open: PSLT §9 new developer tools terms (not read), distribution, current-version check of the Developer Terms. AI/ML 6.16: option B (conflict 5).

| Item | Position |
|---|---|
| Adobe General Terms (Oct 3, 2025; per research) | 6.6: UXP is an interface Adobe provides, so the plugin path fits; browser automation of web apps plausibly does not (6.6, 6.18) -> out of MVP. 6.7: plugin never bypasses credit limits or feature gates. 17(B): recording scope limited (5a item 6) |
| Adobe AI/ML: Developer Terms 6.16, 6.11 (read) | 6.16: no use of Adobe services, software or output "derived from" them to create, train, test or improve AI, and none for identifying natural persons. 6.11: no re-identification by linking data. Adobe output never goes to eval, 9a measurement or tuning; Adobe-touched assets: human review only, no AI judge, no previews to vendors (conflict 5, option B) |
| Adobe Developer Terms (local PDF, June 18 2024, 16 pages; check Adobe's current version; record in `legal/adobe.md`) | Own machine, own use: allowed (4.1(A) development and testing licence). Shipping to others: Adobe approval (5.1; may re-approve after updates; may stop distribution with 10 days' notice), approved channels only (5.2), object code inside approved software only (4.1(A)), no sublicensing (6.8), own EULA and privacy notice (6.15, 6.10); Adobe may terminate any time (14.2); stop distribution at once on termination (14.3). 6.7: API limits apply to end users too. No explicit bot or scraping ban found (6.1, 6.7, 3.1 closest). 23.1 says "Development Software" (likely a typo for "Developer Software"). Until approval: plugin on the owner's machine only (conflict 6) |
| UXP distribution page | Per research: independent sharing needs no Adobe review. Developer Terms 5.1 requires approval; the scope follows 5.1 |
| Adobe PSLT 2026v2 (read; bilingual jp file, no section 10; `legal/adobe.md`) | §9: new developer tools are governed by adobe.com/go/new-developer-tools-terms: NOT READ, the B1 gap for the plugin. §6.6(A): no Adobe API credentials embedded in the UXP plugin; ours uses none (CI step 9 scans for key patterns). §6.2 and §7 (Firefly API): dormant while Firefly is off. Still checks, not passes: Adobe generative ops, Adobe Fonts in agent-set text, unattended runs |
| Developer tools addendum 2026v1 | Applies only to Firefly Creative Production customers not on PSLT 2026v2 or later. The owner's PSLT is 2026v2, so its section 1 does not apply (the owner pasted the same text) |
| CapCut (capcut.com terms, section 5; user Q3) | Bars automated scripts and reverse engineering. No binding, no draft-file writing, no automation; manual use only |
| Antigravity (terms clause 6, research summary only; user Q5) | Reportedly bars "using third party software, tools, or services to access the Service"; read verbatim before any use. Excluded from every MVP runtime path, including routing and multi-model agents; owner's own direct tool only (conflict 7) |
| Cursor | Prices not published; AUP reportedly bars automated access (unverified). Build time only, owner-driven |
| xAI Grok | Terms unread (403). Out of runtime until read (B6). grok-4.1-fast price from a secondary source only |
| Meta MUSE (user Q9) | Standard Model API only (dev.meta.ai/products/meta-model-api); never a "contributor" variant. ToS and AUP unread: off (B6) |
| YouTube Data API, Google APIs (later phase) | Upload allowed with conditions (section 7, per research): owner's specific, express consent per upload (Developer Policies I.2), one project per client, quota, audit only if needed, AI disclosure. Remaining unverified items: B5 |
| Instagram Graph API (later phase) | Professional accounts only; conditions in section 7. App review, Reels specs, AI-label rule unverified (B5). The public media host is a privacy item (section 8) |
| Firefly Services API, Higgsfield | Optional, generation only, Brand role, customer's own credentials and terms. Firefly is off by default (PSLT §6.2, §7 dormant). Higgsfield (brief): no resale of API access; agent activity is the account holder's; keys never client-side beyond the customer's machine; no scraping; "no competing product": ask before any multi-customer offer. Wrappers: only `geopopos/higgsfield_ai_mcp` (MIT); never `creativecgl` |
| DIGITAL brand | Non-commercial student org (terms page section 1). No LICENSE in the repo (verified); the brand belongs to the org. Owner authorization on file (profile consent record, 2026-11-20; scope: demo use and the MVP). Campaign restriction waived for the MVP (owner); copy makes no commercial claims about DIGITAL unless the owner says so |
| pyCapCut, open-higgsfield | No license: pattern or UI reference only; no code reuse |
| PhotoCraft (storytold/photocraft), FilmCraft (Phase 2, not MVP) | Apache-2.0 (per the coordinator's check; not re-checked here). Clean-room claim is self-declared, unverified. Section 5 gate applies before any use. Acrobat Pro's counterpart is pdfcraft; no printcraft repo exists |
| Vendor input-data terms | Anthropic, OpenAI, Google, xAI, Meta, Adobe, Higgsfield: training, retention, region (unverified; B6). `people=y` material goes only to vendors named in that image's consent record |
| AI disclosure, ownership | `manifest.json` flags `ai_generated` and provider. Copyright in purely generated assets: (unverified, may be none) |
| Models, ffmpeg, `mcp`, Herdr, fonts | Wan 2.2 Apache 2.0 (brief), not used. ffmpeg `--enable-gpl` (verified): called as a process, not bundled. `mcp` MIT and Herdr Apache 2.0 (verified). DIGITAL fonts SIL OFL 1.1 (per source file) |
| Asset rights | Owned or public-domain inputs with a `rights.csv` row; fonts licensed for ads; music owned or licensed; people photos need per-image consent (5b) |

## 14. Open questions (one line each)

1-3. Answered 2026-11-20: DIGITAL authorized by the owner; wordmark for the whole MVP; no club-wide meeting (section 6).
4. Portfolio profile: which files in PortfolioWebsiteV1 are allowed voice and fact sources?
5. Can you paste adobe.com/go/new-developer-tools-terms (PSLT §9, the B1 gap), and is the 2024 Developer Terms PDF current?
6. Answered 2026-11-21: option B; Adobe-touched assets go to human review only (conflict 5 closed).
7. Later-phase Instagram needs media on a public URL: which host (your site, a storage bucket, other), deleted right after publish?
8. Answered 2026-11-20: Gemini is the runtime fallback judge with a Google key, off until B6 passes (conflict 4 closed).

## Review disputes

**Review 1** (Fable 5.2, revision 1): 8 issues, 5 applied in full, 3 in part.
1. Issue 7 fix 3 (delete `cursor-agent`, `devin`): disputed; the user wants each harness where it fits. Both stay build-time; data and keys moved out of the code repo.
2. Superseded by user answers: issue 2 fix 1 (deny all people edits -> deny without consent), issue 8 fix 1 (Higgsfield default -> generation off), issue 7 fix 1 (fail closed -> fallback judge, conflict 4).

**Review 2** (Fable 5.2, B1 fix, revision 4): 8 issues (4 high, 3 medium, 1 low), all applied, none disputed. Issues 7, 8 and issue 4's Devin line were judgment calls that only narrow scope. Issue 2's "17(C)" label is superseded by the user's citation (Developer Terms AI/ML clause, PSLT 6.2); the no-Adobe-renders precaution now covers the judge too.
