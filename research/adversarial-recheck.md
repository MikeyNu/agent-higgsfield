# Repaired spending-guard recheck

Final result: all original reported attacks now block for their intended reason. No remaining spending or output-cap bypass was found in this focused recheck. The reviewer did not edit source or call network, provider or paid tools.

The final CLI recheck ran **33 cases: 8 valid controls passed and 25 invalid/over-limit cases blocked**. Every case included the repaired format's required `outputs_per_submission`, `max_outputs`, `max_outputs_per_submission` and ledger `output_count` fields. There were **zero missing-field errors**, so attack rejection was not an artifact of obsolete fixtures. All CLI results were parseable JSON, with exit 0 for passing cases, exit 2 for blocked cases and empty stderr.

The repository suite independently passed **37/37 tests** after the final repair.

Final tested script SHA256: `096df8296cfe7571ddf3cdaef3e2813b02303b4844fdb995b74d4ce8fa10ac55`.

## Original findings

| Finding | Final observed result |
|---|---|
| Raw JSON fractional credit rounds before checking | Blocked as an unsupported monetary encoding; quote, allowance and ledger locations checked independently. |
| Invalid media/conflict pointers disable checks | Blocked for invalid JSON pointers, including null media pointers and conflict strings lacking a slash. |
| Current fingerprint with contradictory ledger task ID | Blocked for task identity conflict. |
| Nested false/zero equality in fixed, enum and media records | Each mismatch blocked by the corresponding exact-value check. |
| Unsupported unused schema branch | Blocked for unsupported `pattern` field. |
| Unpaired surrogate breaks CLI error output | Returns parseable JSON failure, exit 2 and no traceback. |
| Output count previously unmodeled | Batch and total output limits now checked independently from submission limits. |

## Focused check of new behavior

- A complete refreshed synthetic example passes; the malformed attacks inherit complete valid fixtures.
- A 50-digit decimal-string sum exactly on its ceiling passes; adding the smallest tested fraction beyond that ceiling blocks. JSON floats fail at every monetary location.
- A two-output batch exactly at its authorized total and per-submission boundaries passes. Exceeding either relevant cap blocks.
- An intrinsically fixed one-output route passes; a fixed two-output route exceeding the batch cap blocks.
- Prior charged, reserved and unknown outputs all count against the total.
- Task-scoped and request-scoped retries of the exact same authorized request pass when sufficient budget, attempts and outputs remain.
- A task-scoped revision with a changed prompt and output count passes within its allocation; the new consistency check does not require unrelated prior fingerprints to share a count.

## Additional issue found and repaired during recheck

The first recheck found one Medium consistency issue introduced by output accounting: a charged ledger row could use the current two-output request fingerprint while claiming `output_count:1`. With `max_outputs:3`, the guard counted one prior plus two pending outputs and passed, although the identical fingerprint fixes the prior requested count at two.

The engineer repaired this. The current fingerprint now requires the matching requested output count; repeated historical fingerprints also must have consistent counts. Independent final CLI checks show:

1. Same current fingerprint with the understated prior count blocks for count inconsistency.
2. Correct prior count two with total ceiling three blocks for the actual four-output total.
3. Raising the ceiling to four permits legitimate task-scoped and request-scoped retries.
4. Conflicting output counts across the same historical fingerprint block even when the ordinary budget, attempt and output sums fit.
5. Consistent historical counts pass.

## Published evidence

[Final CLI outcomes](adversarial-recheck-results.json) contains the 33 final results and tested source hash. The independent scratch harness refreshed timestamps and rejected any failure caused by missing required fields. The permanent regression cases are included in [the unit suite](../tests/test_preflight.py), which can be rerun from the repository root with `python -m unittest discover -s tests -v`.

The scratch harness and intermediate manifests are not part of the runtime skill. This final record supersedes the original review's open-issue status. Stored quote timestamps expire; tests construct fresh synthetic evidence.

The offline guard still cannot authenticate evidence, establish ledger completeness, guarantee provider billing or provide atomic reservations. Those are documented architectural limits, not failures of this recheck.
