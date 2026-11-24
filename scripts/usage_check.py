#!/usr/bin/python3 -I
"""Report plan usage from ~/.claude/usage.json as JSON, for the usage-guard skill.

Output fields:
  status         "ok" | "warn" | "unknown"
  threshold      percent that triggers "warn" (USAGE_WARN_PCT, default 80)
  windows        per active window: used_percentage, resets_at (epoch), resets_local
  hot            windows at/above threshold
  sleep_seconds  when "warn": integer seconds until the latest hot window resets,
                 plus a buffer; always 1..MAX_SLEEP_S
  wake_local     when "warn": local time the sleep ends
  data_age_s     seconds since the status line last wrote the cache (null if unknown)

The cache is validated by usage_common; an untrusted cache reads as "unknown".
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from usage_common import MAX_AHEAD_S, read_cache  # noqa: E402

BUFFER_S = 60
MAX_SLEEP_S = MAX_AHEAD_S + BUFFER_S


def local(epoch):
    return time.strftime("%a %b %d %H:%M", time.localtime(epoch))


def threshold():
    try:
        value = float(os.environ.get("USAGE_WARN_PCT", "80"))
    except ValueError:
        return 80.0
    return value if 1 <= value <= 100 else 80.0


def main():
    now = int(time.time())
    limits, updated = read_cache(now)
    if limits is None:
        print(json.dumps({"status": "unknown", "reason": "usage cache missing or failed validation"}))
        return

    limit = threshold()
    windows, hot = {}, []
    for key, win in limits.items():
        if win["resets_at"] <= now:
            continue  # already reset
        windows[key] = {**win, "resets_local": local(win["resets_at"])}
        if win["used_percentage"] >= limit:
            hot.append(key)

    out = {
        "status": "warn" if hot else ("ok" if windows else "unknown"),
        "threshold": limit,
        "windows": windows,
        "hot": hot,
        "data_age_s": (now - updated) if updated else None,
    }
    if hot:
        wake = max(windows[k]["resets_at"] for k in hot) + BUFFER_S
        out["sleep_seconds"] = int(min(max(wake - now, 1), MAX_SLEEP_S))
        out["wake_local"] = local(now + out["sleep_seconds"])
    print(json.dumps(out))


if __name__ == "__main__":
    main()
