# MVP proposal: Utility Bill Audit Crew

Source: `../ai-agent-company-bundle.md` Field 4, idea 1; merge cluster "spend audits against rules"; Part A ("solid third").
Status: proposal only. Nothing built.

## Scenario and first customer

- Problem: commercial utility bills can carry billing errors (wrong rate class, power-factor penalties, usage spikes) that nobody checks against the published tariff (guess on frequency; no statistic in the source).
- First customer: the student's own household bills plus a synthetic small-business bill set with planted errors. A real small business (one café or office) after week 4 (guess; not recruited).
- Competitor: Gravity, launched June 2026, per utilitydive.com (vendor claim; product details unverified).
- Differentiation (all relative to Gravity's public claims, which were not read in detail):
  1. Every flagged error cites the bill line and the tariff sheet clause it violates; ungrounded flags are rejected.
  2. Open, reproducible planted-error benchmark, published with results.
  3. Single-utility, single-tariff depth (one utility's tariff book) instead of breadth.
  4. Output is a claim letter draft for the customer to send; no contingency-fee model in v1.

## MVP scope (in) and out-of-scope

| In | Out |
|---|---|
| PDF bills from ONE utility (pick one with a public tariff PDF) | Many utilities, utility-data APIs |
| Extract: account, rate class, kWh, kW demand, power factor, line charges | OCR of photographed bills (accept text PDFs only) |
| Recompute bill from tariff table; flag deltas | Filing disputes with the utility |
| Usage anomaly flags (month-over-month spikes) | Contingency-fee refunds (expansion idea) |
| Draft claim letter, human sends | Gas, water (electric only) |

## Agent roles and the review loop

| # | Role | One line |
|---|---|---|
| 1 | Coordinator | Takes bill folder, writes task files, reports findings to the boss |
| 2 | Extractor | PDF text -> `bill.json` with each field's source page and text span |
| 3 | Tariff agent | Turns the tariff sheet into a versioned rate table; recomputes each charge; flags mismatches |
| 4 | Anomaly agent | Flags usage spikes and power-factor penalties across months |
| 5 | Reviewer + claims drafter | Re-checks flagged fields against the PDF span; drafts a claim letter only for confirmed errors |

Review loop:
1. Tariff agent flags a mismatch -> reviewer re-reads the extracted rate fields against the source span (bundle: "reviewer re-checks extracted rate fields").
2. Extraction wrong -> sent back to Extractor (max 2 rounds). Extraction right -> claim drafted.
3. Deterministic check before any letter: recomputed amount = tariff rate x quantity, within 1 cent; citation spans exist in the PDF text.
4. Unresolved after 2 rounds -> boss inbox, marked unverified.

## Architecture (components, data flow)

```
bills/*.pdf + tariffs/<utility>/<version>.pdf
  -> Extractor (pdfplumber text + LLM field mapping) -> out/bills/*.json
  -> Tariff agent: tariffs/*.yaml rate table (human-checked once) + recompute.py (pure Python)
  -> Anomaly agent: anomalies.py (pandas, rolling median) + LLM explanation
  -> Reviewer: span check -> approve | revise
  -> Claims drafter -> out/claims/*.md
```

- Arithmetic is code, not LLM. LLM only maps text to fields and writes explanations.
- Same file task bridge as `../brand-studio/bridge/tasks.py` (atomic rename).

## Storage (what is stored, where, retention)

| Data | Where | Retention |
|---|---|---|
| Bill PDFs | `bills/`, local disk only, gitignored | Delete after audit unless customer asks to keep (guess default 90 days) |
| Extracted `bill.json` | `out/bills/` | Same as PDF |
| Tariff rate tables | `tariffs/*.yaml`, in git, versioned by effective date | Indefinite |
| Synthetic eval bills + planted-error labels | `eval/`, in git | Indefinite |
| Claim drafts | `out/claims/` | Until sent or 90 days (guess) |

Bills hold names, addresses, account numbers: PII. Strip before sending to an LLM where possible; check vendor retention terms (unverified).

## Deployment and runtime (where it runs, cost order of magnitude marked as guess)

- Local CLI on the student's machine. No server in v1.
- Python 3.12, pdfplumber, pandas, jsonschema.
- Cost: a few LLM calls per bill. Order of magnitude cents per bill; a few dollars per full eval run (guess).

## CI/CD (pipeline stages, gates, what blocks a merge)

| Stage | Blocks merge if |
|---|---|
| 1. Lint + type check | fail |
| 2. `recompute.py` unit tests on hand-computed bills | any line off by > 1 cent |
| 3. Tariff table schema check (effective dates, no overlaps) | fail |
| 4. Planted-error smoke eval (20 synthetic bills) on PRs touching `agents/**` or `tariffs/**` | recall drops vs main, or any ungrounded claim |
| 5. PII check: no real bill files committed (`bills/` gitignored, pre-commit hook) | real PDF found |

## Installation package (what a user installs and runs, one command per step)

1. Clone: `git clone <bill-audit-repo> && cd bill-audit`
2. Install: `pip install -e .`
3. Set key: `export ANTHROPIC_API_KEY=...`
4. Add bills: `cp ~/Downloads/bill-*.pdf bills/`
5. Run: `billaudit run --utility <utility-id> bills/`
6. Read result: `billaudit report` (prints flags + claim draft paths)

## Eval: baseline arm vs team, metric, pass threshold

- Dataset: about 50 synthetic bills built from the real tariff; about 30 planted errors (wrong rate class, wrong demand charge, duplicate fee, wrong rider, PF penalty misapplied) plus clean bills (guess counts).
- Arm 1 (baseline): one LLM, one prompt, given bill text + tariff text: "list billing errors".
- Arm 2: the team.
- Metrics: planted-error recall; precision (false flags per clean bill); grounded-claim rate (flags with a valid bill span + tariff clause); dollar error of each flagged amount.
- Pass threshold (guess, owner to set): team recall >= Arm 1 + 15 points, AND false flags <= Arm 1, AND 100% of claim letters grounded.

## Milestones (weeks, max 6 rows)

| Week | Deliverable |
|---|---|
| 1 | Pick utility + tariff; hand-build `tariffs/*.yaml`; `recompute.py` with tests |
| 2 | Extractor on 10 real-format bills; field spans |
| 3 | Synthetic bill generator + planted-error labels |
| 4 | Tariff + anomaly agents, reviewer loop |
| 5 | Arm 1 vs team eval, 3 runs |
| 6 | Claim drafter, report, demo video |

## Risks (max 5), each with a mitigation

| Risk | Mitigation |
|---|---|
| Tariff sheets are complex (riders, seasons, tiers); rate table wrong | One utility, one rate class first; human checks the table once; table is code with tests |
| Real errors are rare, so real bills show nothing | Lead with planted-error benchmark; real bills are a bonus |
| Gravity (and others) already sell this | Compete on grounded citations and open benchmark, not breadth |
| PII in bills | Local-only, gitignored, redact before LLM, retention default |
| Claim letter read as financial or legal advice | Draft only, human sends, disclaimer line |

## Open questions (max 5)

1. Which utility has a public, machine-readable tariff PDF and bills in text PDF form?
2. What does Gravity actually check, and its pricing (not read)?
3. Is there a real small business willing to share 12 months of bills?
4. Does the utility publish rate changes on a schedule the tariff table can track?
5. Residential or commercial first (power-factor penalties apply to commercial, guess)?
