---
name: jira-acli
description: |
  Operate Jira through Atlassian's official CLI (acli) instead of MCP tools, saving over 90% of context.
  Use for: looking up, creating, editing, commenting on, and transitioning issues, and for batch operations; also lets Codex or other CLI-agent workers read and write Jira themselves.
  Three traps to know (tested 2026-09-18, acli 1.3.36):
  - Comments and descriptions must be ADF JSON. Plain markdown is not rendered. Convert with scripts/md2adf.py.
  - --status and --type take names, and the names are translated to the account's language. Use an English account and send English names (Done, Task).
  - Pipe output through --csv, or --json with jq. Bare --json is larger than MCP, and the default table carries ANSI color codes.
  Still use MCP for: listing the available transitions, and deleting work items.
  Worker note: a workspace-write sandbox cannot read the keychain OAuth token, so acli reports unauthorized.
allowed-tools: Bash, Read
---

# Use acli for Jira, not MCP

The official Atlassian CLI covers everyday Jira work.

Two reasons to replace MCP, in order of importance:

1. **Codex and other CLI-agent workers can use it.** MCP connectors are bound to a claude.ai account, so workers cannot reach them. Dispatch briefs end up saying "do not read or write Jira", and every gate report has to route back through the orchestrator. acli is a local binary, so workers run it directly.
2. **It saves context.** Write operations return 60 to 80 characters instead of several thousand. For queries, pipe through `jq` so only the fields you need enter context. Measured numbers are at the end.

## Setup

```bash
brew tap atlassian/homebrew-acli
brew trust atlassian/acli        # Homebrew now requires trusting a tap first
brew install acli
acli jira auth login --web       # OAuth; needs interactive site selection, do not run in the background
acli jira auth status            # confirm: Authentication Type: oauth
```

`--web` waits at an interactive menu for Enter. In the background it hangs forever, and `auth status` still says unauthorized. With no interactive terminal, use an API token:

```bash
echo "$TOKEN" | acli jira auth login --site <site>.atlassian.net --email <email> --token
```

Only versions released in the last six months are supported. Run `acli --version` before use, and do not hard-code command syntax elsewhere.

## Three traps

### 1. Comments and descriptions must be ADF

The help text says "plain text or ADF", but sending markdown does not render. The whole text lands in one paragraph, and `##`, `**`, and backticks show up as literal characters. Use the converter shipped with this skill:

```bash
python3 scripts/md2adf.py -i note.md -o note.adf.json
acli jira workitem comment create --key PROJ-1 --body-file note.adf.json
```

The converter supports headings, bold, italic, strikethrough, inline code, links, ordered and bullet lists (one nested level), code blocks (with language), blockquotes, and horizontal rules. It does not support tables, images, mentions, or panels. Write ADF by hand for those.

Short plain-text comments need no conversion. Use `--body "one line"`.

### 2. Send English names for status and type

`--status` and `--type` accept **names** only, not status ids or transition ids (both return `No allowed transitions found` in testing). Names are translated according to the **caller's account language**. If the account language is not English, acli expects translated names, which will not match the English names MCP returns.

Set the Atlassian account language to English so acli and MCP agree:

```bash
acli jira workitem transition --key PROJ-1 --status "Done" --yes
acli jira workitem create --project PROJ --type "Task" --summary "..."
```

Common default names are To Do, In Progress, and Done. Projects can define more (for example Backlog or Selected for Development), and status ids differ per project, so do not copy ids from another site. When a name is rejected, check what language the current state comes back in with `--fields "key,status" --csv`. If the account language changed, the names change with it (a wrong `create --type` lists the valid values).

### 3. acli does not list available transitions

A failed transition only returns `No allowed transitions found for given status`, with no list of options. To explore, fall back to the MCP tool `getTransitionsForJiraIssue`, or call the REST API directly.

## Output format

**Never let bare `--json` enter context.** It returns the full REST structure with many null fields. For the same query (16 issues), measured:

| Method | Characters | Use |
| --- | ---: | --- |
| `--json` | 33,001 | Input for jq only; do not read it directly |
| `--fields ... --json` | 17,386 | Same |
| Default table | 7,992 | Carries ANSI color codes; avoid |
| `--csv` | 1,159 | **For people and for context** |
| `--json` piped to jq | 1,140 | **Use when you need to pick fields** |
| `--count` | one line | When you only need the count |

Only `search` has `--csv`; `view` does not. To shrink `view` output, pipe through jq.

```bash
acli jira workitem search --jql "$JQL" --fields "key,summary,status" --csv
acli jira workitem search --jql "$JQL" --json \
  | jq -r '.[] | "\(.key)\t\(.fields.status.name)\t\(.fields.summary)"'
```

Creating is the same: with `--json` the reply is 8,052 characters. Without it you get one 78-character line with a success message and the URL.

## Common commands

```bash
# Query
acli jira workitem search --jql "project = X AND statusCategory != Done" --csv
acli jira workitem search --jql "$JQL" --count
acli jira workitem view PROJ-1 --fields "summary,status,description"   # the key is positional, not --key

# Create
acli jira workitem create --project PROJ --type "Task" --summary "..." \
  --description-file desc.adf.json

# Comment (ADF)
acli jira workitem comment create --key PROJ-1 --body-file note.adf.json
acli jira workitem comment create --jql "$JQL" --body-file note.adf.json   # batch
# Read comments with view, not comment list (list has no created date and flattens ADF, dropping list items)
acli jira workitem view PROJ-1 --fields "comment" --json \
  | jq -r '.fields.comment.comments[] | "\(.created[0:10]) \(.author.displayName): \([.body | .. | objects | select(.type=="text") | .text] | join(" "))"'

# Transition (batch supported)
acli jira workitem transition --key "PROJ-1,PROJ-2" --status "Done" --yes
acli jira workitem transition --jql "$JQL" --status "In Progress" --yes

# Edit fields
acli jira workitem edit --key PROJ-1 --summary "..."
```

`comment create`, `transition`, `delete`, and `edit` all support `--key "A-1,A-2"` for batches and `--jql` for conditional batches, so one call handles many issues. Add `--ignore-errors` so a failing batch carries on with the rest.

## Running inside a sandbox (read this before dispatching workers)

**Inside a `workspace-write` sandbox, acli reports unauthorized.** The OAuth token lives in the macOS keychain (`~/.config/acli/jira_config.yaml` holds only non-sensitive fields such as site, cloud_id, and email). The sandbox blocks keychain access, so `acli jira auth status` exits 1. Tested 2026-09-18 with Codex Desktop: with elevated permissions the same command exits 0 and authenticates.

When you hand Jira work to a worker, loosen the sandbox (`-s danger-full-access`, with the dispatch brief limiting what the worker may touch), or switch to an API token passed through environment variables. This conflicts with the default `workspace-write` sandbox, so say it explicitly in the dispatch brief.

## When MCP is still needed

- **Listing available transitions.** acli has no such command. A wrong transition only returns `No allowed transitions found for given status` and never lists valid values (a wrong `create --type` does list them). MCP returns two names per transition: `name` (the action) and `to.name` (the target status). They are usually the same but not always. Send acli the **target status name** (`to.name`).
- **Deleting work items.** With OAuth login, delete was blocked by a permission error (`AuthException`, the account had no delete permission in the project). MCP has no delete tool either, so delete in the web UI.

## Measured numbers (2026-09-18, acli 1.3.36)

| Operation | MCP average reply | acli reply |
| --- | ---: | ---: |
| Create issue | 4,718 | 78 |
| Comment | 3,501 | 61 |
| Transition | 4,968 | 70 |
| Batch transition of two issues | 9,936 (two calls) | 176 (one call) |
| Query 16 issues | 14,383 | 1,159 |

The MCP numbers come from one week of my own usage (2026-09-11 to 2026-09-18): 303 calls, 1.54 million characters in total. Your numbers will differ.
