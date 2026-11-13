# CLAUDE.md

@AGENTS.md

@docs/WRITING_AND_COMMUNICATION_RULES.md

## Claude-specific notes

The rules above bind Claude Code too. These notes add what only applies to Claude.

### Writing

The writing rules are imported above, so they load in every session.
Follow them in the files you write and in your replies in chat.

### Which model for which work

| Model | Work |
|---|---|
| Fable | Design: the v0 design, policies, hard debugging, surfacing open decisions |
| Opus | Building against `docs/V0.md`; first instances; code review |
| Sonnet | Repeating an established pattern; doc syncs; status updates |
| Haiku | Quick lookups; no repo changes |

### Asking the owner

- Put a ⚠ decision to the owner with the question tool: two to four options, the recommended one first and marked.
- Explain the question in plain words before the options. The owner often answers with a variant of their own; fold it into the plan rather than forcing a listed option.

### The agents under test

- Notebook `05` calls Claude through the official `anthropic` Python SDK. Before you write that code, load the `claude-api` skill and follow it, because the API changes.
- Start with `claude-opus-5-5` (D13). Notebook `06` compares it with the other agents. The harness design is in `docs/V0.md`, section "Agents and tools".
