"""04 - Search sandbox Locations scoped to ORGANIZATION_ID."""
import argparse, sys
from satusehat_client import get, print_raw, require_bundle, required_env

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.parse_args()
    try:
        organization_id = required_env("ORGANIZATION_ID")
        data, response = get("Location", {"organization": organization_id, "_count": "10"})
        resources = require_bundle(data, "Location")
        print_raw(data)
        print("Pencarian Location berhasil.")
        print(f"HTTP: {response.status_code}")
        print(f"total: {data.get('total', len(resources))}")
        print(f"hasil halaman ini: {len(resources)}")
        print(f"memiliki next page: {'ya' if any(x.get('relation') == 'next' for x in data.get('link', [])) else 'tidak'}")
        print("Detail Location tidak diulang dalam summary.")
        return 0
    except (ValueError, RuntimeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
