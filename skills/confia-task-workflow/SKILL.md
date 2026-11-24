---
name: confia-task-workflow
description: Creates tasks and implement their functionality based on a Design doc checking resource usage and account credits
---

As described in $ARGUMENTS design doc file run skill with arguments /task-creator $ARGUMENTS. Spawn a subagent :model opus5.5 :effort high for this task.

After that check account credits with /usage-guard skill.

Finally for every task in the folder created by task-creator skill run /implement-all-steps skill using a :model sonnet5.5 :effort medium. Make sure that /usage-guard skill will be trigger after each step implemented or subagent execution and this instruction will be pass on to EVERY subagent created even subagent's subagents.
