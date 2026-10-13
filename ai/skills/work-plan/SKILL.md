---
name: work-plan
description: Plan a piece of work together with the user, then write the agreed plan into the work records and the handoff so the main agent can carry it out autonomously in a new conversation. Use when the user says "let's plan", "go autonomous", "what's next", or "make a work plan", or wants to open a new Story or a new research direction. Not for a single small edit, an ordinary progress report, or a one-off question.
---

# Work plan

Ask the user to spend time on alignment only once. After that, the main agent can run the work from the handoff in a new conversation, stay on target, and avoid growing a second way of doing the same thing.

The project's own rules (which system holds the work records, the ticket hierarchy, where the architecture map lives, how work is delegated and which models do what, cleanup rules) follow that project's `AGENTS.md` and the work documents it links to. This skill does not set them. If none are found, use the general approach below and say in the plan which default you used.

## 1. Read the current state

1. Read the project's `AGENTS.md`, the handoff file, and the work documents.
2. Search the work records (for example Jira) for older tickets on the same topic by keyword, closed ones included. If one overlaps, reuse or rewrite it instead of opening a new one.
3. Read the architecture map (architecture diagram, flow chart, interface table). If the project has no map yet, or the flow this work touches is not on it, first take stock of that flow: from input to the result the user sees, who does each step, what it writes, and what happens if it is missing. Record facts only. Read-only workers can do this in parallel.

## 2. Reproduce against the current state

The plan cannot rest only on a ticket's description or an old assessment. Reproduce the problem once with the code and output on the current main line: is it still there, how big is it, and which parts did another ticket already fix in passing. For work that changes rules, use the existing output to estimate roughly how many places will be affected, and put the number in the plan.

## 3. External research (research topics only)

When the research direction is not settled, send a different model to do web research as a reference. Frame the questions in product terms, and attach a source, date, and type to every conclusion. The main agent spot-checks the sources before using anything.

## 4. Draft the plan and align with the user

Write it as a product manager would, in plain language: first what the user runs into and what changes for them, then the technology. Say whether each number was measured or calculated. When the user must decide something, ask one thing at a time, each with a recommendation and its reason.

Align on seven points:

1. **Business value**: what is different for users or the business once this is done.
2. **Use scenarios**: what the user can do afterward, written as real examples of "current result vs expected result". Also write what will not be possible.
3. **Direction**: which path this work takes, which it does not, and why.
4. **Goal**: the completion condition, in a form that can be accepted.
5. **Way of working**: how tickets are split and ordered; who does each one (which model, a single layer or a team); acceptance written first (tests or frozen criteria) before the work starts; a small trial run before scaling up.
6. **Stop conditions**: when to stop and report back. Also write counter-examples: situations where it is fine not to stop.
7. **Architecture position**: which flows, layers, and interfaces this work touches; which existing modules and settings it reuses and what it adds. Check against the map for two things: will this create a second way of doing the same thing, and does the placement of the new piece match the current architecture. For each architecture decision, compare "the smallest change" with "the change consistent with the architecture", and say which one you chose.

When you need a second opinion on architecture or direction, you can ask an advisor model. The decision still belongs to the main agent, and the result goes back to the code and the data for checking.

## 5. After the user confirms, put it on record

Do not start work before the user confirms. After they do:

1. Open tickets according to the project's ticket hierarchy. The scenario (Story) carries Given / When / Then and how it will be accepted. Each piece of work gets one ticket, attached to its parent, tagged with its component, and linked with "blocks" to the scenario it unblocks. If you cannot say which scenario a piece of work unblocks, do not open a ticket for it; write it as a comment on an existing ticket.
2. If the work touches the architecture, write a decision record (why, the decision, the comparison for architecture consistency) and update the map.
3. In the handoff file, write the current task, the next step, and what the user still has to decide. Link to the tickets and the decision record without copying their content.
4. Write the criteria, thresholds, and stop conditions the plan settled into the work records before any data is seen, so the record shows they were frozen in advance.

## 6. Autonomous execution

Run from the handoff and the tickets. The main agent delegates, accepts, merges, and keeps the records:

- A delegation brief states the purpose, the principles, the boundaries, and the success criteria, plus the architecture position the main agent wrote. A worker stops and asks when it needs a new module, an interface change, or a new data format. It does not decide those itself.
- Accept on the result itself (data files, diff, tests), and recompute key numbers with a program. Compare the diff against the map: if a module or interface appears that is not on the map, send it back, or update the map on purpose.
- Before using numbers to make a product decision, the prompts and flow must use the product's shared modules. A research script does not bring its own copy.
- When each ticket is done, update the source of truth, the work records, and the handoff, and clear the artifacts this work produced that will not be needed again.
- Choices inside an agreed interface are the main agent's to make. If the work would change the map (a new module, a new interface, a new flow, a change to an existing data format), or hits a product trade-off outside the plan, stop that piece, note it under "needs the user's decision" in the handoff, and keep doing the work it does not affect.
- After each ticket, check context and quota. Above about 70% of context, write the handoff first and tell the user. When quota is nearly used up, stop starting new work and do only cleanup and handoff.

## Reporting

During alignment: one message that covers the seven points, the order of tickets, and the division of labor, with the one thing the user must decide on the last line. After putting it on record: list which tickets were opened, what changed in the decision record and the map, and the entry point of the handoff. During autonomous execution: for each important step, give the result first, then the evidence and the next step. List the things that need a decision separately.
