"""
test_predict.py

Simple smoke test for the /predict endpoint. Sends two real reservations
from the Test set (Section 12 of the workbook) -- one with near-certain
cancellation (deposit_type=non_refund) and one ordinary reservation -- and
checks that the service responds with a sensible prediction for each.

Requires the service to be running first:
    Windows:      pipenv run waitress-serve --listen=0.0.0.0:9696 predict:app
    Linux/Docker: gunicorn --bind=0.0.0.0:9696 predict:app

Usage:
    pipenv run python test_predict.py
"""

import json
import requests

URL = "http://localhost:9696/predict"


def load_payload(path):
    with open(path, "r") as f:
        return json.load(f)


def run_case(name, payload_path, expected_will_cancel):
    payload = load_payload(payload_path)
    response = requests.post(URL, json=payload)
    response.raise_for_status()
    result = response.json()

    print(f"--- {name} ---")
    print(json.dumps(result, indent=2))

    status = "OK" if result["will_cancel"] == expected_will_cancel else "UNEXPECTED"
    print(f"Expected will_cancel={expected_will_cancel} -> {status}")
    print()


if __name__ == "__main__":
    run_case("Sample: likely to cancel", "tests/sample_will_cancel.json", expected_will_cancel=True)
    run_case("Sample: likely to stay", "tests/sample_wont_cancel.json", expected_will_cancel=False)