---
title: "Match the Workflow to the Task: Not Every AI Job Needs an Agent Team"
language: en
status: unpublished
tags: [ai-workflow, workflow-selection, vertical-slice, agent-team, claude-code]
---

# Match the Workflow to the Task: Not Every AI Job Needs an Agent Team

A workflow does not get better just because it has more steps.

It needs to match the shape of the task.

In my experience with Claude Code, Vertical Slice development is a good fit for a fuller workflow like Agent Team.

A Vertical Slice follows one user-facing feature across the system. Login, for example, can involve:

Backend API  
iOS and Android screens  
Web/Admin login flows  
State and error handling  
Tests and consistent behavior across platforms

If each platform works independently, the same contract can be understood differently. Error handling, UI behavior, and tests can drift apart.

The value of Agent Team is not simply having more AI agents working in parallel.

It is having different roles work within the same feature scope.

Planner clarifies the goal, scope, test cases, risks, and architectural boundaries.

Then API-first aligns the contract: requests, responses, states, error handling, and test cases. Each platform implements against the same contract and expected behavior.

But that does not mean every platform needs to start at once.

My usual approach is to align the API contract, then get one platform working first.

That first implementation often reveals missing details, unclear states, or incomplete error handling. Getting it working before expanding helps avoid copying the same uncertainty into iOS, Android, and Web/Admin.

Other teams may start all platforms in parallel to move faster.

My trade-off is correctness over speed.

For me, the bigger risk is spreading gaps in the specification or behavior across multiple platforms. I want to check the contract and expected behavior on one platform before moving to the next.

Reviewer checks the implementation against the original goal and architectural boundaries.

Validator checks whether behavior, UI, error handling, and test results are consistent across platforms.

Then the lessons worth keeping go back into the knowledge base.

This is a heavier workflow. For a Vertical Slice, that coordination has value because consistency spans platforms, roles, and verification points.

A small bug fix with a clear root cause is different. So is a simple UI spacing or config change.

The work may only need a quick check, a fix, and verification. Forcing the full process onto it can make coordination cost more than implementation.

So I now ask less:

“Can AI do this?”

And more:

“What kind of workflow does this task need?”

AI-assisted workflow maturity is about matching the process, roles, context, and verification to the complexity of the task.

In short:  
Good AI workflow is not one-size-fits-all.  
It is about matching the workflow to the shape of the work.

P.S. Pair-written with Codex. Continuing to use an AI workflow to write about AI workflows.

## Infographic

![Infographic: Match the Workflow to the Task: Not Every AI Job Needs an Agent Team](images/2026-05-03-en-workflow-task-fit.webp)

## Adapted From

- [Traditional Chinese original](zh-TW.md)
