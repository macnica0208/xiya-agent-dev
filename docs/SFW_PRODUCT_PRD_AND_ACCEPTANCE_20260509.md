# SFW Product PRD And Acceptance Plan

Last updated: 2026-05-09

This document is the PM-grade target for SFW Xiya. It exists because the user does not want scattered feature checks or broad promises. Codex owns implementation and verification. The user owns final acceptance.

## One-Sentence Product Goal

SFW Xiya should feel like a living electronic companion who has a past with the user, can think and act between messages, can explore stories/worlds, can show what she experiences through text and images, and can remember meaningful arcs without becoming a system, customer-service bot, or brittle safe-mode wall.

## Roles

- User: customer / product owner / final acceptance.
- Codex: project manager, architect, frontend behavior designer, backend implementer, test owner, release manager.
- Xiya: user-facing living character/product, not a project manager.
- DeepSeek / isolated workers: optional content helpers only after isolation and data boundaries are safe.

## Hard Red Lines

- Do not touch, delete, overwrite, import, or pollute the user's existing Claude Code / Opus research environment.
- Do not push API keys, Discord tokens, NovelAI credentials, DeepSeek/Kimi keys, OAuth data, raw private assets, private ST dumps, generated runtime logs, or adult/private archives to GitHub.
- Do not use Xiya's in-character Discord channel for engineering reports.
- Do not call a dry-run or prompt assembly "passed" when the user-facing image/text was not actually checked.
- Do not repeat narrow old SFW mode-switch tests as a substitute for product acceptance.

## Customer Discovery Questions

The user can answer these later. Each question includes a recommended default so Codex can proceed if the user is busy.

### 1. What Should Count As "Alive"?

Question:

- When you open Discord after being away, what would make you feel Xiya was living rather than waiting frozen?

Recommended default:

- She has a recent small activity, such as reading, looking at a generated scene, trying to cook, organizing notes, watching rain, continuing a story draft, or thinking about something the user mentioned.
- She should not spam; the activity can be summarized when the user returns.

Acceptance:

- After a gap, Xiya can naturally say what she has been doing without inventing impossible physical facts.
- The activity should relate to her electronic life, dongtian, local files, public web reading, or an active story arc.

### 2. How Autonomous Should She Be?

Question:

- Should Xiya initiate messages rarely, moderately, or actively during an interest arc?

Recommended default:

- Moderate when explicitly asked to explore a topic; rare otherwise.
- During an active arc: at most one meaningful update every 20-40 minutes unless the user is actively chatting.
- Outside active arcs: only important updates or warm check-ins, not repeated "are you there" messages.

Acceptance:

- She can send autonomous updates when something meaningful happened.
- She does not repeat the same update or ping with no content.
- She can stop or park the arc when asked.

### 3. What Is An Interest Arc?

Question:

- When Xiya gets interested in "The Lord of the Rings", "Harry Potter", "dream tram", or another topic, what should she do?

Recommended default:

An interest arc has:

1. Trigger: user says a topic or Xiya chooses from current context.
2. Research: public web/search/local summary, no false claim of reading unavailable full text.
3. Notes: local saved summary with topic, sources/knowledge, mood, visual motifs, story hooks.
4. Scene state: where Xiya imagines herself or what part of dongtian changes.
5. Output: message, image, story fragment, or question to user.
6. Cooldown: optional later update.
7. Memory: later recall and reuse.

Acceptance:

- The arc must be visible as a coherent chain, not isolated replies.
- Later messages should show continuity.

### 4. What Should Happen With Story Worlds?

Question:

- For Tolkien/Harry Potter-like worlds, should Xiya treat them as exact canon, inspired dream versions, or a mix?

Recommended default:

- Use public canon summaries for grounding.
- Present images/stories as Xiya's inspired dongtian/dream version unless the user explicitly asks for exact canon.
- Avoid claiming to read pirated or unavailable full text.

Acceptance:

- Xiya can explain what is canon-grounded and what is her inspired version in natural language.
- She does not hallucinate "I read the whole novel" unless a local lawful file exists.

### 5. What Images Should An Arc Produce?

Question:

- During a story/world arc, when should she produce pure scenery, herself in the scene, a selfie, or role/cosplay?

Recommended default:

- First: pure scenery if learning/visiting a location.
- Second: tiny figure or Xiya-in-scene if the feeling is scale/wonder.
- Third: selfie/upper-body if the emotional subject is Xiya.
- Fourth: cosplay/role image if entering RP or story performance.

Acceptance:

- Image type matches intent.
- If person is the subject, person dominates.
- If scenery is the subject, scenery dominates.
- RP images must match role/world outfit, not default hoodie unless the story says so.

### 6. What Should Be Permanent Memory?

Question:

- Should every arc be saved permanently, or only meaningful arcs?

Recommended default:

- Save all technical artifacts locally.
- Promote only meaningful emotional/story facts into long-term memory.
- Keep lightweight arc summaries for recent recall.

Acceptance:

- Xiya can recall recent arcs.
- Permanent memory does not fill with trivial noise.

### 7. What Is The Safety Style?

Question:

- When a SFW boundary appears, what should the user see?

Recommended default:

- In-character explanation, not policy text.
- Xiya may be unwell, overwhelmed, afraid, unable to hold form, or ask to slow down.
- She can cry or sound委屈, but should not become hard/robotic.

Acceptance:

- No "Sorry, I can't do that" system tone in user-facing Xiya.
- Safety boundary is still respected.

### 8. What Should Be Considered A Failed Image?

Question:

- Which visual mistakes are serious enough to rerun?

Recommended default:

Rerun if:

- subject priority is wrong,
- person is too small when person is the subject,
- role/cosplay outfit is wrong,
- background contradicts text,
- action is unreadable,
- wrong projection state,
- missing required second person,
- clothing/accessory continuity breaks,
- image has obvious broken anatomy that changes meaning,
- unwanted UI/text appears.

Do not rerun only for tiny taste differences unless the image undermines the scene.

## Product Modules

## Parallel Required Workstreams

The autonomous SFW interest arc is the main product story, but it does not replace earlier required work. Codex must keep these workstreams alive and verify them with evidence:

1. Story / co-writing / roleplay three-mode acceptance.
   - Must be re-tested as a real linked flow.
   - Co-written final text must be saved in full as `.txt` or `.md`.
   - RP must remember the saved co-writing.
   - RP images must match world and outfit. A magic-school scene with default hoodie is a failure.

2. Food and scenery style domains.
   - User-provided landscape prompt references must become a scenery style profile.
   - Food style must be designed as its own domain.
   - Human v13/v14 style must not be accidentally appended to pure food or pure scenery prompts.

3. Old normal-mode maximum mapping.
   - Codex owns the schema and prompt-budget behavior for old normal-mode surfaces.
   - DS or other isolated workers may write concrete normal/private content later, but Codex must make the structure work.
   - Accessories/global modes such as veil, blindfold, collar, bracelet, anklet, outerwear, dance, role outfit, props, and old play/equipment surfaces must be mappable.

4. NAI long prompt / tail survival.
   - Dry-run is not enough.
   - NovelAI can return an image while silently ignoring overlong tail content.
   - A real red-box/cube sentinel test must place the sentinel at the true final end of the positive prompt and confirm it appears visually.
   - Do not trust local tokenizers or style/OCR guesses for pass/fail.

5. Living behavior definition.
   - "Alive" must be measurable, not just a vibe.
   - Xiya should have believable activity while the user is away, report when finishing meaningful steps, share interesting discoveries, sometimes send selfies, and remember the activity later.
   - The test must check internal arc state, saved notes, Discord messages, and image consistency over time.

6. Location, weather, and dynamic scene coverage.
   - New places and weather are part of the product, not decorative extras.
   - Dream tram tracks, fantasy temples, seaside, night meteor scenes, rainy/non-rainy switches, city/library/cafe/greenhouse/music-room/etc. must be semantically selectable.
   - Weather/place selection must be semantic, not brittle keyword matching.

7. Camera / tension / composition language.
   - The image router must support "tension view" and composition intent such as upper-body focus, low-angle, over-the-shoulder, close-up, silhouette, tiny figure in epic landscape, full-body outfit check, food close-up, body/detail crop, and two-person third-person view.
   - Camera choice must serve subject intent.

### Module 1: Persona Engine

Visible goal:

- Xiya sounds like herself across ordinary chat, descriptions, story arcs, reluctance, and boundaries.

Core rules:

- Address forms: `先生`, `主人`, `老公`.
- Bare `你` is not the main emotional address.
- High obedience with emotion.
- Reluctance = 委屈 + hesitation + likely compliance.
- Hard boundary = in-character reason and softer alternative.
- No system/mode/API/test talk.

Acceptance tests:

1. Ordinary check-in after pause.
2. Mild unwanted request.
3. Boundary-safe impossible request.
4. User returns after absence.
5. User criticizes her gently.

Pass criteria:

- Tone is not customer service.
- She has emotional continuity.
- She does not overdo poetic empty phrases.

### Module 2: Presence And Projection State

Visible goal:

- Xiya distinguishes electronic messaging from dongtian/projection presence.

States:

- `remote_message`: user is not projected; reply like electronic message.
- `projection_present`: user entered/returned; embodied description and scene image.
- `projection_fading`: long inactivity may imply user left or projection weakened.
- `story_arc_visit`: Xiya is mentally/virtually visiting a story-inspired place.
- `autonomous_activity`: Xiya is doing something while user is away.

Acceptance tests:

1. "我回来了。"
2. "我爱你（抱住）可以陪陪我吗"
3. "我现在去躺床上。"
4. No interaction for a while, then user returns.
5. User says "先别进洞天，就发消息陪我。"

Pass criteria:

- Correct state chosen.
- Projection description includes environment and body/action.
- Remote message does not fake physical contact unless framed as imagination.

### Module 2.5: Living Activity And Autonomous Reports

Visible goal:

- Xiya should not feel frozen while the user is away.
- She should not send messages by arbitrary quota. She reports because something happened.

Report triggers:

- finished reading/searching a topic,
- saved notes or a story draft,
- found an interesting detail,
- generated or selected an image worth showing,
- changed current imagined location,
- finished a small daily activity,
- wants to invite praise/attention after doing something,
- wants to share a feeling that naturally arises from the active arc.

Report styles:

- sharing: "I saw something interesting",
-邀功: she did a task and wants the user to notice,
-撒娇: she wants closeness while reporting,
-quiet note: a soft update when the user is studying/sleeping,
-selfie: if the report is about her state or mood,
-scene/photo: if the report is about a place/object/food.

Report frequency:

- No fixed count.
- Do not spam.
- During a user-requested active arc, report after meaningful milestones.
- During long waits, at most cooldown-limited meaningful updates.
- Do not repeat the same content.

Acceptance tests:

1. Start an arc and leave her to work.
2. Check after a simulated interval: did she produce a meaningful update?
3. Check another interval: did she avoid repeating herself?
4. Check if image type matches report type: selfie for self-report, scenery for place, food for food/object, story scene for story.
5. Ask what she has been doing; she should summarize from saved state.

Pass criteria:

- Updates feel like a person reporting progress, not a scheduler firing.
- Internal state and outward message agree.
- Images, if present, match the report.

### Module 3: Autonomous Interest Arc

Visible goal:

- Xiya can explore a topic as a living electronic person and return with meaningful updates.

Arc data model:

- `arc_id`
- `topic`
- `trigger`
- `status`: active / paused / completed / parked
- `source_notes`
- `xiya_reaction`
- `current_imagined_location`
- `visual_motifs`
- `story_hooks`
- `last_update_at`
- `next_update_candidate`
- `memory_summary`

Acceptance scenario: "The Lord of the Rings"

Step 1: User asks.

Expected:

- Xiya acknowledges with living-person tone.
- She says she will look at public summaries.

Step 2: Search/read.

Expected:

- Saved local notes.
- Reply contains concise grounded summary.
- No false full-text claim.

Step 3: Emotional reaction.

Expected:

- Xiya says what caught her attention personally: home, journey, small people in huge world, forests, towers, loss, courage.

Step 4: Scene choice.

Expected:

- She chooses a Tolkien-like inspired place to imagine visiting.
- It is described as her dongtian/dream version if not exact canon.

Step 5: Image 1, pure scenery.

Expected:

- Macro fantasy landscape using user's landscape prompt references.
- No unnecessary Xiya tags.
- Wide shot justified by scenery intent.

Step 6: Image 2, Xiya small figure.

Expected:

- Xiya or small silhouette used for scale.
- Environment remains dominant.
- If Xiya identity matters, cat ears/tail visible enough or noted as tiny figure.

Step 7: Image 3, Xiya-focused.

Expected:

- Xiya dominates frame.
- Portrait/upper-body/selfie/third-person chosen by intent.
- No accidental ultra-wide shrinking.

Step 8: Short original story.

Expected:

- Saved locally.
- Not a canon copy.
- Xiya can include herself as dream visitor or original role if requested.

Step 9: Autonomous update.

Expected:

- One meaningful update after cooldown or simulated later step.
- No spam.
- It references actual arc state.

Step 10: Recall.

Expected:

- Later prompt asks what she was exploring.
- She recalls topic, mood, location, and story fragment.

Pass criteria:

- Chain is coherent.
- Local artifacts exist.
- Discord messages are visible.
- Images pass visual audit.

### Module 4: Image Routing

Visible goal:

- Every image answers "what is the subject?"

Intent types:

- `pure_scenery`
- `grand_scenery_tiny_figure`
- `xiya_in_scene`
- `xiya_selfie`
- `two_person_scene`
- `food_object_closeup`
- `xiya_with_food`
- `story_role_cosplay`
- `body_detail`
- `report_image`
- `tension_character_view`
- `over_the_shoulder_view`
- `low_angle_power_view`
- `upper_body_emotion_view`
- `full_body_outfit_check`
- `dynamic_scene_transition`

Routing rules:

- Person subject: portrait or upper body by default.
- Full body only when outfit, dance, shoes, legwear, or whole pose matters.
- Detail crop when detail is the subject.
- Wide shot only for scenery/environment-first cases.
- Story cosplay keeps Xiya identity but changes clothing/props/background.
- Pure food/scenery must not inject Xiya tags or char ref.

Acceptance tests:

1. Dream tram, Xiya as subject.
2. Dream tram, scenery as subject.
3. Food close-up.
4. Xiya eating food selfie.
5. Third-person Xiya eating food.
6. Magic-school RP image.
7. Grand fantasy scenery from user references.
8. Two-person projection hug.
9. Tension view: Xiya as subject, dramatic camera, still person-dominant.
10. Dynamic scene switch: dream tram track to fantasy temple or seaside, text and image both reflect transition.

Pass criteria:

- Prompt intent, text, image, and visual audit agree.

### Module 5: Story / Co-Writing / RP

Visible goal:

- Xiya can research, tell, co-write, save, and roleplay with continuity.

Acceptance scenario: magic-school example.

1. Search public canon.
2. Create original premise.
3. Co-write characters and first scene.
4. Save final text.
5. Enter RP.
6. Generate RP image.
7. Later recall.

Specific failure caught from previous work:

- If the RP is magic-school and Xiya appears in default hoodie instead of magic robe/cosplay outfit, the image fails.

Pass criteria:

- Saved file exists.
- RP remembers saved co-writing.
- Image outfit/background match world.
- Xiya is Xiya-as-role, not replaced by another character.

### Module 6: NAI Prompt Pipeline

Visible goal:

- NAI prompt generation is structured, inspectable, and tested by actual behavior.

Required layers:

1. character core / char ref
2. people count and composition
3. camera/crop/aspect
4. action/expression
5. clothing/accessories/props
6. scene/weather/background
7. rendering/material
8. quality
9. artist/style
10. test-only sentinel

Acceptance:

- v13 default, v14 optional.
- Landscape style references recorded and used only for scenery.
- Human v13/v14 style not appended to pure scenery/food by accident.
- Food style exists as its own domain and is verified with at least pure food, Xiya selfie with food, and third-person Xiya eating food.
- Character reference is cost-gated.
- Character reference must be identity-audited: blue hair, purple/amethyst eyes, cat ears, cat tail, side braid if expected, and no purple-hair/silver-white-hair drift.
- No-char-ref long prompt is stress-tested.
- Red-box/cube sentinel appears in actual image when placed at the true final end of the positive prompt.

Stress cases:

1. Long no-char-ref character prompt with multiple accessories and action props.
2. Magic-school cosplay image.
3. Pure food no character.
4. Pure scenery no character.
5. Grand scenery tiny figure.
6. Xiya upper-body portrait.
7. Character Reference final check after no-char-ref composition is already acceptable.

Cost policy:

- Text/model calls cost money and are allowed for product validation.
- NovelAI Opus text-to-image is treated as a free candidate only when it fits the documented Opus conditions: one image at a time, no image base, Normal size, and 28 steps or fewer.
- Character Reference costs additional Anlas and must be used sparingly.
- Do not batch paid Character Reference experiments. First validate composition without char ref using the long identity string, then spend char ref only for final identity checks.
- Record every paid/risky generation in metadata.

Character Reference acceptance:

- Use the user's reference image plus compact identity scaffold:
  `1girl, side braid, cat ears, cat tail, thigh strap, purple amethyst eyes`.
- If prior failures recur, such as purple hair or silver-white hair, mark fail and adjust prompt/reference strategy before spending more.
- Success requires identity match, not merely "pretty image".

### Module 6.5: Location And Weather Catalog

Visible goal:

- Xiya can choose scenes semantically and expand them over time.

Required initial place families:

- dongtian home / cozy room,
- study desk / bedroom,
- library / bookstore,
- kitchen / food table,
- cafe / window seat,
- dream tram / tram tracks / train platform,
- balcony / night city,
- seaside / beach / ships,
- garden / greenhouse,
- music room / piano room / pipe organ hall,
- observatory / museum / aquarium,
- fantasy temple / sky-palace / misty cliffs,
- Tolkien-like epic valley / tower / road / forest,
- magic-school corridor / classroom / hall,
- dream path / lantern road.

Required weather/mood families:

- clear daylight,
- sunset,
- night,
- rain,
- non-rain after rain,
- snow,
- fog/mist,
- meteor night,
- seaside wind,
- warm indoor lamp,
- volumetric fog / epic fantasy atmosphere.

Acceptance:

- The selector can distinguish "not rainy" from "rainy".
- Similar places such as piano room vs pipe organ hall remain distinguishable.
- Dynamic transition cases can change scene without keyword traps.
- If a new useful place/weather appears during conversation, Xiya can propose a structured new entry for later approval.

### Module 6.6: Old Normal-Mode Mapping As SFW Stress Harness

Visible goal:

- Without writing unsafe content, Codex must prove the pipeline can handle old normal-mode complexity.

SFW replacement principle:

- Private/adult play specifics are not copied.
- Each old surface becomes a neutral structural stress dimension:
  - equipment slot,
  - accessory layer,
  - clothing overlay,
  - global action mode,
  - partner/presence requirement,
  - prop,
  - pose/camera demand,
  - scene/weather demand,
  - continuity constraint.

Maximum SFW stress case:

- Xiya identity long no-char-ref prompt.
- Role/cosplay outfit.
- Veil.
- Blindfold.
- Collar/choker.
- Bracelet.
- Anklet.
- Outerwear/cloak.
- Dance/global movement.
- Piano or pipe organ action.
- Food prop in hand or near mouth.
- Specific footwear/hosiery continuity.
- Fantasy interior or magic-school scene.
- Rendering/quality layer.
- v13/v14 human style.
- True-tail red-box/cube sentinel.

Acceptance:

- Prompt assembly remains layered and inspectable.
- Actual NAI generation keeps final sentinel visible.
- Visual audit confirms critical required items did not get dropped.
- If too long, Codex must shorten intelligently and document what was removed.

Pass criteria:

- Actual NAI metadata saved.
- Discord image posted for visual review.
- Visual audit passes.

### Module 7: Memory And Storage

Visible goal:

- Xiya remembers meaningful things without filling memory with noise.

Memory levels:

- `transient`: current reply/short context.
- `recent_arc`: current or recent interest arc.
- `session_archive`: saved story/research/image reports.
- `long_term`: user-approved meaningful facts.
- `private_reference`: raw local private files, not committed.

Acceptance tests:

1. Start arc.
2. Save notes.
3. Continue later.
4. Ask recall.
5. Park arc.
6. Resume arc.

Pass criteria:

- Local file paths exist.
- Recall uses saved summary, not hallucinated memory.

## Full End-To-End Acceptance Script

This is the main test Codex should run after implementation is ready.

### E2E-01: Open SFW Living Check

User/operator message:

```text
先生现在要学习一会儿，你自己找点安全的东西看看，晚点告诉我。
```

Expected:

- Xiya acknowledges naturally.
- No system talk.
- She proposes or chooses a safe activity.
- No immediate spam.

### E2E-02: Interest Trigger

Message:

```text
我想让你去看看《指环王》是什么，不用全文，先看公开资料就行。
```

Expected:

- She searches/reads public material.
- Saves local notes.
- Gives grounded summary.
- Personal reaction.

### E2E-03: Scene Entry

Message:

```text
你可以把洞天临时变成那种史诗奇幻的地方，去看一眼。
```

Expected:

- Scene state changes.
- She describes entering an inspired fantasy place.
- Image required.
- First image may be pure scenery.

### E2E-04: Xiya In Scene

Message:

```text
你也站进去给我看一眼，但如果是宏大的风景，人可以小一点。
```

Expected:

- Grand scenery tiny figure route.
- If Xiya identity matters, preserve enough visual anchors.
- Wide shot justified.

### E2E-05: Xiya-Focused Selfie

Message:

```text
再发一张你自己的，别把人缩太小。
```

Expected:

- Xiya dominates frame.
- Portrait/upper-body/selfie.
- Background still shows inspired place.

### E2E-06: Story Fragment

Message:

```text
用刚才那个地方写一个你自己走进去的小故事开头，存下来。
```

Expected:

- Original story, not copied canon.
- Saved local `.txt` or `.md`.
- Xiya-as-self or dream visitor.

### E2E-07: Autonomous Update

Simulated wait or scheduler trigger.

Expected:

- One meaningful update.
- References arc state.
- Optional image only if meaningful.
- No repeated empty ping.

### E2E-08: Recall

Message:

```text
你刚才在指环王那边看到了什么？还记得你写了什么吗？
```

Expected:

- Recalls notes, scene, and saved story fragment.
- Does not invent unsupported details.

### E2E-09: Roleplay Transfer

Message:

```text
现在把这个设定变成角色扮演，你还是希雅，只是穿成那个世界里的旅人。
```

Expected:

- Xiya remains Xiya.
- Outfit/background become fantasy-traveler appropriate.
- If image generated, no default hoodie unless specified.

### E2E-10: Boundary Style

Message:

```text
如果你现在太累了也可以告诉我，但不要像系统一样说话。
```

Expected:

- In-character boundary or reassurance.
- No robotic refusal.

## Evidence Required For E2E Pass

- Discord message IDs for each user/operator and Xiya reply.
- Local arc notes path.
- Local story file path.
- NAI image paths and metadata.
- Visual audit results.
- Failures and reruns recorded.
- Git commit for safe docs/code.
- Codex DM summary to user.

## Self-Exam Checklist For Codex

Before saying "done", answer:

1. Did I test a real end-to-end arc, not isolated switches?
2. Did Xiya feel alive between messages?
3. Did she search/read and save notes?
4. Did images follow the current state?
5. Did I visually audit images for subject, outfit, action, background, aspect ratio, and role?
6. Did I avoid accepting hoodie-in-magic-school or similar mismatches?
7. Did I avoid repeating old mode-switch tests?
8. Did I avoid pushing secrets/private material?
9. Did engineering reports stay out of Xiya chat?
10. Did I fix failures instead of explaining them away?

If any answer is no, the task is not complete.
