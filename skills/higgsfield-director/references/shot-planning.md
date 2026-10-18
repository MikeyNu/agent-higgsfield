# Plan shots, then compile prompts

## Compact shot contract

Use only fields that constrain this deliverable:

```text
Goal / intended use:
Output: count, aspect ratio, duration, required delivery quality
Invariants: identity, product geometry, wardrobe, lighting, exact text
References: ID -> purpose (appearance / opening / ending / motion / sound)
Opening: subject position, foreground, middle distance, background
Action: one principal event, ordered beats
Camera: start, path, target, speed/easing, landing, lens intent
Continuity: what persists across time and joins
Audio: dialogue / ambience / music / silent, as supported
Acceptance: observable pass criteria and hard failures
```

Separate **hard tool controls**, **soft prompt instructions** and **post-production requirements**. A duration parameter is stronger than “ten seconds” in prose. A time-coded paragraph is not a frame-accurate animation curve. More words do not make conflicting instructions feasible.

## Compile for mode

- Text-to-image/video: establish subject, scene, composition, action, materials/light and relevant constraints.
- Image-to-video: keep the approved image as the appearance anchor; describe what changes after that frame. Do not unnecessarily redescribe a conflicting scene.
- Reference-to-video: explicitly assign roles; do not assume upload order means identity, style or camera. Use the exact reference syntax supported by that family.
- Editing: state one requested change, its scope and preserved properties. Use masks/ranges only when exposed.
- Multi-shot: separate shot descriptions and target durations. Use actual shot controls where available. Keep a continuity bible with persistent subject, outfit, props, light and direction of travel.

Write concrete movement: a dolly translates the camera; a pan rotates it; a zoom changes focal length. Name the movement, starting and ending framing, and intended speed. Avoid simultaneous “locked camera” and “orbit,” or “single unbroken shot” and “hard cut.” Do not demand a camera pass through solid geometry.

## Reference discipline

Inspect resolution, crop, hand/face detail, hidden surfaces, perspective and unwanted text before upload. An image can anchor visible appearance, not unseen geometry. Match a motion-reference person's framing and visible limbs to the intended performance. Avoid conflicting references and cuts in a continuous driving performance.

For a chain, reuse an accepted endpoint only when the mode supports it. Review the seam for position, scale, light, velocity and perspective. Chaining can accumulate drift. A copied last frame alone does not guarantee a seamless continuation.

## Frame control hierarchy

1. Prompted beat or timestamp: approximate intent.
2. Supported first/end or actual keyframe controls: stronger anchors, uncertain intermediate frames.
3. Driving video/blockout: stronger motion evidence, possible reinterpretation.
4. Deterministic animation/compositing: explicit geometry, camera and timing; still verify the render.

For exactness, move up this hierarchy before buying repeated prompt variations. Do not represent a storyboard contact sheet as guaranteed frames. Treat low-resolution experiments as evidence about their tested settings, not proof of a different final model.

## Nu Labs continuous-scroll example

Use one coherent architectural scene with a verified navigable camera path. Define opening, passage through the curved threshold, settled reading positions and exit. Keep lighting and topology stable. Generate/render the background without website copy; use semantic HTML for exact logo, navigation and text. If the exported video itself must contain exact branding, composite the original artwork into the video too; HTML alone does not meet that requirement. Plan mobile framing and a static reduced-motion poster separately.

Original prompt skeleton, to adapt to the chosen model: “The camera advances at eye level through the open curved passage, keeping the lens fixed and the horizon level. Near surfaces pass the frame edges while the far room remains stable. The architecture stays rigid. The move settles facing the far wall.” These words express intent, not a motion guarantee.

Sources: [Kling I2V guidance](https://kling.ai/quickstart/image-to-video-guide), [Google Veo prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide), [Higgsfield camera control](https://higgsfield.ai/blog/ai-video-camera-control). The control hierarchy and Nu Labs application are engineering recommendations.
