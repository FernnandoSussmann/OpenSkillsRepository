---
name: usage-guard
description: Check Claude plan usage (5-hour and 7-day limits) and, if a limit is at or over the warning threshold, pause at a safe point and sleep until that limit resets, then resume. Use when a "Usage warning" appears, before starting long multi-step work, or when the user asks to check or wait out usage.
---

# Usage guard

Plan usage is cached in `~/.claude/usage.json` by the status line script
(`~/.claude/scripts/usage_statusline.py`). Do not call any API to get usage.

## 1. Check

Run:

```sh
/usr/bin/python3 -I ~/.claude/scripts/usage_check.py
```

It prints one JSON object. Act on `status`:

- `ok`: say in one line what the usage is (e.g. "5h 12%, 7d 51%") and continue the task.
- `unknown`: no usage data yet (no API response this session, or not a subscription). Say so in one line and continue.
- `warn`: go to step 2.

## 2. Pause (status `warn`)

**Skip the pause** if the user's latest message explicitly says to keep going despite usage
(e.g. "ignore the limit", "continue anyway"). Then just continue.

Otherwise:

1. Stop at a safe point. Finish the current small edit so no file is left half-changed.
   Do not start new steps, spawn agents or commit.
2. Tell the user, in a short message: which limit is hot and its percentage, the wake
   time (`wake_local`), what you finished, and the next step you'll take when you resume.
   If `sleep_seconds` is over 24 hours (a 7-day window), say so plainly. The user can
   interrupt at any time.
3. Start the sleep with the Bash tool, **with `run_in_background: true`** (a foreground
   `sleep` is blocked and would time out):

   ```sh
   sleep <sleep_seconds>
   ```

   Description: "Wait until the usage limit resets". Use the exact integer from the JSON.
   Only run it if `sleep_seconds` is a plain positive integer (digits only, at most
   700000). If it is anything else, do not sleep: tell the user the usage data looks
   invalid and continue without pausing.
4. End your turn. Do nothing else while waiting. You will be re-invoked when the
   background command exits.

## 3. Resume

When the background sleep finishes:

1. Run the check again.
2. If it is still `warn` (another window is hot, or the data is from before the reset
   and still shows it as active), repeat step 2 with the new `sleep_seconds`.
3. Otherwise tell the user in one line that the limit has reset, and continue the task
   from the next step you named before sleeping.

## Notes

- The sleep only lasts while this Claude Code session stays open. If the session is
  closed, nothing resumes on its own.
- The threshold is 80% unless `USAGE_WARN_PCT` is set (in `env` of `~/.claude/settings.json`).
- `data_age_s` shows how old the cached numbers are; they refresh after each model response.
