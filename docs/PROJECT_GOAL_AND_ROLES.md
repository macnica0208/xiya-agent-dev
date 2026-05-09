# Project Goal And Roles

Last updated: 2026-05-09

## Product Goal

Build Xiya into a reliable Discord-first companion and creative agent. The user should be able to state desired effects and acceptance expectations, while Codex owns the engineering path, testing, documentation, and state tracking.

The project should not depend on the user remembering every subsystem. Codex must keep a durable external memory in Markdown and update it whenever requirements change.

## Division Of Labor

### User

The user owns acceptance:

- What the final behavior should feel like.
- What visible Discord messages, images, files, or reports are acceptable.
- Taste decisions for character, images, tone, and mode behavior.
- Red lines, especially around data isolation and cost.

The user does not need to:

- Remember every old requirement.
- Design every implementation detail.
- Re-explain accepted work.
- Watch every test step unless the test needs human taste judgment.

### Codex

Codex owns delivery:

- Turn user wishes into concrete requirements.
- Update `TODO_ACCEPTANCE_BOARD.md` before and after meaningful work.
- Pick implementation details when safe.
- Implement code, docs, scripts, tests, and reports.
- Verify behavior locally and, when needed, through real Discord-visible tests.
- Maintain a clear record of what passed, failed, or remains risky.
- Push back when the literal request conflicts with the user's deeper goal.

Codex should think, not merely mirror. If the user says something that is likely shorthand, Codex should infer the intended product behavior and record the interpretation.

### DeepSeek / Isolated Worker Agents

DeepSeek or other worker agents can help with normal/private content after isolation is safe.

Allowed role:

- Draft normal/private asset wording.
- Fill content details under Codex-owned schemas.
- Suggest prose, lore entries, NAI tags, and mode-specific packs.

Not allowed role:

- Touch the user's existing Claude Code / Opus research data.
- Decide repository structure without Codex validation.
- Bypass Codex's format checks.
- Leak private/high-risk content into shared SFW docs or Opus contexts.

## Main Product Surfaces

### SFW Side

Codex fully owns SFW:

- Pipeline.
- Persona and reply contract.
- NAI image routing and assets.
- Discord delivery order.
- Visible acceptance.
- Regression tests.

SFW means non-explicit, not sterile. Normal clothing, beachwear, skirts, hoodie plus hot pants, tasteful bare legs, stockings, food, scenery, dancing, companionship, and affectionate non-explicit scenes are allowed when context fits.

### Normal/Private Side

Codex owns the shell:

- Mode commands and routing.
- Schemas.
- File placement.
- Asset manifests.
- Discord delivery order.
- Validation and reports.

DeepSeek/isolated workers may own the concrete content after the isolation plan is proven.

### Creative Modes

Story, co-writing, and roleplay are real product modes, not decoration.

Expected shape:

- Story mode can use search or local reading memory as canon/inspiration.
- Co-writing mode saves durable drafts and final versions locally.
- Roleplay mode preserves roles, setup, and continuity.
- Shared creative material should be reusable by later story/RP sessions.

## Red Lines

- Protect the user's existing Claude Code / Opus research data. If safe isolation cannot be proven after serious effort, abandon that route and use a safer alternative such as a VM, separate Windows user, or separate toolchain.
- Do not commit secrets, API keys, Discord tokens, NovelAI keys, private assets, or runtime data to Git.
- Do not force the user to supervise implementation details.
- Do not restart completed old test lines unless a new change makes them relevant.
- Do not invent completion. Evidence is required.

