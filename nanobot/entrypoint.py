#!/usr/bin/env python3
"""Entrypoint for nanobot Docker deployment.

Resolves environment variables into config.json at runtime, then launches nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> str:
    """Read config.json, inject env vars, write resolved config, return path."""
    config_path = Path(__file__).parent / "config.json"
    resolved_path = Path(__file__).parent / "config.resolved.json"
    workspace_path = Path(__file__).parent / "workspace"

    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider config from env vars
    llm_api_key = os.environ.get("LLM_API_KEY", "")
    llm_base_url = os.environ.get("LLM_API_BASE_URL", "")
    llm_model = os.environ.get("LLM_API_MODEL", "")

    if "providers" in config and "custom" in config["providers"]:
        if llm_api_key:
            config["providers"]["custom"]["apiKey"] = llm_api_key
        if llm_base_url:
            config["providers"]["custom"]["apiBase"] = llm_base_url

    if "agents" in config and "defaults" in config["agents"]:
        if llm_model:
            config["agents"]["defaults"]["model"] = llm_model

    # Resolve gateway config from env vars
    gateway_address = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")

    config["gateway"] = {
        "host": gateway_address,
        "port": int(gateway_port),
    }

    # Resolve webchat channel config from env vars
    webchat_address = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "")

    if "channels" not in config:
        config["channels"] = {}

    config["channels"]["webchat"] = {
        "enabled": True,
        "host": webchat_address,
        "port": int(webchat_port),
        "allow_from": ["*"],
        "access_key": access_key,
    }

    # Resolve MCP server env vars (backend URL and API key)
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY", "")

    if "tools" in config and "mcpServers" in config["tools"] and "lms" in config["tools"]["mcpServers"]:
        if "env" not in config["tools"]["mcpServers"]["lms"]:
            config["tools"]["mcpServers"]["lms"]["env"] = {}
        if lms_backend_url:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(resolved_path), str(workspace_path)


if __name__ == "__main__":
    resolved_config, workspace = resolve_config()
    print(f"Starting nanobot gateway with resolved config: {resolved_config}")
    print(f"Workspace: {workspace}")
    sys.stdout.flush()

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace])
