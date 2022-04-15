import requests
import re
import time
import json
import urllib.request

baseURL = "https://liquipedia.net"


def getTeamsURL():
    url = "https://liquipedia.net/valorant/Portal:Teams"
    r = requests.get(url)
    content = r.text
    result = re.findall(
        r'<tr>.*?<span class="team-template-text"><a href="(.*?)".*?</tr>', content)
    return result


def getAchievements(data):
    achievements = re.findall(r'<tr>.*?<td(.*?)</tr>', data, re.DOTALL)
    achievements = achievements if len(achievements) > 0 else []
    return achievements


def getAchievement(data):
    '''
    {
        "date": "",
        "placement": "",
        "tournament": "",
        "prize": "",
    }
    '''
    regex = {
        "date": r'\d\d\d\d-\d\d-\d\d',
        "placement": r'<td class="placement-text".*?<b.*?>(.*?)<',
        "tournament": r'<td style="text-align:left;">.*?>(.*?)<',
        "prize": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td>(.*?)\n',
    }

    date = re.findall(regex["date"], data)
    placement = re.findall(regex["placement"], data)
    tournament = re.findall(regex["tournament"], data)
    prize = re.findall(regex["prize"], data, re.DOTALL)

    achievement = {
        "date": date[0] if len(date) > 0 else "",
        "placement": placement[0] if len(placement) > 0 else "",
        "tournament": tournament[0] if len(tournament) > 0 else "",
        "prize": prize[0] if len(prize) > 0 else "",
    }
    return achievement


def getTeamData(url):
    '''
    [
        {
            "name": "",
            "location": "",
            "logo": "",
            "region": "",
            "Total Winnings": "",
            "Achievements": [],
        },...
    ]

    '''
    regex = {
        "name": r'<h1 id="firstHeading".*?"auto">(.*?)<.*?</h1>',
        "location": r'Location.*?\n.*?title="(.*?)"',
        "logo": r'infobox-image lightmode.*?src="(.*?)"',
        "region": r'Region.*?\n.*?title="(.*?)"',
        "Total Winnings": r'Total Winnings.*?\n.*?>(.*?)<',
        "Achievements": r'<div class="content1.*?Achievements.*?<tbody>(.*?)</tbody>',
    }

    r = requests.get(url)
    content = r.text
    name = re.findall(regex["name"], content)
    location = re.findall(regex["location"], content)
    logo = re.findall(regex["logo"], content)
    region = re.findall(regex["region"], content)
    total_winnings = re.findall(regex["Total Winnings"], content)
    achievements = re.findall(regex["Achievements"], content, re.DOTALL)
    achievements = getAchievements(
        achievements[0] if len(achievements) > 0 else "")

    achievements_data = []
    for achievement in achievements:
        achievements_data.append(getAchievement(achievement))

    team = {
        "name": name[0] if len(name) > 0 else "",
        "location": location[0] if len(location) > 0 else "",
        "logo": baseURL+logo[0] if len(logo) > 0 else "",
        "region": region[0] if len(region) > 0 else "",
        "Total Winnings": total_winnings[0] if len(total_winnings) > 0 else "",
        "Achievements": achievements_data,
    }
    return team


def write_json(new_data, filename):
    with open(filename, mode='r', encoding='utf-8') as j:
        data = json.load(j)
    data.extend(new_data)
    with open(filename, 'w', encoding='utf-8') as j:
        json.dump(data, j, ensure_ascii=False, indent=4)


def loadImage(url, filename):
    urllib.request.urlretrieve(url, filename)


if __name__ == "__main__":
    with open("Data/teams.json", mode='r', encoding='utf-8') as j:
        teams = json.load(j)
    for team in teams:
        print(team["name"])
        if(team["logo"] != ""):
            loadImage(team["logo"], "Data/images/teams/"+team["url"]+".png")
            time.sleep(3)

    # teamsURL = getTeamsURL()
    # for i in range(len(teamsURL)):
    #     teamsURL[i] = teamsURL[i].replace("/valorant/", "")

    # with open("Data/teams.json", mode='r', encoding='utf-8') as j:
    #     teams = json.load(j)
    # new_data = []
    # for i in range(len(teams)):
    #     teams[i]["url"] = teamsURL[i]
    #     new_data.append(teams[i])
    # with open("teams.json", 'w', encoding='utf-8') as j:
    #     json.dump(new_data, j, ensure_ascii=False, indent=4)

    # for team in teams:
    #     print(team["name"])
    # teamsURL = getTeamsURL()
    # print(teamsURL)

    # teamsURL = getTeamsURL()
    # for url in teamsURL:
    #     url = baseURL + url
    #     teamData = getTeamData(url)
    #     print(teamData)
    #     write_json([teamData], "teams.json")
    #     time.sleep(3)
