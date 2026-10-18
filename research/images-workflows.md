# Image models and specialist workflows: research handoff
Reviewed 18 October 2026 UTC. Read-only research; no media uploaded, account mutated, generation submitted, or paid render tested. Public provider guidance describes capabilities, not guaranteed output. A sampled live Higgsfield MCP image catalog is saved separately as image-models-snapshot.json.

## Priority findings
1. Resolve the live model ID, surface, mode and schema before compiling a prompt. The official GitHub skill catalog currently uses a Nano Banana alias differently from live MCP. Public web pages also disagree internally on Seedream Pro maximum resolution. Do not reproduce those aliases or numbers as timeless facts. [I01 I10 I25]
2. Prompting is only one control layer. Reference inputs, compatible media roles, masks, camera controls, native editing, deterministic composition and verification all matter. A detailed prompt is not a pixel-exact or frame-exact guarantee. [I02 I03 I05 I06]
3. Do not call every control a model. Cinema Studio is a production surface; Katana is an editing workflow; Genjutsu selects different motion-transfer and replacement models; 3D Jutsu is an editable scene workspace. [I12 I13 I15 I16]
4. Scope matters: provider API features are not automatically exposed through Higgsfield web, MCP or desktop plugins. A missing parameter cannot be inserted into a request merely because a provider document mentions it. [I01 I10 I18]
5. "Motion Director" could not be established as an exact current official model/tool name. Read-only recipe lookup for /motion-director returned the generic unknown-token path. Treat it as unresolved user vocabulary until a live catalog or screenshot identifies the surface. Do not silently map it to Kling Motion Control, Higgsfield DoP or Cinema Studio's Director's Panel. [I12 I14 I18 I19]

## Model-specific handoff
Six concise runtime references have been written in agent-higgsfield/skills/higgsfield-director/references: gpt-image.md, gemini-image.md, seedream.md, flux.md, soul.md and other-image.md. They contain original examples and version-specific limitations with primary links. Do not duplicate their content into the core skill. Read only the selected family at runtime.

The image catalog contains 46 entries in the saved snapshot. It includes specialized utilities as well as generation models. The parent agent has a broader catalog snapshot for routing. Most catalog-only entries lack independent performance evidence; their documented descriptions and controls are routing clues, not benchmark results. Unknown versions need capability discovery and a task-specific check before inheriting older guidance.

## Workflow-specific operating guidance

| Workflow | What drives it | Best cost-conscious control | Boundary |
|---|---|---|---|
| Cinema Studio | Versioned production surface with camera, film, lighting, references and edit/extension modes | Establish cast/location and an approved keyframe; align prompt with selected controls; select single-shot tempo for a continuous camera journey | Web 4.0 features do not prove equivalent MCP controls. Recheck active version. [I12] |
| Higgsfield DoP | Native image-to-video model plus a camera/effect preset | Choose the approved still and one compatible motion blueprint; do not request a conflicting move in prose | DoP, Motion Control and a Director panel are different concepts. [I14] |
| Genjutsu Motion Transfer | Driving video supplies movement, camera and timing; reference images supply new subjects/look | Inspect source timing/framing first, then use the shortest valid shot containing the necessary action | Direct motion transfer and object replacement have different model IDs. [I13 I15] |
| Genjutsu Object Swap | Source video plus replacement references and localized brief | Specify target and what must remain; inspect occlusion/contact frames | Do not re-specify the whole world when only one element changes. [I13 I15] |
| Genjutsu Styles | Published style recipe applied to user's video | Resolve exact returned style ID, inputs and price | Style IDs are not video generation model IDs. [I15] |
| Katana | Source footage to edit, or explicit reference edit with subject assets | Measure cuts, duration, frame rate, shot size and motion; use actual footage for ordinary edits and only generate missing shots; build an edit decision list | Named preset sessions and free-run counters are mutations, not research. The live recipe must be read before a run. [I16 I17] |
| 3D Jutsu | Editable geometry, lights, cameras and animation | Block the entire spatial route once, preview camera and silhouettes, edit objects without paying for repeated image approximations, then authorize selected AI finishing only | Local scene rendering and AI generation are separate operations. A paid scene finishing call needs a fresh quote. [I21 I22] |
| Desktop Blender add-on / Bridge | Existing Blender application plus Higgsfield cloud generation | Work in a saved scene, create deterministic camera/geometry, inspect a low-cost preview before cloud finishing | Add-on uses the same account credits; Bridge connects an agent to the installed add-on. [I23] |
| /use-blender local MCP | Dedicated local background Blender process | Save checkpoints and render deterministic geometry locally before spending on AI | This route requires local host access and cannot see unsaved work in an already-open desktop scene. It is separate from cloud 3D Jutsu and the add-on. [I24] |

## Nu Labs scrub-journey inference
For Mikey's continuous 3D landing-page journey, prefer an explicit 3D blockout and camera spline if geometric continuity or logo silhouette is critical. Bake the journey into deterministic frame positions, inspect start/intermediate/end poses, reserve quiet composition areas for real HTML typography, then use paid generation only where its visual contribution justifies the uncertainty. Generate section plates with consistent lens, world scale, light direction and movement direction. A timestamped text prompt is an approximate intention, not a frame-accurate animation track. This is a proposed engineering workflow, not an already rendered or tested result.

## QA and adversarial cases to add
- Unknown "Motion Director": resolve name without inventing a callable model.
- Old catalog alias disagrees with live MCP: choose live ID/schema; record discrepancy.
- Soul style plus image reference: reject incompatible combination before quoting.
- Seedream Pro supplied a mask: do not submit unsupported media role.
- GPT text correct but company logo distorted: fail identity gate; use original logo or targeted repair.
- Reference is for style only: do not treat it as edit target or identity.
- FLUX negative-prompt request: compile positive visual constraints; do not add unsupported field.
- Exact hex/geometry request: measure result or use deterministic composition; do not assert precision.
- User has a complete video: use existing footage/edit route instead of automatically paying to regenerate it.
- Blender request from cloud: identify route correctly; do not claim a desktop installation.
- Upscaler adds skin/label details: do not call them recovered facts.
- General model metadata or price estimate succeeds: this is not generation validation or permission to spend.

## Source register
See images-workflows-sources.json. Web references are primary provider or first-party Higgsfield. I01/I15/I17/I19/I20/I22/I24 are read-only published tool metadata/recipes, not web pages. Public docs, live schema and generated-output QA answer different questions. No premium model performance or pass-rate claims were tested.
