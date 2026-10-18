# Spend deliberately

Research, browsing and estimates do not authorize generation. A model preference is not a budget. Preserve an explicit allocation already authorized for this task.

## Prepare a bounded proposal

Before asking for missing spending authorization, finish the brief, prompt, reference mapping, selected route, settings and exact quote. Ask once, concretely: “The proposed one-clip test is quoted at X credits. May I spend up to Y credits across at most N attempts, including the listed finishing steps?” Do not substitute those example letters for actual tool results.

Record the user's chosen maximum, output/attempt cap, permitted models or workflow, charge mode and scope. A task-wide allocation can cover planned revisions without repeated questions. A request-only authorization covers only that request. Do not interpret “keep trying” as an unlimited budget.

## Quote the actual operation

- Include output count, duration, reference-video billing, quality, resolution, audio, training, enhancement, export/render and any recipe sub-jobs. Quote every billable stage or obtain a bounded workflow quote. Do not advertise a whole workflow at its first step's price.
- Use the active surface's estimator or displayed quote. Account credits and API currency are separate units. Never convert with an invented exchange rate or use an old marketing price.
- Inspect returned coercions. A nearest-supported duration, changed aspect ratio or capped batch can change the deliverable. Do not silently submit an adjusted request. Reconcile it with the user's constraints and bind the quote to the actual prepared parameters.
- A price estimate can import HTTPS references and create media records. For a price-only/no-upload request, omit references if the estimator permits it and label the quote provisional. Do not call an estimate “read-only” merely because it submits no generation.
- Reuse confirmed UUIDs and returned `prepared_params`; avoid repeatedly importing the same URL. A successful quote does not establish reference existence, ownership, duration validity or readiness.

## Payment mode is explicit

Do not infer that web Unlimited means free MCP/API usage. The dated public help says automated surfaces consume credits, while the observed MCP contract also exposes `use_unlim`, `unlim_choice` and some free-generation paths. This conflict requires the current route's response, not a blanket assertion in either direction.

If the server returns a payment choice, no generation was submitted. Preserve the request and obtain the user's choice unless already authorized. Request free generations only when the user asks; inspect current eligibility. Never fall back from rejected free/Unlimited to credits automatically. A zero-credit quote does not authorize an unwanted generation, external upload or publication.

## Reserve and reconcile

Before submission reserve the full quoted charge and an attempt in the task ledger. The available amount is the approved ceiling minus confirmed charges and all unresolved reservations. Do not count expected refunds or remaining account balance as new authorization. Count each batch output and recipe sub-job according to the quote's scope.

Use a stable local request ID and a fingerprint of the exact tool, parameters and input identities. This local fingerprint is not a provider idempotency key. Retain provider job IDs immediately. An unknown outcome remains reserved; inspect existing jobs before retrying. Do not resend to show a widget, change resolution or recover a lost response.

A failed job can still have a charge. Release a reservation or record a refund only after authoritative reconciliation. Do not respend a reported refund until the ledger reflects it. When no status recovery is available, stop and report the uncertainty.

Run the offline [preflight contract](preflight-contract.md) before any submission. Its timestamps are local freshness policy, not vendor price-expiry promises. It checks supplied records; it cannot prove consent, live prices, ownership or actual billing. Native tool gates remain mandatory.

Sources: [Higgsfield credit usage](https://higgsfield.ai/creator-hub/help-center/credits/what-uses-my-credits), plus current `estimate_image_cost`, `estimate_video_cost`, `generate_image`, `generate_video` and model-discovery tool contracts inspected 19 October 2026, Johannesburg time. No account balances are included in the research record.
