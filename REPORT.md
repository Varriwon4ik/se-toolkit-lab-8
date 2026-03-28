# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question 1: "What is the agentic loop?"**

```
The agentic loop is the core iterative process that autonomous AI agents use to accomplish
tasks. It's a continuous cycle of:

The Basic Loop

 1 Perceive — Gather information from the environment (observations, user input, tool outputs,
   etc.)
 2 Think/Reason — Process the information, plan next steps, make decisions
 3 Act — Execute actions (call tools, send messages, modify files, etc.)
 4 Repeat — Observe the results and continue the loop until the goal is achieved

Why It Matters

Unlike a simple query-response model, the agentic loop enables:

 • Autonomy — Agents can work independently toward goals
 • Adaptation — Agents adjust based on feedback and changing conditions
 • Multi-step reasoning — Complex tasks are broken into sequential actions
 • Self-correction — Agents can detect errors and try alternative approaches

Example

For a task like "research and summarize recent AI news":

 1 Perceive: Understand the request
 2 Think: Plan to search for news, then summarize
 3 Act: Call web_search tool
 4 Perceive: Get search results
 5 Think: Evaluate results, plan to fetch top articles
 6 Act: Call web_fetch on selected URLs
 7 Think: Synthesize information
 8 Act: Deliver summary to user

This loop continues until the task is complete or the agent determines it cannot proceed.
```

**Question 2: "What labs are available in our LMS?"**

```
Based on the LMS (Lab Management System) in this workspace, here are the available labs:

Lab 8 — The Agent is the Interface

This is the current lab in your workspace. It focuses on building an AI agent as a
natural-language interface for an LMS system.

Required Tasks:

 1 Task 1 — Set Up the Agent (install nanobot, configure Qwen API, add MCP tools, write skill
   prompt)
 2 Task 2 — Deploy and Connect a Web Client (Dockerize nanobot, add WebSocket channel +
   Flutter chat UI)
 3 Task 3 — Give the Agent New Eyes (explore observability data, write log/trace MCP tools)
 4 Task 4 — Diagnose a Failure and Make the Agent Proactive (investigate failure, schedule
   health checks, fix a planted bug)
 5 Task 5 — (additional required task)

Optional Tasks:

 1 Task 1 — Add a Telegram Bot Client (same agent, different interface)
```

Note: The agent doesn't know about the actual LMS backend data yet — it's reading from the workspace files. This is expected for Part A (no MCP tools configured).

## Task 1B — Agent with LMS tools

**Question 1: "What labs are available?"**

```
Here are all the labs available in your LMS:

                                                        
 Lab ID  Title                                          
 ────────────────────────────────────────────────────── 
 Lab 01  Products, Architecture & Roles                 
 Lab 02  Run, Fix, and Deploy a Backend Service         
 Lab 03  Backend API: Explore, Debug, Implement, Deploy 
 Lab 04  Testing, Front-end, and AI Agents              
 Lab 05  Data Pipeline and Analytics Dashboard          
 Lab 06  Build Your Own Agent                           
 Lab 07  Build a Client with an AI Coding Agent         
 Lab 08  lab-08 (The Agent is the Interface)            
                                                        

You have 8 labs total. Lab 08 is the one currently in your workspace (/root/se-toolkit-lab-8).
```

**Question 2: "Describe the architecture of the LMS system"**

The agent provided a detailed architecture description including:

- **7 Docker containers**: Caddy (reverse proxy), FastAPI backend, PostgreSQL, pgAdmin, Nanobot, Telegram Bot
- **High-level flow**: Student → Caddy (:42002) → FastAPI (:8000) → PostgreSQL
- **AI agent flow**: User → Nanobot (WS :8765) → MCP Tools → FastAPI → PostgreSQL
- **Data model**: OBER-based with Item, Learner, and Interacts tables
- **Key design decisions**: Monolith with layered structure, Caddy reverse proxy, SQLModel ORM, async database access

**Bonus: "Which lab has the lowest pass rate?"**

```
Based on the pass rate data, Lab 02 — Run, Fix, and Deploy a Backend Service has the lowest
overall pass rate.

Pass Rate Summary by Lab

 Lab     Avg Score  Tasks              
 ───────────────────────────────────── 
 Lab 01  51.4%      8 tasks            
 Lab 02  48.3% ⚠️   6 tasks            
 Lab 03  53.6%      5 tasks            
 Lab 04  55.9%      4 tasks            
 Lab 05  67.3%      4 tasks            
 Lab 06  59.3%      3 tasks            
 Lab 07  67.3%      4 tasks            
 Lab 08  N/A        No submissions yet

Lab 02 Breakdown

The low pass rate is largely due to one particularly challenging task:

                                                                     
 Task                                            Avg Score  Attempts 
 ─────────────────────────────────────────────────────────────────── 
 Optional 2: Make your VM a proxy                0.0%       3        
 Optional 1: Implement the /outcomes endpoint    36.4%      11       
 Task 4: Deploy the web server to the VM         56.2%      84       
 Task 1: Run the web server                      67.9%      210      
 Task 2: Identify, report, and fix a bug         66.7%      216      
 Optional 3: Implement the post-order traversal  62.5%      6
```

The agent correctly called multiple MCP tools (`lms_labs`, `lms_pass_rates`) and analyzed the data to provide insights.

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

The agent now handles ambiguous queries much better. Instead of guessing or hallucinating, it:

1. First gathered comprehensive data using multiple MCP tools
2. Presented completion rates for all labs
3. Showed average scores by lab and task
4. Provided key insights

**Response excerpt:**

```
📊 LMS Lab Scores Overview

Completion Rates (Passed / Total Students)

 Lab     Title                                           Completion Rate  Passed  Total 
 ────────────────────────────────────────────────────────────────────────────────────── 
 Lab 01  Products, Architecture & Roles                  100.0% ✅        258     258   
 Lab 02  Run, Fix, and Deploy a Backend Service          89.1%            131     147   
 Lab 03  Backend API: Explore, Debug, Implement, Deploy  89.1%            156     175   
 Lab 04  Testing, Front-end, and AI Agents               96.7%            238     246   
 Lab 05  Data Pipeline and Analytics Dashboard           98.4%            246     250   
 Lab 06  Build Your Own Agent                            98.4%            241     245   
 Lab 07  Build a Client with an AI Coding Agent          99.6% ✅         236     237   
 Lab 08  The Agent is the Interface                      0.0%             0       0     

📈 Key Insights

 Metric                   Value                      
 ─────────────────────────────────────────────────── 
 Highest Completion Rate  Lab 07 (99.6%)             
 Lowest Completion Rate   Lab 02 & Lab 03 (89.1%)    
 Highest Avg Task Score   Lab 05 - Task 3 (74.1%)    
 Lowest Avg Task Score    Lab 02 - Optional 2 (0.0%) 
 Most Attempted Task      Lab 01 - Lab setup (3,149) 
```

**Skill prompt location:** `nanobot/workspace/skills/lms/SKILL.md`

The skill prompt teaches the agent:
- Which `lms_*` tools are available and when to use each
- To ask for clarification when a lab parameter is needed but not provided
- To format numeric results nicely (percentages, counts)
- To keep responses concise but informative
- To explain its current tools and limits when asked "what can you do?"

## Task 2A — Deployed agent

Nanobot gateway startup log excerpt:

```
Starting nanobot gateway with resolved config: /app/config.resolved.json
Workspace: /app/workspace
🐈 Starting nanobot gateway version 0.1.4.post6 on port 18790...
  Created HEARTBEAT.md
  Created AGENTS.md
  Created TOOLS.md
  Created SOUL.md
  Created USER.md
  Created memory/MEMORY.md
  Created memory/HISTORY.md
2026-03-28 10:45:20.559 | INFO     | nanobot.cron.service:start:202 - Cron service started with 0 jobs
2026-03-28 10:45:20.559 | INFO     | nanobot.heartbeat.service:start:124 - Heartbeat started (every 1800s)
```

The gateway is running. (Note: "No channels enabled" warning appears until we install the webchat channel plugin in Part B.)

## Task 2B — Web client

**WebSocket endpoint test:**

The WebSocket endpoint at `ws://localhost:42002/ws/chat` is accessible and returns "426 Upgrade Required" when accessed via HTTP (expected behavior for WebSocket endpoints).

**Flutter web client:**

The Flutter web client is accessible at `http://localhost:42002/flutter/`. 

To test:
1. Open `http://<your-vm-ip>:42002/flutter` in a browser
2. Log in with your `NANOBOT_ACCESS_KEY` (set in `.env.docker.secret`)
3. Ask the agent questions like "What can you do?" or "What labs are available?"

**Files created/modified:**

- `nanobot/entrypoint.py` — Runtime config resolver for Docker deployment
- `nanobot/Dockerfile` — Multi-stage build with uv
- `nanobot/config.json` — Added webchat channel config
- `nanobot/pyproject.toml` — Added nanobot-webchat dependencies
- `docker-compose.yml` — Uncommented nanobot and client-web-flutter services
- `caddy/Caddyfile` — Uncommented `/ws/chat` and `/flutter` routes
- `nanobot-websocket-channel/` — Git submodule for WebSocket channel and Flutter client

## Task 3A — Structured logging

### Happy-path log excerpt (request_started → request_completed with status 200)

```
2026-03-28 19:57:58,656 INFO [app.main] [main.py:60] [trace_id=adfbb2068fb8391f86db94456c3d3959 span_id=cce23db63458843c resource.service.name=Learning Management Service trace_sampled=True] - request_started
2026-03-28 19:57:58,845 INFO [app.auth] [auth.py:30] [trace_id=adfbb2068fb8391f86db94456c3d3959 span_id=cce23db63458843c resource.service.name=Learning Management Service trace_sampled=True] - auth_success
2026-03-28 19:57:58,915 INFO [app.db.items] [items.py:16] [trace_id=adfbb2068fb8391f86db94456c3d3959 span_id=cce23db63458843c resource.service.name=Learning Management Service trace_sampled=True] - db_query
2026-03-28 19:58:00,437 INFO [app.main] [main.py:68] [trace_id=adfbb2068fb8391f86db94456c3d3959 span_id=cce23db63458843c resource.service.name=Learning Management Service trace_sampled=True] - request_completed
INFO:     172.21.0.1:49990 - "GET /items/ HTTP/1.1" 200 OK
```

The log shows the complete request lifecycle:
1. `request_started` — Request received
2. `auth_success` — API key validated
3. `db_query` — Database query executed
4. `request_completed` — Response sent with status 200

### Error-path log excerpt (db_query with error)

```
2026-03-28 20:23:33,440 INFO [app.main] [main.py:60] [trace_id=099fd8f1605f6250d3e8841113aead85 span_id=aca5f4dbd72aae70 resource.service.name=Learning Management Service trace_sampled=True] - request_started
2026-03-28 20:23:33,443 INFO [app.auth] [auth.py:30] [trace_id=099fd8f1605f6250d3e8841113aead85 span_id=aca5f4dbd72aae70 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
2026-03-28 20:23:33,445 INFO [app.db.items] [items.py:16] [trace_id=099fd8f1605f6250d3e8841113aead85 span_id=aca5f4dbd72aae70 resource.service.name=Learning Management Service trace_sampled=True] - db_query
2026-03-28 20:23:33,936 ERROR [app.db.items] [items.py:20] [trace_id=099fd8f1605f6250d3e8841113aead85 span_id=aca5f4dbd72aae70 resource.service.name=Learning Management Service trace_sampled=True] - db_query
2026-03-28 20:23:33,939 INFO [app.main] [main.py:68] [trace_id=099fd8f1605f6250d3e8841113aead85 span_id=aca5f4dbd72aae70 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
INFO:     172.21.0.1:55188 - "GET /items/ HTTP/1.1" 404 Not Found
```

The error log shows:
1. `request_started` — Request received
2. `auth_success` — API key validated
3. `db_query` — Database query attempted
4. `ERROR db_query` — Database connection failed (PostgreSQL was stopped)
5. `request_completed` — Response sent with status 404

### VictoriaLogs query result

Querying VictoriaLogs directly via HTTP API with `severity:ERROR`:

```json
{
  "_msg": "db_query",
  "_stream": "{service.name=\"Learning Management Service\",telemetry.auto.version=\"0.61b0\",telemetry.sdk.language=\"python\",telemetry.sdk.name=\"opentelemetry\",telemetry.sdk.version=\"1.40.0\"}",
  "_time": "2026-03-28T20:23:33.936923648Z",
  "error": "[Errno -2] Name or service not known",
  "event": "db_query",
  "operation": "select",
  "service.name": "Learning Management Service",
  "severity": "ERROR",
  "trace_id": "099fd8f1605f6250d3e8841113aead85",
  "span_id": "aca5f4dbd72aae70"
}
```

The structured log in VictoriaLogs contains:
- **error**: `[Errno -2] Name or service not known` — DNS resolution failure for PostgreSQL
- **severity**: `ERROR` — Log level
- **service.name**: `Learning Management Service` — Source service
- **trace_id** and **span_id** — For correlation with traces
- **_time**: Precise timestamp

VictoriaLogs UI is accessible at `http://localhost:42010/utils/victorialogs/select/vmui` and provides a web interface for querying logs with LogsQL.

## Task 3B — Traces

### Healthy trace span hierarchy

Trace ID: `984b4b3b8a32b78ac1beda1c4293f9e4` (successful request with status 200)

**Span hierarchy:**

```
GET /items/ (root span)
├── SELECT db-lab-8 (84.97ms) — PostgreSQL database query
│   ├── db.name: db-lab-8
│   ├── db.system: postgresql
│   ├── db.user: postgres
│   ├── net.peer.name: postgres
│   ├── net.peer.port: 5432
│   └── db.statement: SELECT item.id, item.type, ... FROM item
├── GET /items/ http send (107μs) — HTTP response start (status 200)
└── GET /items/ http send (25μs) — HTTP response body
```

**Key observations:**
- Total trace duration: ~85ms
- Database query took 84.97ms (the majority of request time)
- HTTP response sending took only ~132μs combined
- All spans have `span.kind: client` for DB operations
- No errors in any span tags

### Error trace

Trace ID: `099fd8f1605f6250d3e8841113aead85` (failed request with status 404)

**Span hierarchy:**

```
GET /items/ (root span: aca5f4dbd72aae70)
├── SELECT db-lab-8 (FAILED)
│   ├── error: "[Errno -2] Name or service not known"
│   ├── db.system: postgresql
│   └── (PostgreSQL was stopped - connection refused)
├── GET /items/ http send (54μs) — HTTP response start (status 404)
└── GET /items/ http send (30μs) — HTTP response body
```

**Key observations:**
- The error occurred in the database span
- Error message: `[Errno -2] Name or service not known` — DNS resolution failure
- The HTTP response was still sent (404 status) but with error detail
- Trace shows the exact point of failure: database connection

### Comparing healthy vs error traces

| Aspect | Healthy Trace | Error Trace |
|--------|---------------|-------------|
| **Status** | 200 OK | 404 Not Found |
| **DB span duration** | 84.97ms | Failed immediately |
| **Error tag** | None | `error: "[Errno -2] Name or service not known"` |
| **Root cause** | N/A | PostgreSQL service stopped |

VictoriaTraces UI is accessible at `http://localhost:42011/utils/victoriatraces` and provides:
- Service-level trace listing
- Trace timeline visualization
- Span hierarchy with tags and logs
- Error highlighting

## Task 3C — Observability MCP tools

### MCP Tools Implemented

The observability MCP server provides 4 tools:

| Tool | Description | API Endpoint |
|------|-------------|--------------|
| `logs_search` | Search logs using LogsQL query | `GET /select/logsql/query` |
| `logs_error_count` | Count errors per service over time window | `GET /select/logsql/query` |
| `traces_list` | List recent traces for a service | `GET /select/jaeger/api/traces` |
| `traces_get` | Fetch specific trace by ID | `GET /select/jaeger/api/traces/{trace_id}` |

### Agent Response: "Any errors in the last hour?" (Normal Conditions)

When PostgreSQL is running, the agent uses the MCP tools to check for errors:

**Step 1: Check error count**
```json
{
  "time_window": "1h",
  "total_errors": 3,
  "by_service": [
    {
      "service": "Learning Management Service",
      "error_count": 3
    }
  ]
}
```

**Step 2: Search for error details**
The agent finds errors from earlier testing (when PostgreSQL was stopped):
- Error: `[Errno -2] Name or service not known`
- Event: `db_query`
- Service: `Learning Management Service`
- Trace ID: `099fd8f1605f6250d3e8841113aead85`

**Agent's expected response:**
> "Yes, there are 3 errors in the last hour, all from the Learning Management Service. The errors are database connection failures with the message '[Errno -2] Name or service not known'. This indicates the service couldn't reach PostgreSQL. Would you like to see the full trace?"

### Agent Response: "Any errors in the last hour?" (Failure Conditions)

After stopping PostgreSQL and triggering a request:

**Step 1: Check error count**
```json
{
  "time_window": "1h",
  "total_errors": 4,
  "by_service": [
    {
      "service": "Learning Management Service",
      "error_count": 4
    }
  ]
}
```

**Step 2: Search for error details**
```json
{
  "_msg": "db_query",
  "_time": "2026-03-28T20:28:28.822107904Z",
  "error": "[Errno -2] Name or service not known",
  "event": "db_query",
  "operation": "select",
  "service.name": "Learning Management Service",
  "severity": "ERROR",
  "trace_id": "b3260240d5226b67e54ee3a5512a2a67"
}
```

**Step 3: List traces with errors**
```json
{
  "traces": [
    {
      "trace_id": "099fd8f1605f6250d3e8841113aead85",
      "span_count": 5,
      "has_error": true,
      "services": ["Learning Management Service"]
    }
  ]
}
```

**Agent's expected response:**
> "Yes, there are 4 errors in the last hour from the Learning Management Service. The most recent error occurred at 20:28:28 UTC with message '[Errno -2] Name or service not known' during a database SELECT operation. This indicates PostgreSQL is unreachable. Trace `b3260240d5226b67e54ee3a5512a2a67` shows the failure. Would you like me to fetch the full trace details?"

### Files Created/Modified

| File | Purpose |
|------|---------|
| `mcp/mcp_observability/server.py` | MCP server with 4 observability tools |
| `mcp/mcp_observability/__init__.py` | Package init |
| `mcp/mcp_observability/__main__.py` | Entry point |
| `nanobot/workspace/skills/observability/SKILL.md` | Agent skill documentation |
| `nanobot/config.json` | MCP server configuration |
| `docker-compose.yml` | Environment variables for observability MCP |

### Verification

The MCP tools are registered and working:
```
MCP server 'observability': connected, 4 tools registered
- mcp_observability_logs_search
- mcp_observability_logs_error_count
- mcp_observability_traces_list
- mcp_observability_traces_get
```

## Task 4A — Multi-step investigation

### Enhanced Observability Skill

Updated `nanobot/workspace/skills/observability/SKILL.md` to guide the agent for one-shot investigation:

When the user asks **"What went wrong?"** or **"Check system health"**:
1. Search recent error logs first (`logs_search` with `severity:ERROR`)
2. Extract the `trace_id` from the most recent error
3. Fetch the full trace (`traces_get`)
4. Analyze spans for errors
5. Summarize findings concisely combining log and trace evidence

### Investigation Response (PostgreSQL stopped)

**Question: "What went wrong?"**

```
======================================================================
INVESTIGATION SUMMARY
======================================================================

The last request failed at 2026-03-28T21:09:55.898198784Z.

LOG EVIDENCE:
  - Error: "(sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: connection is closed"
  - Event: db_query
  - Service: Learning Management Service

TRACE EVIDENCE:
  - Trace ID: bfa5fb0bf2a73c6e11be6bbece1ec367
  - Failed span: SELECT db-lab-8
  - Duration: 31.29ms

ROOT CAUSE:
PostgreSQL database is unreachable. The error indicates
the backend cannot establish a connection to the database.

NOTE: The API returned "Items not found" (404), but the real error is
a database connection failure. This is a bug in the exception handler.
```

The agent successfully:
1. ✅ Searched error logs and found the most recent failure
2. ✅ Extracted the trace ID from the log entry
3. ✅ Fetched the full trace and identified the failing span
4. ✅ Combined log and trace evidence into a coherent summary
5. ✅ Identified the root cause (PostgreSQL unreachable)
6. ✅ Noted the misleading API response (404 instead of 500)

## Task 4B — Proactive health check

### Cron Tool for Scheduled Health Checks

The nanobot agent includes a built-in `cron` tool for scheduling recurring tasks.

**How to create a health check from the Flutter chat:**

1. Open the Flutter chat at `http://<vm-ip>:42002/flutter`
2. Send the message:
   > "Create a health check for this chat that runs every 2 minutes. Each run should check for backend errors in the last 2 minutes, inspect a trace if needed, and post a short summary here. If there are no recent errors, say the system looks healthy. Use your cron tool."

3. The agent will use the cron tool with:
   - `action: "add"`
   - `message: "Health check: check for backend errors..."`
   - `every_seconds: 120`

4. Verify with: **"List scheduled jobs."**

**Expected output:**
```
Scheduled jobs:
- Health check: check for backend err (id: <job-id>, every 2m)
  Next run: 2026-03-28T21:XX:XX (UTC)
```

**Proactive Health Report (while PostgreSQL is stopped):**

When the cron job runs, it will:
1. Call `logs_error_count(start="2m")` to check for recent errors
2. If errors found, call `logs_search` for details
3. Extract trace_id and call `traces_get` if needed
4. Post a summary to the chat

**Example proactive report:**
```
🏥 Health Check Report (21:15:00 UTC)

⚠️ UNHEALTHY: Found 2 errors in the last 2 minutes.

Latest error:
- Time: 2026-03-28T21:14:32Z
- Error: "[Errno -2] Name or service not known"
- Service: Learning Management Service
- Operation: SELECT db-lab-8

Root cause: PostgreSQL database is unreachable.
```

**To remove the test job:**
> "Remove the health check job" or "Remove job <job-id>"

---

## Task 4C — Bug fix and recovery

### Root Cause

**Location:** `backend/app/routers/items.py`, `get_items()` endpoint

**Planted Bug:** The exception handler caught all exceptions and returned a misleading 404 "Items not found" error, masking the actual database connection failure.

```python
# BUGGY CODE:
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",  # ❌ Misleading!
        ) from exc
```

**Problem:** When PostgreSQL was unavailable, the database raised a `SQLAlchemyError`, but the handler returned 404 instead of 500, making debugging difficult.

### Fix

Changed the exception handler to properly distinguish database errors and return 500 with the actual error message:

```python
# FIXED CODE:
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except SQLAlchemyError as exc:
        # Database errors should return 500, not mask as 404
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(exc)}",
        ) from exc
    except Exception as exc:
        # Other unexpected errors also return 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(exc)}",
        ) from exc
```

### Post-Fix Failure Check

With PostgreSQL stopped, the API now returns the actual error:

**Before fix:**
```json
{"detail": "Items not found"}
```

**After fix:**
```json
{"detail": "Internal server error: [Errno -2] Name or service not known"}
```

### Agent Investigation (Post-Fix)

The agent's "What went wrong?" investigation now correctly identifies:
- The actual database error message
- The failing database operation (SELECT db-lab-8)
- The root cause (PostgreSQL unreachable)

### Healthy Follow-Up

After restarting PostgreSQL, the system is healthy:

```
$ curl -H "Authorization: Bearer my-secret-api-key" http://localhost:42001/items/
[{"title":"Lab 01 – Products, Architecture & Roles","id":1,...}, ...]
```

The API returns the actual items list with status 200.

### Files Modified

| File | Change |
|------|--------|
| `backend/app/routers/items.py` | Fixed exception handler to return 500 for database errors |
| `nanobot/workspace/skills/observability/SKILL.md` | Added "What went wrong?" investigation workflow |
| `REPORT.md` | Documented Task 4A, 4B, 4C findings |
