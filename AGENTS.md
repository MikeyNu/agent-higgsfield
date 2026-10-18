# Repository contract

- This repository contains a reusable skill, not an autonomous generation service.
- Read skills/higgsfield-director/SKILL.md before changing behavior.
- Never run paid media generation as a test. Offline fixtures must use synthetic IDs.
- Preserve explicit user intent, existing authorizations, spending limits and native approval gates.
- Do not publish account balances, tokens, private media URLs, private job IDs or client references.
- Verify changing capabilities against the current tool surface. A provider feature is not proof that Higgsfield exposes it.
- Attribute technical guidance to primary sources. Label practitioner evidence and untested hypotheses.
- Keep the main skill concise. Put model-specific guidance in independently loadable references.
- Do not claim exact visual fidelity or generation benchmarks from offline tests.
- Run python -m unittest discover -s tests -v and the skill validator before publishing.
- Use no em dashes in authored prose.
