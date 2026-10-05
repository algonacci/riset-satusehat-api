"""01 - Generate an OAuth2 access token for the SATUSEHAT API."""

import argparse
import os
import sys
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


DEFAULT_AUTH_URL = (
    "https://api-satusehat-stg.dto.kemkes.go.id/oauth2/v1/accesstoken"
)


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} belum diisi.")
    return value


def generate_token(auth_url: str, client_id: str, client_secret: str) -> dict[str, Any]:
    response = httpx.post(
        auth_url,
        params={"grant_type": "client_credentials"},
        data={"client_id": client_id, "client_secret": client_secret},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30.0,
    )

    try:
        response_data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"SATUSEHAT mengembalikan respons non-JSON (HTTP {response.status_code})."
        ) from exc

    if response.is_error:
        detail = response_data.get("error_description") or response_data.get("error")
        raise RuntimeError(
            f"Gagal generate token (HTTP {response.status_code}): {detail or response_data}"
        )

    return response_data


def mask_secret(value: str) -> str:
    if len(value) <= 12:
        return "***"
    return f"{value[:6]}...{value[-6:]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--show-token",
        action="store_true",
        help="Tampilkan access token secara lengkap (default: dimasking).",
    )
    args = parser.parse_args()

    load_dotenv(Path(__file__).with_name(".env"))

    try:
        client_id = required_env("CLIENT_ID")
        client_secret = required_env("CLIENT_SECRET")
        auth_url = os.getenv("SATUSEHAT_AUTH_URL", DEFAULT_AUTH_URL)
        result = generate_token(auth_url, client_id, client_secret)
    except (ValueError, RuntimeError, httpx.HTTPError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    access_token = result.get("access_token")
    if not access_token:
        print(f"Error: access_token tidak ditemukan dalam respons: {result}", file=sys.stderr)
        return 1

    displayed_token = access_token if args.show_token else mask_secret(access_token)
    print("Token berhasil dibuat.")
    print(f"access_token: {displayed_token}")
    print(f"token_type: {result.get('token_type', '-')}")
    print(f"expires_in: {result.get('expires_in', '-')} detik")

    if not args.show_token:
        print("Jalankan dengan --show-token untuk menampilkan token lengkap.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
