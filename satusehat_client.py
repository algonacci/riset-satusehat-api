"""Shared, sandbox-only helpers for SATUSEHAT read-only research scripts."""

import os
import re
import json
from importlib import import_module
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


def load_config() -> tuple[str, str]:
    load_dotenv(Path(__file__).with_name(".env"))
    common = import_module("02_get_capability_statement")
    auth = import_module("01_generate_token")
    base_url = common.validate_sandbox_url(
        os.getenv("SATUSEHAT_FHIR_BASE_URL", common.DEFAULT_FHIR_BASE_URL)
    )
    auth_url = common.validate_auth_url(
        os.getenv("SATUSEHAT_AUTH_URL", auth.DEFAULT_AUTH_URL)
    )
    token_data = auth.generate_token(
        auth_url, auth.required_env("CLIENT_ID"), auth.required_env("CLIENT_SECRET")
    )
    token = token_data.get("access_token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("Respons autentikasi tidak memiliki access_token.")
    return base_url, token


def required_env(name: str) -> str:
    load_dotenv(Path(__file__).with_name(".env"))
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} belum diisi.")
    return value


def get_with_token(
    base_url: str,
    token: str,
    resource_path: str,
    params: dict[str, str] | None = None,
) -> tuple[dict[str, Any], httpx.Response]:
    response = httpx.get(
        f"{base_url}/{resource_path.lstrip('/')}",
        params=params,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/fhir+json"},
        timeout=30.0,
    )
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Respons non-JSON (HTTP {response.status_code}).") from exc
    if response.is_error:
        detail = ""
        if data.get("resourceType") == "OperationOutcome":
            issues = data.get("issue", [])
            if issues and isinstance(issues[0], dict):
                detail = f", code={issues[0].get('code', 'unknown')}"
        raise RuntimeError(f"Request gagal (HTTP {response.status_code}{detail}).")
    return data, response


def get(resource_path: str, params: dict[str, str] | None = None) -> tuple[dict[str, Any], httpx.Response]:
    base_url, token = load_config()
    return get_with_token(base_url, token, resource_path, params)


def require_bundle(data: dict[str, Any], expected_type: str) -> list[dict[str, Any]]:
    if data.get("resourceType") != "Bundle" or data.get("type") != "searchset":
        raise RuntimeError("Respons bukan FHIR searchset Bundle.")
    resources = []
    for entry in data.get("entry", []):
        resource = entry.get("resource") if isinstance(entry, dict) else None
        if isinstance(resource, dict) and resource.get("resourceType") == expected_type:
            resources.append(resource)
    return resources


def require_resource(data: dict[str, Any], expected_type: str, expected_id: str) -> None:
    if data.get("resourceType") != expected_type or data.get("id") != expected_id:
        raise RuntimeError(f"Respons bukan {expected_type} yang diminta.")


def safe_summary(resource: dict[str, Any]) -> str:
    return (
        f"active={resource.get('active', '-')}, "
        f"identifier_count={len(resource.get('identifier', [])) if isinstance(resource.get('identifier'), list) else 0}"
    )
RESOURCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,64}$")


def print_raw(data: dict[str, Any]) -> None:
    """Print a sandbox response as formatted JSON without auth headers."""
    print("=== RAW RESPONSE (SANDBOX) ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("=== SUMMARY ===")


def validate_resource_id(value: str) -> str:
    if not RESOURCE_ID_PATTERN.fullmatch(value):
        raise ValueError("Format logical ID FHIR tidak valid.")
    return value
