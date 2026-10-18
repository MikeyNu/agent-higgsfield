# Offline preflight contract

Read when preparing a paid or otherwise limited generation. This is a local advisory gate, not an executor, billing authority, consent verifier, universal provider adapter, or proof that a quote/capability snapshot is genuine. A fabricated manifest can pass. Inspect the actual tool response and user authorization. Never relabel invented evidence as verified evidence.

## Run

```sh
python skills/higgsfield-director/scripts/preflight.py path/to/manifest.json
python -m unittest discover -s tests -v
```

The CLI prints one JSON object: `ok`, `errors`, `warnings`, `fingerprint`. Exit `0` means local checks passed; `2` means blocked. It never calls a provider, generates content, writes a reservation, or spends credits. All generation, including zero-credit modes, still needs actual generation intent. The example in `assets/request.example.json` is deliberately non-executable and fails until real evidence replaces its placeholders, old timestamps, plan intent and unconfirmed media.

## Envelope, version 1

| Field | Contract |
|---|---|
| `version` | Integer `1`. |
| `request_id` | Unique ID for this submission attempt, outside the quote fingerprint. Never reuse an ID already in the ledger. |
| `request` | Exactly `task_id`, `tool`, `model`, `payment_mode`, `params`. Use exact provider/tool identifiers and the complete final submitted argument object. |
| `capability` | Fresh observed schema and account controls, described below. |
| `quote` | Fresh all-output cost for the exact final request. |
| `consent` | Traceable existing generation authorization, scope and limits. |
| `media` | Confirmations bound to exact submitted assets and slots. |
| `coercions` | Explicit accepted changes, or `[]`. |
| `ledger` | Every previous charged, reserved and uncertain submission under the relevant authorization, including other prompt versions. |

Unknown envelope, request and fixed-record fields fail closed. Credit fields accept only nonnegative finite decimal strings such as `"12.5"` or exact JSON integers. JSON fractional numbers, including `12.5` and `1.0`, are rejected because ordinary JSON parsing can already have rounded them before the gate sees them. Preserve the quoted decimal amount from authoritative evidence; do not recover supposed precision by stringifying an already rounded value. Booleans, NaN, infinity, negatives and exponents beyond 100 places fail. Decimal addition preserves small fractions rather than rounding them away. `max_attempts` counts tool submissions; independent output caps count every requested/reserved output, including retries. Price must cover the full batch.

### Capability snapshot

Required fields:

- `checked_at`: timezone-aware ISO 8601 timestamp, no older than 24 hours. Refresh sooner whenever the model, mode, plan, tool schema or controls change.
- `source`: actual evidence reference, such as the relevant tool response or account UI observation. A public article does not establish account entitlement.
- `tool`, `model`, `payment_modes`: exact submission identifiers and available modes. Modes are `credits`, `unlimited`, `free`. No aliases or entitlements are inferred.
- `params_schema`: recursive schema of the actual submitting tool's arguments. Supported types: `object`, `array`, `string`, `integer`, `number`, `boolean`, `null`. Optional constraints: `enum`, `minimum`, `maximum`, `minLength`, `maxLength`, `minItems`, `maxItems`. Objects use `properties` and `required`; unknown properties are always rejected. Arrays require `items`. Unions, regexes and general JSON Schema features are unsupported. Do not silently erase a live constraint that cannot be represented; perform the additional check explicitly and extend the validator when needed.
- `model_pointer`: JSON pointer into `request.params` selecting the actual model, or `null` for a tool intrinsically bound to this one model. The selection must match `request.model` exactly.
- `bindings`: optional `duration`, `ratio`, `count` names mapped to pointers into the final params. Include applicable controls. Every pointer must resolve and its value must pass the discovered schema. Duration and count must also be positive. Model-specific enumerations and bounds belong in `params_schema`.
- `outputs_per_submission`: `null` when `bindings.count` identifies an actual count parameter. Otherwise a positive integer observed for a tool intrinsically producing a fixed number of outputs. Never omit a real count binding to substitute a smaller fixed value, or infer that one submission returns one output. If the maximum output quantity is unknown, stop.
- `media_slots`: role names mapped to `{"pointer":"/actual_parameter"}`. Include every asset-bearing parameter. An array-valued slot can cover an entire reference list; its confirmation then binds the exact whole list, and the schema limits its cardinality.
- `fixed_values`: pointers mapped to exact required values, for example `{"/credit_fallback":false}` if that control actually exists. Never invent a provider parameter just to satisfy this guard.
- `conflicts`: arrays of mutually exclusive parameter pointers, for example `[["/start_image","/video_reference"]]` only if observed as incompatible. Omit unused controls entirely; a present false/null field still counts as present for this conservative check.

The entire schema is checked, including unused branches. All media, binding, fixed-value and conflict pointers must be well formed and resolve to declared schema parameters. Exact-value checks compare types recursively, so nested `false`, `0` and `0.0` are different values. A malformed or missing media pointer cannot silently disable confirmation.

**Normalize evidence to the tool being called.** A backend model record may name `image_references` or `video_references`, while the generic submission tool uses `image`, `video`, `start_image`, `end_image`. Discover the actual tool schema and accepted mapping. The snapshot, media pointers and fingerprint use final tool arguments. Do not mechanically pass backend field names, infer that similarly named roles are interchangeable, or invent a mapping to make validation pass.

### Request fingerprint and quote

Fingerprint is SHA256 of the UTF-8 encoding of `json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)`. This is the script's specific canonicalization, not RFC 8785. Use its `fingerprint()` function or returned value rather than hashing pretty-printed JSON. Request IDs, timestamps, evidence and consent are outside this hash. Tool, model, mode, task and every argument are inside it.

Quote fields: `checked_at`, `source`, `request_fingerprint`, `payment_mode`, `charge_credits`, `includes_all_outputs:true`, `fallback:false`. Timestamp must be no older than five minutes; timestamps over 30 seconds in the future fail. `charge_credits` is the exact current total or conservative confirmed upper bound for all outputs, fees and settings. If the provider cannot establish an upper bound, stop. `free` and `unlimited` require zero credit charge, explicit entitlement evidence and permission for that mode. Never fall back to credits automatically.

Normalize the returned pricing once: use the provider's full batch total, never multiply a total by the output count again. If both displayed `credits` and `credits_exact` exist, do not round down or select the smaller value without documented billing semantics. Retain the conservative confirmed total and evidence explaining the normalization. The guard compares that normalized total; it cannot determine which provider response field is billable.

An estimate may return `prepared_params` or coercions that rewrite the model ID, duration, ratio or inputs. Inspect that response first. Obtain acceptance for material changes not already covered by the user's task authorization, normalize to the actual submitting tool, and fingerprint that final request. If the estimate does not clearly price those final arguments, estimate again before submission. A prompt edit, different asset or changed output count requires a matching quote. A quote does not itself grant permission.

### Consent, media and changes

Consent fields:

- `intent:"generate"`, `source`: record the actual user's instruction, never a proposed instruction or the agent's own decision. Research, plan and quote intent are blocked.
- `scope`: exactly one of `{"task_id":"..."}` or `{"request_fingerprint":"..."}`.
- `approved_models`, `approved_tools`, `permitted_payment_modes`: explicit arrays representing what the user already authorized.
- `ceiling_credits`, `max_attempts`, `max_outputs`: total authorized credit, submission and output limits for that scope, including prior charged, reserved and uncertain attempts. `max_outputs_per_submission` independently caps the size of any one batch. Counts must be positive integers. A one-call allowance is not automatically permission to create a multi-output batch.

Task scope permits new prompts and retries under the same allocation and approved model/tool/mode choices. **Do not demand permission for each prompt change when that work is already authorized.** Derive the count limits from the user's existing task allocation where clear, for example one initial clip plus one permitted retry gives two submissions, two total outputs, and one per submission. Update the quote, use a new request ID and preserve the ledger. Request scope is intentionally narrower and does not cover a changed request. If the user has not established a numeric allocation or acceptable maximum, obtain that boundary before spending; this does not require repeating settled permissions.

Each media record is `{"role":"first_frame","pointer":"/start_image","value":"actual-reference","confirmed":true,"source":"actual asset authorization"}`. Role names and pointers must match discovered slots. Confirm the exact source, rights/authorization, accessibility, intended crop, aspect and ordering before setting true. The script only checks the record's consistency, not the pixels or the asset's existence.

Each coercion is `{"description":"...","accepted":true,"source":"user instruction or existing task scope covering it"}`. Unaccepted changes block. Keep `[]` when no changes were proposed. An accepted change still needs valid parameters, matching cost and permitted scope.

### Reservation and reconciliation

Each ledger row has `request_id`, `task_id`, `request_fingerprint`, `status`, `amount_credits`, `output_count`. Supported statuses: `charged`, `reserved`, `unknown`. `output_count` retains the positive original requested/reserved output count. For reserved or unknown work, retain the original confirmed charge total/upper bound, not zero or only the portion already visible. If the possible charge or output quantity cannot be bounded, stop and reconcile before further spending. A timeout or missing job ID is not evidence of failure or a refund. A fingerprint includes the task ID; rows associating the same fingerprint with conflicting tasks are invalid and cannot exclude that spend from the applicable scope.

Rows sharing the current request fingerprint must retain its full requested output count. Repeated ledger fingerprints must also have consistent task IDs and requested output counts. These checks prevent a known two-output request from being recorded as one output to bypass the allowance. They establish internal consistency only, not authenticity of historical requests or charges.

The gate counts all three statuses in budget, attempt and output totals. It blocks duplicate IDs and any unresolved row with the current request fingerprint. After passing, **reserve the quoted total, attempt and full output count in the shared ledger before calling the generation tool**. This script does not provide locking, atomic reservations, or protection against concurrent external writers. One owner must serialize ledger check, reservation and submission unless a real atomic reservation mechanism exists; rerun the check against the latest ledger. A changed or lowered allowance, quote or request invalidates an earlier pass. Submit once, record the provider job ID in the surrounding audit log, and reconcile actual charge from provider evidence. A local fingerprint is not a provider idempotency key and cannot prevent remote duplicate jobs. Do not erase uncertainty, infer refunds, reset task IDs or remove old rows to recover budget. Refund/release accounting requires an explicitly verified reconciliation and a reviewed extension to this conservative ledger format.

The snapshot and quote can still change after preflight. Check the live final submit screen or returned prepared request. If anything differs, stop, revise the manifest and recheck. Passing this offline gate is necessary for this workflow, but never sufficient evidence to bypass user intent or provider restrictions.
