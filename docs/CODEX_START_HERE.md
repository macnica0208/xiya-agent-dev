# Codex Start Here

Last updated: 2026-05-09

This is the first file Codex must read before continuing Xiya work. Its job is to prevent context drift after compaction, sleep, interruption, or a new session.

## Read Order

Read these files in order before making non-trivial changes:

1. `docs/CODEX_START_HERE.md`
2. `docs/PROJECT_GOAL_AND_ROLES.md`
3. `docs/WORKFLOW.md`
4. `docs/TODO_ACCEPTANCE_BOARD.md`
5. `docs/CURRENT_ACCEPTANCE_PLAN_20260509.md`
6. Relevant specialist docs only when the active task needs them:
   - `docs/REQUIREMENT_INTAKE_TEMPLATE.md`
   - `docs/SESSION_CLOSEOUT_TEMPLATE.md`
   - `docs/deepseek_claude_code_isolation.md`
   - `docs/SESSION_REQUIREMENTS_20260509.md`
   - `docs/CURRENT_TASK_BOARD_20260509.md`
   - `docs/LEGACY_NORMAL_NAI_PIPELINE_20260508.md`
   - `docs/SFW_DISCORD_ACCEPTANCE_TEST_LIST.md`

If these files disagree, use this priority:

1. Newest explicit user message.
2. `TODO_ACCEPTANCE_BOARD.md`.
3. `WORKFLOW.md`.
4. `PROJECT_GOAL_AND_ROLES.md`.
5. `CURRENT_ACCEPTANCE_PLAN_20260509.md`.
6. Older historical docs.

## Per-Turn Ritual

Before acting:

1. Identify the newest user request. Do not continue an older task just because it is familiar.
2. Compare the request with `TODO_ACCEPTANCE_BOARD.md`.
3. If the request adds, changes, or cancels work, update the board.
4. Use `REQUIREMENT_INTAKE_TEMPLATE.md` for broad requests.
5. Separate acceptance from implementation:
   - Acceptance is what the user must see or approve.
   - Implementation is Codex's responsibility unless the user explicitly wants to choose.
6. If ambiguity changes acceptance, ask a short question.
7. If ambiguity is only implementation detail, choose conservatively and document the choice.

During work:

1. Keep visible proof for important claims:
   - Discord message ID for visible bot tests.
   - Report path for local validation.
   - Image path / metadata for NAI samples.
   - Git command output or commit hash for Git work.
2. Do not mark a task complete without evidence.
3. Do not re-run old accepted SFW numbered tests unless a new change directly risks them.

Before final response:

1. Update `TODO_ACCEPTANCE_BOARD.md` if status changed.
2. Use `SESSION_CLOSEOUT_TEMPLATE.md` for meaningful sessions.
3. Mention what changed, what was verified, and what remains.
4. If something is blocked, name the exact blocker and the next safe action.

## Current Mainline

The old SFW numbered regression was accepted. It is historical coverage, not the current mainline.

Current mainline:

1. Durable workflow memory docs and acceptance board.
2. NAI prompt pipeline improvement:
   - v13 default.
   - v14 available.
   - char reference gated by cost and used only when useful.
   - food/scenery/person routing kept separate.
   - normal-mode old asset mapping still needs structure validation.
3. Story / co-writing / roleplay persistence and linked acceptance.
4. Claude Code + DeepSeek isolation, with original Claude/Opus research data protected.
5. Git/GitHub safe version-control workflow.

## Drift Guards

- Do not say "done" without a file path, test artifact, Discord ID, commit hash, or explicit reason no artifact applies.
- Do not treat the user's examples as exhaustive. Infer the real product need and record it.
- Do not make the user remember project state. The board is the memory.
- Do not let implementation details leak into Xiya's in-character Discord replies.
- Do not use brittle keyword fallbacks for semantic mode/place/play/weather routing when an LLM decision layer is available.
- Do not put normal/private content into Opus or the user's existing Claude Code research environment.
