# Model routing: measured table (draft)

Date: 2026-11-20. Companion to `scope.md` section 9a. Status: draft; every "start" cell is a candidate until the week 5
eval measures it. Prices: per coordinator research on primary pages (verified) unless marked; per million tokens, input/output.

## Rules

1. Deterministic code first. A model runs only where code cannot do the job.
2. Start at the cheapest candidate that the task's needs allow (modality, context, speed); keep it if its measured pass
   rate meets the check threshold.
3. A failed check escalates one tier. The step log records task, tier, model, tokens and cost.
4. Two axes: difficulty (easy, medium, hard) and speed need (interactive: the owner is waiting in Default mode or a
   takeover; batch: owner-started Auto runs and the eval; no scheduled or unattended runs on Adobe apps, `scope.md` conflict 8).
5. Routed subtasks are single calls made by the companion's router with the customer's own keys. Role-level work (plans,
   scripts, copy) stays in the Herdr panes on the role's harness.
6. Measurement uses fixtures and Pillow renders only, never Adobe output (Developer Terms 6.16; `scope.md` conflict 5, closed). n = 50 per cell (guess).
7. Re-measure on any model, price or check change, and before each retirement date.

## Price and capability data

| Provider | Model | Price in/out | Notes |
|---|---|---|---|
| Anthropic | Fable 5.2 | $8/$40 | Top; adaptive thinking; hard reasoning |
| Anthropic | Opus 5.5 | $4/$20 | Default top. Retires Sep 22 2027 |
| Anthropic | Sonnet 5.5 | $2/$10 | Mid. Retires Sep 28 2027 |
| Anthropic | Haiku 5.5 | $0.10/$0.50 up to 100K input; $0.50/$2.50 above | Cheapest image-capable, fastest named. Retires Oct 7 2027 |
| OpenAI | gpt-6.2-astra | $8/$40 | Hard coding. Context 272K vs 1.05M: sources conflict, verify |
| OpenAI | gpt-6.2-sol | $2/$10 | Go-to coding |
| OpenAI | gpt-6.1-terra | $1/$5 | Vision, computer use |
| OpenAI | gpt-6-luna | $0.10/$0.50 | Cheapest vision; "fast" |
| OpenAI | gpt-5.4-mini | $0.75/$4.50 | - |
| OpenAI | gpt-5.4-nano | $0.20/$1.25 | Vision not stated: no vision tasks |
| Google | gemini-4-carbon | $2/$10; **$4/$20 from Dec 1 2026** | Strongest reasoning |
| Google | gemini-4-argon | $2/$10; **$4/$20 from Dec 1 2026** (same price as carbon) | Efficient |
| Google | gemini-4-neon | $3/$15 | - |
| Google | gemini-4-hydrogen | $1.50/$7.50 | No third-party confirmation |
| Google | gemini-3.8-flash | $0.75/$3.75; **rises Jan 1 2027** (new price not given) | - |
| Google | gemini-3.5-flash-lite | $0.30/$2.50 | Fastest 3.5; video input |
| Google | gemini-2.5-flash-lite | $0.10/$0.40 | Budget multimodal |
| Google | gemini-3.1-pro-preview | $2/$12 | Preview: not for routing |
| xAI | grok-4.7 | $2/$6 | Flagship; vision; reasoning; 500K. Terms unread (403): out of runtime |
| xAI | grok-4.1-fast | $0.20/$0.50 | Cheapest vision; **secondary source only**; 2M context. Out of runtime |
| xAI | grok-build-0.1 | $1/$2 | Coding. Out of runtime |
| Cursor | - | Not published | AUP reportedly bars automated access (unverified): build time only |

Price notes:
- OpenAI prices rise above 272K input tokens: keep routed prompts under 272K.
- Haiku 5.5 rises above 100K input: keep routed prompts under 100K.
- Google, Dec 1 2026: gemini-2.5-pro routes to 3.8 Flash; gemini-2.5-flash routes to 3.5 Flash-Lite. Plan with post-Dec-1
  prices: the week 5 eval runs after that date.
- Customer keys: Anthropic and OpenAI required; Google optional (eval; fallback judge, `scope.md` conflict 4); Grok only
  after its terms are read (B6). Antigravity is never a routing target or part of any multi-model agent (`scope.md` conflict 7).

## Tier ladders (runtime providers)

| Tier | Anthropic | OpenAI | Google (fallback judge, eval only) |
|---|---|---|---|
| Easy | Haiku 5.5 | gpt-6-luna | gemini-2.5-flash-lite |
| Medium | Sonnet 5.5 | gpt-6.1-terra (vision), gpt-6.2-sol (text, code) | gemini-3.5-flash-lite (video) |
| Hard | Opus 5.5, then Fable 5.2 | gpt-6.2-astra | gemini-4-carbon ($4/$20 from Dec 1 2026) |

## Per-task routing (draft; thresholds are guesses)

| Task | Difficulty | Speed | Deterministic first | Start | Escalate 1 | Escalate 2 | Pass check |
|---|---|---|---|---|---|---|---|
| Classification and routing | Easy | Interactive | Rules on task JSON fields | Haiku 5.5 or gpt-6-luna | Sonnet 5.5 | Human queue | 95% on 50 labelled tasks |
| JSON repair | Easy | Interactive | Parse + schema; structured output flags | Haiku 5.5 or gpt-6-luna | Sonnet 5.5 | Human queue | 100% schema-valid |
| Quote and citation checks | Easy | Batch | Exact and normalized match vs claims, banned facts | Haiku 5.5 or gpt-6-luna | Sonnet 5.5 or gpt-6.2-sol | Opus 5.5 | 98% on 50 claims |
| Vision pass/fail on a crop | Easy | Batch | Palette, brightness, aspect stats | Haiku 5.5 or gpt-6-luna | gpt-6.1-terra or Sonnet 5.5 | Opus 5.5 | 90% vs owner labels on 50 Pillow crops |
| Caption length and tone rewrite | Medium | Interactive | Word-boundary trim (length only) | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 | Stage 1 rules + tone judge, 90% |
| Copywriter (headline, caption, alt text) | Hard, kept expensive | Interactive | Length and banned-claim lint after | Opus 5.5 | Fable 5.2 | Human queue | Blind tone test (`scope.md` section 11) |
| Script (Reel: hook, beats, on-screen text) | Medium | Batch | Beat template; duration math | Sonnet 5.5 or gpt-6.2-sol | Opus 5.5 | Fable 5.2 | Fits 15-90 s (guess); no banned facts; voice check |
| Director plan (shot list, order, in/out, pacing) | Hard | Batch | ffprobe durations and sizes; keyframe extraction | Opus 5.5 (keyframes as images) | Fable 5.2 | Human queue | Valid against the clip inventory; owner rating |
| Brand assets (wordmark cards, lower thirds) | Medium | Batch | Layout presets and colors from the profile | Sonnet 5.5 | Opus 5.5 | Human queue | Stage 1 color and type rules |
| Brand critic judgment (stage 2; non-Adobe assets and copy only, `scope.md` conflict 5) | Hard, kept expensive | Batch | `critic.py` stage 1 | Codex, gpt-6.2-sol (guess) | Codex, gpt-6.2-astra | Fallback judge: Gemini (gemini-4-carbon), else Claude Opus 5.5 flagged same-vendor | `scope.md` section 11 |

Speed rule: interactive cells prefer the fastest named model in the tier (Haiku 5.5, gpt-6-luna); batch cells may wait for
the cheaper option. Batch APIs at a discount are a later option (not measured; unverified for these models).

## What the week 5 eval fills in

Per cell: pass rate with a 95% interval, cost per completed task (including escalations), p50 latency. The router then
writes `runs/routing.json`: per task, the cheapest model whose lower interval bound meets the threshold.
