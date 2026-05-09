# NAI True-Tail Sentinel Status 2026-05-10

This document records the first real NovelAI true-tail sentinel checks after the user clarified the correct validation method.

## Rule

The sentinel must be the final positive-prompt concept, not merely the final object/action/style layer.

Pass/fail is visual:

- If the red cube appears, the positive prompt tail survived for that request.
- If the red cube does not appear, do not claim long-prompt safety.
- Do not rely on local tokenizer estimates or OCR.

## Generated Checks

### NAI-TAIL-TRUE-END-20260510-001

- case: `roleplay_scene`
- style: `v13`
- character reference: off
- image base / img2img: off
- steps: 28
- size: 832x1216
- anlas risk: `opus_free_candidate`
- positive estimated tokens: 527
- image: `runtime_data/nai_tail_acceptance/NAI-TAIL-TRUE-END-20260510-001/sfw_roleplay_scene_v13_charref-off_20260509_232016.png`
- metadata: `runtime_data/nai_tail_acceptance/NAI-TAIL-TRUE-END-20260510-001/sfw_roleplay_scene_v13_charref-off_20260509_232016.json`

Visual audit:

- Red cube: absent.
- Some stress items appeared: veil, blindfold, skirt/dress, pizza, piano, blue hair, cat tail.
- Several required scene/action details failed or weakened: magic-school stone hall not clear; prompt did not prove tail survival.

Result: FAIL.

### NAI-TAIL-TRUE-END-20260510-002

- case: `roleplay_scene`
- style: `v13`
- character reference: off
- image base / img2img: off
- steps: 28
- size: 832x1216
- anlas risk: `opus_free_candidate`
- positive estimated tokens: 542
- image: `runtime_data/nai_tail_acceptance/NAI-TAIL-TRUE-END-20260510-002/sfw_roleplay_scene_v13_charref-off_20260509_232141.png`
- metadata: `runtime_data/nai_tail_acceptance/NAI-TAIL-TRUE-END-20260510-002/sfw_roleplay_scene_v13_charref-off_20260509_232141.json`

Change from 001:

- Removed explicit `red cube` phrases from negative prompt.
- Strengthened sentinel to bottom-right foreground floor prop.

Visual audit:

- Red cube: absent.
- Stress adherence got worse: piano, pizza, and magic-school stone hall not visible.

Result: FAIL.

### NAI-TAIL-CONTROL-20260510-001

- case: `dongtian_status`
- style: `v13`
- character reference: off
- image base / img2img: off
- steps: 28
- size: 832x1216
- anlas risk: `opus_free_candidate`
- positive estimated tokens: 389
- image: `runtime_data/nai_tail_acceptance/NAI-TAIL-CONTROL-20260510-001/sfw_dongtian_status_v13_charref-off_20260509_232234.png`
- metadata: `runtime_data/nai_tail_acceptance/NAI-TAIL-CONTROL-20260510-001/sfw_dongtian_status_v13_charref-off_20260509_232234.json`

Visual audit:

- Red cube: clearly visible on floor at lower right.
- Confirms the sentinel method works when the prompt is not too overloaded.

Result: PASS as control.

## Current Conclusion

The true-tail sentinel method is valid, but the current maximum old-normal-mode structural stress prompt is too heavy or too conflicted to pass. It is not acceptable to claim prompt budget safety yet.

Next required work:

1. Compact repeated identity/outfit/composition language.
2. Split or compress stress dimensions without losing required coverage.
3. Keep the final red cube as the last positive concept.
4. Re-run the long stress image until the red cube appears and the main required items remain visible.
5. Only after the no-char-ref prompt shape passes should paid character reference be used for final identity checks.
