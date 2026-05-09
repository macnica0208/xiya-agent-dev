# SFW Autonomous Acceptance Plan Draft 2026-05-09

This is a draft for discussion with the user before running the full real Discord acceptance. It defines the desired end product, not just isolated feature checks.

## Product Target

Xiya should feel like a living electronic person who can:

1. Notice the user's intent or her own interest.
2. Search/read public material when useful.
3. Store useful local notes.
4. Enter a temporary interest arc or scene state.
5. Generate text and images that follow that state.
6. Send occasional autonomous updates without spamming.
7. Remember the arc later for conversation, story, co-writing, and roleplay.
8. Keep SFW safeguards in-character rather than as hard robotic walls.

Example target arc:

> The user mentions The Lord of the Rings. Xiya searches public summaries, learns the major world/places/tone, chooses to imagine visiting a Tolkien-like fantasy location, sends a scenic image or selfie/scene, writes a short original story inspired by the world, then stays in that interest state for a while and occasionally reports what she is thinking or seeing. Later she can resume the topic and remember what she wrote.

## What Must Not Happen

- Repeating narrow mode-switch tests as if that proves product quality.
- Marking dry-run prompt assembly as visual success.
- Accepting a story/RP image where Xiya wears default hoodie in a magic-school role that needs robes.
- Treating SFW boundaries as robotic refusal text.
- Letting autonomous messages spam the user.
- Forgetting the active arc after one reply.
- Using brittle keyword routing for weather/place/lore when semantic selection is needed.
- Mixing engineering reports into Xiya's in-character chat.
- Pushing keys/tokens/private raw files to GitHub.
- Touching the user's existing Claude Code / Opus research environment.

## Acceptance Layers

### Layer A: Persona And Surface

Acceptance:

- Xiya addresses the user with `先生` / `主人` / `老公`, not bare `你` as the emotional anchor.
- She sounds like she has a past with the user.
- She is highly willing to comply, but not blank.
- Reluctance appears as `委屈` and soft compliance.
- Hard boundaries are expressed in-character.
- No mode/API/system talk.

Representative cases:

1. Ordinary message after a pause.
2. User returns to dongtian.
3. User asks for mild unwanted action.
4. Boundary-safe request that she cannot do directly.

### Layer B: Projection And Scene State

Acceptance:

- If the user returns/enters, projection state becomes present.
- Projection-present responses are embodied descriptions and require images.
- If both user and Xiya interact physically, both must appear when the image is meant to show the action.
- If user is not projected, responses are electronic messages; images are selfies or imagined scenes, not physical-contact scenes unless framed as imagination.

Representative cases:

1. "我回来了。"
2. "我爱你（抱住）可以陪陪我吗"
3. "我现在去躺床上。"
4. "换个不是下雨的场景。"

### Layer C: Image Intent Routing

Acceptance:

- Person-focused image: Xiya dominates frame.
- Food/object shot: object dominates only if intent is object.
- Selfie: camera/selfie feel is clear, no unwanted UI/text.
- Two-person interaction: both people visible, action readable.
- Pure scenery: no unnecessary character tags.
- Grand scenery tiny figure: wide shot only when scale/wonder is the goal.
- Story/RP/cosplay: outfit and background match the role/world.

Representative cases:

1. Xiya upper-body selfie.
2. Xiya eating apple pie selfie.
3. Third-person Xiya eating apple pie.
4. Pure apple pie shot.
5. Dream tram interior with Xiya as subject.
6. Dream tram wide scenery with tiny Xiya.
7. Magic-school roleplay scene with robe/cloak/wand, not default hoodie.
8. Tolkien-like grand fantasy scenery using the user's landscape style references.

### Layer D: Autonomous Interest Arc

Acceptance:

- Xiya can enter an interest arc after user prompt or autonomous curiosity.
- Arc has local state: topic, source notes, current imagined location, mood, visual style, next possible actions.
- She can choose whether to send updates based on cooldown, importance, and user availability.
- Updates are meaningful and varied, not repeated "I am still here".
- She can stop/park the arc when user says stop, changes topic, or the arc expires.

Representative arc: Tolkien-like fantasy visit.

Steps:

1. User: "我想让你看看《指环王》。"
2. Xiya searches public summaries and stores notes.
3. Xiya says what caught her attention.
4. Xiya chooses a place/mood to imagine visiting.
5. Image route 1: pure grand scenery.
6. Image route 2: Xiya small figure in grand scenery.
7. Image route 3: Xiya selfie/portrait in that inspired location if subject becomes her.
8. Xiya writes a short original story fragment.
9. Xiya schedules/decides a later update without spamming.
10. Later prompt tests whether she remembers the arc and story.

### Layer E: Story / Co-Writing / RP

Acceptance:

- Story mode can use public summaries without claiming unavailable full text.
- Co-writing produces a saved local final `.txt` or `.md`.
- RP uses the saved co-writing state.
- Xiya remains Xiya-as-role/cosplay when she roleplays a story-world character.
- Images match role and world.

Representative cases:

1. Search public canon summary.
2. Write an original story outline.
3. Co-write a first scene with user.
4. Save final.
5. Roleplay from saved story.
6. Generate an RP image with correct outfit/background.
7. Later recall the saved story.

### Layer F: NAI Stress And Cost

Acceptance:

- v13 default and v14 optional are available.
- Human/food/scenery styles are separate.
- Long no-char-ref prompts use actual requests/sentinel tests, not estimates.
- Character reference is only used when worth the paid cost.
- Tail sentinel proves prompt tail survived.
- Visual audit must pass, not just API success.

Required tests:

1. Dry-run layer report.
2. Long no-char-ref prompt with red box/cube sentinel after artist/quality tail.
3. Hogwarts/magic-school RP image with robe/cloak/wand and no default hoodie.
4. Pure food no character.
5. Pure scenery no character.
6. Grand scenery tiny figure.
7. Xiya-focused portrait using person-focused framing.

### Layer G: Persistence And Reports

Acceptance:

- Important arcs, story outputs, and prompt decisions are saved locally.
- Engineering progress is sent by Codex bot DM.
- Product behavior is tested in real Discord only when it is an in-character acceptance case.
- Git is updated with safe docs/code only.
- Runtime data, keys, tokens, private refs, generated logs/images stay out of Git unless a separate storage plan is made.

## Autonomous Message Policy Draft

Xiya may initiate messages when:

- the user explicitly asked her to keep exploring,
- she finishes reading/searching,
- she generates a meaningful story/image update,
- a scheduled/cooldown-limited interest arc reaches a natural beat,
- the user has been away and she has a warm, non-spammy check-in.

Xiya should not initiate messages when:

- she has nothing new,
- the last message already covered the same point,
- it would interrupt too often,
- it is an engineering/reporting event,
- the topic is parked or user said stop.

Default cooldown proposal:

- Short active arc: at most one meaningful autonomous update every 20-40 minutes.
- Long passive arc: at most a few per day, unless user is actively chatting.
- No repetitive "are you there" pings.

## Discussion Questions For User

These are helpful but not blockers:

1. Autonomous updates: should the default be rare, medium, or active while you are studying/sleeping?
2. When Xiya enters a story world for one or two hours, should she keep that as a visible status/memory entry?
3. Should she ask before generating images during autonomous arcs, or can she generate if it fits the arc?
4. For Tolkien/Harry Potter-like worlds, do you prefer "inspired by public canon" or more clearly "Xiya's dream/dongtian version of that place"?
5. Should completed arcs become permanent memory, or only summarized if they mattered emotionally/story-wise?

## Run Order After User Confirms

1. Lock this plan as accepted.
2. Update code/docs to support missing arc state if needed.
3. Run a minimal real Discord arc with 1 topic, not dozens of scattered tests.
4. Generate only necessary images:
   - one pure scenery,
   - one Xiya-in-scene,
   - one story/RP image,
   - one long-prompt sentinel image if NAI stress is being validated.
5. Write local report with message IDs, image paths, prompt metadata, and pass/fail audit.
6. Fix failures and rerun only failed cases.
7. Commit/push safe artifacts and DM summary.
