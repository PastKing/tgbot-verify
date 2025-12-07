import json
import os
import sys
from typing import List

import requests


ACCOUNT_ID = os.getenv("ACCOUNT_ID", "32bfda....b22")
TOKEN = os.getenv(
    "TOKEN",
    "eyYmQwZSI.....Y6vBlVVKNmBmY",
)


def prompt_emails() -> List[str]:
    raw_value = input("Enter emails to invite (comma or semicolon separated): ").strip()
    emails = [
        email.strip()
        for email in raw_value.replace(";", ",").split(",")
        if email.strip()
    ]

    if not emails:
        print("No valid email provided, exiting.")
        sys.exit(1)

    return emails


def build_headers() -> dict:
    return {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "accept-encoding": "gzip, deflate, br, zstd",
        "referer": "https://chatgpt.com/admin/members",
        "authorization": f"Bearer {TOKEN}",
        "chatgpt-account-id": ACCOUNT_ID,
        "content-type": "application/json",
    }


def send_invites(email_addresses: List[str]) -> None:
    url = f"https://chatgpt.com/backend-api/accounts/{ACCOUNT_ID}/invites"
    payload = {
        "email_addresses": email_addresses,
        "role": "standard-user",
        "resend_emails": False,
    }

    try:
        response = requests.post(url, headers=build_headers(), json=payload, timeout=20)
    except requests.exceptions.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(1)

    if response.ok:
        print("Invite succeeded, response:")
        try:
            print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        except ValueError:
            print(response.text)
    else:
        print(f"Request failed, status code: {response.status_code}")
        print(response.text)


def main() -> None:
    if not ACCOUNT_ID or not TOKEN:
        print("Missing ACCOUNT_ID or TOKEN; cannot send invites.")
        sys.exit(1)

    emails = prompt_emails()
    send_invites(emails)


if __name__ == "__main__":
    main()
