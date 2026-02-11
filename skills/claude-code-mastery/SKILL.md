---
name: claude-code-mastery
description: 50 practical tips for using Claude Code effectively, from foundations to advanced parallel workflows.
metadata: {}
---

# Claude Code Mastery (50 Tips)

Source video: https://youtu.be/mZzhfPle9QU

## Act 1 — Foundations (1–25)

1. Start from repository root.
2. Run `/init` immediately.
3. Use hierarchical `CLAUDE.md` (root + folder-level).
4. Keep `CLAUDE.md` concise.
5. Structure `CLAUDE.md` as: What / Domain / Validation.
6. `Shift+Tab` toggles Plan vs Code mode.
7. `Esc` interrupts generation.
8. Double `Esc` clears current input.
9. Double `Esc` on empty input rewinds state.
10. Drag screenshots directly for visual bugs.
11. Add context text with screenshots.
12. `/clear` resets context.
13. `/context` checks token usage.
14. Let auto-compaction do its job.
15. `/model` switches model.
16. `/resume` restores a prior session.
17. `/mcp` inspects MCP status.
18. `/help` lists commands.
19. Use git as your safety net (commit before risky edits).
20. Add a “Critical Rules” section in `CLAUDE.md`.
21. Ask Claude to update project rules when needed.
22. Use workflow triggers in `CLAUDE.md`.
23. Commit `CLAUDE.md` to git.
24. Use dangerous skip mode only in throwaway environments.
25. Combine skip permissions with strict allowlists.

## Act 2 — Daily Workflow (26–32)

26. Start new features in Plan mode.
27. Fresh context beats bloated context.
28. Persist progress before ending sessions.
29. Lazy-load context instead of dumping everything.
30. Give explicit verification commands.
31. Use stronger models for hard tasks.
32. Read reasoning/thinking blocks for debugging.

## Act 3 — Power User (33–40)

33. Use four primitives: Skills, Commands, MCPs, Subagents.
34. Skills = recurring workflows.
35. Commands = shorthand for frequent actions.
36. Let Claude create command files for consistency.
37. MCPs = external service integration.
38. Ask Claude to install/configure MCPs.
39. Subagents provide isolated context and parallel work.
40. Avoid instruction overload in rule files.

## Act 4 — Advanced (41–50)

41. Run multiple Claude sessions in parallel.
42. Use terminal split panes for visibility.
43. Enable notifications for long tasks.
44. Use git worktrees for strong isolation.
45. Connect browser tooling for UI tasks.
46. Use browser + logs for faster debugging.
47. Use hooks to intercept workflow steps.
48. Auto-format with post-tool hooks.
49. Block dangerous commands with pre-tool hooks.
50. Explore ecosystem plugins/extensions.

## Core Principle

**Context is king.**

Good context + clear constraints + concrete verification commands consistently produce better outcomes.
