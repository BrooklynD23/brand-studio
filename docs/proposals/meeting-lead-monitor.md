# MVP proposal: Public Meeting Lead Monitor

Source: `../ai-agent-company-bundle.md` Field 15, idea 1; sweep Rank 1 (23/25); Part A ("runner-up", baseline closer to 3).
Status: proposal only. Nothing built.

## Scenario and first customer

- Problem: local reporters cannot watch every city council, school board and planning meeting. Leads get missed.
- First customer: one beat (e.g. one city council + its planning commission) for a student newspaper or one local reporter (guess; not recruited).
- Source evidence: Connecticut Public did similar work (LMA award 2025, per bundle).
- Existing (bundle): Local Lens, SeeGov, City Meetings NYC. Named by the brief but not in the bundle and not checked: Civic IQ, WallFly, GovSpend (unverified what each does).
- Differentiation (guess, since competitors were not read):
  1. Every quote and figure in a brief carries a transcript timestamp; mismatches are rejected, then marked unverified.
  2. Max 3 leads per meeting, so the reporter reads a short list, not a summary.
  3. Open-source, runs for one beat at near-zero cost.

## MVP scope (in) and out-of-scope

| In | Out |
|---|---|
| One body's meetings from a public video/agenda page | Many jurisdictions, scraping at scale |
| Transcribe (or use published captions) | Live-stream real-time monitoring |
| Up to 3 leads per meeting, each with timestamped quotes | Writing publishable articles |
| Brief as markdown + one Slack/email message | Paid newsroom product |
| Human queue for unverified items | Sentiment or "who's lying" judgments |

## Agent roles and the review loop

| # | Role | One line |
|---|---|---|
| 1 | Coordinator | Takes the beat config, schedules runs, reports to the boss |
| 2 | Ingest | Detects new uploads, downloads audio or captions, produces timestamped transcript |
| 3 | Lead flagger | Picks up to 3 newsworthy items per meeting with reasons (vote, money, conflict, new project) |
| 4 | Brief writer | Writes a timestamped brief per lead |
| 5 | Quote verifier (reviewer) | Matches every quote and figure to transcript text at its timestamp |

Slack router from the bundle is a 10-line script, not an agent.

Review loop:
1. Verifier does a fuzzy match of each quote against the transcript window (+-30 s, guess) and exact match for numbers.
2. Mismatch -> back to Brief writer once (bundle: "mismatches return once").
3. Still failing -> item goes to the human queue marked UNVERIFIED.
4. Known weakness: "is this a good lead" has no ground truth; the verifier checks facts, not newsworthiness.

## Architecture (components, data flow)

```
beat.yaml (body name, video page URL, agenda URL)
  -> Ingest: yt-dlp or direct download -> faster-whisper (local) or captions -> out/transcripts/*.json (segments with start/end)
  -> Lead flagger (LLM) + agenda PDF text -> out/leads/*.json
  -> Brief writer (LLM) -> out/briefs/*.md
  -> Verifier: rapidfuzz match + number regex -> approve | revise | unverified
  -> router.py -> Slack webhook or email
```

- Transcription is the slowest step; local Whisper avoids per-minute API cost (guess on speed on the student's machine).
- Task bridge: same file pattern as `../brand-studio/bridge/tasks.py`.

## Storage (what is stored, where, retention)

| Data | Where | Retention |
|---|---|---|
| Downloaded audio | `cache/audio/`, gitignored | Delete after transcription |
| Transcripts | `out/transcripts/` | Keep (public record, small) |
| Leads, briefs, verifier results | `out/` JSON/MD | Keep for eval |
| Hand-labeled lead sets | `eval/`, in git | Indefinite |
| Slack webhook URL | env var | Never in git |

All inputs are public meeting records. Check each site's terms for downloading video (unverified).

## Deployment and runtime (where it runs, cost order of magnitude marked as guess)

- v1: local CLI, run by cron or by hand after each meeting.
- v2: a scheduled GitHub Actions job for captions-only beats (Whisper on CPU runners may be too slow, guess).
- Cost: LLM on a 2-3 hour transcript, a few calls. Order of magnitude under a dollar per meeting (guess). Whisper local: free, compute-bound.

## CI/CD (pipeline stages, gates, what blocks a merge)

| Stage | Blocks merge if |
|---|---|
| 1. Lint + type check | fail |
| 2. Verifier unit tests (paraphrased quote, wrong number, wrong timestamp) | any fail |
| 3. Fixture run: 2 short recorded transcripts end to end, no network | crash or schema fail |
| 4. Eval smoke on 5 labeled meetings for PRs touching `agents/**` | quote accuracy drops at all |

## Installation package (what a user installs and runs, one command per step)

1. Clone: `git clone <meeting-monitor-repo> && cd meeting-monitor`
2. Install: `pip install -e .` (includes faster-whisper, yt-dlp, rapidfuzz)
3. Install ffmpeg: `sudo apt install ffmpeg`
4. Set key: `export ANTHROPIC_API_KEY=...`
5. Configure beat: `cp beat.example.yaml beat.yaml` and edit the URLs
6. Run: `meetmon run --beat beat.yaml --latest`

## Eval: baseline arm vs team, metric, pass threshold

- Dataset: 10 past meetings of the chosen body. A human (student or partner reporter) labels the "real leads" by checking what local outlets later covered (proxy ground truth, guess).
- Arm 1: one LLM given the full transcript, asked for 3 leads with quotes.
- Arm 2: the team.
- Metrics:
  - Quote/figure accuracy: share of quotes and numbers that match the transcript (deterministic; headline).
  - Lead hit rate: share of the 3 leads that match a later-covered story (proxy).
  - Unverified rate and reporter minutes per meeting.
- Pass threshold (guess, owner to set): team quote accuracy >= 98% and > Arm 1; lead hit rate >= Arm 1.

## Milestones (weeks, max 6 rows)

| Week | Deliverable |
|---|---|
| 1 | Pick beat; ingest + transcripts for 10 past meetings |
| 2 | Verifier (deterministic) with tests |
| 3 | Lead flagger + brief writer; review loop |
| 4 | Label 10 meetings; Arm 1 vs team eval |
| 5 | Router to Slack/email; one live meeting end to end |
| 6 | Report + demo video |

## Risks (max 5), each with a mitigation

| Risk | Mitigation |
|---|---|
| No ground truth for "good lead" | Headline the checkable metric (quote accuracy); use later coverage as a proxy |
| Whisper errors on names and numbers | Prefer official captions or minutes when present; verifier marks low-confidence segments |
| Crowded market (Local Lens, SeeGov, others unverified) | Narrow to one beat, open-source, verified quotes |
| Site terms forbid downloading video | Check terms per site; use captions/minutes where download is not allowed |
| Misquote published by a reporter | Brief is a lead, not copy; every quote links to the timestamp for the reporter to check |

## Open questions (max 5)

1. Which body and which reporter or student paper is the first customer?
2. What do Civic IQ, WallFly and GovSpend actually do (not in bundle, unverified)?
3. Does the body publish captions or minutes, or only video?
4. Slack or email for delivery?
5. Who labels the 10 eval meetings, and how many hours does that take?
