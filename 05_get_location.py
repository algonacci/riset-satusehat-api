"""05 - Get one sandbox Location by explicit logical ID."""
import argparse, sys
from satusehat_client import get, print_raw, require_resource, safe_summary, validate_resource_id

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("location_id")
    args = parser.parse_args(); args.location_id = validate_resource_id(args.location_id)
    try:
        data, _ = get(f"Location/{args.location_id}")
        require_resource(data, "Location", args.location_id)
        print_raw(data)
        print("Location berhasil dibaca."); print(safe_summary(data))
        print(f"status: {data.get('status', '-')}")
        print("Detail Location tidak diulang dalam summary."); return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
