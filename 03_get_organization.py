"""03 - Read the credential's SATUSEHAT sandbox Organization safely."""

import argparse
import json
import os
import re
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


ID_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,64}$")


def validate_resource_id(value: str) -> str:
    if not ID_PATTERN.fullmatch(value):
        raise ValueError("ORGANIZATION_ID memiliki format resource ID yang tidak valid.")
    return value


def outcome_summary(data: dict[str, Any]) -> str:
    issues = data.get("issue")
    if not isinstance(issues, list) or not issues or not isinstance(issues[0], dict):
        return "OperationOutcome tanpa detail issue"
    return (
        f"OperationOutcome severity={issues[0].get('severity', 'unknown')}, "
        f"code={issues[0].get('code', 'unknown')}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    load_dotenv(Path(__file__).with_name(".env"))

    try:
        common = import_module("02_get_capability_statement")
        auth = import_module("01_generate_token")
        organization_id = validate_resource_id(auth.required_env("ORGANIZATION_ID"))
        base_url = common.validate_sandbox_url(
            os.getenv("SATUSEHAT_FHIR_BASE_URL", common.DEFAULT_FHIR_BASE_URL)
        )
        auth_url = common.validate_auth_url(
            os.getenv("SATUSEHAT_AUTH_URL", auth.DEFAULT_AUTH_URL)
        )
        token_data = auth.generate_token(
            auth_url,
            auth.required_env("CLIENT_ID"),
            auth.required_env("CLIENT_SECRET"),
        )
        token = token_data.get("access_token")
        if not isinstance(token, str) or not token:
            raise RuntimeError("Respons autentikasi tidak memiliki access_token.")

        response = httpx.get(
            f"{base_url}/Organization/{organization_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/fhir+json",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Organization endpoint memberi respons non-JSON "
                f"(HTTP {response.status_code})."
            ) from exc

        if response.is_error:
            detail = outcome_summary(data) if data.get("resourceType") == "OperationOutcome" else ""
            raise RuntimeError(
                f"GET Organization gagal (HTTP {response.status_code})"
                f"{f': {detail}' if detail else '.'}"
            )
        if data.get("resourceType") != "Organization":
            raise RuntimeError("Respons sukses bukan resource Organization.")
        if data.get("id") != organization_id:
            raise RuntimeError("ID Organization pada respons tidak sesuai request.")

        print("=== RAW RESPONSE (SANDBOX) ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=== SUMMARY ===")
        identifiers = data.get("identifier")
        identifier_count = len(identifiers) if isinstance(identifiers, list) else 0
        endpoint_count = len(data.get("endpoint", [])) if isinstance(data.get("endpoint"), list) else 0
        print("Organization berhasil dibaca.")
        print("resourceType: Organization")
        print("id cocok dengan ORGANIZATION_ID: ya")
        print(f"active: {data.get('active', '-')}")
        print(f"jumlah identifier: {identifier_count}")
        print(f"memiliki partOf: {'ya' if isinstance(data.get('partOf'), dict) else 'tidak'}")
        print(f"jumlah endpoint reference: {endpoint_count}")
        print("Nama, identifier, alamat, dan kontak tidak diulang dalam summary.")
    except (ValueError, RuntimeError, httpx.HTTPError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
