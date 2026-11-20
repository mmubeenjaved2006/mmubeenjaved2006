
"""Fetch real GitHub contributions using the GitHub GraphQL API."""

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER = "mmubeenjaved2006"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "Missing GitHub token. Set GH_TOKEN in GitHub Actions."
    )

today = datetime.now(timezone.utc)
start = today - timedelta(days=365)

query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

payload = json.dumps({
    "query": query,
    "variables": {
        "login": USER,
        "from": start.isoformat(),
        "to": today.isoformat()
    }
}).encode("utf-8")

request = Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mubeen-GitHub-Profile"
    },
    method="POST"
)

try:
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
except HTTPError as error:
    details = error.read().decode("utf-8", errors="replace")
    raise RuntimeError(
        f"GitHub API HTTP {error.code}: {details}"
    ) from error
except URLError as error:
    raise RuntimeError(
        f"Could not connect to GitHub API: {error}"
    ) from error

if result.get("errors"):
    raise RuntimeError(
        f"GitHub GraphQL errors: {result['errors']}"
    )

user = (result.get("data") or {}).get("user")
if not user:
    raise RuntimeError("GitHub user not found.")

weeks = (
    user["contributionsCollection"]
    ["contributionCalendar"]["weeks"]
)

days = [
    {
        "date": day["date"],
        "count": day["contributionCount"]
    }
    for week in weeks
    for day in week["contributionDays"]
]

days.sort(key=lambda item: item["date"])

if len(days) < 300:
    raise RuntimeError(
        f"Only received {len(days)} contribution days."
    )

output = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "contributions.json"
)

output.parent.mkdir(parents=True, exist_ok=True)

output.write_text(
    json.dumps(
        {"user": USER, "days": days},
        indent=2
    ) + "\n",
    encoding="utf-8"
)

print(f"Successfully fetched {len(days)} contribution days.")
print(f"Saved to: {output}")
