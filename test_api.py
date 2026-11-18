import requests

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

params = {
    "week": 11,
    "seasontype": 2,
    "season": 2026
}

r = requests.get(url, params=params)
data = r.json()

for event in data['events']:
    print(event['name'])

for event in data["events"]:
    competitors = event["competitions"][0]["competitors"]

    away_team = ""
    home_team = ""

    for competitor in competitors:
        if competitor["homeAway"] == "away":
            away_team = competitor["team"]["displayName"]
        else:
            home_team = competitor["team"]["displayName"]

    print(f"{away_team} @ {home_team}")



for event in data["events"]:
    competitors = event["competitions"][0]["competitors"]

    for competitor in competitors:
        team = competitor["team"]

        name = team["displayName"]
        logo = team.get("logo")
        home_away = competitor["homeAway"]

        records = competitor.get("records", [])
        record = records[0]["summary"] if records else "N/A"

        print(name, record, logo, home_away)