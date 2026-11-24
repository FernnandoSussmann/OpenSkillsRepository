"""Shared, defensive handling of plan-usage data for the usage scripts.

Threat model: the status line script reads JSON from stdin and the other
scripts read ~/.claude/usage.json. Treat both as untrusted: bound their size,
accept only the exact fields and value ranges we use, never follow symlinks,
and only trust a cache file that is a regular file owned by the current user
and not writable by others. Anything that fails a check is dropped, never
"repaired".
"""
import json
import math
import os
import stat
import tempfile
import time

CACHE = os.path.expanduser("~/.claude/usage.json")
MAX_STDIN_BYTES = 1 << 20  # 1 MiB: status line input is a few KiB
MAX_CACHE_BYTES = 16 << 10  # 16 KiB: the cache is ~200 bytes
WINDOWS = ("five_hour", "seven_day")
MAX_PCT = 200.0  # percentages above 100 are possible once exceeded; beyond this is bogus
MAX_AHEAD_S = 8 * 86400  # no window resets more than ~7 days out
MAX_BEHIND_S = 86400  # tolerate a recently passed reset; the readers skip it anyway


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def clean_limits(raw, now=None):
    """Return only valid {window: {used_percentage, resets_at}} entries from raw."""
    now = int(time.time()) if now is None else now
    if not isinstance(raw, dict):
        return {}
    out = {}
    for key in WINDOWS:
        win = raw.get(key)
        if not isinstance(win, dict):
            continue
        pct, resets = win.get("used_percentage"), win.get("resets_at")
        if not _is_number(pct) or not 0 <= pct <= MAX_PCT:
            continue
        if not _is_number(resets) or resets != int(resets):
            continue
        resets = int(resets)
        if not now - MAX_BEHIND_S <= resets <= now + MAX_AHEAD_S:
            continue
        out[key] = {"used_percentage": float(pct), "resets_at": resets}
    return out


def read_stdin_json(stream):
    """Parse at most MAX_STDIN_BYTES of JSON from a binary stream; {} on any problem."""
    data = stream.read(MAX_STDIN_BYTES + 1)
    if len(data) > MAX_STDIN_BYTES:
        return {}
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        return {}
    return obj if isinstance(obj, dict) else {}


def write_cache(limits, now=None):
    """Atomically write validated limits to CACHE with 0600 permissions."""
    now = int(time.time()) if now is None else now
    directory = os.path.dirname(CACHE)
    st = os.lstat(directory)
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid():
        return
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".usage.")  # created 0600
    try:
        with os.fdopen(fd, "w") as f:
            json.dump({"rate_limits": limits, "updated_at": now}, f)
        os.replace(tmp, CACHE)  # replaces a symlink itself, never its target
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def read_cache(now=None):
    """Return (limits, updated_at) from a trusted CACHE, or (None, None)."""
    now = int(time.time()) if now is None else now
    try:
        fd = os.open(CACHE, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        return None, None
    try:
        st = os.fstat(fd)
        if (
            not stat.S_ISREG(st.st_mode)
            or st.st_uid != os.getuid()
            or st.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
            or st.st_size > MAX_CACHE_BYTES
        ):
            return None, None
        data = os.read(fd, MAX_CACHE_BYTES + 1)
    finally:
        os.close(fd)
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None, None
    if not isinstance(obj, dict):
        return None, None
    updated = obj.get("updated_at")
    if not _is_number(updated) or not now - MAX_AHEAD_S <= updated <= now + 60:
        updated = None
    return clean_limits(obj.get("rate_limits"), now), (int(updated) if updated else None)


def safe_text(value, limit=40):
    """Printable, single-line, length-bounded text (blocks terminal escape injection)."""
    if not isinstance(value, str):
        return ""
    return "".join(c for c in value if c.isprintable())[:limit]
