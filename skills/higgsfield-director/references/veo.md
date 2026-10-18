# Veo

Checked 2026-10-19. Discover the exact Veo version and Standard, Fast or other variant. Do not treat them as interchangeable.

## Compile the request

- **T2V:** specify subject, action, environment, framing, camera and light.
- **I2V:** use a starting image close to the intended opening and describe the movement that follows.
- **Subject references:** define appearance without assuming each reference becomes a sequential frame.
- **First/last frames:** use the dedicated inputs when exposed. Endpoints do not specify the complete intervening path.
- **Audio:** place speech, ambience and individual sound effects in separate sentences. Keep dialogue brief enough for the clip.
- **Negatives:** when a compatible negative-prompt field exists, list unwanted concepts, such as subtitles or camera shake, instead of commands beginning with no or don't [1].

Google documents subject references, first/last frames and extension, with mode-specific restrictions [2]. These are provider capabilities. Higgsfield's older guide assigns different controls to Standard and Fast [3]; recheck the live route before using either.

## Original I2V example

> Continue the approved bright studio image. The camera slowly dollies forward toward the matte black circular opening. The surrounding white panels remain rigid. Soft daylight and exposure stay constant. The move finishes just before the opening, with a clear view through it. A quiet room tone accompanies the shot.

Set actual duration, ratio and available audio controls outside prose. If the delivery must be silent, use a verified audio control or remove the track in post-production.

## Diagnose before revising

Unexpected motion: simplify to one camera path and one subject action. Appearance drift: improve the starting/reference image and remove contradictory descriptions. Dialogue errors: shorten the line or use a dedicated speech/lipsync workflow. Unstable transition: align the endpoints' perspective and lighting before another attempt.

Do not promise perfect identity from marketing claims or assume that adding 4K to the prompt changes output resolution.

Sources: [Google prompting](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide) · [Google Veo API](https://ai.google.dev/gemini-api/docs/veo) · [Higgsfield integration](https://higgsfield.ai/blog/How-to-Use-Google-Veo-3.1-Complete-Guide-for-the-New-Model)
