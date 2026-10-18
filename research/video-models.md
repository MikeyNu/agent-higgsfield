# Video model directive research

Accessed 2026-10-19 (Africa/Johannesburg). First-party technical sources only. This is a research input, not a claim of paid generation testing. Source IDs resolve in video-sources.json.

## Non-negotiable distinctions

1. A model name is not a capability contract. Record exact version, mode, Higgsfield surface (web, MCP, CLI, API), available inputs, settings and live quote before submission. A provider capability does not prove that the selected Higgsfield route exposes it.
2. Timing written in prose is guidance. A supported duration field controls the container; a supported shot/keyframe field constrains structure; neither warrants a promise that every intervening frame will be correct. Frame-accurate deliverables need deterministic animation/compositing or a checked source performance.
3. References reduce ambiguity. They do not guarantee immutable identity, typography, geometry or physics. The clip must be inspected throughout, including cuts and interpolated frames.
4. A lower-cost mode, resolution or model is a different experiment. It may validate composition but does not prove final motion quality. Reuse or upscale an accepted result when suitable; rerendering at higher resolution can change it.
5. Never claim that all AI-video problems are solved by longer prompts. Use asset preparation, reference roles, blockouts, shorter shots, editing and bounded retries.

## Compact model cards

### Kling 2.x and 3.0

- T2V: define subject, visible action, environment, camera and lighting. I2V: let the source image carry appearance; describe subject and background motion simply. Major deviations from the image can provoke an unwanted cut. Choose physically plausible movement and reduce complex trajectories [V01].
- On Higgsfield 3.0, separately set audio and clip duration. Use actual multi-shot controls when offered, plus explicit action and camera for each shot; use Elements for reusable subjects. For Motion Control, the character image should expose hands/arms as relevant and the performance reference should avoid cuts [V02,V03].
- Confirm the exact first/end-frame route. Do not assume the 2.6 route has 3.0 controls. The 3.0 4K API route documents sound, duration, elements, cfg_scale, multi_shots and multi_prompt, not a universal negative_prompt field [V25].
- For continuity, reuse an accepted final frame as the next opening constraint. This anchors appearance but does not guarantee matching velocity or geometry across the join. Test the join and crop.

### Kling 4.0, only if exposed

Provider release dated 14 October 2026. Its documentation distinguishes Omni Reference from Keyframes; the entry points cannot be combined. It documents up to ten keyframes, asset role mapping, and descriptive positive language rather than broad negative lists. Instructions excluding subtitles or music are specifically discussed. Timestamped actions are supported prompting guidance. Some features are labeled coming soon, including extension and HDR in one section [V04]. No Higgsfield 4.0 route was verified in this research. Do not silently upgrade 3.0 to 4.0.

### Seedance 2.0 and 2.5

- 2.0 supports multimodal references in the provider documentation. Assign each attachment one clear purpose, such as identity, composition, motion, camera or audio. A storyboard is a blueprint, not the requested final visual style. The provider's examples explicitly cite image references and camera/action intent [V05].
- Higgsfield's help recommends short I2V drafts, concrete camera verbs, inspecting the full clip and changing one variable per revision. Distinguish in-clip references from reusable Elements across separate jobs [V06].
- 2.5: use concise labeled sections for global look, scene, reference roles, action/camera beats, continuity and audio. This is an official Higgsfield tutorial pattern, not proof that labels themselves guarantee compliance. Do not include sections irrelevant to the shot [V07].
- 2.5 provider guidance adds richer reference interpretation, clay/white-model workflows and targeted time-based editing [V08]. For tightly planned 3D travel, a simple camera blockout can carry spatial intent more reliably than adjectives. This last recommendation is an engineering inference, and must be tested.
- Higgsfield's verified reference route exposes image/video/audio arrays, duration 4 to 30 seconds, 480p/720p/1080p, aspect ratio, output format and generate_audio [V09]. Exact reference count and mode combinations require live inspection. Do not generalize this schema to every surface.
- Budget especially carefully with reference video: the public API pricing description counts both input and generated video duration in token-based billing. Web credits and API currency are separate pricing surfaces [V10].

### Veo 3.1

- Use visual description, action, camera and light; write audio direction in separate sentences. In a supported negative-prompt field, Google recommends unwanted concepts such as subtitles or camera shake, rather than imperative phrasing like do not show them [V13]. Do not assume a dedicated negative field exists on Higgsfield.
- A starting frame and subject reference images serve different roles. Google documents first/last-frame generation and up to three subject reference images, but route combinations and constraints must be checked [V12].
- Higgsfield's older integration guide distinguishes Standard and Fast and associates different controls with them [V11]. Treat that as historical platform evidence, not a current capability guarantee. Native-audio behavior, resolution, length and reference modes must come from the selected route.
- Avoid overloading one short clip with elaborate choreography, multiple camera paths and lengthy dialogue. This is a production heuristic rather than a measured model limit.

### Sora 2, availability must be verified

- Higgsfield's prompt guide recommends distinct shot blocks, one camera move and one subject action per beat, concrete foreground/midground/background anchors, and brief dialogue in its own block [V14].
- OpenAI's cookbook emphasizes that results vary and shorter shots often follow instructions more reliably. It distinguishes prose from actual model/size/duration fields. The page is explicitly archived, so use the creative methodology, not its parameter table as current API truth [V15].
- No evidence in this research establishes a Higgsfield Sora end-frame, seed, negative-prompt or exact keyframe interface. Never borrow those controls from other families.

### Wan 2.x and 3.0 Prime

- Provider T2V formula: subject + environment + motion + aesthetic/camera treatment + style. I2V should primarily specify motion and camera because the image supplies scene appearance [V16].
- Wan 3.0 guidance uses role-labeled references and shot-number/timestamp blocks. It warns that first/last-frame mode and all-reference mode are mutually exclusive. It permits concise targeted negative instructions; do not transplant Veo's negative-field grammar to Wan or vice versa [V17].
- The verified Higgsfield Wan 3.0 Prime reference route offers seed, 2 to 30 seconds, 480p/720p/1080p, optional audio and thinking, plus media reference arrays. File and webpage inputs cannot be combined and enable thinking [V18]. Do not turn on extra processing without budget justification.
- Wan 2.6 reference-to-video on the verified Higgsfield API route only lists 5 or 10 seconds, although product marketing advertises broader family capability [V19]. This demonstrates why route schemas outrank family marketing.

### MiniMax Hailuo 2.3 and H3

- Hailuo 2.3 provider documentation supplies bracketed camera directives such as [Push in], [Tracking shot] and [Static shot]. Multiple commands within one bracket are simultaneous; separately placed commands are sequential. It recommends no more than three simultaneous commands. Provider prompt_optimizer defaults true and can be disabled for closer control, if the selected route exposes it [V20].
- H3 is a different generation. Its provider workflow supports first/end frames and separate reference modes, with explicit reference roles. Provider guidance also supports camera cues adjacent to relevant action text [V21].
- The observed Higgsfield H3 reference route lists 5 to 15 seconds and 2K only [V22], while provider H3 documentation describes additional output choices. Do not offer a cheap 768p Higgsfield H3 draft unless the active route actually supports one.

### Grok Imagine

Higgsfield documents natural-language scene and sound prompting with reference images [V24]. Provider 1.5 documentation distinguishes first-frame animation, reference generation, first/end/midpoint constraints, editing and extension. The lower-cost lite version has fewer controls, and editing/extension use a different model [V23]. These provider controls must not be assumed present in Higgsfield. For I2V, describe what happens after the still and set the intended sound. For edits, state the requested change and the visual properties to preserve.

## Contradictions and recency checks

- Seedance 2.5 Higgsfield blog says 50 reference images. ByteDance launch and Higgsfield help specify 30 images, 10 video clips and 10 audio clips. Use the latter as documented family limits and the live surface as the actual limit [V06,V07,V08].
- Different Higgsfield Kling 3.0 blogs advertise different shot counts. Do not hardcode a universal maximum; the active route decides.
- Seedance help mixes a 1080p 2.5 table with a generic instruction to scale to 4K. The selected route, not that prose, decides final resolution [V06,V09].
- API catalog prices, promotional discounts, web credits and unlimited-plan benefits are not interchangeable. No quote should be computed from this research snapshot.
- OpenAI's Sora recipe is archived. Kling 4.0 is newly documented by its provider but was not verified on Higgsfield. Maintain explicit unverified status.
- Higgsfield's current public catalog includes Seedance 2.5, Kling 3.0, Wan 3.0 Prime and MiniMax H3. Older skill defaults that only know Seedance 2.0 and Hailuo 2.3 are incomplete [V26].

## Original operational recommendations for the skill

These are engineering controls inferred from the evidence, not vendor guarantees.

- Compile a model-neutral shot plan into the selected model's actual syntax. Validate one movement path, reference-role clarity, scene feasibility, duration budget and dialogue length before spending.
- For a continuous scroll journey, define one scene, camera start/end, passage through landmarks, stable light, depth layers and readable overlay zones. Keep website typography and UI out of generated footage; composite them as deterministic HTML or graphics.
- If exact spatial travel matters, prefer a 3D blockout/Blender camera path as a reference or render the geometry directly. A pair of images alone cannot establish the path through an unseen environment.
- Multi-shot filmmaking and a single continuous scroll journey are different tasks. Explicitly choose one; avoid a multi-shot preset for a continuous traveling camera.
- A storyboard with ten panels is not ten guaranteed keyframes. Use actual supported keyframe controls or split into bounded shots with explicit review checkpoints.
- Before retries, diagnose whether the defect is identity, action, timing, camera, geometry, text, audio or encoding. Change the smallest causal variable, preserve accepted assets and record the cost.
- Inspect beginning, middle, end, transitions and any risky hand/object contact at actual playback speed and frame stepping. Contact sheets alone cannot reveal all temporal failures.
- Set a strict approved spend ceiling and retry ceiling outside the prompt. On an ambiguous timeout, inspect the existing job ID before resubmitting.
