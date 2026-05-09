# TODO And Acceptance Board

Last updated: 2026-05-09

This is the durable project board. When the user gives a new requirement, update this file first or immediately after the current action. Do not rely on conversation memory alone.

## Status Legend

- `ACTIVE`: current mainline work.
- `NEXT`: queued soon.
- `BLOCKED`: cannot proceed until a concrete input or safety condition is met.
- `DONE`: accepted or verified; do not re-open unless a later change breaks it.
- `PARKED`: remembered idea, not current.

## Active

| ID | Status | Owner | Requirement | Acceptance The User Should See | Evidence / Current State | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| WF-01 | ACTIVE | Codex | Keep external memory updated so Codex does not lose the thread after compaction or sleep. | Future sessions read the entry docs first, update this board for new requirements, and close meaningful work with evidence. | Workflow scaffold completed and pushed in commit `3b44158`; ongoing maintenance remains active by design. | Keep these files updated whenever requirements change. |
| SFW-QUALITY-01 | ACTIVE | Codex + User | Upgrade SFW from a working safe mode into a polished primary product with strong text, images, autonomy, and memory. | User can review a current capability map, then provide preferred landscape examples/tags and desired functions; Codex turns them into acceptance tasks for text-image alignment, projection handling, autonomous messaging, and NAI scenery/food/person routing. | New requirement captured from user on 2026-05-09. DM report surface is available, so engineering reports should not pollute Xiya's main chat. | First explain current SFW capabilities and the exact asset/function inputs needed from the user. |
| SFW-TONE-ST-01 | ACTIVE | Codex + User | Use selected SillyTavern examples as tone/action references for Xiya's SFW personality, without copying unsafe content or polluting roleplay memory. | User can show preferred ST lines/actions; Codex extracts style principles such as intimacy, pacing, softness, action framing, and address style into SFW persona requirements. | User said the original motivation came from a liked ST card and will show non-explicit or manually cleaned examples. Local SillyTavern found at `E:\SillyTavern-1.15.0`, launched on `http://127.0.0.1:8000`. | Wait for user to show examples; then turn examples into a tone acceptance doc. |
| SFW-SCENERY-SELFIE-01 | ACTIVE | Codex | Expand SFW image routing beyond pure scenery/selfie/both-person basics. | Xiya can visually "visit" article/story/canon-inspired places as an electronic character: selfie with the location/object, cute pose in a grand setting, small-back-view landscape, pure scenery, food/object shots, or third-person scene depending on intent. | User clarified examples like Harry Potter / Lord of the Rings inspired locations, macro scenery with cute action, and scenic selfies. | Add image intent taxonomy and acceptance cases after receiving landscape examples/tags. |
| NAI-01 | ACTIVE | Codex | Improve NAI prompt pipeline without wasting prompt budget. | v13 default, v14 optional, style strings pure, quality separated, char ref gated, food/scenery/person routing separated, long prompts checked by actual request/logs. | `CURRENT_ACCEPTANCE_PLAN_20260509.md`; recent Discord NAI evidence IDs are recorded there. | Continue from latest pipeline, not old SFW numbered tests. |
| NAI-02 | ACTIVE | Codex | Map old normal-mode robot structure into the new pipeline shell. | Accessories/global modes such as veil, blindfold, collar, bracelet, anklet, outerwear, dancing are represented structurally; content can later be filled by DS. | Old docs/assets exist; not fully mapped in a single acceptance artifact yet. | Produce schema/map and actual maximum-length request log before claiming done. |
| NAI-LONG-PROMPT-01 | ACTIVE | Codex | Validate long no-char-ref prompts, not only compact char-ref prompts. | A worst-case prompt using the old long Xiya character string plus multiple accessories/global modes/actions/props still keeps the final sentinel tag visible in the generated image/request result. Example stress case: blindfold, collar, bracelet, anklet, outerwear, playing piano, pizza in mouth, plus scene/style/quality. | User approved the previous red-cube tail check and asked to place sentinel at the true final tail, even after quality tags. | Build actual maximum-length request logs and visual sentinel tests before claiming NAI prompt budget is safe. |
| CREATIVE-01 | NEXT | Codex | Story/co-writing/RP must persist useful memory and final drafts. | A story can be researched, co-written, saved locally, and later used for RP continuity. | Linked acceptance already has one report, but deeper long-form memory design remains. | Expand persistence design and run next visible end-to-end test when requested. |
| CLAUDE-DS-01 | BLOCKED | Codex + User | Use Claude Code shell with DeepSeek v4 pro only if isolated from existing Claude/Opus research data. | Dry-run shows separate HOME/APPDATA/TEMP and no original Claude data touched; real launch only when `claude` exists and DS key is set in isolated env. | Dry-run script/report exist; current shell lacks `claude` on PATH and `DEEPSEEK_API_KEY`. | Do not real-launch until prerequisites and isolation are confirmed. |

## Done / Accepted

| ID | Status | Result | Evidence |
| --- | --- | --- | --- |
| SFW-OLD-REGRESSION | DONE | Old SFW numbered Discord regression accepted as historical coverage. Do not keep re-running it as mainline. | `docs/SFW_DISCORD_ACCEPTANCE_TEST_LIST.md`, `docs/sfw_acceptance_matrix.md`, prior Discord-visible tests. |
| NAI-V13-V14-CLEAN | DONE | v13/v14 artist strings purified; repeated style names preserved; quality/control items separated. | `docs/CURRENT_ACCEPTANCE_PLAN_20260509.md`; Discord messages `1502758259285561365`, `1502755796239515900`. |
| NAI-CHARREF-SMOKE | DONE | NovelAI character reference call accepted; identity good; selfie UI/text issue recorded and negated for future. | Discord message `1502756291691413574`; marked `paid_5_anlas`. |
| CREATIVE-LINK-SMOKE | DONE | Story/co-writing/RP linked acceptance smoke test produced a saved local artifact. | `runtime_data/creative_acceptance/CREATIVE-LINK-REAL-20260509-01/report.md`, Discord message `1502751476957712477`. |
| CLAUDE-DS-DRYRUN | DONE | Isolation launcher dry-run created and did not launch real Claude. | `scripts/launch_claude_code_deepseek_isolated.ps1`, `runtime_data/claude_deepseek_isolation/deepseek_cc_isolation_dryrun_20260509_202144.json`, Discord message `1502752780388139050`. |
| GIT-INITIAL-REMOTE | DONE | Initial Git repository and GitHub remote are connected through a project-specific SSH key, without changing the old HTTPS account. First safe docs-only commit pushed to `main`. | Repo: `https://github.com/macnica0208/xiya-agent-dev`; commit `a33af1b`; remote `git@github-xiya:macnica0208/xiya-agent-dev.git`. |
| WORKFLOW-SCAFFOLD | DONE | Codex operating workflow is formalized: start-here read order, workflow loop, requirement intake template, closeout template, and board rules. | Commit `3b44158`; files `docs/CODEX_START_HERE.md`, `docs/WORKFLOW.md`, `docs/REQUIREMENT_INTAKE_TEMPLATE.md`, `docs/SESSION_CLOSEOUT_TEMPLATE.md`, `docs/TODO_ACCEPTANCE_BOARD.md`. |
| DISCORD-REPORT-DM | DONE | Engineering report surface is separated from Xiya's in-character channel. Codex/test bot can DM the user directly, and future engineering reports should use that route. | DM smoke message IDs `1502779119602106458` and `1502779570410094673`; helper script `scripts/post_codex_dm_report.py`; ignored runtime config `runtime_data/codex_report_dm_config.json`. |

## Parked But Remembered

| ID | Status | Requirement | Resume Condition |
| --- | --- | --- | --- |
| GH-CONNECTOR-01 | PARKED | Use GitHub connector for issues/PRs after repo exists. | User provides repo or asks Codex to create one through available GitHub tooling. |
| DISCORD-TEST-BOT-01 | PARKED | Use backup/codex bot as visible operator when testing Xiya. | Need confirmed token/session route; avoid noisy REST polling. |
| MEMORY-EXPAND-01 | PARKED | Let Xiya propose pending new place/weather/lore entries in correct format. | After semantic selection and world/lore schema stabilize. |

## Board Rules

- User acceptance lives here; implementation details can live in specialist docs.
- Do not delete completed rows immediately. Move them to `DONE` so future Codex can see they are settled.
- If a new user message conflicts with this board, update the board and note why.
- If Codex cannot prove a claim, keep the row `ACTIVE` or `BLOCKED`.
- Broad requests should be normalized through `docs/REQUIREMENT_INTAKE_TEMPLATE.md`.
- Meaningful sessions should close through `docs/SESSION_CLOSEOUT_TEMPLATE.md`.
