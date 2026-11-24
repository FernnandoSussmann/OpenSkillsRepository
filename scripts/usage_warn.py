#!/usr/bin/python3 -I
"""UserPromptSubmit hook: warn (user + Claude) when plan usage is past a threshold.

Reads ~/.claude/usage.json (validated by usage_common). Threshold defaults to
80% and can be overridden with USAGE_WARN_PCT. Silent when below threshold,
when the cache is missing or untrusted, or when a window has already reset.
Never blocks the prompt. Hook stdin is not read: nothing in it is needed.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from usage_common import read_cache  # noqa: E402

LABELS = {"five_hour": "5-hour", "seven_day": "7-day"}


def threshold():
    try:
        value = float(os.environ.get("USAGE_WARN_PCT", "80"))
    except ValueError:
        return 80.0
    return value if 1 <= value <= 100 else 80.0


def main():
    limits, _ = read_cache()
    if not limits:
        return
    now, limit = time.time(), threshold()
    hot = []
    for key, label in LABELS.items():
        win = limits.get(key)
        if not win or win["resets_at"] <= now or win["used_percentage"] < limit:
            continue
        reset_str = time.strftime("%a %H:%M", time.localtime(win["resets_at"]))
        hot.append(f"{label} limit at {win['used_percentage']:.0f}% (resets {reset_str})")
    if not hot:
        return
    msg = "Usage warning: " + "; ".join(hot) + "."
    print(json.dumps({
        "systemMessage": msg,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg
            + " Before doing anything else, invoke the usage-guard skill: it pauses"
            " at a safe point and sleeps until the limit resets.",
        },
    }))


if __name__ == "__main__":
    main()
