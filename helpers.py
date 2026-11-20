import requests
from datetime import datetime, timezone


ESPN_SCOREBOARD_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
)


def current_nfl_season():
    now = datetime.now(timezone.utc)

    if now.month >= 8:
        return now.year

    return now.year - 1


def get_scoreboard(season, week=None):
    params = {
        "season": season,
        "seasontype": 2
    }

    if week is not None:
        params["week"] = week

    response = requests.get(
        ESPN_SCOREBOARD_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_current_nfl_week(season):
    data = get_scoreboard(season)

    return data["week"]["number"]


def is_game_locked(event, now=None):
    if now is None:
        now = datetime.now(timezone.utc)

    kickoff = datetime.fromisoformat(
        event["date"].replace("Z", "+00:00")
    )

    return (
        now >= kickoff
        or event["status"]["type"]["state"] == "post"
    )
