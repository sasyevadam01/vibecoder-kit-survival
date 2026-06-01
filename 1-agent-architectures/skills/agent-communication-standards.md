---
name: agent-communication-standards
description: Guidelines for agentic communication including Bottom-Line First (BLUF) formatting and context window compression.
---

# Agent Communication Standards

## Overview

In multi-agent systems, communication overhead is the primary driver of high latency and token cost. This document outlines standard practices for structural dialogue design, focusing on Bottom-Line First (BLUF) presentation and Context Compression rules. These principles keep interactions dense, actionable, and cost-effective.

## The BLUF Protocol (Bottom-Line First)

When agents communicate with each other or with users, they must lead with the conclusion or key request.

### Principles of BLUF

1. **Immediate Delivery**: Place the final recommendation, primary question, or critical error in the first two sentences.
2. **Supporting Detail Separation**: Reserve technical rationales, logs, and background context for subsequent sections.
3. **Structured Formats**: Use consistent header patterns to allow rapid parsing by either human readers or parser utilities.

### Bad Example
> We have run the diagnostic sequence on the server cluster. After checking the logs in `/var/log` and checking for database locks, we noticed a high CPU spike on node 3. We attempted a restart, but it timed out. Therefore, we need human approval to force-reboot node 3 to prevent cascading outages.

### Good Example
> **Action Required**: Approve force-reboot of Node 3 to prevent a cascading outage.
> 
> **Context**:
> - Node 3 is experiencing a high CPU spike.
> - A standard restart has timed out.
> - Diagnostic logs indicate database connections are piling up.

## Context Compression (Karpathy Rules)

Context compression limits token bloat by ensuring that agents only pass high-density information.

### Rule 1: Use Structural Signposts
Instead of dump-printing raw files, use file basenames with precise line numbers or JSON paths to refer to segments. Do not include unreferenced parts.

### Rule 2: Token Pruning
Prune log outputs, stack traces, and data dumps aggressively.
- Keep only the first 5 and last 10 lines of large error traces.
- Replace repetitive JSON arrays with structural schemas or singular examples followed by an array length notation: `[ { "id": 1, ... } /* and 49 more items */ ]`.

### Rule 3: De-duplicate Memory
Never echo back the entire prompt of the caller or restate the whole instruction. Rely on shared state files or artifacts rather than passing raw text strings back and forth across agent boundaries.

### Rule 4: Typography and Presentation
When presenting design proposals or UI guides, enforce specific typographical hierarchies:
- **Headings**: Use **Plus Jakarta Sans** for prominent, high-impact titles.
- **Body Text**: Use **Outfit** for reading comfort and geometric clarity.
- **Forbidden Fonts**: Never recommend or reference other standard default system sans-serif fonts in visual layouts.
