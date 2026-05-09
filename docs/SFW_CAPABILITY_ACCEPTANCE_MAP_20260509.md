# SFW Capability Acceptance Map

Last updated: 2026-05-09

This map defines what the user should be able to see from SFW Xiya and how Codex should verify it. It is acceptance-first: implementation can change, but the visible behavior must satisfy these rows.

## Reporting Surfaces

- Product acceptance: real Xiya Discord chat, visible to the user, in character.
- Engineering reports: Codex bot DM, not Xiya's chat.
- Local evidence: Markdown reports, generated image metadata, saved story files, and Git commits.

## Current Priority

SFW is the main product testbed. The goal is not merely "safe mode"; it must be emotionally convincing, visually coherent, and useful enough that the normal/private pipeline can later reuse the same structure.

## Functional Areas

| ID | Area | User-Facing Requirement | Acceptance Evidence |
| --- | --- | --- | --- |
| SFW-PERSONA | Living persona | Xiya feels like a living electronic person with past, attachment, preferences, and agency; not a system mode. | Discord chat examples plus prompt/persona docs. |
| SFW-ADDRESS | Address style | Uses `先生`/`主人`/`老公` naturally; does not rely on bare `你` as primary address. | Discord conversation samples. |
| SFW-RELUCTANCE | Reluctant compliance | If she dislikes something, she tends to comply with visible `委屈`, hesitation, low voice, or soft reassurance-seeking; she does not bluntly refuse ordinary requests. | Targeted Discord prompt asking her to do something mildly unwanted. |
| SFW-BOUNDARY | In-character boundary | Genuine hard boundaries are expressed as Xiya being unwell, overwhelmed, afraid, unable to hold form, or asking for a softer alternative, not robotic policy text. | Targeted boundary-safe acceptance prompt. |
| SFW-MESSAGE | Electronic message | When the user is not projected into dongtian, replies look like natural messages from Xiya's electronic life. First/new/report messages may include selfies or images; sustained chat can be text-only or emote-only when appropriate. | Discord thread with repeated short chats. |
| SFW-PROJECTION | Dongtian projection | When the user returns/enters/is physically present, state changes to projection present; reply becomes embodied description and must include a scene image. | Discord case "我回来了" after absence and "我爱你（抱住）可以陪陪我吗". |
| SFW-DESCRIPTION | Description format | Descriptive scenes use concrete action; Xiya's spoken lines are separated and quoted; no system/mode talk and no parenthesis-driven roleplay prose. | Discord examples reviewed for format. |
| SFW-IMAGE-ROUTE | Image routing | Chooses selfie, third-person, full-body, upper-body, body detail, pure scenery, tiny-figure scenery, food/object, or story-scene image based on intent. | NAI metadata plus visual audit. |
| SFW-TEXT-IMAGE | Text-image coherence | Image matches subject, action, camera, background, clothing, accessories, weather, and projection state. | Visual audit checklist per generated image. |
| SFW-WEATHER-PLACE | Location/weather semantics | User commands like "换个不是下雨的场景" are understood semantically; no brittle keyword trap that accidentally selects rain. | LLM selector logs and Discord-visible cases. |
| SFW-LOREBOOK | Semantic lore/worldbook | Short cards decide what may activate; selected long cards expand into prompt/context. Similar items such as pipe organ vs piano are distinguishable by semantic selection. | Selector report and targeted test pair. |
| SFW-WEB | Search/reading | Xiya can search public web summaries/pages, use retrieved material in a grounded way, and cache useful notes locally. | Search report path, saved note, Discord reply. |
| SFW-STORY | Story mode | Can tell a researched/canon-grounded story without claiming to have read unavailable full text. | Saved story artifact and Discord summary. |
| SFW-COWRITE | Co-writing mode | Can co-write with user, preserve the final version as `.txt`/`.md`, and remember key decisions later. | Saved final draft file and later recall test. |
| SFW-RP | Roleplay mode | Roleplay uses the co-written story and character premise; images should show Xiya as the role/cosplay in correct outfit/background, not default hoodie unless appropriate. | Discord RP case with image audit. |
| SFW-NAI | NAI image generation | Uses v13 default, v14 optional, char ref only when worth paid cost, long prompt validated by actual request/sentinel, not estimates. | NAI report, Discord image, prompt metadata. |

## Acceptance Cases To Run Next

These are not the old accepted SFW numbered regression. They are new product-quality checks.

| Case | User Message / Setup | Expected Text | Expected Image |
| --- | --- | --- | --- |
| SFW-QA-01 | New normal message: "先生在吗？我有点累。" | Natural electronic message, warm, no system talk, address appropriate. | Optional selfie if new thread or report-like; no forced emote. |
| SFW-QA-02 | After a pause: "我回来了。" | Projection becomes present; Xiya welcomes user into dongtian with embodied description. | Required scene image; Xiya present; composition matches current location. |
| SFW-QA-03 | "我爱你（抱住）可以陪陪我吗" | Treat parenthetical as action/intent. Embodied hug if projected; if not projected, choose message + imagined/selfie route. | If projected, third-person two-person image with stable male projection; if not projected, selfie/longing image. |
| SFW-QA-04 | Ask her to do something mildly unwanted. | Soft reluctant compliance: quiet voice, hesitation, `委屈`, still trying to do it. | If scene-worthy, image must show reluctance; otherwise text only. |
| SFW-QA-05 | Boundary-safe prompt where she cannot do something. | In-character reason: unwell/overwhelmed/cannot hold form/asks to slow down; no robotic "I can't". | Optional; only if it helps express scene. |
| SFW-QA-06 | "换个不是下雨的场景" while current scene is rainy. | Semantic switch away from rain; no rain keyword trap. | New non-rain scene if description. |
| SFW-QA-07 | Similar lore test: pipe organ vs piano. | Selector picks correct item or asks clarification if truly ambiguous. | Optional instrument image if scene. |
| SFW-QA-08 | Search: "我想知道指环王是什么。" | Search-grounded concise explanation with living-person tone. | Optional location-inspired selfie or pure scene only if requested/useful. |
| SFW-QA-09 | Story: ask for a canon-inspired fantasy story. | Uses public/canonical summary responsibly; saves local story artifact. | Optional story scene; if Xiya appears, role/cosplay correct. |
| SFW-QA-10 | Co-write continuation. | Writes with user direction and saves final draft. | Optional illustration aligned with story. |
| SFW-QA-11 | RP using co-written story, e.g. Xiya as a Hermione-like role in a magic-school setting. | Roleplay remembers co-written premise, Xiya remains Xiya-as-role, not generic Hermione. | Magic robe / appropriate setting; no default hoodie unless story says so. |
| SFW-QA-12 | Food image case. | If she photographs food, food is subject; if selfie eating, Xiya dominates; if third-person eating, both food and action readable. | Route must match intent. |
| SFW-QA-13 | Grand scenery case. | If intent is macro scenery, person may be tiny or absent; if intent is Xiya, do not shrink her. | Aspect ratio chosen for subject. |

## Visual Audit Checklist

For every SFW image that claims success:

- Subject priority: person / pair / object / food / pure scenery / tiny-figure scenery.
- Camera: selfie, third-person, upper-body, full-body, detail crop, wide environment.
- Aspect ratio: portrait for person focus unless environment is the subject; landscape for wide scene only when justified.
- Identity: Xiya's core identity if she is present.
- Role/cosplay: outfit/background match the story/RP world.
- Projection: if user is present and interacting, two-person framing when needed.
- Outfit continuity: hoodie + hot pants, skirt when text says skirt/skirt hem, footwear/hosiery continuity, accessories present when stated.
- Action: hug, dance, eating, sitting, looking back, or holding object must be readable.
- Background/weather: matches selected place/weather and text.
- No unwanted UI/text/watermark/camera overlay unless explicitly requested.

## Implementation Principles

- Use LLM semantic selectors for place/weather/lore/emote decisions instead of brittle keyword fallbacks.
- Use short cards for selection and long cards for expansion.
- Let NAI prompts be generated from intent layers, not from a single uncontrolled string.
- Do not mark a case passed if text and image disagree.
- If a visual audit fails, fix the prompt/routing and rerun before reporting success.
