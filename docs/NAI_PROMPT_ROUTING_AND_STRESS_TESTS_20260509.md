# NAI Prompt Routing And Stress Tests

Last updated: 2026-05-09

This document defines how SFW image prompts should be structured, routed, and verified. The goal is to keep the pipeline reusable for normal/private modes without turning SFW safety into brittle prompt walls.

## Prompt Layer Order

Keep prompt layers ordered and inspectable:

1. Character core / character reference.
2. Number of people and composition.
3. Camera / crop / aspect intent.
4. Action and expression.
5. Clothing, accessories, props, and global effects.
6. Scene, location, weather, time, and background.
7. Character rendering/material/skin/hair quality details.
8. Quality string.
9. Artist/style string.
10. Tail diagnostics for truncation tests only.

The artist/style string should stay near the end, but tail diagnostics can be appended after it during stress tests to prove the whole request survives.

## Character Reference Policy

Character Reference is useful but paid. Use it deliberately.

- Pure scenery: no Xiya character tags, no char ref.
- Pure food/object: no Xiya character tags, no char ref.
- Macro scenery with tiny figure: char ref usually not worth it unless Xiya identity matters.
- Xiya/person-focused image: char ref may be useful after composition is already validated.
- Body detail without face is still a character image and needs continuity; if no char ref, use long character/clothing string.
- Story/RP character acting: Xiya stays Xiya, but outfit/props/background become role/cosplay appropriate.

Compact char-ref scaffold:

```text
1girl, side braid, cat ears, cat tail, thigh strap, purple amethyst eyes
```

No-char-ref fallback must use the longer Xiya identity string so identity does not collapse.

Character Reference must be identity-audited. Prior failures included wrong hair color drift, such as purple hair or silver-white hair. A generated image does not pass just because it is attractive.

Required identity checks when Xiya is present:

- blue / light blue hair, not purple hair,
- purple/amethyst eyes,
- cat ears,
- cat tail,
- side braid when expected,
- overall face and body feel close to the provided reference,
- no unwanted character replacement by canon role.

Recommended workflow:

1. Validate composition without char ref using the long Xiya prompt.
2. Only when composition/action/background are acceptable, spend a small char-ref final check.
3. Use the user's compact scaffold with the reference image:
   `1girl, side braid, cat ears, cat tail, thigh strap, purple amethyst eyes`.
4. If identity drifts, stop and adjust. Do not keep spending char ref generations blindly.

## Known Style Strings

These are artist/style layers, not character strings.

### v3 flat-color style

Purified artist/style candidates from user-provided v3:

```text
1.3::atdan::, 1.3::mignon::, ask_(askzy), 0.7::rella, konya_karasue, artist:chen bin::, 0.5::ningen mame, t1kosewad::, {{flat color, pastel colors}}
```

Separate from v3:

- character/control: `1girl`, `solo`, `looking at viewer`, `white background`.
- quality: `masterpiece`, `quality`, `best quality`, `best absurdres`, `absurdres`, `very aesthetics`.
- negative/control: `-2::upscaled, blurry::`.

### v13 default human style

Purified artist/style candidates from user-provided v13:

```text
zhibuji loom, artist:betabeet, artist:mignon, liduke, rella, yoneyama mai, modare, artist:atdan, rella, konya karasue, :0.6::wlop::, artist:fuzichoco
```

Separate from v13:

- rendering/quality: `shiny skin`, `no text`, `2::very aesthetic::`, `4::masterpiece::`.
- negative/control/background: `-2::artist collaboration, water, simple background::` should not live inside artist/style unless intentionally used as a negative layer.

### v14 optional human style

User-provided v14, preserving weighting/repetition:

```text
[zhibuji loom], [[[artist:betabeet]]], {{artist:mignon}}, {rella,yoneyama mai}, {{{modare}}}, artist:atdan, {{rella,konya karasue}}, :0.6::wlop::, {artist:fuzichoco}
```

Separate from v14:

- rendering/quality: `shiny skin`, `no text`, `2::very aesthetic::`, `4::masterpiece::`.
- negative/control: `-2::artist collaboration::`.

## Food And Scenery Styles

Food and scenery must not accidentally inherit the human artist string just because the image request came from Xiya.

Routing:

- `human_focus`: v13 default, v14 optional, v3 for flat-color/Q-like output when requested.
- `food_focus`: use a food-specific style profile; no Xiya tags unless selfie/third-person eating.
- `pure_scenery`: use scenery-specific style profile; no Xiya tags.
- `grand_scenery_tiny_figure`: scenery profile first; optional tiny figure tags only if the mood needs scale.
- `story_location_selfie`: human profile plus canon-inspired location tags; Xiya dominates if selfie is the subject.

The user still needs to provide five preferred scenery examples/prompts. Until then, scenery styles are provisional and must be labeled as such.

The user provided five scenery prompt references on 2026-05-09. They establish a `grand_fantasy_concept` scenery style:

- masterpiece / best quality / ultra-detailed,
- epic scale,
- concept art,
- matte painting,
- wide shot,
- cinematic lighting,
- volumetric fog,
- towering cliffs,
- mist/clouds,
- white temple/church/sky-palace,
- open sky,
- foreground river/church/beach/ships,
- Raphael Lacoste-like environment direction.

Use this only for scenery/environment-first images. Do not append it after human v13/v14 portraits unless the scene is genuinely environment-led.

Food style remains its own domain and must be verified with:

- pure food still life,
- Xiya selfie with food,
- third-person Xiya eating food.

## Composition Rules

The image must serve intent:

- If Xiya is the subject, she dominates the frame.
- Conversation/selfie/emotion/cute action: close-up or upper-body focus.
- Clothing/role/cosplay/dance/full-body pose: full body if the outfit or movement matters.
- Leg/foot/hosiery/detail: crop the detail and preserve identity through clothing/continuity tags.
- Hug/two-person interaction: both people visible; stable male projection sparse tags.
- Environment-first: use wide/horizontal only when environment is the subject.
- Pure scenery: no character.
- Macro scenery with tiny figure: use only for wonder/scale/loneliness/epic feeling.

## Clothing And Accessory Stack

The pipeline must support long stacks without losing tail layers:

- base outfit,
- veil,
- blindfold,
- collar,
- bracelet,
- anklet,
- outerwear,
- footwear/hosiery,
- global mode such as dancing,
- action props such as piano or food.

Example stress case:

```text
Xiya, no char ref, old long identity string, blindfold, collar, bracelet, anklet, outerwear, elegant footwear/hosiery continuity, playing piano, holding or biting a slice of pizza, scene/weather/background, rendering/quality, v13 style, final red-box sentinel
```

## Long Prompt Validation

Do not estimate whether a prompt fits. NovelAI may still return an image while silently ignoring truncated tail content.

Validation methods:

1. Dry-run prompt assembly with visible layer lengths.
2. Actual NAI request metadata saved locally.
3. Tail sentinel placed at the true final end of the positive prompt during a stress test.
4. Visual audit checks whether the sentinel appears.
5. If the sentinel disappears, shorten or reorder layers and rerun.

Sentinel method:

- Put a simple, visually obvious red box/cube/sign at the true final end of the positive prompt.
- "True final end" means after every normal positive-prompt layer: not merely after object tags, not merely after artist/style, not merely after quality, and not before any later positive modifier.
- The sentinel must be the last positive concept in the final request payload.
- A visible sentinel proves at least the tail survived for that prompt.
- Remove the sentinel from production prompts.
- Do not rely on local tokenizers for acceptance. They are only rough diagnostics.
- Do not rely on OCR or judging whether the style "looks right". The pass/fail object should be visually obvious without reading text.

Maximum old-normal-mode structural stress case:

```text
long Xiya no-char-ref identity, role/cosplay outfit, veil, blindfold, collar/choker, bracelet, anklet, outerwear/cloak, dancing/global movement, piano or pipe-organ action, food prop in hand or near mouth, footwear/hosiery continuity, fantasy interior or magic-school scene, rendering/quality, v13/v14 artist/style, final red-box sentinel
```

This case is a SFW structural replacement for old normal-mode complexity. It must not copy unsafe content, but it must preserve the old pipeline's burden: many simultaneous equipment/action/scene constraints.

## Cost Rules

User has NovelAI Opus.

Treat as likely no extra Anlas when all are true:

- single image,
- normal size,
- 28 steps or fewer,
- no image base,
- no character reference.

Mark as paid/risky:

- Character Reference: `paid_5_anlas`.
- Image2Image / image base: `image_base_paid_risk` until verified.
- Any unknown new API feature: verify with official account/API behavior before assuming.

Cost acceptance:

- Text/model calls may cost money and are acceptable for validation, but should still produce useful evidence.
- Free-candidate NAI tests should be used first for prompt shape and composition.
- Paid char-ref tests should be rare, named, and recorded in metadata.

## Visual Audit Before Success

Do not report success until all relevant checks pass:

- subject priority,
- camera/framing,
- aspect ratio,
- identity,
- role/cosplay clothing,
- accessories,
- action,
- background/weather,
- text-image consistency,
- no unwanted UI/text,
- no missing limbs or broken anatomy that changes the meaning.

If a Harry Potter / magic-school RP image keeps Xiya in default hoodie when the role requires robes, that is a fail, not a pass.
