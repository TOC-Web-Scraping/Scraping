import requests
import re
import time
import json


def getTeamsURL():
    url = "https://liquipedia.net/valorant/Portal:Teams"
    r = requests.get(url)
    content = r.text
    result = re.findall(
        r'<tr>.*?<span class="team-template-text"><a href="(.*?)".*?</tr>', content)
    return result


def getTeamData(url):
    '''
    [
        {
            "name": "",
            "location": "",
            "logo": "",
            "region": "",
        },...
    ]

    '''
    regex = {
        "name": r'<h1 id="firstHeading".*?"auto">(.*?)<.*?</h1>',
        "location": r'Location.*?\n.*?title="(.*?)"',
        "logo": r'infobox-image lightmode.*?src="(.*?)"',
        "region": r'Region.*?\n.*?title="(.*?)"',
    }

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
    return team


if __name__ == "__main__":
    teams = []
    teamsURL = getTeamsURL()
    count = 0
    for url in teamsURL:
        url = "https://liquipedia.net" + url
        teamData = getTeamData(url)
        print(teamData)
        teams.append(teamData)
        if count == 10:
            break
        count += 1

    with open('teams.json', 'w', encoding='utf-8') as j:
        json.dump(teams, j, ensure_ascii=False, indent=4)
