---
title: "How I Use an Agent Team to Build a Close-Loop Development Process"
language: en
status: unpublished
tags: [ai-workflow, agent-team, close-loop, validation, observability, retrospective]
---

# How I Use an Agent Team to Build a Close-Loop Development Process

Picking up from my last post, where I said complex tasks suit an Agent Team workflow.

Here is how I combine an Agent Team with a close loop in practice, so AI-assisted development does more than finish a single task. It keeps building up project assets.

When people hear "Agent Team," the first thing that comes to mind is:

"Run a few AIs in parallel."

In my experience, that is not where the value is.

The value is turning development into a close loop you can plan, execute, verify, fix, and learn from.

My basic flow looks like this:

```text
Planner
  ↓
Executor
  ↓
Validator
  ├─ FAIL → back to Executor to fix → Validator re-verifies
  └─ PASS → open PR
        ↓
     Code Reviewer
        ├─ FAIL → Executor fixes → Validator re-verifies → update PR → review again
        └─ PASS → Merge
              ↓
         Retrospective
              ↓
Lessons Learned / Memory / Workflow updates
```

**1. Planner: think the problem through first**

The Planner's job is not to rush into code.

It is to explore, compare, and analyze possible solutions first.

For complex or high-risk tasks, I plan with three models.

Claude, Codex, and Gemini each propose an approach from a different angle, and then I merge them into one final plan.

Once the approach is settled, I do not hand it straight to the Executor.

I first get the Planner, Executor, and Validator aligned on the plan.

The Executor spots technical gaps from the implementation side.

The Validator spots test gaps from the verification side.

That feedback makes the plan more complete and cuts the cost of fixing things later.

After the spec is aligned, I create the Jira issue and the sub-task for each platform.

**2. Executor: build with each platform's context**

Depending on the scope, the Executor sends out agents for different platforms, for example:

Backend, iOS, Android, and Frontend.

The Executor's job is not to copy the plan.

It explores the existing codebase first, then implements according to each platform's best practices.

The same feature can follow different architecture conventions, state management, and error handling on different platforms.

So the point of an Agent Team is not to let each agent do its own thing.

It is to have them work from one shared plan and one shared spec, while still building something that fits each platform.

**3. Validator: make sure the output really meets the requirement**

With AI workflows, the problem is usually not that code can't be produced.

It is whether what was produced really meets the original requirement.

So the Validator's most important job is to check whether the implementation reached the original goal.

The key issue here is observability.

That is, how does the Validator get enough data to judge whether the output is actually correct?

Each platform verifies differently.

Backend:

build, log checks, and functional tests.

App and Frontend:

screenshots, logs, and walking through the interaction flow. That covers the screen, the state, error handling, and whether the real usage flow behaves as expected.

For cross-platform features, I also check that Android, iOS, and Web behave consistently.

If the Validator reports FAIL, it goes back to the Executor to fix, and the Validator verifies again.

This is also why the Planner, Executor, and Validator need to align during planning.

The Executor understands the implementation boundaries early.

The Validator confirms the verification method early.

By the time development starts, the close loop is much easier to converge.

I only go back to the user when there is a design disagreement, a scope change, or a screen or log result that needs a human eye.

**4. PR and code review: let review focus on quality**

Only after the Validator reports PASS do we move to the PR and code review.

In other words, first confirm the feature runs and the behavior meets the requirement. Then check code quality, architectural consistency, side effects, and maintainability.

If the code review fails:

back to the Executor to fix → the Validator re-verifies → update the PR → review again.

If it passes:

do the branch operations that follow the team's Git Flow, for example feature / dev / staging / main.

**5. Retrospective: leave the lessons for the next round**

This is the part I think matters most.

After each task, I look back at a few things.

Efficiency:

How many rounds of FAIL did we go through? What caused each one?

Quality:

Was the Planner's spec accurate enough? How good was the Executor's implementation? Did the Validator miss anything?

Process:

Which steps can be merged or dropped? Is any step missing?

Tools:

Is there a better way to use MCP tools, test tools, or verification methods?

These reviews are not just chat logs.

They get written back into the workflow docs, lessons learned, and memory. When needed, I also adjust the agent prompts.

The goal is for each module's close loop to run more smoothly than the last, with fewer FAIL rounds.

This also echoes what I said in my first post:

The value of an AI workflow is not only what got done today. It is whether the work leaves context that the next piece of work can use.

So to me, an Agent Team is not "opening a few more AIs."

It is closer to an engineering management structure.

Complex tasks can be planned, built, verified, fixed, and reviewed, and then what we learned feeds into the next round.

Without a close loop, multiple agents just multiply the uncertainty in parallel.

But with a clearly designed close loop, an Agent Team can turn AI-assisted development from one-off output into an engineering process that keeps improving.

## Adapted From

- [Traditional Chinese original](zh-TW.md)
