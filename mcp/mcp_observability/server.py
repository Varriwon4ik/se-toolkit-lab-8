"""Stdio MCP server exposing VictoriaLogs and VictoriaTraces as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_VICTORIALOGS_URL: str = ""
_VICTORIATRACES_URL: str = ""


def _get_victorialogs_url() -> str:
    """Get VictoriaLogs base URL from environment."""
    return os.environ.get("VICTORIALOGS_URL", "http://localhost:9428")


def _get_victoriatraces_url() -> str:
    """Get VictoriaTraces base URL from environment."""
    return os.environ.get("VICTORIATRACES_URL", "http://localhost:10428")


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _LogsSearchArgs(BaseModel):
    query: str = Field(
        default="*",
        description="LogsQL query string. Use '*' for all logs. Examples: 'error', 'severity:ERROR', '_stream:{service=\"backend\"} AND level:error'",
    )
    limit: int = Field(default=10, ge=1, le=1000, description="Max entries to return (1-1000)")
    start: str = Field(
        default="",
        description="Start time (optional). Format: Unix timestamp or relative like '1h', '30m', '1d'",
    )
    end: str = Field(
        default="",
        description="End time (optional). Format: Unix timestamp or relative like '1h', '30m', '1d'",
    )


class _LogsErrorCountArgs(BaseModel):
    start: str = Field(
        default="1h",
        description="Start time relative to now. Examples: '1h', '30m', '1d', '7d'",
    )


class _TracesListArgs(BaseModel):
    service: str = Field(
        default="",
        description="Service name to filter traces (e.g., 'Learning Management Service')",
    )
    operation: str = Field(
        default="",
        description="Operation name to filter (optional)",
    )
    limit: int = Field(default=5, ge=1, le=100, description="Max traces to return (1-100)")


class _TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _text(data: Any) -> list[TextContent]:
    """Serialize data to JSON text."""
    if isinstance(data, (dict, list)):
        content = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        content = str(data)
    return [TextContent(type="text", text=content)]


async def _http_get(url: str, params: dict[str, Any] | None = None) -> Any:
    """Make an async HTTP GET request."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        # Check if response is NDJSON (VictoriaLogs returns newline-delimited JSON)
        content = response.text.strip()
        if "\n" in content:
            # Parse NDJSON
            results = []
            for line in content.split("\n"):
                line = line.strip()
                if line:
                    results.append(json.loads(line))
            return results
        return response.json()


# ---------------------------------------------------------------------------
# Log tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearchArgs) -> list[TextContent]:
    """Search logs using VictoriaLogs LogsQL query."""
    url = f"{_get_victorialogs_url()}/select/logsql/query"
    params = {
        "query": args.query,
        "limit": args.limit,
    }
    if args.start:
        params["start"] = args.start
    if args.end:
        params["end"] = args.end

    try:
        result = await _http_get(url, params)
        # VictoriaLogs returns a list of log entries
        if isinstance(result, list):
            return _text({"entries": result, "count": len(result)})
        return _text(result)
    except httpx.ConnectError as e:
        return _text({"error": f"Cannot connect to VictoriaLogs: {e}"})
    except httpx.HTTPStatusError as e:
        return _text({"error": f"HTTP error: {e.response.status_code} - {e.response.text}"})
    except Exception as e:
        return _text({"error": f"Error searching logs: {type(e).__name__}: {e}"})


async def _logs_error_count(args: _LogsErrorCountArgs) -> list[TextContent]:
    """Count errors per service over a time window."""
    # Query VictoriaLogs for ERROR severity logs with time filter
    url = f"{_get_victorialogs_url()}/select/logsql/query"
    # Use simple query with time range - VictoriaLogs handles start parameter
    query = 'severity:ERROR'
    params = {"query": query, "limit": 1000, "start": args.start}

    try:
        result = await _http_get(url, params)
        # Count errors by service from the raw log entries
        errors_by_service = {}
        total = 0
        if isinstance(result, list):
            for entry in result:
                service_name = entry.get("service.name", "unknown")
                errors_by_service[service_name] = errors_by_service.get(service_name, 0) + 1
                total += 1

        # Convert to list format
        by_service = [{"service": svc, "error_count": cnt} for svc, cnt in errors_by_service.items()]
        by_service.sort(key=lambda x: x["error_count"], reverse=True)

        return _text({
            "time_window": args.start,
            "total_errors": total,
            "by_service": by_service,
        })
    except httpx.ConnectError as e:
        return _text({"error": f"Cannot connect to VictoriaLogs: {e}"})
    except Exception as e:
        return _text({"error": f"Error counting errors: {type(e).__name__}: {e}"})


# ---------------------------------------------------------------------------
# Trace tool handlers
# ---------------------------------------------------------------------------


async def _traces_list(args: _TracesListArgs) -> list[TextContent]:
    """List recent traces for a service."""
    url = f"{_get_victoriatraces_url()}/select/jaeger/api/traces"
    params = {"limit": args.limit}
    if args.service:
        params["service"] = args.service
    if args.operation:
        params["operation"] = args.operation

    try:
        result = await _http_get(url, params)
        # Jaeger API returns {"data": [traces]}
        if isinstance(result, dict) and "data" in result:
            traces = result["data"]
            # Simplify trace summary
            trace_summaries = []
            for trace in traces[: args.limit]:
                trace_id = trace.get("traceID", trace.get("id", "unknown"))
                spans = trace.get("spans", [])
                span_count = len(spans)
                # Get the earliest span start time
                start_time = min((s.get("startTime", 0) for s in spans), default=0) if spans else 0
                # Check for errors
                has_error = any(
                    any(t.get("key") == "error" for t in s.get("tags", [])) for s in spans
                )
                trace_summaries.append({
                    "trace_id": trace_id,
                    "span_count": span_count,
                    "start_time": start_time,
                    "has_error": has_error,
                    "services": list(set(
                        trace.get("processes", {}).get(s.get("processID", ""), {}).get("serviceName", "unknown")
                        for s in spans
                    )),
                })
            return _text({"traces": trace_summaries, "count": len(trace_summaries)})
        return _text(result)
    except httpx.ConnectError as e:
        return _text({"error": f"Cannot connect to VictoriaTraces: {e}"})
    except httpx.HTTPStatusError as e:
        return _text({"error": f"HTTP error: {e.response.status_code} - {e.response.text}"})
    except Exception as e:
        return _text({"error": f"Error listing traces: {type(e).__name__}: {e}"})


async def _traces_get(args: _TracesGetArgs) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    url = f"{_get_victoriatraces_url()}/select/jaeger/api/traces/{args.trace_id}"

    try:
        result = await _http_get(url)
        # Jaeger API returns {"data": [trace]}
        if isinstance(result, dict) and "data" in result:
            traces = result["data"]
            if traces:
                trace = traces[0]
                # Simplify trace details
                spans = trace.get("spans", [])
                span_details = []
                for span in spans:
                    tags = {t.get("key"): t.get("value") for t in span.get("tags", [])}
                    span_details.append({
                        "span_id": span.get("spanID"),
                        "operation": span.get("operationName"),
                        "duration_us": span.get("duration"),
                        "start_time": span.get("startTime"),
                        "tags": tags,
                        "has_error": "error" in tags,
                    })
                # Sort by start time
                span_details.sort(key=lambda s: s["start_time"] or 0)
                return _text({
                    "trace_id": trace.get("traceID"),
                    "span_count": len(spans),
                    "spans": span_details,
                })
        return _text({"error": f"Trace {args.trace_id} not found"})
    except httpx.ConnectError as e:
        return _text({"error": f"Cannot connect to VictoriaTraces: {e}"})
    except httpx.HTTPStatusError as e:
        return _text({"error": f"HTTP error: {e.response.status_code} - {e.response.text}"})
    except Exception as e:
        return _text({"error": f"Error fetching trace: {type(e).__name__}: {e}"})


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (model, handler, Tool(name=name, description=description, inputSchema=schema))


_register(
    "logs_search",
    "Search logs in VictoriaLogs using LogsQL. Use query='*' for all logs, 'severity:ERROR' for errors, or LogsQL like '_stream:{service=\"backend\"}'.",
    _LogsSearchArgs,
    _logs_search,
)

_register(
    "logs_error_count",
    "Count errors per service over a time window. Returns total error count and breakdown by service.",
    _LogsErrorCountArgs,
    _logs_error_count,
)

_register(
    "traces_list",
    "List recent traces. Filter by service name and operation. Returns trace summaries with error status.",
    _TracesListArgs,
    _traces_list,
)

_register(
    "traces_get",
    "Fetch a specific trace by ID. Returns span hierarchy with timing and error details.",
    _TracesGetArgs,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
