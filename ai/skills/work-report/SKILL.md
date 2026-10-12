---
name: work-report
description: Build and maintain a layered, illustrated work report. Use when the work has a lot of information, runs for a long time, or is hard to grasp from text alone; also use when the user asks to update the work web page. Not for ordinary product websites or simple text replies.
---

# Illustrated work report

Let the reader grasp status and results from a big picture and a conclusion first, then dig into process and evidence as needed. Build on the project's official records. For long-running work, record key progress, decision turns, and their basis at one entry point, so the reader can follow the context when they come back. The report does not invent research conclusions or replace the work-management system.

## Division of labor and content

- Delegate building and maintaining the report as the task needs. Use a mid-tier model that is good at layout and writing. Reuse the existing web-page agent; the main agent may also build it. The user's choice comes first. A web-page agent does not spawn further agents.
- The main agent provides a task summary, confirmed results, unknowns and limits, and entry points to the necessary evidence. It provides next steps only when follow-up is necessary. If delegating, the agent finishes the presentation itself. The main agent checks the conclusions and the key screens, and does not redo every production check.
- Next steps state the priority and the reason. List trade-offs only when a decision is needed. Authorized work continues on its own. Do not invent follow-up when none is needed.
- Separate current results, past results, illustrations, and plans not yet run. A pipeline that runs end to end does not mean the content or the goal is accepted. Choose images within the project's data boundary. Do not move sensitive answers or credentials onto the display page.

## Presentation

- Use a picture instead of words when you can. The reader should see the result at a glance without reading between the lines. Pair a big picture with a little text. Choose visuals that explain the work: source-versus-result comparisons, difference markers, flow or structure diagrams. If no suitable photo exists, draw a diagram. Do not use a decorative image in place of evidence.
- When the reader has to check something, lay it out the way the reader checks it (for example, three columns: template, source, output). Mark differences, frame the key parts, and gray out the irrelevant parts right on the screen. Put comparison information on the screen, not inside an explanation that needs a click.
- The first layer uses a big picture and little text to answer: where are we, what did we get, where are we stuck. Important milestones and decision turns go in the next layer. Reasons and evidence expand on demand. Deeper layers link back to the formal report and evidence.
- Use a monospace font for the whole page (a deliberate choice for reading comfort). For CJK text, use a monospace stack the system has (for example `ui-monospace, "SF Mono", Menlo, "Noto Sans Mono CJK TC", monospace`). Headings and body use the same family; do not mix in a sans-serif font.
- Default body text is about 20px, captions and expanded content about 18px, and secondary labels at least 16px. Adjust to content and screen, and do not shrink back to small text on phones. Keep a readable line width, line height, and contrast. A big image does not mean the small text inside a full-page screenshot is readable.
- [assets/starter](assets/starter/) is a general base to adapt, not a fixed layout. Read it only when building a new page or resetting the layout. When updating an existing page, maintain its current content directly. Replace the template's sample text with this task's facts; never treat it as finished work.

## Local output and delivery

- By default, compile Tailwind to a local CSS file. The static page opens offline. It needs no hosting, deployment, CDN runtime, or front-end framework. Follow the user if they specify otherwise.
- Reuse the project's existing entry point and update the same report at each key step. If there is none, use `status/index.html` under a suitable delivery directory. Keep the needed `style.css`, the Tailwind input, and a short build note. Create comparison versions only when a comparison is needed. Clean up only files that are superseded and have no dependents. Do not delete formal evidence.
- Prefer sharing an existing Tailwind toolchain; do not rebuild the environment for every report. For the new base, see [references/build.md](references/build.md) for compiling and regenerating.
- After an update, check the compile, images and local links, the expand/collapse behavior, and the font size, overflow, and clipping on representative screens. Do only the necessary checks, not a full test suite every time.
- Open or refresh the right page in the browser automatically and confirm it shows the latest content. Do not disturb unrelated tabs. If a tool policy or permission blocks this, do not bypass it. Deliver the file entry point and state honestly that the display and visual check was not completed.
- In the reply, give the fixed entry point, the key results, and the necessary limits, plus a next-step suggestion. Keep the web page and the delivered text consistent.
