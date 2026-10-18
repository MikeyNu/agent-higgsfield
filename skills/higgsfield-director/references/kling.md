# Kling

Checked 2026-10-19. Match the exact version and generation, edit, Omni or Motion Control mode. Provider features are not automatically Higgsfield controls.

## Compile the request

- **T2V:** subject, action, scene, camera, light. Describe visible behavior instead of abstract quality words.
- **I2V:** preserve the image's appearance; emphasize subject/background motion. Large departures from the source can trigger cuts. Keep motions physically plausible [1].
- **Kling 3.0:** use supported shot controls for separate shots, with one clear action and camera move each. Start/end images constrain endpoints. Elements can carry reusable subjects. Confirm the selected mode exposes these controls [2].
- **Motion Control:** supply a clean performance without cuts and a compatible character image with relevant limbs visible. Do not treat it as an arbitrary 3D camera-path generator [2].
- **Kling 4.0:** provider documentation distinguishes Omni Reference from Keyframes and says those entry points cannot combine. It supports explicit asset roles and discourages broad negative lists [3]. It was absent from the checked Higgsfield tool catalog. Discover availability before offering it.

## Original I2V example

> Preserve the supplied sculpture's three separate forms and matte white surface. One continuous shot: the camera trucks slowly right at a constant height, revealing the gap between the central and right forms. The sculpture remains stationary. Soft side lighting stays constant. End with the gap visible in the right third.

Set duration, ratio and supported audio controls outside the prompt. For multiple shots, turn each shot into the actual supported scene structure. Do not invent a universal negative-prompt parameter.

## Diagnose before revising

Unwanted cut: remove action inconsistent with the starting image. Identity drift: improve the source or attach a supported Element. Wrong motion: simplify camera direction or use a motion reference. Bad join: inspect both endpoint pose and velocity; matching stills alone do not ensure continuity.

**Documentation conflict:** Higgsfield articles disagree on maximum shot count. Use the current schema, not a memorized limit.

Sources: [1: Kling I2V](https://kling.ai/quickstart/image-to-video-guide) · [2: Higgsfield Kling](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-kling) · [3: Kling 4.0](https://kling.ai/quickstart/kling-4-model-user-guide)
