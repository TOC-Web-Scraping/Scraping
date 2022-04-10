import requests
import re
import time
import json

teams = []
f = open("teams.txt", "r")
teams_url = f.readlines()

'''
{
    "name": "",
    "location": "",
    "logo": "",
    "region": "",
}
'''
regex = {
    "name": r'<h1 id="firstHeading".*?"auto">(.*?)<.*?</h1>',
    "location": r'Location.*?\n.*?title="(.*?)"',
    "logo": r'infobox-image lightmode.*?src="(.*?)"',
    "region": r'Region.*?\n.*?title="(.*?)"',
}

for team_url in teams_url:
    url = "https://liquipedia.net"+team_url.strip()
    r = requests.get(url)
    content = r.text
    name = re.findall(regex["name"], content)
    location = re.findall(regex["location"], content)
    logo = re.findall(regex["logo"], content)
    region = re.findall(regex["region"], content)

    team = {
        "name": name[0] if len(name) > 0 else "",
        "location": location[0] if len(location) > 0 else "",
        "logo": logo[0] if len(logo) > 0 else "",
        "region": region[0] if len(region) > 0 else "",
    }
    print(team)
    teams.append(team)
    time.sleep(3)

with open('teams.json', 'w', encoding='utf-8') as j:
    json.dump(teams, j, ensure_ascii=False, indent=4)
