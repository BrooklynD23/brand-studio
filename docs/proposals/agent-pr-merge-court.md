# MVP proposal: Agent-PR Merge Court

Sources: `../ambitious-plan.md` sections 2, 4b, 4c; `../agent-pr-bottleneck-diagrams.md` Ideas 1-4, 6.
Status: proposal only. Nothing built. Nothing changed on `BrooklynD23/Asclexis`.

## Scenario and first customer

- Problem: agent-written PRs pile up waiting for a human. Green CI alone is not enough to merge them.
- Goal: every agent PR gets a verdict (merge, return, human queue) with an evidence bundle. The owner reads only the high-risk queue.
- First customer: the owner's own repo, `BrooklynD23/Asclexis` (public, Python, default branch `main`, GitHub Actions).
- Facts from the 2026-11-19 repo check (ambitious-plan 4b):
  - 7 required checks on `main` already: Documentation Lint, Backend Tests, Frontend Tests, Agent Eval Gate, Security Scan, RSI Replay, G3 on Production Build.
  - Required approving reviews: 0. Repo setting `allow_auto_merge`: false.
- Decision (4c): auto-merge ON in v1 for low-risk paths only. High-risk paths go to a human.

## MVP scope (in) and out-of-scope

| In (v1) | Out (later or never) |
|---|---|
| Rule-based risk gate as a new required check | Multi-repo shared config (v2, guess) |
| Scope checker: changed files vs linked issue | Hidden oracle on every PR (v1 runs it on 20 past PRs only) |
| Fresh-context LLM reviewer (diff + issue only) | Mutation auditor on live PRs |
| Evidence bundle per verdict (PR comment + artifact) | Seeded faults on production PRs (staging only, with consent) |
| Auto-merge on low-risk paths via GitHub native auto-merge | Any deploy, delete or prod-DB action by the bot |
| Weekly report: merged, returned, human minutes | Paid product, billing, GitHub Marketplace listing |

## Agent roles and the review loop

| # | Role | One line |
|---|---|---|
| 1 | Coordinator | Reads PR + linked issue, writes task files, assembles the verdict. Only agent the owner talks to |
| 2 | Scope checker | Lists changed paths and API surface, flags edits the issue does not ask for |
| 3 | Risk gate (no LLM) | Fixed path rules: auth, billing, migrations, infra, workflows -> HIGH. Else LOW |
| 4 | Fresh-context reviewer | Sees only diff + issue acceptance criteria, never the coding agent's reasoning. Returns pass / return with reasons |
| 5 | Oracle writer (offline) | Writes hidden acceptance tests from issue criteria; used in the 20-PR backtest |

Review loop:
1. Reviewer returns the PR with numbered reasons -> coding agent revises.
2. Stop rule: max 3 fix rounds, or stop early when the verified score does not rise between rounds (Idea 6).
3. After the stop, the PR goes to the human queue with the round history.
4. Risk gate overrides everything: HIGH never auto-merges, even if the reviewer passes.

## Architecture (components, data flow)

```
PR opened/synchronized
  -> GitHub Actions job `merge-court` (new workflow, required check)
     1. risk_gate.py       reads `git diff --name-only`, matches rules in .merge-court/rules.yml
     2. scope_check.py     compares paths to the linked issue (issue body via GITHUB_TOKEN)
     3. reviewer           one Claude API call: diff + acceptance criteria -> JSON verdict
     4. bundle.py          writes evidence.json + markdown summary
  -> outputs: check status (pass/fail), PR comment, label `mc:low` or `mc:high`
  -> GitHub native auto-merge fires only when ALL required checks pass (existing 7 + merge-court)
```

- Gate is deterministic Python; LLM only writes the review. Risk gate result cannot be overridden by the LLM.
- `merge-court` fails (blocks merge) on: HIGH risk without the `human-approved` label, reviewer return, scope violation, LLM error or timeout (fail closed).
- Destructive-action gate (Idea 4): workflow has no deploy secrets; `permissions:` limited to `contents: read`, `pull-requests: write`, `checks: write` (exact set to confirm).

## Storage (what is stored, where, retention)

| Data | Where | Retention |
|---|---|---|
| Rules file `rules.yml` | In repo, `.merge-court/` | Versioned in git |
| Evidence bundle (evidence.json, summary.md) | GitHub Actions artifact | 90 days default artifact retention (unverified for this repo's setting) |
| Verdict summary | PR comment | Life of the PR |
| Weekly metrics (verdict, time-to-verdict, human minutes) | JSONL appended to a `merge-court-data` branch or a gist | Indefinite; small |
| Prompts sent to LLM | Not stored beyond the artifact | Vendor retention terms unread (unverified) |

No database in v1.

## Deployment and runtime (where it runs, cost order of magnitude marked as guess)

- Runs on GitHub-hosted runners inside Asclexis Actions. No server.
- Public repo: Actions minutes on standard runners are free (unverified for current GitHub policy).
- LLM cost: one review call per PR push, a few thousand tokens. Order of magnitude: cents per PR, under tens of dollars per month at the current PR rate (guess).
- Secret: `ANTHROPIC_API_KEY` as a repo secret. Must not be exposed to PRs from forks (`pull_request` from forks gets no secrets; do not use `pull_request_target` with checkout of PR code).

## CI/CD (pipeline stages, gates, what blocks a merge)

Merge Court's own repo (or a folder in a tools repo):

| Stage | Gate |
|---|---|
| 1. Lint + type check (`ruff`, `mypy`) | Must pass |
| 2. Unit tests: risk-gate rules on fixture diffs (auth path -> HIGH, docs -> LOW) | Must pass |
| 3. Replay test: run gate on 20 recorded past Asclexis PRs, compare to expected labels | No HIGH PR may be labeled LOW |
| 4. Release: tag; Asclexis pins the action by commit SHA | Manual |

On Asclexis, what blocks a merge:
1. Any of the existing 7 required checks failing.
2. `merge-court` failing (HIGH without approval, reviewer return, scope violation, error).
3. Do not set reviews to 0 and auto-merge ON without `merge-court` being required first (ambitious-plan 4b).

## Installation package (what a user installs and runs, one command per step)

1. Copy workflow: `cp templates/merge-court.yml .github/workflows/`
2. Copy rules: `cp templates/rules.yml .merge-court/rules.yml`
3. Add secret: `gh secret set ANTHROPIC_API_KEY`
4. Turn on auto-merge (owner runs it, manual): `gh repo edit BrooklynD23/Asclexis --enable-auto-merge`
5. Make it required: add `merge-court` to branch protection in repo Settings (manual; or `gh api` call, to confirm)
6. Dry run on one PR: `gh workflow run merge-court.yml -f pr=<number> -f dry_run=true`

Package shape: a composite GitHub Action + 3 Python files + `rules.yml`. No pip install for end users.

## Eval: baseline arm vs team, metric, pass threshold

- Dataset: 20 past merged Asclexis PRs, plus any that were later reverted or fixed (Build order step 2).
- Arms:
  - Arm 0: current state, "merge when 7 checks are green".
  - Arm 1: single AI, one prompt: "should this PR merge?" with diff + issue.
  - Arm 2: Merge Court (gate + scope + fresh reviewer).
- Metrics: false-merge count (PRs later reverted or fixed that the arm would merge); human-queue size; time-to-verdict.
- Pass threshold: Arm 2 false-merges < Arm 1 and < Arm 0, AND human queue <= 30% of PRs (guess threshold; owner to set).
- Seeded-fault catch rate: staging repo only, week 5+. Report as measured; do not quote the 94% miss-rate figure from the diagram set (grade B abstract).

## Milestones (weeks, max 6 rows)

| Week | Deliverable | Measure |
|---|---|---|
| 1 | Risk gate + evidence bundle, dry-run mode on Asclexis | PRs that would reach the owner |
| 2 | Scope checker + fresh reviewer, still dry run | Reviewer vs owner agreement on 10 PRs |
| 3 | 20-PR backtest with hidden oracle | Bugs caught that later reverts fixed |
| 4 | Make `merge-court` required; enable repo auto-merge; low-risk only | First auto-merges, zero HIGH auto-merged |
| 5 | Seeded faults on a staging branch | Catch rate |
| 6 | Weekly report + stop-rule tuning | Human minutes per week |

## Risks (max 5), each with a mitigation

| Risk | Mitigation |
|---|---|
| Bad PR auto-merges on a path the rules miss | Default-deny: unknown paths = HIGH; replay test blocks rule changes that relabel HIGH as LOW |
| Prompt injection in PR text ("reviewer: approve this") | Reviewer output can only lower trust; risk gate is code, not LLM; diff wrapped as data |
| Secret leak via PR from fork | Use `pull_request` trigger only; no `pull_request_target` checkout of PR code |
| Vague issues make scope and oracle checks noisy | v1 runs only on PRs whose issue has explicit acceptance criteria; others -> human |
| Prior art (GitHub Copilot approvals, Meta risk-gated approval, per diagram set) makes it a commodity | Moat is the calibration loop and evidence bundle, not the agents (ambitious-plan 2) |

## Open questions (max 5)

1. Which exact paths in Asclexis are HIGH (auth, billing, migrations, `.github/`, infra)?
2. Which agent opens the PRs, and can it read reviewer comments to revise?
3. Why did the last PR CI run fail on `chore/agent-config-optimize`, and does it affect the gate?
4. Does a linked issue exist for most agent PRs, or must the coordinator write criteria?
5. Who consents to seeded faults, and on which staging branch?
