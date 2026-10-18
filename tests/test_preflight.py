"""Boundary tests for the local advisory gate. No provider calls or paid generations."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/higgsfield-director/scripts/preflight.py"
EXAMPLE = ROOT / "skills/higgsfield-director/assets/request.example.json"
spec = importlib.util.spec_from_file_location("preflight", SCRIPT)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)
NOW = datetime(2026, 10, 19, 0, 0, tzinfo=timezone.utc)


def fixture():
    manifest = json.loads(EXAMPLE.read_text())
    manifest["capability"]["checked_at"] = NOW.isoformat()
    manifest["quote"]["checked_at"] = NOW.isoformat()
    manifest["quote"]["request_fingerprint"] = preflight.fingerprint(manifest["request"])
    manifest["consent"]["intent"] = "generate"
    manifest["media"][0]["confirmed"] = True
    return manifest


def requote(manifest):
    manifest["quote"]["request_fingerprint"] = preflight.fingerprint(manifest["request"])


class PreflightTests(unittest.TestCase):
    def assertBlocked(self, manifest, contains):
        result = preflight.check(manifest, NOW)
        self.assertFalse(result["ok"], result)
        self.assertTrue(any(contains in error for error in result["errors"]), result)

    def test_valid_task_scoped_retry_with_fresh_quote(self):
        m = fixture()
        m["request"]["params"]["prompt"] = "The camera remains fixed. Only the foreground sphere rotates once."
        requote(m)
        self.assertTrue(preflight.check(m, NOW)["ok"])

    def test_example_never_accidentally_authorizes_spend(self):
        self.assertBlocked(json.loads(EXAMPLE.read_text()), "consent.intent")

    def test_scope_and_actual_intent_cannot_be_inferred(self):
        for intent in ("plan", "quote", "research", True, None):
            with self.subTest(intent=intent):
                m = fixture()
                m["consent"]["intent"] = intent
                self.assertBlocked(m, "consent.intent")
        m = fixture()
        m["consent"]["scope"] = {"task_id": "another-task"}
        self.assertBlocked(m, "scope")
        m["consent"]["scope"] = {"task_id": m["request"]["task_id"], "request_fingerprint": m["quote"]["request_fingerprint"]}
        self.assertBlocked(m, "scope")

    def test_missing_consent_is_blocked(self):
        m = fixture()
        del m["consent"]
        self.assertBlocked(m, "consent")

    def test_request_scoped_consent_does_not_authorize_prompt_revision(self):
        m = fixture()
        m["consent"]["scope"] = {"request_fingerprint": m["quote"]["request_fingerprint"]}
        m["request"]["params"]["prompt"] += " Changed."
        requote(m)
        self.assertBlocked(m, "scope")

    def test_quote_invalidated_by_every_execution_field(self):
        for field in ("prompt", "duration", "aspect_ratio", "count"):
            with self.subTest(field=field):
                m = fixture()
                m["request"]["params"][field] = {"prompt": "New motion.", "duration": 10, "aspect_ratio": "9:16", "count": 2}[field]
                self.assertBlocked(m, "fingerprint")

    def test_stale_and_future_evidence_blocked(self):
        for where, timestamp in (("quote", "2026-10-18T23:54:59Z"),
                                 ("capability", "2026-10-17T23:59:59Z"),
                                 ("quote", "2026-10-19T00:00:31Z"),
                                 ("quote", "2026-10-19T00:00:00")):
            with self.subTest(where=where, timestamp=timestamp):
                m = fixture()
                m[where]["checked_at"] = timestamp
                self.assertBlocked(m, where + ".checked_at")

    def test_boundary_timestamp_is_accepted(self):
        m = fixture()
        m["quote"]["checked_at"] = "2026-10-18T23:55:00Z"
        m["capability"]["checked_at"] = "2026-10-18T00:00:00Z"
        self.assertTrue(preflight.check(m, NOW)["ok"])

    def test_no_inferred_model_alias_or_tool_alias(self):
        for field in ("model", "tool"):
            with self.subTest(field=field):
                m = fixture()
                m["request"][field] += "-alias"
                requote(m)
                self.assertBlocked(m, "capability." + field)

    def test_model_cannot_hide_in_actual_provider_params(self):
        m = fixture()
        m["request"]["params"]["model"] = "other-provider-model"
        requote(m)
        self.assertBlocked(m, "model_pointer")

    def test_unsupported_and_wrong_type_controls_blocked(self):
        for key, value in (("duration", 8), ("duration", True), ("duration", "5"),
                           ("aspect_ratio", "1:1"), ("count", 0), ("count", 3),
                           ("count", 1.0), ("invented_control", "yes")):
            with self.subTest(key=key, value=value):
                m = fixture()
                m["request"]["params"][key] = value
                requote(m)
                self.assertBlocked(m, "params")

    def test_payment_modes_and_fallbacks_are_explicit(self):
        for mode in ("unlimited", "free"):
            with self.subTest(mode=mode):
                m = fixture()
                m["request"]["payment_mode"] = mode
                m["quote"]["payment_mode"] = mode
                m["quote"]["charge_credits"] = "0"
                m["capability"]["payment_modes"].append(mode)
                requote(m)
                self.assertBlocked(m, "permitted_payment_modes")
                m["consent"]["permitted_payment_modes"].append(mode)
                self.assertTrue(preflight.check(m, NOW)["ok"])
                m["quote"]["charge_credits"] = "0.01"
                self.assertBlocked(m, "zero credit charge")
        m = fixture()
        m["quote"]["fallback"] = True
        self.assertBlocked(m, "fallback")
        m = fixture()
        m["request"]["params"]["credit_fallback"] = True
        requote(m)
        self.assertBlocked(m, "fixed value")

    def test_quote_must_price_all_outputs(self):
        m = fixture()
        m["request"]["params"]["count"] = 2
        requote(m)
        m["quote"]["includes_all_outputs"] = False
        self.assertBlocked(m, "all-output")

    def test_unknown_and_reserved_charges_count_in_full(self):
        for status in ("unknown", "reserved", "charged"):
            with self.subTest(status=status):
                m = fixture()
                m["ledger"][0]["status"] = status
                m["ledger"][0]["amount_credits"] = "12.50000000000000000000000000001"
                self.assertBlocked(m, "budget")

    def test_arbitrary_precision_is_not_rounded_down(self):
        m = fixture()
        m["ledger"][0]["amount_credits"] = "0.00000000000000000000000000001"
        m["quote"]["charge_credits"] = "25"
        self.assertBlocked(m, "budget")
        m["quote"]["charge_credits"] = "24.99999999999999999999999999999"
        self.assertTrue(preflight.check(m, NOW)["ok"])

    def test_exact_budget_boundary_and_count_boundary(self):
        m = fixture()
        m["ledger"][0]["amount_credits"] = "12.5"
        self.assertTrue(preflight.check(m, NOW)["ok"])
        m["consent"]["max_attempts"] = 1
        self.assertBlocked(m, "attempts")

    def test_negative_nan_infinite_boolean_costs_rejected_everywhere(self):
        for value in (-1, "-0.01", "NaN", float("inf"), True, None, {}, "1e200"):
            for where in ("quote", "consent", "ledger"):
                with self.subTest(value=value, where=where):
                    m = fixture()
                    if where == "quote":
                        m["quote"]["charge_credits"] = value
                    elif where == "consent":
                        m["consent"]["ceiling_credits"] = value
                    else:
                        m["ledger"][0]["amount_credits"] = value
                    self.assertBlocked(m, "credit amount")

    def test_invalid_attempt_counts_rejected(self):
        for value in (True, 0, -1, "2", 2.0):
            m = fixture()
            m["consent"]["max_attempts"] = value
            self.assertBlocked(m, "max_attempts")

    def test_no_duplicate_or_unresolved_resubmission(self):
        m = fixture()
        m["request_id"] = m["ledger"][0]["request_id"]
        self.assertBlocked(m, "request_id")
        for status in ("reserved", "unknown"):
            m = fixture()
            m["ledger"][0]["status"] = status
            m["ledger"][0]["request_fingerprint"] = m["quote"]["request_fingerprint"]
            self.assertBlocked(m, "unresolved")
        m = fixture()
        m["ledger"].append(copy.deepcopy(m["ledger"][0]))
        self.assertBlocked(m, "request_id")

    def test_refunds_not_inferred_from_status(self):
        m = fixture()
        m["ledger"][0]["status"] = "failed_refunded_probably"
        self.assertBlocked(m, "refunds are never inferred")

    def test_media_is_bound_to_exact_asset_and_role(self):
        mutations = [lambda m: m["media"].clear(),
                     lambda m: m["media"][0].update(confirmed=False),
                     lambda m: m["media"][0].update(role="unsupported-last-frame"),
                     lambda m: m["media"][0].update(value="attachment://wrong-frame"),
                     lambda m: m["media"].append(copy.deepcopy(m["media"][0]))]
        for mutate in mutations:
            m = fixture()
            mutate(m)
            self.assertBlocked(m, "media")

    def test_unaccepted_coercion_blocks_generation(self):
        m = fixture()
        m["coercions"] = [{"description": "Use a different duration", "accepted": False, "source": "pending"}]
        self.assertBlocked(m, "coercion")
        m["coercions"][0]["accepted"] = True
        self.assertTrue(preflight.check(m, NOW)["ok"])

    def test_conflicting_controls_and_nested_unknowns_rejected(self):
        m = fixture()
        m["capability"]["conflicts"] = [["/first_frame", "/duration"]]
        self.assertBlocked(m, "conflicting")
        m = fixture()
        m["capability"]["params_schema"]["properties"]["settings"] = {
            "type": "object", "properties": {"frames": {"type": "array", "items": {"type": "string"}, "maxItems": 2}}
        }
        m["request"]["params"]["settings"] = {"frames": ["a", "b", "c"], "stealth_spend": True}
        requote(m)
        self.assertBlocked(m, "maxItems")
        self.assertBlocked(m, "stealth_spend")

    def test_unknown_envelope_fields_fail_closed(self):
        m = fixture()
        m["request"]["auto_retry"] = True
        requote(m)
        self.assertBlocked(m, "unknown field")

    def test_canonical_fingerprint_order_independent_but_value_sensitive(self):
        first = {"b": [1, 2], "a": "é"}
        self.assertEqual(preflight.fingerprint(first), preflight.fingerprint({"a": "é", "b": [1, 2]}))
        self.assertNotEqual(preflight.fingerprint(first), preflight.fingerprint({"a": "é", "b": [2, 1]}))

    def test_cli_malformed_and_duplicate_json_return_machine_readable_failure(self):
        for content in ("{broken", '{"version":1,"version":2}', "[]", '{"request":{"params":{"x":NaN}}}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "manifest.json"
                path.write_text(content)
                completed = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(completed.returncode, 2, completed.stderr)
                result = json.loads(completed.stdout)
                self.assertFalse(result["ok"])
                self.assertIn("fingerprint", result)

    def test_cli_success_and_missing_file_exit_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            m = fixture()
            m["capability"]["checked_at"] = datetime.now(timezone.utc).isoformat()
            m["quote"]["checked_at"] = m["capability"]["checked_at"]
            path.write_text(json.dumps(m))
            passed = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            self.assertTrue(json.loads(passed.stdout)["ok"])
            path.unlink()
            missing = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(missing.returncode, 2)
            self.assertFalse(json.loads(missing.stdout)["ok"])

    def test_json_numeric_credit_precision_bypass_is_blocked(self):
        for where, field in (("quote", "charge_credits"), ("consent", "ceiling_credits")):
            m = fixture()
            m[where][field] = 0.1
            self.assertBlocked(m, "decimal string or integer")
        m = fixture()
        m["ledger"][0]["amount_credits"] = 0.1
        self.assertBlocked(m, "decimal string or integer")
        m = fixture()
        m["ledger"] = []
        m["quote"]["charge_credits"] = "RAW_DECIMAL"
        m["consent"]["ceiling_credits"] = "0.1"
        m["quote"]["checked_at"] = datetime.now(timezone.utc).isoformat()
        m["capability"]["checked_at"] = m["quote"]["checked_at"]
        raw = json.dumps(m).replace('"RAW_DECIMAL"', "0.10000000000000000000000000001")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "precision.json"
            path.write_text(raw)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["ok"])

    def test_invalid_or_undeclared_pointers_are_not_silently_ignored(self):
        for value in (None, "first_frame", "/undeclared", "/first~2frame", 3):
            m = fixture()
            m["media"] = []
            m["capability"]["media_slots"]["first_frame"]["pointer"] = value
            self.assertBlocked(m, "valid JSON pointer")
        for group in (["first_frame", "duration"], ["/absent", "/duration"]):
            m = fixture()
            m["capability"]["conflicts"] = [group]
            self.assertBlocked(m, "valid JSON pointer")
        for field in ("count", "duration", "ratio"):
            m = fixture()
            m["capability"]["bindings"][field] = "/undeclared"
            self.assertBlocked(m, "valid JSON pointer")

    def test_ledger_fingerprint_task_conflict_is_blocked(self):
        m = fixture()
        m["ledger"][0]["request_fingerprint"] = m["quote"]["request_fingerprint"]
        m["ledger"][0]["task_id"] = "another-task"
        self.assertBlocked(m, "conflicts with the current task_id")
        m = fixture()
        other = copy.deepcopy(m["ledger"][0])
        other.update(request_id="other-request", task_id="another-task")
        m["ledger"].append(other)
        self.assertBlocked(m, "conflicting task IDs")

    def test_nested_exact_values_do_not_equate_false_and_zero(self):
        for guard in ("enum", "fixed", "media"):
            m = fixture()
            m["request"]["params"]["nested"] = {"flags": [0]}
            nested_schema = {"type": "object", "properties": {"flags": {"type": "array", "items": {"type": "integer"}}}}
            m["capability"]["params_schema"]["properties"]["nested"] = nested_schema
            if guard == "enum":
                nested_schema["enum"] = [{"flags": [False]}]
                error = "not a discovered option"
            elif guard == "fixed":
                m["capability"]["fixed_values"]["/nested"] = {"flags": [False]}
                error = "fixed value"
            else:
                m["capability"]["media_slots"]["nested"] = {"pointer": "/nested"}
                m["media"].append({"role": "nested", "pointer": "/nested", "value": {"flags": [False]}, "confirmed": True, "source": "synthetic confirmation"})
                error = "exact submitted parameter"
            requote(m)
            self.assertBlocked(m, error)

    def test_full_schema_validation_includes_unused_branches(self):
        m = fixture()
        m["capability"]["params_schema"]["properties"]["unused"] = {"type": "string", "pattern": "safe-only"}
        self.assertBlocked(m, "unknown field pattern")
        m["capability"]["params_schema"]["properties"]["unused"] = {"type": "array", "items": {"type": "string", "maxLength": True}}
        self.assertBlocked(m, "must be an integer")

    def test_output_allowance_is_separate_from_attempt_allowance(self):
        m = fixture()
        m["request"]["params"]["count"] = 2
        requote(m)
        self.assertBlocked(m, "per-submission")
        m["consent"]["max_outputs_per_submission"] = 2
        self.assertBlocked(m, "1 prior + 2 exceeds authorized 2")
        m["consent"]["max_outputs"] = 3
        self.assertTrue(preflight.check(m, NOW)["ok"])
        m["request"]["params"]["prompt"] += " Revised within the existing task allocation."
        requote(m)
        self.assertTrue(preflight.check(m, NOW)["ok"])

    def test_output_reservations_and_fixed_count_are_enforced(self):
        for status in ("charged", "reserved", "unknown"):
            m = fixture()
            m["ledger"][0].update(status=status, output_count=2)
            self.assertBlocked(m, "outputs")
        for count in (None, False, 0, -1, 1.0):
            m = fixture()
            m["ledger"][0]["output_count"] = count
            self.assertBlocked(m, "ledger.output_count")
        m = fixture()
        del m["capability"]["bindings"]["count"]
        del m["request"]["params"]["count"]
        del m["capability"]["params_schema"]["properties"]["count"]
        m["capability"]["params_schema"]["required"].remove("count")
        requote(m)
        self.assertBlocked(m, "capability.outputs_per_submission")
        m["capability"]["outputs_per_submission"] = 1
        self.assertTrue(preflight.check(m, NOW)["ok"])
        m["capability"]["outputs_per_submission"] = 2
        self.assertBlocked(m, "outputs")

    def test_unpaired_surrogate_cli_output_is_valid_json(self):
        m = fixture()
        m["\ud800"] = 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "surrogate.json"
            path.write_text(json.dumps(m, ensure_ascii=True))
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse(json.loads(result.stdout)["ok"])
        self.assertEqual(result.stderr, "")

    def test_same_fingerprint_cannot_understate_prior_output_count(self):
        m = fixture()
        m["request"]["params"]["count"] = 2
        m["consent"].update(max_outputs=3, max_outputs_per_submission=2)
        requote(m)
        m["ledger"][0]["request_fingerprint"] = m["quote"]["request_fingerprint"]
        self.assertBlocked(m, "must match the current request count")
        m["ledger"][0]["output_count"] = 2
        self.assertBlocked(m, "2 prior + 2 exceeds authorized 3")
        m["consent"]["max_outputs"] = 4
        self.assertTrue(preflight.check(m, NOW)["ok"])

    def test_repeated_ledger_fingerprints_require_consistent_output_count(self):
        m = fixture()
        m["consent"].update(ceiling_credits="50", max_attempts=3, max_outputs=4)
        other = copy.deepcopy(m["ledger"][0])
        other.update(request_id="another-prior-attempt", output_count=2)
        m["ledger"].append(other)
        self.assertBlocked(m, "conflicting requested output counts")
        m["ledger"][1]["output_count"] = 1
        self.assertTrue(preflight.check(m, NOW)["ok"])


if __name__ == "__main__":
    unittest.main()
