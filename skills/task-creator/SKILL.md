---
name: task-creator
description: Creates task to implement a functionality based on a Design doc
---

As described in $ARGUMENTS design doc file create tasks to implement described functionality. Save those steps in a folder called `steps/{DESIGN_DOC_NAME}/$ARGUMENTS` inside `design_doc` folder.

# When creating a step file
- Be specific.
- Describe what must be done.
- You can add example code to it if necessary.
- You must guarantee that guardrails will be present in all steps generated.
- Make sure tests will be created for that functionality.
- Make sure that quality gates will pass.
- Explicitly say to never write credentials in the code. All credentials must be added at runtime.
- Search for possible security vulnerabilities in this task, how to fix them or make sure they will not exist. Also tell how to check them.
- Never ask to create empty files or folder structure, leave it to be created only when needed.
- Create a guidance check-list/definition of done for each task.

# How it will run
In any step of this process if you are in doubt ask, do not assume anything.

1. Create an agent that will create those steps. Add a TL;DR session in the beginning of the document summarizing what it says.
2. Create a second agent that will validate if they match what is specified in the design doc.
3. If something is off correct it.


# Final considerations
Create from 1 to 5 steps max per design doc, try to balance the workload between them. Less than 5 is better. Make sure to explicitly say which task can be done in parallel and which must be sequential. Parallel tasks must be grouped in the same MD file so when an agent implement it it can create worktrees and span sub-agents to work on them at the same time. Do not read other steps, only design doc file.
Make sure that every task will leave this application in a usable state. If it is the last task from a Design Doc guarantee that it delivers a complete feature that works and not unconnected pices especially if this app has a frontend and backend. Make sure also that any web page or screen is reachable.
Add a last task that must check if all the design doc criteria were met, if not it should implement it. After every thing is OK task description files (with MD extension) related to that design doc must be deleted. Make sure it will look to the last worked branch related to this DD as main branch may not be updated.
Estimate size and how many lines of code this task would change. Add it after document title
