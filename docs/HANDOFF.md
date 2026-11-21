# Handoff: Brand Studio (for the next orchestrator)

Date: 2026-11-21. Owner: BrooklynD23 (the user). Read this first, then `mvp-scope/scope.md` (rev 14, the source of truth).

## What the project is
A local companion app that makes brand-consistent marketing assets (Instagram Post 4:5, Reels 9:16) for DIGITAL (owner's non-profit student org, full authorization on file) and Portfolio. Agents (Herdr panes, one per role) do the work; the owner approves before anything leaves the machine. MVP ends at a human-approved folder. Posting is a later phase.

## Where things are
- Scope (source of truth): `mvp-scope/scope.md` (rev 14, cap 450 lines).
- Routing: `mvp-scope/model-routing.md`.
- Adobe clause record: `mvp-scope/legal/adobe.md`.
- UXP regression plan (B3): `mvp-scope/b3-adapter-regression.md`.
- Proposals (6), diagrams (6), drawing board: `proposals/`, `diagrams/`, `drawing-board/`.
- Working code: `brand-studio/` (adapters, bridge, 3 passing tests, `.venv` with pillow, mcp, pytest, ruff).
- Private repo: https://github.com/BrooklynD23/brand-studio (created 2026-11-21, pushed `main`). Docs in it are a snapshot copied on 2026-11-21; re-sync when the scope changes.

## Installed and verified
- Deno 2.9.8 (`~/.deno/bin/deno`, not on PATH).
- Herdr 0.9.5 (`~/.local/bin/herdr`, not on PATH).
- brand-studio venv, tests 3/3 pass.
- bwrap 0.9.0, ffmpeg 6.1.1, WSL2.
- Harnesses: claude 2.1.329, codex 0.169.0, gemini 0.32.1, cursor-agent, devin.
- `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1` set in `~/.claude/settings.json` (exists in 2.1.322-2.1.329; effect unverified).

## Not installed / owner action
- Photoshop: user confirmed it launches on Windows. Exact path still unresolved (two earlier checks disagreed). Verify at the B3 spike.
- Premiere Pro and CapCut: user said they'll be installed. Not confirmed.
- UXP Developer Tool: needs the owner's Adobe login.
- CapCut is manual use only (its terms bar automation).

## Decisions made (settled; do not reopen without the owner)
- Owner's DIGITAL authorization recorded as consent (2026-11-20). Non-commercial rule waived for MVP.
- Wordmark "DIGITAL" stands in for a logo. Sub-teams only; no club-wide meeting.
- Customers bring their own keys: Anthropic and OpenAI required; Google optional (fallback judge, after B6).
- Conflict 5, option B: Adobe-touched assets go to human review only; no AI judge, no vendor previews. Stage 1 local hints allowed on those assets, never into the judge path.
- Conflict 4: Codex primary judge; Gemini fallback only with a Google key and after B6; until then a same-vendor Claude fallback, flagged.
- Antigravity excluded from every runtime path (verify clause 6 verbatim).
- PhotoCraft/FilmCraft (storytold, Apache-2.0, self-declared clean room): Phase 2 optional adapter only, after three gates. Not in MVP.
- Budget default $10 per package, customer-settable.
- Modes: Default (accept edits, revertible) and Auto (approval-required list always stops).
- Formats: Instagram Post 4:5 (1080x1350), Reels 9:16 (1080x1920). Both in MVP.
- Team: 7 LLM roles in Herdr panes plus code (Packager). Script and Director are in MVP.
- Later phase: YouTube Shorts and Instagram posting, one approval click per post, own bucket for media.

## Still open (blocking or pending)
1. **Conflict 3** (posting rule): owner has not confirmed one approval click per post.
2. **Conflict 6** (plugin stays out of public repos; grader gets a private invite): owner said "confirmed" earlier, then asked about the rec. Confirm.
3. **B1 Adobe terms**: partly closed (own use allowed under Developer Terms 4.1(A)). Still open: the new developer tools terms at `adobe.com/go/new-developer-tools-terms` (NOT READ; this governs the plugin); the current Developer Terms version (copy read is June 2024); the worldwide PSLT (file read is the Japanese-bilingual copy; its section 10 does not exist).
4. **Drawing board labels** below 11px: owner has not answered whether to enlarge and republish.
5. **B2** credential isolation (week 3): designed, not built.
6. **B3** UXP regression suite (week 2): planned, not built. Needs Photoshop path + UXP Developer Tool.
7. **B4** DIGITAL profile wizard (week 1): not built.
8. **B5** YouTube and Instagram posting terms: later phase; YouTube unverified-project check needs Cloud Console.
9. **B6** vendor data terms: OpenAI before week 5; Google, Meta, Grok unread. Grok terms returned 403. Cursor AUP unread (build-time only). Meta MUSE off.
10. **PhotoCraft Phase 2 gates**: clean-room process read, CLI/API check, security review. Scope agent was asked to add this in rev 15 (not yet confirmed at handoff).

## How to work with this owner
- Ask in rounds: numbered, one recommendation each, and wait. Accept "yes" as the recommendation.
- Short answers first. Plain status with done / open / needed-from-you.
- Subagents: read a file only if needed; they report back as messages. A scope agent (`a8ed15a42c7c9d305`) owns `scope.md`; send it edits rather than editing the file yourself, or coordinate.
- Do not publish, post, or push without asking. The repo is private; keep it that way until the owner says otherwise.
- Never state legal conclusions as fact; cite the clause and mark what was not read.

## Next steps, in order
1. Confirm conflicts 3 and 6 with the owner.
2. Get the new developer tools terms (adobe.com/go/new-developer-tools-terms) from the owner.
3. Re-sync `brand-studio/docs/` from `mvp-scope/`, commit, push (ask first).
4. Week 1: profile wizard (B4); UXP spike once Photoshop path is confirmed; decide the drawing-board label fix.
5. Week 2: B3 regression suite. Week 3: B2 credential isolation.
