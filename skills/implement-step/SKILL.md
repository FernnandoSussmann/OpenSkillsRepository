---
name: implement-step
description: Implement step
---

Implement $ARGUMENTS.

If it does not exists create a branch with the name of the design doc that generated this task. Then create a new git branch. Init one agent for implementation, after another one to run pre-hook activities and finally a third that will compare modified files with what was specified in that step file. If the task file has tasks that can be done in parallel run the same way but using a worktree for each to be able to do them simultaneously.

SPANNING THOSE AGENTS ARE MANDATORY.

After all agents run make sure again all pre-commit requisites are archived and if an error occurs fix it. When all is done open a PR to de design doc branch.

# Final considerations
- Never ask to create empty files or folder structure, leave it to be created only when needed.
- In any step of this process if you are in doubt ask, do not assume anything.
- If a PR template exists follow it.
- Avoid creating a lots of commentaries. Make sure we can understand the project by reading it's code. Comments must be the last resort for unexpected behaviours, external infrastructure response or side effects.
- Prefer not to create a file that is over 500 lines. If is inevitable and you can justify it that's ok. Just remember to make files readable, manageable and clear what intent that holds.
- Make sure to delete all worktrees when you are done.
