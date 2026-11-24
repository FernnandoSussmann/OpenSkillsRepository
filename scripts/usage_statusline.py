#!/usr/bin/python3 -I
"""Claude Code status line: show 5h/7d plan usage and cache it to ~/.claude/usage.json.

Claude Code pipes session JSON on stdin. `rate_limits` is only present for
subscribers, after the first API response, while a window is active. All input
is validated by usage_common before it is displayed or written.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from usage_common import clean_limits, read_stdin_json, safe_text, write_cache  # noqa: E402


def fmt_reset(epoch):
    secs = int(epoch - time.time())
    if secs <= 0:
        return "now"
    days, rem = divmod(secs, 86400)
    hours, rem = divmod(rem, 3600)
    mins = rem // 60
    if days:
        return f"{days}d{hours}h"
    if hours:
        return f"{hours}h{mins:02d}m"
    return f"{mins}m"


def main():
    data = read_stdin_json(sys.stdin.buffer)
    limits = clean_limits(data.get("rate_limits"))
    if limits:
        try:
            write_cache(limits)
        except OSError:
            pass  # never break the status line over the cache

    parts = []
    model = data.get("model")
    name = safe_text(model.get("display_name")) if isinstance(model, dict) else ""
    if name:
        parts.append(name)
    for key, label in (("five_hour", "5h"), ("seven_day", "7d")):
        win = limits.get(key)
        if win:
            parts.append(f"{label}: {win['used_percentage']:.0f}% (resets {fmt_reset(win['resets_at'])})")
    if not limits:
        parts.append("usage: n/a yet")
    print(" · ".join(parts))


if __name__ == "__main__":
    main()
