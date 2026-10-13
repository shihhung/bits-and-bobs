# bits-and-bobs

Odds and ends: tools, articles, proofs of concept, and a few AI tools and skills.

## Layout

| Folder | Contents |
| --- | --- |
| `ai/skills/` | Skills, one folder each, containing a `SKILL.md` |
| `ai/claude/` | Claude-related notes and configs |
| `ai/codex/` | Codex-related notes and configs |
| `tools/` | General tools (not AI-related) |
| `articles/` | Articles |
| `pocs/` | Proofs of concept |

## Index

| Name | Type | Description |
| --- | --- | --- |
| [handoff](ai/skills/handoff/) | Skill | Review work in progress and write a clean handoff for the next conversation |
| [work-report](ai/skills/work-report/) | Skill | Build and maintain a layered, illustrated, offline-readable work report |
| [jira-acli](ai/skills/jira-acli/) | Skill | Operate Jira through Atlassian's CLI (acli) instead of MCP, with a markdown to ADF converter |
| [Articles](articles/) | Articles | LinkedIn articles on software workflow in the age of AI (Traditional Chinese and English) |

## How the skills fit together

`handoff` closes a phase of work. It asks for a record in the project's official history (for example Jira) and an illustrated report. The other two skills supply those pieces:

```
handoff  ->  work-report   (illustrated status report)
         ->  jira-acli     (read and update the official Jira record)
```

Each skill works on its own, but they were written to be used together.

## License

| Folder | License |
| --- | --- |
| `ai/`, `tools/`, `pocs/` (skills, scripts, and code) | [MIT](LICENSE) |
| `articles/` (text and images) | [CC BY 4.0](articles/LICENSE). Share and adapt with credit to Ivan Lin. |

`ai/skills/work-report/assets/starter/style.css` contains compiled Tailwind CSS, which keeps its own MIT notice at the top of the file.
