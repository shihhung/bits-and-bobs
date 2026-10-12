---
name: handoff
description: Review work in progress, discuss what to continue, and, when the user asks for a handoff, update the HANDOFF file and existing work records. Use when switching conversations, passing work to someone else, or closing a phase. Not for ordinary progress reports or one-off summaries.
---

# Handoff

Let the next conversation pick up the work directly, without rewriting history that already lives in Jira or another official record.

## First, decide which part to do

- **Review / discuss first**: Check the current state against evidence. Say what is done, what is unconfirmed, the trade-offs of the approach, and the feasible next steps. If the user only asked to discuss, do not edit files or publish records because of this skill.
- **Write the handoff**: When the user asks to make it official, update the necessary records and the handoff entry point based on what was discussed. If they also ask for a commit, push, or other actions, do them under that request's authorization. Do not treat them as fixed steps of every handoff.

## Check and organize

1. Read the `AGENTS.md` that applies, the existing handoff file, the work records, and the actual artifacts and version state. Verify conclusions against primary sources and the output that is currently in effect. Keep facts, inferences, and unknowns separate. Preserve the user's existing changes.
2. Before editing the handoff file, take stock of what can be cleaned up, then clean first and add after, so the file does not keep growing:
   - process and entry points of closed work
   - text that duplicates an official record or the source of truth
   - doubts that were fixed or are now outdated
   - next steps already merged into other items
   - stable practices written as detail (move them to the source of truth or `AGENTS.md`)

   Confirm the status and destination of each item. Delete only what exists elsewhere or is no longer valid. If a fact is recorded nowhere else, add it to the official record first, or rewrite it as one line and keep it. In the report, list what was removed and where it went.
3. Find the project's official history record (for example Jira). Before tidying the handoff file, write the results of this work into it. Use the project's own tool or skill. Do not assume every project uses Jira.
   - Go through every ticket this work touched. Status matches real progress (started work moves to in progress; delivered work with evidence collected is closed). Conclusions, evidence links, and open decisions are all in comments. If there is a parent ticket or Story, it gets one summary comment linking to the child tickets' comments.
   - After writing, read it back and check: rendering is correct (for example, asterisks turned into italics, tables broken), and links and comment numbers are right.
   - Remove duplicated text from the handoff file only after confirming the content is already in the official record.
4. If the project requires an illustrated work report (for example, the work-status principle in `AGENTS.md`, or when there is a lot of information or the work ran long), confirm that this work's key progress, decision turns, and open decisions are updated at the report's entry point. If there is no report yet, create or update the same report with the `work-report` skill. The handoff file and official record only link to it and do not repeat its content.
5. Keep only what the next person really needs in the handoff file: current goal and state, the next actionable step, open questions or constraints, the latest valid artifacts, primary evidence, and entry points to the official records. Historical detail stays in its original record. Stable cross-task principles stay in `AGENTS.md`, not in the handoff file.
6. Check links, paths, branch / run identity, and whether locally stored or Git-ignored artifacts can still be obtained. Claim only the checks you actually did. Do not write "tests pass", "text coverage", or "model suggestion" as content acceptance.
7. If the project has a cleanup policy or a listing tool for work artifacts, run a list-only pass that deletes nothing: which data left by closed work can be cleaned, which should be moved to a storage location first, and roughly how large each is. Follow the project documents for the rules; do not set new ones in this skill. Do not delete or move anything during handoff. List it for the user to decide when to handle it. Skip this step for projects with no policy or tool.

In the report, briefly state the conclusion, which tickets were updated (status and comment numbers), the work report's entry point, which entry points were edited, work artifacts waiting for cleanup (when step 7 ran), and any limits the next person must know. Do not paste the whole history again.
