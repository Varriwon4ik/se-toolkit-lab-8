# Observability Skills — How to Use Logs and Traces MCP Tools

You have access to VictoriaLogs and VictoriaTraces via MCP tools. This skill teaches you how to use them effectively for debugging and monitoring.

## Available Tools

### VictoriaLogs Tools

| Tool | When to Use | Parameters |
|------|-------------|------------|
| `logs_search` | Search logs by keyword, service, or severity | `query` (LogsQL), `limit` (1-1000), `start`, `end` |
| `logs_error_count` | Count errors per service over a time window | `start` (e.g., "1h", "30m", "1d") |

### VictoriaTraces Tools

| Tool | When to Use | Parameters |
|------|-------------|------------|
| `traces_list` | List recent traces for a service | `service`, `operation`, `limit` (1-100) |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required) |

## LogsQL Query Examples

VictoriaLogs uses LogsQL for querying. Common patterns:

| Query | Description |
|-------|-------------|
| `*` | All logs |
| `error` | Logs containing "error" |
| `severity:ERROR` | Only ERROR level logs |
| `severity:WARN` | Only WARN level logs |
| `_stream:{service.name="Learning Management Service"}` | Logs from specific service |
| `_stream:{service.name="Learning Management Service"} AND severity:ERROR` | Errors from specific service |
| `event:request_started` | Request start events |
| `event:db_query` | Database query events |

## How to Respond to Common Questions

### "Any errors in the last hour?"

1. Call `logs_error_count` with `start="1h"`
2. If errors found, call `logs_search` with `query="severity:ERROR"` and `start="1h"` to get details
3. Summarize: which services have errors, what the errors are
4. If traces are mentioned, call `traces_list` to find related traces

### "What went wrong?" or "Check system health"

This is a **one-shot investigation** — chain log and trace tools together:

1. **Search recent error logs first:**
   ```
   logs_search(query="severity:ERROR", limit=10, start="5m")
   ```

2. **Extract the trace_id** from the most recent error log entry

3. **Fetch the full trace:**
   ```
   traces_get(trace_id="<extracted_trace_id>")
   ```

4. **Analyze the trace:**
   - Look for spans with `has_error=true` or an `error` tag
   - Identify which operation failed (e.g., "SELECT db-lab-8", "GET /items/")
   - Note the error message from the span tags

5. **Summarize concisely** — combine log and trace evidence:
   - What the error was (from logs)
   - Where it occurred (from trace span)
   - When it happened (timestamp)
   - Root cause hypothesis (e.g., "PostgreSQL unreachable", "Connection refused")

**Example response format:**
> "The last request failed at {timestamp}. Logs show error: '{error_message}' during {operation}. Trace {trace_id} shows the failure occurred in the {span_operation} span after {duration}ms. Root cause: {root_cause}."

### "Show me logs for the backend service"

1. Call `logs_search` with query=`_stream:{service.name="Learning Management Service"}`
2. Present the logs in a readable format

### "Are there any traces with errors?"

1. Call `traces_list` with `service="Learning Management Service"` and `limit=10`
2. Look for traces with `has_error=true`
3. For each error trace, optionally call `traces_get` for details

### "Debug this trace ID: abc123..."

1. Call `traces_get` with the provided `trace_id`
2. Analyze the span hierarchy
3. Identify which span has the error (look for `has_error=true` or `error` tag)
4. Report the failing operation and error message

### "Show me logs for the backend service"

1. Call `logs_search` with query=`_stream:{service.name="Learning Management Service"}`
2. Present the logs in a readable format

### "Are there any traces with errors?"

1. Call `traces_list` with `service="Learning Management Service"` and `limit=10`
2. Look for traces with `has_error=true`
3. For each error trace, optionally call `traces_get` for details

### "Debug this trace ID: abc123..."

1. Call `traces_get` with the provided `trace_id`
2. Analyze the span hierarchy
3. Identify which span has the error (look for `has_error=true` or `error` tag)
4. Report the failing operation and error message

## Formatting Guidelines

- **Timestamps**: Convert Unix timestamps to readable format (e.g., "2026-03-28 19:49:13")
- **Duration**: Convert microseconds to milliseconds (÷1000) or seconds (÷1,000,000)
- **Error messages**: Quote the actual error text
- **Trace IDs**: Show full ID or truncate with ellipsis if very long
- **Tables**: Use markdown tables for multiple log entries or spans

## Keep Responses Concise

- Lead with the answer ("Yes, there are 3 errors" or "No errors found")
- Show only relevant details (error message, service name, timestamp)
- Don't dump raw JSON — summarize in prose
- Offer to dive deeper if needed ("Want to see the full trace?")

## What You Cannot Do

- You cannot modify logs or traces — only read
- You cannot access logs outside the configured time range
- You cannot correlate logs across different systems without a common trace ID

## Example Workflow: Debugging a Failure

**User**: "The app is broken! What happened?"

**You**:
1. First, check for recent errors:
   ```
   logs_error_count(start="1h")
   ```
2. If errors found, get details:
   ```
   logs_search(query="severity:ERROR", limit=10, start="1h")
   ```
3. Find a trace ID in the error logs
4. Fetch the full trace:
   ```
   traces_get(trace_id="...")
   ```
5. Report: "The database connection failed. The error occurred in the SELECT operation on PostgreSQL. Trace shows the request started at 19:49:13 and failed 100ms later."

## Time Range Format

Use relative time strings:
- `"30m"` — Last 30 minutes
- `"1h"` — Last hour
- `"1d"` — Last day
- `"7d"` — Last week

Or Unix timestamps for absolute times.
