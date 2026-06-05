#!/usr/bin/env python3
"""Infer and print the shape of a JSON or JSONL document."""

import argparse
import json
import sys


def type_name(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    return "object"


def merge(a, b):
    """Combine two inferred schemas into one."""
    if a is None:
        return b
    if b is None:
        return a
    if a == b:
        return a
    if isinstance(a, dict) and isinstance(b, dict):
        out = {}
        for key in set(a) | set(b):
            if key in a and key in b:
                out[key] = merge(a[key], b[key])
            else:
                out[key] = (a.get(key) or b.get(key), "optional")
        return out
    return "|".join(sorted({str(a), str(b)}))


def schema(value, max_items=50):
    if isinstance(value, dict):
        return {k: schema(v, max_items) for k, v in value.items()}
    if isinstance(value, list):
        inner = None
        for item in value[:max_items]:
            inner = merge(inner, schema(item, max_items))
        return ["empty" if inner is None else inner]
    return type_name(value)


def render(node, indent=0, key=None):
    pad = "  " * indent
    label = ("%s: " % key) if key is not None else ""
    if isinstance(node, dict):
        lines = ["%s%s{" % (pad, label)]
        for k in sorted(node):
            lines.extend(render(node[k], indent + 1, k))
        lines.append("%s}" % pad)
        return lines
    if isinstance(node, list):
        lines = ["%s%s[" % (pad, label)]
        lines.extend(render(node[0], indent + 1))
        lines.append("%s]" % pad)
        return lines
    if isinstance(node, tuple):
        return ["%s%s%s  (optional)" % (pad, label, node[0])]
    return ["%s%s%s" % (pad, label, node)]


def load(path, jsonl=False):
    handle = sys.stdin if path == "-" else open(path, encoding="utf-8")
    try:
        if jsonl:
            return [json.loads(line) for line in handle if line.strip()]
        return json.load(handle)
    finally:
        if handle is not sys.stdin:
            handle.close()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("json_file", help="path to the file, or - for stdin")
    ap.add_argument("--lines", action="store_true", help="input is JSONL")
    ap.add_argument("--sample", type=int, default=50,
                    help="how many array items to sample (default 50)")
    args = ap.parse_args(argv)

    data = load(args.json_file, args.lines)
    print("\n".join(render(schema(data, args.sample))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
