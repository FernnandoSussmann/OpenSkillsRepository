---
name: implement-all-steps
description: Implement all steps in a folder
---

Implement all steps (MD files) in $ARGUMENTS folder. Start from the file that has the smaller number to the one with the highest. For example if you have 02-01.md, 02-02.md, 03-01.md, 03-02.md, 03-03.md you execute it in this order 02-01.md -> 02-02.md -> 03-01.md -> 03-02.md -> 03-03.md. When finishing a task  if it does not exists create a branch with the name of the design doc that generated this task. When any task is done create a PR targeting this design doc branch. A new task will always start from the design doc branch if it is the first task or the last task you have done. It will run until all tasks are done.

For each task you must create a sub agent that will:
1. Create a new git branch.
2. Init one agent for implementation, after another one to run pre-hook activities and finally a third that will compare modified files with what was specified in that step file.
3. If the task file has tasks that can be done in parallel run the same way but using a worktree for each to be able to do them simultaneously.

SPANNING THOSE AGENTS ARE MANDATORY.

After all agents run make sure again all pre-commit requisites are archived and if an error occurs fix it. When all is done open a PR to the previous branch.

# Final considerations
- Never ask to create empty files or folder structure, leave it to be created only when needed.
- In any step of this process if you are in doubt ask, do not assume anything.
- If a PR template exists follow it.
- Avoid creating a lots of commentaries. Make sure we can understand the project by reading it's code. Comments must be the last resort for unexpected behaviours, external infrastructure response or side effects.
- If token limit usage is getting close to it's limit don't start the next task until it resets.
- Prefer not to create a file that is over 500 lines. If is inevitable and you can justify it that's ok. Just remember to make files readable, manageable and clear what intent that holds.
- Make sure to delete all worktrees when you are done.
- In between agents creation ALWAYS RUN /usage-guard skill to check if you can keep working.
