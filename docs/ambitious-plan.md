# Ambitious plan: PR Triage product + Brand agent company

Status: DRAFT. Guesses are marked **(guess)**. Run `/grill-with-docs` on this file before building anything.

## 0. Rewritten prompt (ambitious version)

> I run a small B2B SaaS. I have no spare engineers to review the pull requests that my coding agents open. Unreviewed agent PRs either sit for 16+ hours or merge without a real check. Build a triage system that gives every agent PR a verdict with evidence, merges the safe ones on its own, sends the risky ones to me with the reasons, and proves over time that the merges were safe. Before you start, tell me how a good staff engineer running a release process would approach this, and what data and repo access you need from me. Mark every conclusion you are unsure about as a guess.

Altitude moves: from "review PRs" to "decide which agent work is safe to ship, and measure the false-merge rate."

## 1. Top-5 re-score (the list you were unhappy with)

Your goal (B2B SaaS founder, no human bandwidth, agent PRs that are not slop) changes the criteria. The old sweep scored novelty and baseline clarity for a school project. New criteria: **pain** (founder hours saved), **trust** (can we prove a merge was safe), **buildability** (one semester solo), **moat** (what a copy cannot get).

| Rank | Candidate | Pain | Trust | Build | Moat | Notes |
|---|---|---|---|---|---|---|
| 1 | Agent-PR Merge Court (this doc, sec. 2) | 5 | 5 | 3 | 4 | Direct fit to your goal |
| 2 | SAST Alert Triage Crew | 4 | 4 | 4 | 3 | QASecClaw (arXiv 2605.01885) already covers part of it |
| 3 | Utility Bill Audit Crew | 3 | 4 | 4 | 3 | Not SaaS-founder pain |
| 4 | Public Meeting Lead Monitor | 3 | 2 | 5 | 2 | "Good lead" has no ground truth |
| 5 | Adversarial Clause Panel | 3 | 2 | 3 | 2 | Legal liability |

Scores 1-5, **(guess)**. Sales-Tax Nexus Watcher drops out: deterministic core, little agent value.

## 2. Ambitious scope: "Merge Court"

Goal: every agent PR gets a verdict in minutes, with an evidence bundle. The founder only reads the high-risk queue.

### Pipeline (numbered, one job per stage)

1. **Intake**: read the linked issue's acceptance criteria. Turn each criterion into an executable check. This is the SWE alignment: the issue is the spec.
2. **Scope checker**: compare changed files and API surface to the issue. Flag out-of-scope edits.
3. **Hidden oracle writer**: write acceptance tests the coding agent never sees (from the diagram set, Idea 2).
4. **Mutation auditor**: break the diff on purpose and confirm the agent's own tests catch it.
5. **Risk gate (fixed rules, no LLM)**: auth, billing, data-migration, and infra paths go to a human. Low-risk paths go on.
6. **Fresh-context reviewer**: a reviewer that never saw the coding agent's reasoning, only the diff and the spec.
7. **Stop rule**: at most 3 fix rounds. Stop when the verified score stops rising, then hand off (Idea 6).
8. **Destructive-action gate**: any deploy, delete, or prod-DB call needs a human approval. Fails closed on timeout (Idea 4).
9. **Verdict + evidence bundle**: merge, return with reasons, or human queue. Each verdict links to its evidence.
10. **Calibration loop (the moat)**: seed known faults into a share of PRs (sabotage drills, Idea 3). Report the catch rate and the false-merge rate each week. If the rate worsens, tighten the gate automatically and tell the founder.

### What makes it more ambitious than the 12 ideas

- **Merge SLA**: a time budget per verdict, logged. The founder sees the number.
- **Spec-as-tests**: issues in the customer's tracker become the oracle. Agents cannot grade their own work.
- **Oversight telemetry as a product**: the founder gets a weekly report: PRs merged, PRs sent back, minutes of human time, seeded-fault catch rate.
- **Multi-repo**: one gate config per repo, with shared rules. **(guess: v2 feature)**

### Risks (be honest)

- Prior art exists for parts (QASecClaw for SAST triage). The moat is the calibration loop, not the agents.
- Oracle tests for vague issues are hard. Start with issues that have explicit acceptance criteria.
- Seeded faults in production PRs need founder consent. Start on staging branches only.
- Sabotage-catch numbers in the diagram set come from an abstract (94% miss rate, grade B). Do not quote them as fact in the product pitch.

### Build order (smallest proof first)

1. Risk gate + evidence bundle on your own repo. Measure: how many PRs reach you.
2. Add the hidden oracle on 20 past merged PRs. Measure: does it catch the bugs that reverts later fixed?
3. Add seeded faults on a staging repo. Measure: catch rate.
4. Only then enable auto-merge on low-risk paths.

## 3. Brand company (Opus 5.5 team, idea-to-post)

Coordinator is the only agent you talk to. Output folder is the handoff.

| Role | Job | Tool **(guess)** | Model |
|---|---|---|---|
| Coordinator (brand strategist) | Turns your brief into task files | Claude Code | Opus 5.5 |
| Creative director | Concept, brand rules, tone | Claude Code | Opus 5.5 |
| Asset producer | Edit photos, generate images, build layouts | Lightroom / Adobe Express / image-gen API (check API access first) | Opus 5.5 |
| Brand critic (reviewer) | Scores assets against the brand guide. Sends back on fail | Codex | Opus 5.5 |
| Publisher | Schedules posts, uploads to site | Platform scheduler APIs | Sonnet 5.5 (mechanical) |
| Ops monitor | Watches deployment and DB health | Scripts + logs | Haiku 5.5 |
| Analytics | Engagement analysis, loop back to creative | Claude Code | Opus 5.5 |

Constraints to confirm before build:

- Adobe Express and Lightroom automation: check whether your account has API access. If not, the asset producer uses image-gen and manual export.
- Social platform posting by bot: check each platform's terms. Most require a business account and approved API access.
- Only the brand critic can pass an asset to publish. Publisher never reads raw drafts.

## 4. Haiku search fan-out (not run yet)

Plan: one Opus agent launches 5-6 Haiku search agents in one batch, each on one lane:

1. B2B SaaS founder pain: agent PR review backlog
2. Oversight and review-time measurement
3. Existing tools that gate agent PRs (name, price, what they lack)
4. Brand workflow automation with real API access
5. Engagement analytics loops for small brands

Each Haiku agent returns a table: name, source, date, grade (A-D), gap. No more than 10 rows each. Not run: you have not confirmed scope or budget.

## 4b. Answers from repo check (2026-11-19)

Repo: `BrooklynD23/Asclexis` (public, Python, default branch `main`). `HealthCentral` redirects to it. Status: a medical results companion, not an A5 deliverable.

**CI system: GitHub Actions.** Workflows:
1. `ci.yml`: docs lint, backend tests, backend lint, frontend tests, security scan, agent evals, legacy evals, RSI replay. Runs on push to `main` and `Security-Revamp-*`, and on PRs to `main`.
2. `nightly-gates.yml`: scheduled timing gates.
3. `npm-audit.yml`: scheduled audit.

**Branch protection on `main`:**
- Required checks: Documentation Lint, Backend Tests, Frontend Tests, Agent Eval Gate, Security Scan, RSI Replay, G3 on Production Build.
- Required approving reviews: 0. Stale-review dismissal off.
- Repo setting `allow_auto_merge`: **false**. Auto-merge is off at the repo level, so it must be turned on first.

**Recent runs:** latest CI run is `null` (pending or unfinished). Previous runs: 2 success, 1 failure (2026-11-18). Open PRs: #682, #679, #678.

**Impact on Merge Court:**
- Your existing 7 required checks already cover the "Tests + Security + Evals" half of the pipeline. Merge Court adds the layers they lack: scope check, hidden oracle, mutation audit, risk gate, evidence bundle.
- Turn on auto-merge (repo setting), then add a risk-gate job as a required check. Auto-merge runs only once every required check passes.
- Do not drop reviewer count to 0 without also adding a required gate job. Otherwise an agent PR with green tests merges with no check beyond CI.

**Brand team, no API access:** Adobe and social APIs are blocked, so the bridge must avoid desktop control. Options, ranked (all **(guess)** until checked):
1. **Folder bridge (simplest):** agents write assets and task JSON to a shared folder. A local watcher script runs export and upload jobs. No UI control needed.
2. **Local scripting:** Photoshop and Lightroom have their own scripting hooks (Photoshop: ExtendScript/UXP; Lightroom Classic: Lua SDK). Check whether your installed versions expose them before building.
3. **Image-gen API only:** for generation, skip Adobe. Check current API terms and cost first.
4. **MCP:** only if an MCP server exists for a tool you use. Check the MCP registry before writing one.

Social posting: most platforms need a business account plus app review, so the publisher stays a stub until then. Publish-to-website is the first real target.

**Brand guide:** none yet. First build task: the creative director writes a 1-page guide (colors, tone, do/don't), and the critic scores against it. Human-approved before any asset ships.

## 4c. Decisions

- **First customer:** the owner's own repo (`BrooklynD23/Asclexis`).
- **Auto-merge in v1:** yes. Low-risk paths merge on their own. High-risk paths go to a human.

## 4d. Status (2026-11-19)

| Item | State |
|---|---|
| Ambitious plan and rewritten prompt | Done: this file |
| Top-5 re-score | Done (guesses) |
| Merge Court scope | Drafted, not built |
| Asclexis CI and branch-protection check | Done. Auto-merge repo setting still off |
| Latest CI run on `main` | Nightly gates success (2026-11-19). Last PR CI run: failure on `chore/agent-config-optimize` |
| Brand team design | Drafted, not built. No API access, no brand guide |
| Haiku search fan-out | Not run |
| `/grill-with-docs` | Not run. You must run it (user-only skill) |
| Code written | None |

**Next, in order:**
1. Enable auto-merge on `Asclexis`: repo setting, then a required risk-gate check.
2. Investigate the failing `chore/agent-config-optimize` CI run.
3. Run `/grill-with-docs` on this file.

## 5. Open questions for `/grill-with-docs`

Answered: CI system (GitHub Actions), repo (`Asclexis`), auto-merge (off at repo level, not yet enabled), API access (none), brand guide (none). Still open:

1. Who is the first customer: your own repo, or a named founder?
2. Which languages and CI system (GitHub Actions, GitLab)?
3. Is auto-merge allowed on any path yet, or do humans merge everything in v1?
4. Do you have API access to Adobe Express or Lightroom?
5. Brand: is there a written brand guide, and where is it?
