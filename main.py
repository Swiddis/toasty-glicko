import glicko2
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json

USER, LINK, DIFFICULTY = "Discord Username", "Video Link", "Difficulty"

with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Set up credentials
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)


spreadsheet = client.open_by_key(config["spreadsheet_key"])

input_sheet = spreadsheet.get_worksheet(0)
videos_sheet = spreadsheet.get_worksheet(1)
players_sheet = spreadsheet.get_worksheet(2)

data = input_sheet.get_all_records()

players = {player[USER]: glicko2.Player() for player in data}
videos = {video[LINK]: glicko2.Player() for video in data}

for row in data:
    player_name = row[USER]
    video_name = row[LINK]
    difficulty = row[DIFFICULTY]

    score = {
        "Too Easy": 1.0,
        "About Right": 0.5,
        "Too Hard": 0.0,
    }[difficulty]

    player = players[player_name]
    video = videos[video_name]

    pr, prd = player.getRating(), player.getRd()
    player.update_player([video.getRating()], [video.getRd()], [score])
    video.update_player([pr], [prd], [1.0 - score])

players = [[name, p.getRating(), p.getRd()] for name, p in players.items()]
videos = [[link, v.getRating(), v.getRd()] for link, v in videos.items()]

pprint(players)

players.sort(key=lambda x: x[1], reverse=True)
videos.sort(key=lambda x: x[1])

players_sheet.update(
    range_name="A2:B" + str(len(players) + 2),
    values=[[p[0], round(p[1])] for p in players],
    value_input_option="USER_ENTERED",
)

videos_sheet.update(
    range_name="A2:C" + str(len(videos) + 2),
    values=[[v[0], round(v[1]), round(1.0 - v[2] / 300, 2)] for v in videos],
    value_input_option="USER_ENTERED",
)

print("Ratings Updated!")
