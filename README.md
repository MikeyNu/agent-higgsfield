# Higgsfield Director

A model-aware, cost-controlled directive skill for Higgsfield image, video, editing, audio and 3D work.

**Start with [SKILL.md](skills/higgsfield-director/SKILL.md).** Do not load the whole repository. The core directs an agent to the one relevant model guide and workflow.

Use it with a request such as:

> Read the Higgsfield Director skill in this repository. Plan a continuous camera journey from my approved scene. Preserve its architecture and lighting. Prepare the prompt, references and current cost before any generation. My total spending limit is [your chosen amount], including retries and finishing.

Replace the bracketed amount or ask for a quote first. Sharing the repository does not authorize paid generation. The skill respects a task allocation already approved and does not ask again for each revision within that allocation.

## Included

- Independently loadable guides for Kling, Seedance, Veo, Sora, Wan/MiniMax/Grok and new video families; GPT Image, Gemini/Nano Banana, Seedream, FLUX, Soul, Ideogram/Recraft and new image families.
- Workflow direction for Cinema Studio, Genjutsu, Katana, camera controls and three distinct Blender integrations.
- A capability and spending preflight tool, request fingerprints, budget reservations and duplicate-submission checks.
- Shot planning, reference roles, continuity, QA and targeted repair methods.
- Dated primary-source research, qualified practitioner reports, documentation conflicts and an honest test record.

The skill does not guarantee exact output. Precise geometry, typography, timing and camera paths may require deterministic controls or post-production. Prompt guidance never overrides the selected tool's live schema, the user's instructions or approval gates.

## Use as a skill

The installable folder is `skills/higgsfield-director`. It includes standard `SKILL.md` frontmatter and `agents/openai.yaml`. Copy that folder into your agent's supported skill location, or provide this repository link and instruct the agent to read the entry file. No dependencies or credentials are needed for the offline checks.

## Offline verification

```bash
python -m unittest discover -s tests -v
python scripts/check_repository.py
```

The example request intentionally fails closed until actual consent, live capability evidence, confirmed media and a fresh quote are supplied. `preflight.py` never submits a job and cannot authenticate a budget record on its own.

See [research and test scope](research/VALIDATION.md), [source register](research/sources.json) and [catalog snapshot](research/catalog-snapshot.json). The catalog is dated audit evidence, not a permanent list of supported settings or prices.

License: existing MIT license. Research summaries are original paraphrases; linked sources retain their own rights.
