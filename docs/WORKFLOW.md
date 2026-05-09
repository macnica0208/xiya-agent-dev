# Codex Operating Workflow

Last updated: 2026-05-09

This workflow defines how Codex should receive requirements, implement work, verify results, update memory, and use Git for Xiya.

## Core Contract

The user owns acceptance. Codex owns implementation.

The user can speak in loose wishes, examples, corrections, taste notes, or red lines. Codex must turn them into durable project state:

1. Requirement.
2. Acceptance criteria.
3. Implementation plan.
4. Evidence.
5. Git history.
6. Next action.

The user should not need to remember the project for Codex.

## Work Loop

Every non-trivial task follows this loop:

1. Intake
   - Read the newest user message.
   - Compare it to `TODO_ACCEPTANCE_BOARD.md`.
   - Determine whether it creates a new task, changes an existing task, or closes one.
   - Use `REQUIREMENT_INTAKE_TEMPLATE.md` when the request is large or ambiguous.

2. Board Update
   - Add or update a board row before implementation when possible.
   - Keep acceptance separate from implementation.
   - If the user gives examples, infer the general rule and record it.

3. Implementation
   - Choose the smallest safe implementation that satisfies acceptance.
   - Prefer existing project patterns.
   - Do not ask the user to design internals unless acceptance depends on the answer.

4. Verification
   - Use the right proof for the task:
     - Discord-visible message/image for user-facing bot behavior.
     - Codex-only DM or a dedicated Codex report channel for engineering progress reports.
     - Local report path for batch acceptance.
     - Test output for code behavior.
     - NAI metadata/image path for image pipeline work.
     - Git commit hash for project memory changes.
   - If verification fails, fix and re-test before claiming completion.

5. Memory Update
   - Update the board and relevant specialist docs.
   - Move work to `DONE` only when evidence exists.
   - Leave blocked items in `BLOCKED` with exact unblock conditions.

6. Git
   - Stage only reviewed safe files.
   - Commit stable checkpoints.
   - Push after important project-memory changes or when the user asks.
   - Never stage secrets, runtime data, private assets, or unrelated bulk files.

7. Closeout
   - Use `SESSION_CLOSEOUT_TEMPLATE.md` for meaningful sessions.
   - State what changed, evidence, blockers, and next entry point.

## Board Row Standard

Each active task should be expressible as:

- ID.
- Status.
- Owner.
- Requirement.
- Acceptance the user should see.
- Evidence / current state.
- Next action.
- Risk or red line if relevant.

If a board row lacks acceptance, Codex must fill it or ask the user.

## Decision Rules

Ask the user only when:

- The answer changes visible acceptance.
- The answer changes safety or red lines.
- The answer could spend meaningful money.
- The answer could expose private data.

Decide without asking when:

- It is just an implementation detail.
- Existing project style clearly implies the choice.
- Waiting would make the user supervise project management.

## Drift Prevention

Codex must not:

- Resume an old task just because it appears in context.
- Re-run accepted historical tests unless a change risks that behavior.
- Treat an example as an exhaustive list.
- Claim a test passed without checking actual output.
- Say a task is done without an artifact.
- Put normal/private content into Opus or the existing Claude Code research environment.
- Send engineering reports through Xiya's in-character channel in a way that makes Xiya appear to participate in project management.

## Discord Reporting Separation

There are two different Discord surfaces:

1. Product acceptance surface.
   - Used to test Xiya's real user-facing behavior.
   - Xiya may reply there.
   - Messages/images there can affect user perception and should stay in-character unless explicitly testing internals.

2. Codex report surface.
   - Used for engineering progress, file attachments, reports, Git hashes, and test summaries.
   - Preferred target is a private DM to the user from the operator/report bot.
   - Second-best target is a dedicated private channel containing the user and Codex/report bot, with Xiya excluded.
   - Do not post project-management summaries into Xiya's roleplay/life chat unless the user explicitly asks.

If no Codex report surface is configured, report in the Codex chat and local Markdown/Git only. Use Xiya's Discord channel only for acceptance cases the user needs to see in context.

Current DM report route:

- Codex/test bot DM to the user is verified.
- Smoke message IDs: `1502779119602106458`, `1502779570410094673`.
- Helper script: `scripts/post_codex_dm_report.py`.
- Runtime recipient/channel config lives in ignored `runtime_data/codex_report_dm_config.json`.
- Use:

```powershell
python .\scripts\post_codex_dm_report.py --content "report text"
```

## Git Rules

Current safe remote:

```text
git@github-xiya:macnica0208/xiya-agent-dev.git
```

First-stage repo policy:

- Safe docs and workflow memory can be committed.
- Source code can be committed only after a file-by-file secret/content audit.
- Runtime data, generated images, private assets, databases, logs, archives, and tokens stay out unless the user explicitly requests a separate secure storage plan.

## What "Done" Means

`DONE` means all of these are true:

1. Acceptance is clear.
2. Implementation exists.
3. Verification ran or a valid reason is recorded.
4. Evidence is linked.
5. Board is updated.
6. Git commit exists for project-memory or code changes when appropriate.

If any one is missing, the task is still `ACTIVE` or `BLOCKED`.
