"""
RoadmapPilot — an MCP server that lets an AI agent manage a product roadmap.

Exposes tools to add features, update their status, prioritize them,
list the backlog, and summarize where things stand — the core loop of
product roadmap management, but operable by an LLM through natural
conversation instead of a UI.
"""

import json
import os
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("roadmap-pilot")

DATA_FILE = os.path.join(os.path.dirname(__file__), "roadmap_data.json")
VALID_STATUSES = ["backlog", "planned", "in_progress", "shipped"]
VALID_PRIORITIES = ["low", "medium", "high"]


def _load() -> dict:
    if not os.path.exists(DATA_FILE):
        return {"features": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _next_id(data: dict) -> int:
    if not data["features"]:
        return 1
    return max(f["id"] for f in data["features"]) + 1


@mcp.tool()
async def add_feature(title: str, description: str = "", priority: str = "medium") -> str:
    """Add a new feature to the product roadmap.

    Args:
        title: Short name of the feature (e.g. "Dark mode").
        description: Optional longer description of what it does or why it matters.
        priority: One of "low", "medium", "high". Defaults to "medium".
    """
    if priority not in VALID_PRIORITIES:
        return f"Invalid priority '{priority}'. Must be one of: {', '.join(VALID_PRIORITIES)}."

    data = _load()
    feature = {
        "id": _next_id(data),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "backlog",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data["features"].append(feature)
    _save(data)
    return f"Added feature #{feature['id']}: '{title}' (priority: {priority}, status: backlog)."


@mcp.tool()
async def update_status(feature_id: int, status: str) -> str:
    """Update the status of a feature.

    Args:
        feature_id: The numeric ID of the feature (from list_features).
        status: One of "backlog", "planned", "in_progress", "shipped".
    """
    if status not in VALID_STATUSES:
        return f"Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}."

    data = _load()
    for f in data["features"]:
        if f["id"] == feature_id:
            old_status = f["status"]
            f["status"] = status
            _save(data)
            return f"Feature #{feature_id} ('{f['title']}') moved from {old_status} → {status}."
    return f"No feature found with ID {feature_id}."


@mcp.tool()
async def prioritize_feature(feature_id: int, priority: str) -> str:
    """Change the priority of a feature.

    Args:
        feature_id: The numeric ID of the feature (from list_features).
        priority: One of "low", "medium", "high".
    """
    if priority not in VALID_PRIORITIES:
        return f"Invalid priority '{priority}'. Must be one of: {', '.join(VALID_PRIORITIES)}."

    data = _load()
    for f in data["features"]:
        if f["id"] == feature_id:
            old_priority = f["priority"]
            f["priority"] = priority
            _save(data)
            return f"Feature #{feature_id} ('{f['title']}') priority changed from {old_priority} → {priority}."
    return f"No feature found with ID {feature_id}."


@mcp.tool()
async def list_features(status: str = "", priority: str = "") -> str:
    """List features on the roadmap, optionally filtered by status and/or priority.

    Args:
        status: Optional filter — one of "backlog", "planned", "in_progress", "shipped".
        priority: Optional filter — one of "low", "medium", "high".
    """
    data = _load()
    features = data["features"]

    if status:
        features = [f for f in features if f["status"] == status]
    if priority:
        features = [f for f in features if f["priority"] == priority]

    if not features:
        return "No features match that filter."

    lines = []
    for f in sorted(features, key=lambda x: x["id"]):
        lines.append(
            f"#{f['id']} [{f['status']}] [{f['priority']} priority] {f['title']}"
            + (f" — {f['description']}" if f["description"] else "")
        )
    return "\n".join(lines)


@mcp.tool()
async def roadmap_summary() -> str:
    """Get a high-level summary of the roadmap: counts by status and priority."""
    data = _load()
    features = data["features"]

    if not features:
        return "The roadmap is empty. Add a feature with add_feature()."

    by_status = {}
    by_priority = {}
    for f in features:
        by_status[f["status"]] = by_status.get(f["status"], 0) + 1
        by_priority[f["priority"]] = by_priority.get(f["priority"], 0) + 1

    lines = [f"Total features: {len(features)}", "", "By status:"]
    for s in VALID_STATUSES:
        lines.append(f"  {s}: {by_status.get(s, 0)}")
    lines.append("")
    lines.append("By priority:")
    for p in VALID_PRIORITIES:
        lines.append(f"  {p}: {by_priority.get(p, 0)}")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
