"""02 - Probe the SATUSEHAT sandbox FHIR CapabilityStatement safely."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

from importlib import import_module


DEFAULT_FHIR_BASE_URL = "https://api-satusehat-stg.dto.kemkes.go.id/fhir-r4/v1"
SANDBOX_HOST = "api-satusehat-stg.dto.kemkes.go.id"
RELEVANT_RESOURCES = {
    "Location",
    "Organization",
    "Patient",
    "Practitioner",
    "PractitionerRole",
}


def validate_sandbox_url(value: str) -> str:
    url = value.rstrip("/")
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("SATUSEHAT_FHIR_BASE_URL wajib menggunakan HTTPS.")
    if parsed.hostname != SANDBOX_HOST:
        raise ValueError(
            "Host ditolak: riset ini hanya mengizinkan sandbox SATUSEHAT."
        )
    if parsed.query or parsed.fragment:
        raise ValueError("FHIR base URL tidak boleh memiliki query atau fragment.")
    return url


def validate_auth_url(value: str) -> str:
    url = validate_sandbox_url(value)
    if not urlparse(url).path.endswith("/oauth2/v1/accesstoken"):
        raise ValueError("SATUSEHAT_AUTH_URL bukan endpoint token sandbox yang valid.")
    return url


def operation_outcome_summary(data: dict[str, Any]) -> str | None:
    if data.get("resourceType") != "OperationOutcome":
        return None
    issues = data.get("issue")
    if not isinstance(issues, list) or not issues:
        return "OperationOutcome tanpa detail issue."
    issue = issues[0] if isinstance(issues[0], dict) else {}
    severity = issue.get("severity", "unknown")
    code = issue.get("code", "unknown")
    return f"OperationOutcome severity={severity}, code={code}"


def summarize_capability(data: dict[str, Any]) -> None:
    if data.get("resourceType") != "CapabilityStatement":
        outcome = operation_outcome_summary(data)
        raise RuntimeError(outcome or "Respons bukan FHIR CapabilityStatement.")

    software = data.get("software") if isinstance(data.get("software"), dict) else {}
    implementation = (
        data.get("implementation")
        if isinstance(data.get("implementation"), dict)
        else {}
    )
    resources: set[str] = set()
    interactions: set[str] = set()

    for rest in data.get("rest", []):
        if not isinstance(rest, dict):
            continue
        for resource in rest.get("resource", []):
            if not isinstance(resource, dict):
                continue
            resource_type = resource.get("type")
            if isinstance(resource_type, str):
                resources.add(resource_type)
            for interaction in resource.get("interaction", []):
                if isinstance(interaction, dict) and isinstance(
                    interaction.get("code"), str
                ):
                    interactions.add(interaction["code"])

    print("CapabilityStatement berhasil dibaca.")
    print(f"status: {data.get('status', '-')}")
    print(f"FHIR version: {data.get('fhirVersion', '-')}")
    print(f"software: {software.get('name', '-')}")
    print(f"implementation: {implementation.get('description', '-')}")
    print(f"jumlah resource type: {len(resources)}")
    print(f"interaction terdeklarasi: {', '.join(sorted(interactions)) or '-'}")
    relevant = sorted(resources & RELEVANT_RESOURCES)
    print(f"resource Fase 1 terdeklarasi: {', '.join(relevant) or '-'}")
    print("Catatan: metadata bukan bukti bahwa semua interaction diizinkan credential.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    load_dotenv(Path(__file__).with_name(".env"))

    try:
        base_url = validate_sandbox_url(
            os.getenv("SATUSEHAT_FHIR_BASE_URL", DEFAULT_FHIR_BASE_URL)
        )
        auth = import_module("01_generate_token")
        token_data = auth.generate_token(
            validate_auth_url(
                os.getenv("SATUSEHAT_AUTH_URL", auth.DEFAULT_AUTH_URL)
            ),
            auth.required_env("CLIENT_ID"),
            auth.required_env("CLIENT_SECRET"),
        )
        access_token = token_data.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise RuntimeError("Respons autentikasi tidak memiliki access_token.")

        response = httpx.get(
            f"{base_url}/metadata",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/fhir+json",
            },
            timeout=30.0,
        )
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Endpoint metadata memberi respons non-JSON (HTTP {response.status_code})."
            ) from exc

        if response.is_error:
            detail = operation_outcome_summary(data)
            raise RuntimeError(
                f"Endpoint metadata gagal (HTTP {response.status_code})"
                f"{f': {detail}' if detail else '.'}"
            )
        print("=== RAW RESPONSE (SANDBOX) ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=== SUMMARY ===")
        summarize_capability(data)
    except (ValueError, RuntimeError, httpx.HTTPError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
