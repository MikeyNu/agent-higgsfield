#!/usr/bin/env python3
"""Offline advisory spend gate. Never invokes a provider or authenticates evidence."""
import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext

MISSING = object()


def add_credits(a, b):
    with localcontext() as context:
        context.prec = max(28, max(a.adjusted(), b.adjusted(), 0) -
                           min(a.as_tuple().exponent, b.as_tuple().exponent, 0) + 2)
        return a + b


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def fingerprint(request):
    raw = json.dumps(request, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def exact(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(exact(value, b[key]) for key, value in a.items())
    if isinstance(a, list):
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    return a == b


def valid_pointer(path):
    return isinstance(path, str) and path.startswith("/") and not re.search(r"~(?![01])", path)


def pointer(value, path):
    if not valid_pointer(path):
        return MISSING
    try:
        for key in path[1:].split("/"):
            key = key.replace("~1", "/").replace("~0", "~")
            if isinstance(value, list):
                if not key.isdigit() or (len(key) > 1 and key.startswith("0")):
                    return MISSING
                value = value[int(key)]
            else:
                value = value[key]
        return value
    except (KeyError, IndexError, TypeError, ValueError):
        return MISSING


def check(manifest, now=None):
    errors, warnings = [], ["Advisory only: verify live controls, actual consent and ledger completeness before submitting."]
    fp = None
    now = now or datetime.now(timezone.utc)

    def fail(path, message):
        errors.append(f"{path}: {message}")

    def obj(value, path, required, optional=()):
        if not isinstance(value, dict):
            fail(path, "must be an object")
            return {}
        for key in set(required) - value.keys():
            fail(path, f"missing {key}")
        for key in value.keys() - set(required) - set(optional):
            fail(path, f"unknown field {key}")
        return value

    def string(value, path):
        if not isinstance(value, str) or not value.strip():
            fail(path, "must be a nonempty string")
            return False
        return True

    def strings(value, path):
        if not isinstance(value, list) or not value:
            fail(path, "must be a nonempty string array")
            return []
        for item in value:
            string(item, path)
        return value

    def integer(value, path, minimum=0):
        if type(value) is not int or value < minimum:
            fail(path, f"must be an integer >= {minimum}")
            return 0
        return value

    def money(value, path):
        try:
            if type(value) not in (str, int):
                raise ValueError()
            result = Decimal(str(value))
            if not result.is_finite() or result < 0 or abs(result.as_tuple().exponent) > 100 or result.adjusted() > 100:
                raise ValueError()
            return result
        except (ValueError, InvalidOperation):
            fail(path, "must be a finite nonnegative credit amount encoded as a decimal string or integer")
            return Decimal(0)

    def fresh(value, path, seconds):
        try:
            if not isinstance(value, str):
                raise ValueError()
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                raise ValueError()
            age = (now - timestamp).total_seconds()
            if age > seconds or age < -30:
                fail(path, "stale or in the future")
        except (ValueError, TypeError):
            fail(path, "must be an ISO 8601 timestamp with timezone")

    def schema_spec(spec, path):
        if not isinstance(spec, dict) or not isinstance(spec.get("type"), str):
            fail(path, "schema must be an object with a string type")
            return
        kind = spec["type"]
        fields = {"string": ["minLength", "maxLength"], "integer": ["minimum", "maximum"],
                  "number": ["minimum", "maximum"], "boolean": [], "null": [],
                  "array": ["minItems", "maxItems", "items"], "object": ["properties", "required"]}
        if kind not in fields:
            fail(path, "unsupported schema type")
            return
        obj(spec, path, ["type"], ["enum"] + fields[kind])
        if "enum" in spec and (not isinstance(spec["enum"], list) or not spec["enum"]):
            fail(path, "enum must be a nonempty array")
        for field in ["minimum", "maximum", "minLength", "maxLength", "minItems", "maxItems"]:
            if field not in spec:
                continue
            value = spec[field]
            if field in ("minimum", "maximum"):
                if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
                    fail(path, "numeric schema bound must be finite")
            else:
                integer(value, path + "." + field)
        for lower, upper in [("minimum", "maximum"), ("minLength", "maxLength"), ("minItems", "maxItems")]:
            if type(spec.get(lower)) in (int, float) and type(spec.get(upper)) in (int, float) and spec[lower] > spec[upper]:
                fail(path, "schema minimum exceeds maximum")
        if kind == "array":
            schema_spec(spec.get("items"), path + "/items")
        if kind == "object":
            props, required = spec.get("properties"), spec.get("required", [])
            if not isinstance(props, dict) or not isinstance(required, list) or any(not isinstance(x, str) for x in required):
                fail(path, "object schema requires properties and a string array of required names")
                return
            if len(required) != len(set(required)) or set(required) - props.keys():
                fail(path, "required names must be unique declared properties")
            for key, child in props.items():
                schema_spec(child, path + "/" + key)

    def schema(value, spec, path):
        spec = obj(spec, path + " schema", ["type"],
                   ["enum", "minimum", "maximum", "minItems", "maxItems", "items", "properties", "required", "minLength", "maxLength"])
        kind = spec.get("type")
        if not isinstance(kind, str):
            fail(path, "schema type must be a string")
            return
        numeric = type(value) in (int, float) and (type(value) is int or math.isfinite(value))
        valid = {"string": isinstance(value, str), "integer": type(value) is int,
                 "number": numeric, "boolean": type(value) is bool,
                 "array": isinstance(value, list), "object": isinstance(value, dict),
                 "null": value is None}.get(kind, False)
        if not valid:
            fail(path, f"must match discovered type {kind}")
            return
        if "enum" in spec:
            choices = spec["enum"]
            if not isinstance(choices, list) or not any(exact(value, x) for x in choices):
                fail(path, "not a discovered option; aliases are not inferred")
        for bound, relation in [("minimum", lambda a, b: a < b), ("maximum", lambda a, b: a > b)]:
            if bound in spec:
                limit = spec[bound]
                if not numeric or type(limit) not in (int, float) or not math.isfinite(limit):
                    fail(path, "invalid numeric bound")
                elif relation(value, limit):
                    fail(path, f"violates {bound}")
        if isinstance(value, (str, list)):
            for name, test in [("minLength" if isinstance(value, str) else "minItems", lambda n, b: n < b),
                               ("maxLength" if isinstance(value, str) else "maxItems", lambda n, b: n > b)]:
                if name in spec and test(len(value), integer(spec[name], path + "." + name)):
                    fail(path, f"violates {name}")
        if kind == "array":
            if "items" not in spec:
                fail(path, "array schema must specify items")
            else:
                for i, item in enumerate(value):
                    schema(item, spec["items"], f"{path}/{i}")
        if kind == "object":
            props = spec.get("properties", {})
            required = spec.get("required", [])
            if not isinstance(props, dict) or not isinstance(required, list) or any(not isinstance(x, str) for x in required):
                fail(path, "invalid object schema")
                return
            for key in set(required) - value.keys():
                fail(path, f"missing required parameter {key}")
            for key, item in value.items():
                if key not in props:
                    fail(path, f"undiscovered parameter {key}")
                else:
                    schema(item, props[key], path + "/" + key)

    m = obj(manifest, "manifest", ["version", "request_id", "request", "capability", "quote", "consent", "media", "coercions", "ledger"])
    if type(m.get("version")) is not int or m.get("version") != 1:
        fail("version", "only version 1 is supported")
    request_id = m.get("request_id")
    string(request_id, "request_id")
    r = obj(m.get("request"), "request", ["task_id", "tool", "model", "payment_mode", "params"])
    for field in ["task_id", "tool", "model", "payment_mode"]:
        string(r.get(field), "request." + field)
    try:
        fp = fingerprint(r)
    except (ValueError, TypeError):
        fail("request", "must contain finite JSON data")
    cap = obj(m.get("capability"), "capability", ["checked_at", "source", "tool", "model", "payment_modes", "params_schema", "model_pointer", "media_slots", "fixed_values", "conflicts", "bindings", "outputs_per_submission"])
    fresh(cap.get("checked_at"), "capability.checked_at", 86400)
    string(cap.get("source"), "capability.source")
    for field in ["tool", "model"]:
        if cap.get(field) != r.get(field):
            fail("capability." + field, "must match the exact request identifier")
    modes = strings(cap.get("payment_modes"), "capability.payment_modes")
    if r.get("payment_mode") not in modes or r.get("payment_mode") not in ["credits", "unlimited", "free"]:
        fail("request.payment_mode", "not a discovered payment mode")
    params = r.get("params")
    if not isinstance(params, dict):
        fail("request.params", "must be an object")
        params = {}
    schema_spec(cap.get("params_schema"), "capability.params_schema")
    schema(params, cap.get("params_schema"), "params")

    def check_pointer(path, label):
        node = cap.get("params_schema")
        if valid_pointer(path):
            for key in path[1:].split("/"):
                key = key.replace("~1", "/").replace("~0", "~")
                if isinstance(node, dict) and node.get("type") == "object" and isinstance(node.get("properties"), dict):
                    node = node["properties"].get(key)
                elif isinstance(node, dict) and node.get("type") == "array" and key.isdigit() and (key == "0" or not key.startswith("0")):
                    node = node.get("items")
                else:
                    node = None
                    break
            if isinstance(node, dict):
                return True
        fail(label, "must be a valid JSON pointer to a discovered parameter")
        return False

    model_pointer = cap.get("model_pointer")
    if model_pointer is not None:
        check_pointer(model_pointer, "capability.model_pointer")
        if not exact(pointer(params, model_pointer), r.get("model")):
            fail("capability.model_pointer", "selected provider parameter must equal the exact model identifier")
    fixed = cap.get("fixed_values")
    if not isinstance(fixed, dict):
        fail("capability.fixed_values", "must be an object of JSON pointers and exact values")
    else:
        for path, expected in fixed.items():
            check_pointer(path, "capability.fixed_values")
            actual = pointer(params, path)
            if not exact(actual, expected):
                fail("params" + path, "must equal discovered fixed value")
    bindings = obj(cap.get("bindings"), "capability.bindings", [], ["duration", "ratio", "count"])
    for name, path in bindings.items():
        check_pointer(path, "capability.bindings." + name)
        if pointer(params, path) is MISSING:
            fail("capability.bindings." + name, "must resolve to an explicit validated parameter")
    if "count" in bindings:
        output_count = integer(pointer(params, bindings["count"]), "output count", 1)
        if cap.get("outputs_per_submission") is not None:
            fail("capability.outputs_per_submission", "must be null when the actual count parameter is bound")
    else:
        output_count = integer(cap.get("outputs_per_submission"), "capability.outputs_per_submission", 1)
    if "duration" in bindings:
        duration = pointer(params, bindings["duration"])
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration <= 0:
            fail("duration", "must be a finite positive number")
    conflicts = cap.get("conflicts")
    if not isinstance(conflicts, list):
        fail("capability.conflicts", "must be an array")
    else:
        for group in conflicts:
            paths = strings(group, "capability.conflicts")
            if len(paths) < 2:
                fail("capability.conflicts", "each mutually exclusive group needs at least two pointers")
            for path in paths:
                check_pointer(path, "capability.conflicts")
            if sum(pointer(params, path) is not MISSING for path in paths) > 1:
                fail("params", "conflicting controls are present: " + str(paths))
    slots = cap.get("media_slots")
    records = m.get("media")
    if not isinstance(slots, dict) or not isinstance(records, list):
        fail("media", "requires an array of confirmations and an object of discovered slots")
    else:
        seen = set()
        for record in records:
            record = obj(record, "media record", ["role", "pointer", "value", "confirmed", "source"])
            role = record.get("role")
            if not isinstance(role, str) or role not in slots:
                fail("media.role", "unsupported media role")
                continue
            if role in seen:
                fail("media.role", "duplicate role confirmation")
            seen.add(role)
            slot = obj(slots[role], "media slot", ["pointer"])
            if not exact(record.get("pointer"), slot.get("pointer")) or not exact(pointer(params, slot.get("pointer")), record.get("value")):
                fail("media", "confirmation must bind the exact submitted parameter value")
            if record.get("confirmed") is not True:
                fail("media", "user-provided or authorized media must be confirmed")
            string(record.get("source"), "media.source")
        for role, slot in slots.items():
            slot = obj(slot, "media slot", ["pointer"])
            check_pointer(slot.get("pointer"), "media slot pointer")
            if pointer(params, slot.get("pointer")) is not MISSING and role not in seen:
                fail("media", f"unconfirmed input for role {role}")
    coercions = m.get("coercions")
    if not isinstance(coercions, list):
        fail("coercions", "must be an array")
    else:
        for coercion in coercions:
            coercion = obj(coercion, "coercion", ["description", "accepted", "source"])
            if coercion.get("accepted") is not True:
                fail("coercion", "unaccepted substitutions or changes are blocked")
            string(coercion.get("description"), "coercion.description")
            string(coercion.get("source"), "coercion.source")
    quote = obj(m.get("quote"), "quote", ["checked_at", "source", "request_fingerprint", "payment_mode", "charge_credits", "includes_all_outputs", "fallback"])
    fresh(quote.get("checked_at"), "quote.checked_at", 300)
    string(quote.get("source"), "quote.source")
    if quote.get("request_fingerprint") != fp or fp is None:
        fail("quote", "fingerprint must match the exact current request")
    if quote.get("payment_mode") != r.get("payment_mode"):
        fail("quote", "payment mode mismatch or fallback")
    if quote.get("includes_all_outputs") is not True or quote.get("fallback") is not False:
        fail("quote", "requires all-output pricing with no automatic payment fallback")
    charge = money(quote.get("charge_credits"), "quote.charge_credits")
    if r.get("payment_mode") in ("unlimited", "free") and charge != 0:
        fail("quote", "unlimited/free execution must have zero credit charge")
    consent = obj(m.get("consent"), "consent", ["intent", "source", "scope", "approved_models", "approved_tools", "permitted_payment_modes", "ceiling_credits", "max_attempts", "max_outputs", "max_outputs_per_submission"])
    if consent.get("intent") != "generate":
        fail("consent.intent", "actual generation authorization is required; planning is not consent")
    string(consent.get("source"), "consent.source")
    scope = obj(consent.get("scope"), "consent.scope", [], ["task_id", "request_fingerprint"])
    if len(scope) != 1 or (scope.get("task_id") != r.get("task_id") and scope.get("request_fingerprint") != fp):
        fail("consent.scope", "must match exactly one task or request scope")
    for field, value in [("approved_models", r.get("model")), ("approved_tools", r.get("tool")), ("permitted_payment_modes", r.get("payment_mode"))]:
        if value not in strings(consent.get(field), "consent." + field):
            fail("consent." + field, "current selection is not authorized")
    ceiling = money(consent.get("ceiling_credits"), "consent.ceiling_credits")
    maximum = integer(consent.get("max_attempts"), "consent.max_attempts", 1)
    output_maximum = integer(consent.get("max_outputs"), "consent.max_outputs", 1)
    per_submission = integer(consent.get("max_outputs_per_submission"), "consent.max_outputs_per_submission", 1)
    if output_count > per_submission:
        fail("outputs", f"{output_count} outputs exceeds per-submission limit {per_submission}")
    ledger = m.get("ledger")
    spent, attempts, prior_outputs, ids, fingerprint_tasks = Decimal(0), 0, 0, set(), {}
    fingerprint_outputs = {}
    if not isinstance(ledger, list):
        fail("ledger", "must be an array, including prior and uncertain attempts")
    else:
        for entry in ledger:
            entry = obj(entry, "ledger entry", ["request_id", "task_id", "request_fingerprint", "status", "amount_credits", "output_count"])
            for field in ["request_id", "task_id", "request_fingerprint"]:
                string(entry.get(field), "ledger." + field)
            rid = entry.get("request_id")
            if isinstance(rid, str):
                if rid in ids or rid == request_id:
                    fail("ledger", "duplicate or previously submitted request_id")
                ids.add(rid)
            status = entry.get("status")
            ledger_fp, ledger_task = entry.get("request_fingerprint"), entry.get("task_id")
            if ledger_fp == fp and ledger_task != r.get("task_id"):
                fail("ledger", "fingerprint conflicts with the current task_id")
            if isinstance(ledger_fp, str):
                if ledger_fp in fingerprint_tasks and fingerprint_tasks[ledger_fp] != ledger_task:
                    fail("ledger", "one fingerprint cannot belong to conflicting task IDs")
                fingerprint_tasks[ledger_fp] = ledger_task
            if status not in ("charged", "reserved", "unknown"):
                fail("ledger.status", "must be charged, reserved or unknown; refunds are never inferred")
            if status in ("reserved", "unknown") and entry.get("request_fingerprint") == fp:
                fail("ledger", "same request is unresolved; reconcile before resubmitting")
            amount = money(entry.get("amount_credits"), "ledger.amount_credits")
            outputs = integer(entry.get("output_count"), "ledger.output_count", 1)
            if ledger_fp == fp and outputs != output_count:
                fail("ledger.output_count", "must match the current request count for the same fingerprint")
            if isinstance(ledger_fp, str):
                if ledger_fp in fingerprint_outputs and fingerprint_outputs[ledger_fp] != outputs:
                    fail("ledger.output_count", "one fingerprint cannot have conflicting requested output counts")
                fingerprint_outputs[ledger_fp] = outputs
            if ("task_id" in scope and entry.get("task_id") == r.get("task_id")) or ("request_fingerprint" in scope and entry.get("request_fingerprint") == fp):
                spent = add_credits(spent, amount)
                attempts += 1
                prior_outputs += outputs
    if add_credits(spent, charge) > ceiling:
        fail("budget", f"{spent} reserved/charged + {charge} exceeds {ceiling} credits")
    if attempts + 1 > maximum:
        fail("attempts", f"{attempts} prior + 1 exceeds authorized {maximum}")
    if prior_outputs + output_count > output_maximum:
        fail("outputs", f"{prior_outputs} prior + {output_count} exceeds authorized {output_maximum}")
    return {"ok": not errors, "errors": errors, "warnings": warnings, "fingerprint": fp}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    args = parser.parse_args()
    try:
        with open(args.manifest, encoding="utf-8") as stream:
            manifest = json.load(stream, object_pairs_hook=unique_keys)
        result = check(manifest)
    except (OSError, ValueError, TypeError, OverflowError, RecursionError) as error:
        result = {"ok": False, "errors": [f"invalid manifest: {error}"], "warnings": [], "fingerprint": None}
    print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
