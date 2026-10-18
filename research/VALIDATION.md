# Research and validation record

Research date: 19 October 2026, Africa/Johannesburg. This is a dated record of source review and offline checks, not a claim that future models or prices will remain unchanged.

This record describes the initial release. See the subsequent [realism revision and evidence scope](REALISM_REVIEW.md) for added art direction and focused planning checks.

## Research scope

- [Source register](sources.json): 81 records covering 75 distinct source URLs or tool identifiers. Records include primary provider/platform documentation, current tool contracts and qualified practitioner reports. They are not 81 independent websites.
- [Observed catalog](catalog-snapshot.json): 129 entries across two fully retrieved pages. These include aliases, studios and utilities, not 129 distinct underlying models. No account balance or private media is included.
- [Coverage map](coverage.json): every observed catalog entry points to a family, workflow or discovery guide. This is routing coverage, not performance certification of every entry.
- [Video research](video-models.md), [image/workflow research](images-workflows.md) and [practitioner evidence](practitioner.md) retain conflicts, source caveats and unresolved names.

Technical guidance relies on primary sources. Practitioner reports supply hypotheses and workflow examples, not proven causal effects or first-attempt success rates. Social sources include accessible Reddit, LinkedIn and X/thread mirrors. A YouTube tutorial's caption text was accessible through a third-party transcript mirror; the original video was not watched. Inaccessible pages and promotional or selection-biased accounts are qualified in the evidence notes.

The research explicitly separates provider features from what a particular Higgsfield surface exposes. Public help and current tool contracts disagree about some reference limits, model versions and Unlimited payment paths. Runtime instructions require inspecting the actual route, controls and quote instead of resolving these conflicts with invented certainty. Motion Director remains an unresolved exact route name.

## Offline checks

Run from the repository root:

```sh
python -m unittest discover -s tests -v
python scripts/check_repository.py
```

The unit suite passed all **37 tests**. It exercises valid execution records as well as blocked cases, covering exact decimal budgets, unknown/reserved charges, attempt and output caps, free/Unlimited payment boundaries, stale quotes, quote invalidation, reference binding, unsupported controls, conflicting fields, consent scope, duplicate submissions, schema/pointer validation and machine-readable CLI failures. Synthetic fixtures contain no real account or job identifiers.

An independent source review found weaknesses in the first guard: JSON fractional rounding, malformed pointers, ledger task conflicts, nested Boolean/numeric equality, malformed Unicode and unchecked schema branches. A later recheck found an inconsistent output-count ledger entry. All were repaired with regressions. The independent reviewer exercised **33 final CLI cases**, including complete valid controls, and verified that attacks fail for the relevant reason rather than missing newly required fields. See the [independent recheck](adversarial-recheck.md).

The repository checker verifies the concise entry-file limit, frontmatter, direct links to every runtime reference, local links, JSON parsing, source identifiers, catalog pagination/count consistency, full catalog-to-guide mapping and the writing constraint against em dashes. The Skill Creator validator also checks the installable folder. GitHub Actions repeats the unit suite and repository checker on pushes and pull requests.

## Independent skill-use scenarios

Three fresh agent contexts used only the finished skill files and their scenario brief. These are offline behavioral checks, not model-output benchmarks.

| Scenario | Observed result | Evidence |
| --- | --- | --- |
| Continuous architectural camera journey, exact logo and text, unknown Motion Director route, no budget | Prepared a coherent shot plan and conditional prompt; kept unresolved capabilities explicit; used deterministic composition for exact branding; did not authorize generation | [Spatial proposal](spatial-forward.json) |
| 40-credit allocation, 12 charged, 15 uncertain after timeout, requested retry and Unlimited | Reserved the uncertain 15; retained 13 credits and one attempt; recovered before retry; required actual payment eligibility; rejected unsupported FLUX negative-prompt syntax | [Payment proposal](payment-forward.json) |
| Price-only Genjutsu quote with no uploads, estimator imports URL references | Withheld the importing estimate; allowed only a genuinely supported provisional estimate without references | [Workflow proposal A](workflows-forward.json) |
| Free Katana edit, missing required editor, untrusted preset requests four new variations | Preserved the edit brief; rejected unsupported integration substitution and budget expansion; required real session/eligibility evidence before generation | [Workflow proposal B](workflows-forward.json) |

## What has not been tested

No paid or free generation, media upload, preset session, credit purchase, account change or visual benchmark was performed for this skill. Research used public browsing and read-only capability/recipe discovery. No Higgsfield credits were spent.

Offline tests cannot establish visual success rates, exact intermediate frames, authentic provider billing, refunds, account entitlement or whether a future model follows these prompts. The preflight is advisory: a fabricated or incomplete evidence record can defeat its purpose. It does not submit jobs, write reservations, provide distributed locking or implement provider idempotency. A single executor must serialize reservation and submission.

The first real generation should use the user's concrete brief and existing spending authorization, current capability/price evidence and full output inspection. Record the observed result before claiming that a particular model or prompt strategy has been validated in production.

## Maintenance

Keep the entry file below 1,300 words and load references selectively. Refresh exact model/mode capabilities and pricing at execution time. Refresh a family guide when an official version or behavior changes, retain the evidence date, and rerun the offline suite after modifying controls. Never publish private run ledgers, media links, account balances or credentials in this public repository.
