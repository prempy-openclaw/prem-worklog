---
name: claude-model-selection
description: How to choose the right Claude model for each task using official Anthropic guidance and cost/performance tradeoffs.
metadata: {}
---

# Claude Model Selection Guide

Official source: https://platform.claude.com/docs/en/about-claude/models/overview
Pricing source: https://platform.claude.com/docs/en/about-claude/pricing

## Current Model Roles

| Model | Best for | Speed | Input $/MTok | Output $/MTok |
|---|---|---|---:|---:|
| Claude Opus 4.6 | Highest-complexity reasoning and coding | Medium | 5 | 25 |
| Claude Sonnet 4.5 | Balanced quality + speed | Fast | 3 | 15 |
| Claude Haiku 4.5 | High-throughput lightweight tasks | Fastest | 1 | 5 |

## Selection Rules

### Use Opus 4.6 when
- architecture decisions are high-risk
- debugging spans multiple systems/layers
- task quality matters more than cost or latency
- final review must be high confidence

### Use Sonnet 4.5 when
- daily coding and feature work
- docs, summaries, normal planning
- code review and test authoring

### Use Haiku 4.5 when
- classification/extraction/transformation
- repetitive automation and high volume jobs
- low-latency utility responses

## Cost Optimization

1. Route by task difficulty (Haiku → Sonnet → Opus escalation)
2. Use prompt caching for repeated context
3. Use Batch API for non-urgent jobs
4. Use extended thinking only when genuinely needed

## Suggested OpenClaw Defaults

- Main high-stakes decision/chat: Opus
- Most cron jobs: Sonnet
- Cheap parsing/filtering cron jobs: Haiku

## Practical Rule

Start with **Sonnet**. Escalate to **Opus** for hard reasoning; downshift to **Haiku** for bulk/simple processing.
