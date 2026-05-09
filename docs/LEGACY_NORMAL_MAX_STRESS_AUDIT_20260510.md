# Legacy Normal Max Stress Audit 2026-05-10

This is a sanitized audit of the old normal-mode NAI prompt surface. It is used only to derive SFW structural stress cases. Do not copy private/unsafe prompt text into this document.

## Source

- Dry-run command: `python -m xiya_agent_v2.legacy_normal_nai --dry-run --style-profile v13 --out-dir runtime_data\audit_legacy_normal_max_20260510_001 --case-mode all --width 1024 --height 1024`
- Output manifest: `runtime_data\audit_legacy_normal_max_20260510_001\discord_emote_manifest.json`
- Prompt count: 62
- Generation cost: none; dry-run only

## Findings

- Positive prompt length range: 1016 to 1645 chars.
- Average positive prompt length: about 1227 chars.
- Negative prompt length range: 1028 to 1106 chars.
- Average negative prompt length: about 1053 chars.
- Maximum active equipment-like slots in one generated case: 12.
- Active equipment-like slot distribution: 59 cases with 7 slots, 1 case with 8 slots, 1 case with 9 slots, 1 case with 12 slots.
- Partner / two-person visual cases: 10.
- Global visual-mode cases: 3.
- Cases depending on a global visual mode: 2.
- Style strings include weighted / grouped artist tags; these must remain separated from quality and render tags.

## Mechanisms Worth Reusing Or Re-designing

The old system is not a sacred source of truth, but it contains useful engineering ideas:

- Three-slot competition: active visual effects and lingering marks are not all injected. They compete for up to three visible slots.
- Priority first, recency second: stronger items win; ties prefer the more recent item.
- Body-part de-duplication: two candidates that fight for the same visual body area should not both be injected.
- Mark grouping: similar mark types can collapse into one aggregated visual tag instead of multiplying prompt length.
- Global modes override ordinary activities: when a global state is active, activity selection is constrained to compatible actions.
- Ability filtering: activities that need hands/legs/eyes/mouth are filtered when the state makes them impossible.
- Persistent anchors: some visual anchors stay present across activities unless a specific state hides them.
- Style purity: artist/style strings, render-material tags, and quality tags are separate concerns.

## Proposed SFW Mechanism Adaptation

- SFW visual stack should use a capped selector rather than blindly appending every requested tag.
- Default cap: three high-salience transient visual overlays after stable identity/outfit are already present.
- Candidate groups:
  - `mark_face`: cheek star, cheek heart, tiny face paint.
  - `mark_body`: glitter stickers, temporary arm/hand stickers.
  - `eyes`: blindfold / eye mask / dramatic eye effect.
  - `neck`: choker / collar / scarf-like accessory.
  - `wrist`: bracelet / wristband.
  - `ankle`: anklet / footwear-adjacent detail.
  - `outerwear`: coat / cloak / jacket overlay.
  - `action_mode`: dance / performance / role stance.
  - `role_costume`: magic robe, cloak, school uniform, fantasy outfit.
  - `prop`: food, instrument, book, wand, story prop.
- Selection rules:
  - Identity, hair/ears/tail, main outfit, and scene intent are protected.
  - If two SFW marks conflict visually, choose by priority then recency; e.g. a heart sticker can beat a star sticker in a romantic report, while a star sticker can beat a heart sticker in performance/fantasy.
  - If the subject is Xiya, scenery must not consume composition budget unless the scene itself is the intended subject.
  - If owner projection is not the action subject, keep him out of frame or implied.
  - If owner projection is the action subject, use exactly one faceless black-haired tall male owner projection and keep Xiya central unless the action requires equal focus.
  - If the prompt cannot fit all requested layers, drop or compress low-salience transient layers before identity, action, scene intent, or true-tail sentinel.

## Derived SFW Stress Dimensions

The old surface is mapped into neutral SFW dimensions:

- Persistent visual slots: choker/collar, wrist bracelet, anklet, eye/face layer, head/veil layer, footwear/hosiery continuity.
- Mark layer: star stickers, heart stickers, glitter stickers, temporary face paint, stage makeup.
- Outfit overlays: open coat, cloak, jacket, hoodie underneath, role costume visible under overlay.
- Global actions: dance/performance, roleplay costume state, movement state.
- Partner presence: exactly one faceless black-haired tall male owner projection when the scene action requires him.
- Props: instrument, food, book/wand/story prop, furniture or scene anchor.
- Scene/weather: magic-school hall, piano/pipe-organ distinction, warm dongtian room, rain/window, fantasy environment.
- Camera/aspect: portrait for people/action, detail crop for legs/feet, landscape only when environment is the subject.
- Tail budget: true final red cube sentinel after every positive layer.

## Current Max SFW Stress Candidate

No-char-ref, long character identity string, v13 style:

- Xiya as the visible main subject.
- Roleplay cosplay outfit matching a magic-school setting.
- Robe/cloak plus visible skirt/dress; no default hoodie unless explicitly requested.
- Veil, blindfold, choker, bracelet, anklet.
- SFW marks: cheek star sticker, cheek heart sticker, glitter stickers / temporary face paint.
- Outer cloak / jacket overlay without hiding the role costume.
- Dance/performance movement with skirt motion.
- Piano or pipe-organ prop depending on case; they must not collapse into each other.
- Food prop such as apple pie slice or plate when requested.
- Optional owner projection only for two-person cases; faceless, black hair, tall/strong, consistent.
- Fantasy/magic-school scene background.
- v13 artist style and quality split into their own layers.
- Final true-tail red cube at the absolute end.

## Status

- The red cube method works: a shorter control prompt showed the cube.
- Two old max-like roleplay stress images failed: the cube did not appear, so the prompt is not safe yet.
- Next step is to compress/rebuild the stress prompt from these actual dimensions, then rerun no-char-ref NAI and report each image by Codex DM.
- Paid character reference should be tried only once after the no-char-ref worst structure passes.
