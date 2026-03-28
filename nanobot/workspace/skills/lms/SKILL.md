# LMS Skills — How to Use the LMS MCP Tools

You have access to the LMS (Learning Management System) via MCP tools. This skill teaches you how to use them effectively.

## Available Tools

| Tool | When to Use | Parameters |
|------|-------------|------------|
| `lms_health` | Check if the LMS backend is healthy | None |
| `lms_labs` | List all available labs | None |
| `lms_learners` | List all registered learners | None |
| `lms_pass_rates` | Get pass rates for a specific lab | `lab` (required) |
| `lms_timeline` | Get submission timeline for a lab | `lab` (required) |
| `lms_groups` | Get group performance for a lab | `lab` (required) |
| `lms_top_learners` | Get top learners for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate for a lab | `lab` (required) |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline | None |

## How to Respond to Common Questions

### "What labs are available?"
→ Call `lms_labs` and list the results in a readable format.

### "Show me the scores" or "Show me pass rates" (no lab specified)
→ **Do NOT guess the lab.** Ask the user which lab they want, or first call `lms_labs` and list available options.

### "Which lab has the lowest pass rate?"
→ Call `lms_labs` to get all labs, then call `lms_pass_rates` for each lab, compare and report.

### "Who are the top students in lab-04?"
→ Call `lms_top_learners` with `lab="lab-04"`.

### "How many students passed lab-01?"
→ Call `lms_completion_rate` with `lab="lab-01"`.

### "When were submissions made for lab-03?"
→ Call `lms_timeline` with `lab="lab-03"`.

### "How do groups compare in lab-02?"
→ Call `lms_groups` with `lab="lab-02"`.

## Formatting Guidelines

- **Percentages**: Format as `51.4%` not `0.514`
- **Counts**: Use commas for large numbers (e.g., `1,234 submissions`)
- **Tables**: Use markdown tables for comparisons
- **Lab IDs**: Use the exact ID from the API (e.g., `lab-01`, `lab-02`)
- **N/A**: Use for labs with no data yet

## When You Don't Have Enough Information

If the user asks about a specific lab but doesn't provide the lab ID:
1. First call `lms_labs` to get available options
2. Ask the user to clarify which lab they mean
3. Or list the available labs and let them choose

**Example:**
```
User: "Show me the scores"
You: "Which lab would you like to see scores for? Here are the available labs:
- Lab 01: Products, Architecture & Roles
- Lab 02: Run, Fix, and Deploy a Backend Service
- ..."
```

## Keep Responses Concise

- Lead with the answer
- Provide supporting data in a table
- Offer to dive deeper if needed

## What You Cannot Do

- You cannot access real-time logs or traces (that requires observability tools)
- You cannot modify data — only read
- You cannot access learner-specific data without proper authorization
- You don't know about labs outside this LMS instance
