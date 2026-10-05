"""11 - Get one sandbox PractitionerRole by explicit logical ID."""
import argparse, sys
from satusehat_client import get, print_raw, require_resource, safe_summary, validate_resource_id

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("role_id")
    args = parser.parse_args(); args.role_id = validate_resource_id(args.role_id)
    try:
        data, _ = get(f"PractitionerRole/{args.role_id}"); require_resource(data, "PractitionerRole", args.role_id)
        print_raw(data)
        print("PractitionerRole berhasil dibaca."); print(safe_summary(data))
        print(f"jumlah location reference: {len(data.get('location', [])) if isinstance(data.get('location'), list) else 0}")
        print("Detail reference tidak diulang dalam summary."); return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
