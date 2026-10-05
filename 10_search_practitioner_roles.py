"""10 - Search PractitionerRole by Practitioner and credential Organization."""
import argparse, sys
from satusehat_client import get, print_raw, require_bundle, required_env, validate_resource_id

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("practitioner_id")
    args = parser.parse_args(); args.practitioner_id = validate_resource_id(args.practitioner_id)
    try:
        organization_id = required_env("ORGANIZATION_ID")
        data, _ = get("PractitionerRole", {"practitioner": args.practitioner_id, "organization": organization_id, "_count": "10"})
        resources = require_bundle(data, "PractitionerRole")
        print_raw(data)
        print("Pencarian PractitionerRole berhasil."); print(f"total: {data.get('total', len(resources))}")
        print(f"hasil halaman ini: {len(resources)}")
        print("Detail PractitionerRole tidak diulang dalam summary."); return 0
    except (ValueError, RuntimeError) as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
