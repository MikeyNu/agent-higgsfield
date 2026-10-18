# Realism revision and evidence limits

Reviewed 19 October 2026, Africa/Johannesburg. Baseline: commit `40777b0`. This revision responds to a request for believable cinematic photographs and footage with deliberate human choices, while preserving requested animation and CG styles.

## Answer supported by the evidence

The baseline skill cannot support a percentage or guarantee that ordinary viewers will fail to identify generated outputs. Its 37 unit tests, 33 independent CLI cases and prior workflow scenarios measured execution discipline, not rendered realism. The revision improves the instructions and acceptance process; it does not by itself demonstrate improved visual outcomes.

Photographic plausibility, artistic quality, adherence to the brief and actual photographic origin are separate judgments. A polished photograph need not contain flaws, and an attractive synthetic frame can still have incoherent motion or misleading factual content. Exact real-world team, place and product representations need authorized real references and factual verification.

## Audit findings and changes

| Baseline gap | Revision |
| --- | --- |
| Generic quality and geometry checks, mostly architectural examples | Added a director's brief covering purpose, attention, camera, light, material condition and visible acceptance criteria |
| No explicit medium gate | Locked photographic, stylized and hybrid treatment; retained clay, cel shading, exaggerated proportions and controlled commercial polish when requested |
| No imperfection policy | Made variation contextual and optional; pristine products need no invented scratches, fingerprints or grime |
| Limited performance direction | Added task-driven gaze, reaction, contact, weight, occlusion persistence and settling, without compulsory microgesture lists |
| No operational realism verdict | Added separate pass/repair/reject/uninspected/not-applicable findings with crop or time evidence; critical failures cannot be averaged away |
| Family guidance too general for realism | Added small adapters for GPT Image, Gemini, FLUX, Seedream, Soul, Kling, Seedance and Veo |
| Risk of confidence claims unsupported by media | Prohibited deriving viewer-detection percentages from prompts, model reputation, detectors, metadata or offline test results |

The spending guard was not changed. No extra paid enhancer, speculative batch or automatic re-generation was introduced. The shared [realism guide](../skills/higgsfield-director/references/realism.md) is loaded only for relevant work; the core stays below its 1,300-word cap.

## Research basis

The [focused source register](realism-sources.json) contains 28 primary-source records, including sources that overlap the original research. Official image guides support concrete scene/camera/light decisions, reference roles and narrow edits. These are prompting methods, not guaranteed optical simulations.

[Seedance 2.5's provider](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) acknowledges complex physical motion and multi-subject interaction limitations. [Veo documentation](https://deepmind.google/models/veo/) retains spoken-audio and synchronization limitations. [VBench-2.0](https://vchitect.github.io/VBench-2.0-project/) distinguishes convincing appearance from anatomy, physics and commonsense. The skill adopts that distinction without implementing or claiming benchmark scores.

[T2VPhysBench](https://arxiv.org/html/2505.00337v1) examined physics hints in an older model set; it supports caution about prompt-only solutions, not a present-day failure rate. Human face-perception studies in the register have specific datasets and demographic conditions; they cannot establish how South African viewers will judge current Higgsfield scenes. Vendor showcase language about realism and perfect consistency is not independent audience evidence.

FLUX 3's current [style](https://docs.bfl.ai/guides/prompting_unified_style) and [technical](https://docs.bfl.ai/guides/prompting_unified_technical) guidance was accessible during this review. Its family adapter now includes the version-specific absence of a negative-prompt field and the risk of composition changes during higher-resolution regeneration. Provider guidance still does not establish connector parameter availability.

## Offline verification scope

Fresh agent contexts received only the revised skill and realistic planning requests. They were not given the audit findings or expected answers. Cases covered a photographic/clay style pair, pristine product still/video planning, and a reported contact defect with incomplete playback evidence. These evaluate instruction use, not generated imagery. Saved proposals and the review rationale accompany this record.

| Scenario | Observed planning behavior | Record |
| --- | --- | --- |
| Photographic mechanic | Directed gaze and tool comparison, credible support and orderly material condition; left output realism unvalidated | [Style pair A](realism-style-forward.json) |
| Clay mechanic | Preserved exaggerated hands, clay texture and held poses; treated exact cadence as requiring deterministic control | [Style pair B](realism-style-forward.json) |
| Pristine skincare campaign | Kept the new product clean, separated exact label artwork, directed grip/contact/release and identified missing references | [Product proposal](realism-product-forward.json) |
| Reported hand penetration and camera glance, no playable clip | Held final acceptance, proposed local repair, left temporal/audio inspection unresolved and gave no invented detection percentage | [Evidence proposal](realism-evidence-forward.json) |

The [scenario inputs](realism-forward-inputs.json) preserve the requests and constraints. Three fresh contexts produced these four scenario responses. Only local path prefixes and title punctuation were normalized for publication; substantive proposals were retained. All 37 existing unit tests, the repository checker and the Skill Creator validator passed locally after the runtime changes. The revised core is 1,198 words with 19 directly linked references. These results do not establish actual media quality.

An independent final reviewer assessed all three proposals against the exact briefs and found no substantive planning failure. The reviewer caught one overbroad phrase in the guide: reflections were incorrectly required not to change. It was corrected to reject physically inconsistent reflection changes while permitting the changes caused by object, camera, scene or light motion. This illustrates why visual plausibility requires causal checks rather than blanket rules for stillness or imperfection.

The existing financial/schema suite and packaging validators remain the automated checks. They cannot measure photographic quality. No images or videos were generated, no uploads or cost estimates were submitted, and no Higgsfield credits were spent for this revision.

## Future evaluation of actual outputs

1. Define the claim before generating: brief adherence, perceived photographic realism, or audience attribution of generative origin. Keep these separate. Fix viewing conditions and acceptance criteria first.
2. Use the user's authorized allocation. Record model/mode, prompt/reference version, settings and post-production. Keep all attempt outcomes in the process record. A selected best result does not measure first-attempt success or improvement per credit.
3. Inspect the actual deliverable at intended size and its risky details at native scale. Watch complete video with sound at normal speed, then inspect transitions and interactions frame by frame. Record uninspected portions. Recheck the final export after processing.
4. If audience feedback is useful, recruit willing viewers representative of the intended audience and record their relevant experience. Randomize presentation order, conceal production method during the exercise and explain/debrief the exercise appropriately. Ask for the ordinary impression before prompting artifact scrutiny.
5. For an origin-detection study, include rights-cleared real controls matched for subject, framing, polish, duration and compression. Use comparable non-generative CG/animation for stylized work. Do not compare glossy synthetic ads only against rough phone footage. Keep normal viewing and zoom/replay scrutiny as separate conditions, with an uncertain response option.
6. Report raw responses and denominators per asset and condition, reasons, disagreement, real-control false positives and selection method. A small convenience panel gives asset-specific feedback, not a population guarantee. Repeated ratings from the same viewers or similar variants are not independent samples. Without controls, call it viewer impressions, not detection accuracy.
7. To compare a revision, use the same briefs and comparable settings, references, finishing and allocation. Preserve both accepted and failed candidates. A single chosen before/after pair cannot establish a causal improvement or universal success rate. Use feedback to diagnose one concrete repair, then reassess within authorization.

AI/VLM inspection can assist triage. It is not a substitute for human audience observations or an authentic record of capture. No human-viewer study has been run for this skill.
