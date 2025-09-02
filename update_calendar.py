import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.football.org.il/team-details/team-games/?team_id=8203&season_id=27"

resp = requests.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

games = []
for row in soup.select("table tbody tr"):
    cols = [c.get_text(strip=True) for c in row.find_all("td")]
    if len(cols) >= 3:
        date_str = cols[0]
        match = " - ".join(cols[1:3])
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y%m%d")
        except:
            continue
        games.append((date, match))

ics = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Nes Ziona Auto Calendar//EN\n"
for date, match in games:
    ics += "BEGIN:VEVENT\n"
    ics += f"SUMMARY:{match}\n"
    ics += f"DTSTART;VALUE=DATE:{date}\n"
    ics += f"DTEND;VALUE=DATE:{date}\n"
    ics += f"DESCRIPTION:משחק ליגה ג' מרכז – עונת 2025/26\n"
    ics += "END:VEVENT\n"
ics += "END:VCALENDAR"

# שמירה ל-docs/
import os
os.makedirs("docs", exist_ok=True)
with open("docs/nes_ziona.ics", "w", encoding="utf-8") as f:
    f.write(ics)
