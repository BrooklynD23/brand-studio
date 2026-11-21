# MVP proposal: Adversarial Clause Panel

Source: `../ai-agent-company-bundle.md` Field 3, idea 4; sweep Rank 5 (22/25); Part A ("judge can rubber-stamp", "legal liability", baseline closer to 3 without labeled data).
Status: proposal only. Nothing built.

## Scenario and first customer

- Problem: small-business buyers sign vendor contracts (SaaS, services) without counsel and miss one-sided clauses.
- Use: negotiation prep, not legal advice. Output: "clauses to push back on, with the quoted text and a suggested ask."
- First customer: the student, on public sample contracts and a labeled contract dataset. Real SMB user only after a lawyer reviews the disclaimer (guess).
- Existing: LaVern (free, Apache 2.0, May 2026; creator calls it a demo, per artificiallawyer.com via bundle). Commercial: Spellbook, Ironclad, Kira, Falcon (bundle Field 3; features unverified). Research versions of multi-agent legal debate exist (named in brief; not cited in bundle, unverified).
- Differentiation (guess):
  1. Risk scorer rejects any recommendation not tied to a quoted clause (deterministic quote check).
  2. Counterparty simulator argues the other side, so the user sees the likely pushback.
  3. Measured against a labeled dataset instead of demo contracts.

## MVP scope (in) and out-of-scope

| In | Out |
|---|---|
| One contract type: SaaS / services agreements, English, text or DOCX | Litigation, employment, real estate, consumer law |
| Top 10 risky clauses with quoted text and suggested ask | Redlining the document (Playbook Redliner is a separate idea) |
| Debate on disputed clauses, max 2 rounds | Jurisdiction-specific legal conclusions |
| Report with a "not legal advice" banner | Sending anything to the counterparty |
| Eval on a labeled dataset | Storing client contracts in the cloud |

## Agent roles and the review loop

| # | Role | One line |
|---|---|---|
| 1 | Coordinator | Takes the contract and the user's role (buyer), writes tasks, reports |
| 2 | Client advocate | Finds clauses that hurt the buyer, proposes asks, quotes each clause |
| 3 | Counterparty simulator | Argues why the vendor will refuse, also quoting the text |
| 4 | Risk scorer (reviewer) | Rejects ungrounded items; scores severity 1-3 with a reason |
| 5 | Judge | Final ranked list; must cite both sides' quoted text |

Review loop:
1. Deterministic grounding check first: every quote must appear verbatim (after whitespace normalize) in the contract. Fail -> back to author.
2. Advocate and simulator debate each disputed clause, max 2 rounds.
3. Anti-rubber-stamp: the judge sees items in random order, must state one reason to drop at least one item per contract, and its agreement rate is tracked (Part A risk).
4. Low-confidence or high-severity items flagged "ask a lawyer".

## Architecture (components, data flow)

```
contract.docx|.txt -> split.py (python-docx, clause segmentation by headings) -> out/clauses.json
  -> Advocate (LLM) -> out/advocate.json
  -> Simulator (LLM, different vendor if possible) -> out/counter.json
  -> Risk scorer: quote_check.py + LLM severity -> approve | revise
  -> Judge (LLM) -> out/report.md
```

- File task bridge as in `../brand-studio/bridge/tasks.py`.
- Contract text is wrapped as data in prompts (contracts can contain instruction-like text).

## Storage (what is stored, where, retention)

| Data | Where | Retention |
|---|---|---|
| Contracts | `contracts/`, local only, gitignored | Delete after run by default |
| Clause splits, debate logs, report | `out/<run-id>/` | 30 days (guess) or user deletes |
| Public sample contracts + labels | `eval/`, in git | Indefinite (license of dataset to check) |
| Prompts sent to LLM | not stored beyond run logs | Vendor retention terms unread (unverified) |

Contracts may be confidential. v1 uses only public samples.

## Deployment and runtime (where it runs, cost order of magnitude marked as guess)

- Local CLI. No hosted service in v1 (hosting real contracts raises privacy and liability).
- Python 3.12, python-docx, rapidfuzz (quote check), jsonschema.
- Cost: a 20-page contract, about 6-10 LLM calls. Order of magnitude under a dollar per contract (guess).

## CI/CD (pipeline stages, gates, what blocks a merge)

| Stage | Blocks merge if |
|---|---|
| 1. Lint + type check | fail |
| 2. `quote_check.py` tests (paraphrase rejected, exact passes, whitespace normalize) | any fail |
| 3. Clause splitter tests on 3 fixture contracts | wrong clause count |
| 4. Eval smoke on 10 labeled contracts, PRs touching `agents/**` | grounded rate < 100% or recall drops |
| 5. Disclaimer check: report template contains the banner | missing |

## Installation package (what a user installs and runs, one command per step)

1. Clone: `git clone <clause-panel-repo> && cd clause-panel`
2. Install: `pip install -e .`
3. Set key: `export ANTHROPIC_API_KEY=...`
4. Run: `clausepanel review contracts/vendor.docx --role buyer`
5. Open: `clausepanel open-report` (opens `out/<run-id>/report.md`)

## Eval: baseline arm vs team, metric, pass threshold

- Dataset: a public labeled contract dataset. CUAD (Contract Understanding Atticus Dataset) is a candidate (guess; license and fit not checked). Map its clause labels (e.g. cap on liability, termination for convenience) to "risky for buyer" by hand on 30 contracts.
- Arm 1: one LLM, one prompt: "list clauses a buyer should push back on, quote each".
- Arm 2: the team.
- Metrics: recall of hand-labeled risky clauses; grounded rate (quote found verbatim); false-flag rate; judge drop rate (rubber-stamp signal).
- Pass threshold (guess, owner to set): team recall >= Arm 1 + 10 points, grounded rate 100% vs Arm 1 measured, false flags <= Arm 1.

## Milestones (weeks, max 6 rows)

| Week | Deliverable |
|---|---|
| 1 | Pick dataset; label 30 contracts for buyer risk |
| 2 | Splitter + quote check with tests |
| 3 | Advocate + simulator + scorer loop |
| 4 | Judge + anti-rubber-stamp rules |
| 5 | Arm 1 vs team eval, 3 runs |
| 6 | Report, disclaimer review, demo video |

## Risks (max 5), each with a mitigation

| Risk | Mitigation |
|---|---|
| Legal liability / unauthorized practice of law | Negotiation-prep framing, banner, no jurisdiction conclusions, "ask a lawyer" flags; get a lawyer to read the disclaimer before any real user |
| Judge rubber-stamps | Random order, forced drop reason, track agreement rate; different model family |
| Hallucinated clauses | Deterministic verbatim quote check blocks them |
| Labels are subjective (what is "risky") | Two labelers on 10 contracts, report agreement |
| Free open-source rival (LaVern) | Publish the labeled eval; compete on measured recall and grounding |

## Open questions (max 5)

1. Is CUAD (or another dataset) licensed for this use, and does it fit SaaS contracts?
2. Who is the first real SMB user, and do they have counsel?
3. Which research and open-source multi-agent legal tools exist beyond LaVern (unverified)?
4. Buyer-only, or also vendor-side prep?
5. Does any jurisdiction's rule on unauthorized practice affect a free tool (unverified)?
