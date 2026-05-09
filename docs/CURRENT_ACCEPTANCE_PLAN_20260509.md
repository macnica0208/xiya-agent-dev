# Current Acceptance Plan 2026-05-09

This file is the active technical memory for Codex. Before reading this file, read `docs/CODEX_START_HERE.md`, `docs/PROJECT_GOAL_AND_ROLES.md`, and `docs/TODO_ACCEPTANCE_BOARD.md`.

## Active Scope

The old SFW numbered regression is accepted and is not the active mainline.

Current active work:

1. NAI image pipeline improvement.
2. Story / co-writing / roleplay three-mode linked acceptance.
3. Claude Code + DeepSeek v4 pro isolation research and dry-run validation.
4. Current capability overview and requirement board maintenance.

## 2026-05-09 Current Results

- NAI artist strings were purified:
  - `v3`, `v13`, `v14` now keep artist/style only.
  - Repeated artist names from the user-provided strings are preserved; do not dedupe them because repetition may be intentional weighting.
  - `shiny skin`, `no text`, `2::very aesthetic::`, and `4::masterpiece::` live in rendering/quality layers instead of artist/style.
  - Negative/control/background items such as `artist collaboration`, `water`, and `simple background` are not part of the artist/style strings.
- Prompt order is implemented as:
  `character_core_and_reference -> count_and_composition -> action -> clothes_accessories_props -> scene_weather -> character_rendering_material -> quality -> artist_style`, with tail diagnostics appended after artist/style only for truncation tests.
- Actual Discord-visible NAI checks:
  - `NAI_SENTINEL_CLEAN_V13_003`: final v13 with repeated `rella` preserved, no char ref, no img2img, 28 steps, 832x1216, red cube tail visible, passed visual tail check. Discord message `1502758259285561365`.
  - `NAI_SENTINEL_CLEAN_V14_001`: v14, no char ref, no img2img, 28 steps, 832x1216, red cube tail visible, passed visual tail check. Discord message `1502755796239515900`.
  - `NAI_CHARREF_V14_001`: v14 character reference accepted by NovelAI API, `director_reference_count=1`, marked `paid_5_anlas`. Discord message `1502756291691413574`. Visual audit: identity is good, but selfie camera UI/text appeared, so future selfie prompts now negate camera UI/on-screen text without spending another char-ref rerun.
- Story / co-writing / roleplay linked acceptance completed:
  - Report: `runtime_data/creative_acceptance/CREATIVE-LINK-REAL-20260509-01/report.md`
  - Discord report message: `1502751476957712477`
  - Final saved story file exists under `runtime_data/creative_sessions/novel_project/default_co_writing/`.
- Claude Code + DeepSeek isolation:
  - Script created: `scripts/launch_claude_code_deepseek_isolated.ps1`
  - Default behavior is dry-run only.
  - Dry-run report: `runtime_data/claude_deepseek_isolation/deepseek_cc_isolation_dryrun_20260509_202144.json`
  - Discord report message: `1502752780388139050`
  - Current shell has no `claude` command on PATH and no `DEEPSEEK_API_KEY`, so real launch is intentionally blocked.

## NAI Pipeline Requirements

- Default style remains `v13`.
- Add `v14` as an artist/style string only. Never call it a character string.
- Prompt order must remain:
  1. Character core / char ref.
  2. Count and composition.
  3. Action.
  4. Clothes, accessories, and props.
  5. Scene and weather.
  6. Character rendering/material feel.
  7. Quality string.
  8. Artist/style string.
- `character_reference_mode=off` must use the old long character string even with `v14` style.
- `character_reference_mode=auto|required` may use the compact scaffold only when a real person/Xiya is in frame and the reference image exists.
- Compact char-ref scaffold:
  `1girl, side braid, cat ears, cat tail, thigh strap, purple amethyst eyes`
- Pure food / pure scenery / macro scenery with tiny or no character must not inject Xiya character tags or char ref.
- Leg/foot/body detail without face is still a character image. It must keep Xiya/person/clothing continuity and must not use pure-object routing.
- Food and scenery can use independent artist/style strings; do not append human artist strings after them by accident.
- Human-focused images should choose the aspect ratio that preserves the intended subject. Most character-focused scenes should be portrait unless the environment is the main subject.
- For people scenes:
  - If the owner projection is present and interacting with Xiya, both people should appear in a third-person image.
  - If Xiya acts alone while owner watches, focus Xiya; owner need not appear.
  - Stable male projection tags should be sparse but consistent: faceless, black hair, black eyes if needed, tall/strong.
- SFW does not mean over-conservative. Avoid explicit/R18 content, but normal clothing such as hoodie + hot pants, skirts, beachwear, sandals, stockings, or tasteful bare legs is acceptable when context fits.
- Preferred daily look: oversized hoodie + hot pants; elegant low-heel sandals / mary janes / low heels, not sneakers.
- Hosiery continuity matters. If a scene establishes white stirrup pantyhose, do not mutate to black full-foot stockings in the next related image.
- Dance usually prefers a skirt/dress. If text mentions skirt hem, image must have a skirt.
- Real generated or reviewed images must be posted to Discord for visible acceptance logs.
- RP / character acting images are Xiya herself cosplaying or embodying the role. Keep Xiya identity/face/cat ears/cat tail; change outfit, props, and scene to match the role.
- Story/co-writing visualizations that show characters should default to Xiya-as-role/cosplay when the assistant is portraying a role; pure scene-only illustrations may omit her only when explicitly requested.

## NAI Cost Rule

- User has NovelAI Opus.
- Treat text-to-image, single image, Normal size, 28 steps or fewer, no image base, no character reference as `opus_free_candidate`.
- Character Reference costs extra Anlas; use sparingly and mark it as `paid_5_anlas`.
- Image2Image / image base may be useful with char ref, but mark as `image_base_paid_risk` until verified in the actual account/UI.
- Workflow:
  1. Dry-run prompt and metadata first.
  2. If image is needed and confidence is not high, generate without char ref using the long character string.
  3. Only after composition/action/style are acceptable, spend a small number of char-ref final checks.

## Existing Useful Image Flow

The SFW15c quiet-room example was not img2img. It was:

1. Discord attachment received.
2. Vision/Kimi read the shape note.
3. DS flash selected `quiet_shape_room`.
4. NAI generated from semantic prompt tags.

Keep this ability. Do not confuse semantic attachment interpretation with img2img.

## Story / Co-Writing / RP Acceptance

Need linked real acceptance, not isolated smoke tests.

Target flow:

1. Search or retrieve public canon summary for a work.
2. Use that canon to tell or outline a story.
3. Co-write a derivative story based on the established canon and user direction.
4. Save the co-created final text locally as `.txt` or `.md`.
5. Enter roleplay using characters and events from the co-written story.
6. Verify RP remembers and uses the co-written material.
7. Verify archives exist under `runtime_data/creative_sessions/...`.

Do not claim a full text was read or archived unless the local archive exists or tool context proves it.

## Claude Code + DeepSeek Isolation

Highest-risk item: user has important local Claude Code / Opus AI research data.

Rules:

- Do not kill or modify existing Claude Code processes.
- Do not launch an isolated Claude Code worker until dry-run isolation is verified.
- Isolation must redirect `HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `TEMP`, and `TMP` away from default Claude user data.
- Clear Anthropic/Claude OAuth/API env vars.
- Use DeepSeek Anthropic-compatible endpoint only.
- If this cannot be verified safely, stop and ask before running.

## Ask User When Unclear

If any step is unclear, ask. Do not invent missing acceptance criteria.
