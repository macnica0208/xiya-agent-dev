# Current Task Board 2026-05-09

This older task board is retained for context. The canonical current board is now `docs/TODO_ACCEPTANCE_BOARD.md`.

This board supersedes the old SFW numbered regression as the active work plan.

## Current Scope

1. Provide a current capability overview for the user.
2. Improve the NAI pipeline:
   - Add character reference carefully.
   - Keep style versions as artist/style strings only.
   - Separate prompt layers.
   - Add food and scenery artist strings.
   - Keep pure food/scenery free of Xiya character tags and char ref.
   - Reference old normal-mode robot assets and map multi-prop, play, accessory, and global modes.
   - Ensure long combinations do not overflow prompt budgets.
3. Verify the three creative modes:
   - Story.
   - Co-writing.
   - Roleplay.
   - Include web/search, reading memory, local archive, and RP continuity.
4. Research and verify Claude Code isolated DeepSeek v4 pro usage:
   - DeepSeek through Anthropic-compatible endpoint.
   - Separate profile and worktree.
   - No data pollution into Opus/current Claude Code research.

## No Longer Active As Mainline

The old SFW00-SFW10 numbered regression is no longer the main driver. It can remain as historical regression coverage, but do not spend the user's time re-running it unless a new change directly risks those mechanics.

## Discord Visibility Rule

Use real Discord only for the current task's meaningful acceptance:

- NAI image samples that the user needs to inspect.
- Story/co-writing/RP end-to-end proof.
- Any mode/command check needed for the new work.

Do not keep sending old SFW numbered test messages.

## NAI Prompt Layer Order

1. Character core and char reference.
2. Count and composition.
3. Action.
4. Clothes, accessories, and props.
5. Scene and weather.
6. Character rendering/material feel.
7. Artist/style string.
8. Quality string.

## Explicit User Reminders Captured

- `v13`, `v14`, etc. apply to artist/style strings only.
- Character strings are not style versions.
- Char ref costs money; only use it when a person is present and it is worth testing.
- Character-ref scaffold should be short.
- Suggested compact scaffold: `1girl, side braid, cat ears, cat tail, thigh strap, purple amethyst eyes`.
- Possible optional color hints for cat ears/tail are okay; silver tips are not useful.
- Food and scenery styles should be independent.
- Normal-mode mapping should include accessories such as veil, blindfold, collar, bracelet, anklet, outerwear, and global modes such as dancing.
- SFW assets and pipeline remain Codex-owned; normal-mode content can be written by DS, but Codex owns structure and format.
