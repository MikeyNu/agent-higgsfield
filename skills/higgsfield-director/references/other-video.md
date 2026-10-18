# Other video families

Checked 2026-10-19. Inspect exact version, mode and connected surface before using any provider-specific syntax.

## Wan

T2V: subject + scene + motion + camera/light + style. I2V: focus on motion and camera because the image establishes appearance. For Wan 3.0 reference work, map each asset's purpose and use numbered, contiguous time blocks when sequencing matters. Its provider guide distinguishes first/end-frame mode from all-reference mode; they cannot combine. Targeted negative instructions are documented, but avoid generic padding [1].

**Original I2V example:** “The camera rises slowly from desk height to an overhead view. The black notebook remains closed and stationary. Preserve the desk layout, paper edges and soft window light.”

If a camera path fails, simplify it or supply a supported motion reference. If endpoint images differ in geometry, fix them before interpolating. Do not transfer a family-level duration claim to a narrower route.

## MiniMax Hailuo and H3

Hailuo 2.3 provider guidance supports bracketed camera commands. Commands within one bracket are simultaneous; separately placed commands are sequential. Keep combinations simple. A provider prompt optimizer can be disabled for closer control only when the actual route exposes that option [2].

**Original Hailuo example:** “A white ceramic object stands on a black plinth [Truck right]. Its silhouette stays rigid while the camera reveals the far edge.”

H3 has distinct first/end-frame and multimodal-reference workflows. Label which asset defines appearance, motion or camera [3]. Provider output choices can exceed those on Higgsfield. Never offer a cheaper resolution without a supported route.

If motion conflicts with the source pose, change the source or reduce the action. Do not apply old Hailuo limits automatically to H3.

## Grok Imagine

Separate the selected generation model from its edit/extension variants. Provider 1.5 documents references and pinned frames that the lite variant lacks. These are not proof of Higgsfield exposure [4].

**Original edit example:** “Change only the jacket to matte white. Preserve the person's face, hand movement, background, camera path and timing.”

For I2V, describe what happens after the still. For T2V, establish the scene and then motion/sound. Inspect edits for unintended changes outside the target. Do not assume a reference image is a pinned first frame unless the mode says so.

## Gemini video or any unseen family

Do not reuse a similarly named image model or assume Veo semantics. Discover the exact model/version, supported modality, reference roles, duration/ratio constraints, audio behavior and edit controls. Read its current primary documentation and the active tool schema. Produce a small family adapter using only verified fields.

If documentation is insufficient, prepare a model-neutral prompt with subject, change, camera, invariants and sound. Label unknown capabilities and propose a supported alternative. Do not invent hidden controls or spend to discover whether an undocumented feature exists.

Sources: [1: Wan 3.0](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-prompt-guide) · [2: Hailuo camera commands](https://platform.minimax.io/docs/api-reference/video-generation-t2v) · [3: MiniMax H3](https://platform.minimax.io/docs/guides/video-generation) · [4: Grok variants](https://docs.x.ai/developers/model-capabilities/video/overview)
