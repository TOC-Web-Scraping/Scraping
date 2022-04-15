import requests
import re
import time
import json
import time
import random
import urllib

baseURL = "https://liquipedia.net"


def getMatchsPlayer(player):
    matchURL = baseURL+"/valorant/"+player+"/Matches"
    r = requests.get(matchURL, proxies=urllib.request.getproxies())
    content = r.text
    matchs = re.findall(
        r'<tr style.*?2022-.*?</tr>|<tr style.*?2021-.*?</tr>', content)
    '''
    {
        "player": "",
        "date": "",
        "tournament": "",
        "map": "",
        "kill": "",
        "death": "",
        "assist": "",
        "team1": "",
        "team2": "",
        "agents1": [],
        "agents2": [],
        "score": "",
    }
    '''
    regex = {
        "date": r'\d\d\d\d-\d\d-\d\d',
        "tournament": r'<td.*?<td.*?<td.*?<td.*?<td>.*?>(.*?)<',
        "map": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?>.*?>(.*?)<',
        "kill": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?>(.*?)<',
        "death": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?>(.*?)<',
        "assist": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?>(.*?)<',
        "team1": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?title="(.*?)"',
        "team2": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?title="(.*?)"',
        "score": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td>(.*?)</td>',
        "a1": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td>.*?<span.*?<a.*?title="(.*?)"',
        "a2": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?title="(.*?)">',
        "a3": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?title="(.*?)">',
        "a4": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?<a.*?title="(.*?)">',
        "a5": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?<a.*?<a.*?title="(.*?)">',
        "a6": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?title="(.*?)">',
        "a7": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?title="(.*?)">',
        "a8": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?<a.*?title="(.*?)">',
        "a9": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?<a.*?<a.*?title="(.*?)">',
        "a10": r'<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td><a.*?<a.*?<a.*?<a.*?<a.*?title="(.*?)">',
    }
    allMatchs = []
    for match in matchs:
        date = re.findall(regex["date"], match)
        tournament = re.findall(regex["tournament"], match)
        map1 = re.findall(regex["map"], match)
        kill = re.findall(regex["kill"], match)
        death = re.findall(regex["death"], match)
        assist = re.findall(regex["assist"], match)
        team1 = re.findall(regex["team1"], match)
        team2 = re.findall(regex["team2"], match)
        score = re.findall(regex["score"], match)
        a1 = re.findall(regex["a1"], match)
        a2 = re.findall(regex["a2"], match)
        a3 = re.findall(regex["a3"], match)
        a4 = re.findall(regex["a4"], match)
        a5 = re.findall(regex["a5"], match)
        a6 = re.findall(regex["a6"], match)
        a7 = re.findall(regex["a7"], match)
        a8 = re.findall(regex["a8"], match)
        a9 = re.findall(regex["a9"], match)
        a10 = re.findall(regex["a10"], match)

        score[0] = score[0].replace("&#160;", "")
        score[0] = score[0].replace("<b>", "")
        score[0] = score[0].replace("</b>", "")
        score[0] = score[0].replace(" ", "")

        a1 = a1[0] if len(a1) > 0 else ""
        a2 = a2[0] if len(a2) > 0 else ""
        a3 = a3[0] if len(a3) > 0 else ""
        a4 = a4[0] if len(a4) > 0 else ""
        a5 = a5[0] if len(a5) > 0 else ""
        a6 = a6[0] if len(a6) > 0 else ""
        a7 = a7[0] if len(a7) > 0 else ""
        a8 = a8[0] if len(a8) > 0 else ""
        a9 = a9[0] if len(a9) > 0 else ""
        a10 = a10[0] if len(a10) > 0 else ""

        agents1 = [a1, a2, a3, a4, a5]
        agents2 = [a6, a7, a8, a9, a10]

        match = {
            "player": player,
            "date": date[0] if len(date) > 0 else "",
            "tournament": tournament[0] if len(tournament) > 0 else "",
            "map": map1[0] if len(map1) > 0 else "",
            "kill": kill[0] if len(kill) > 0 else "",
            "death": death[0] if len(death) > 0 else "",
            "assist": assist[0] if len(assist) > 0 else "",
            "team1": team1[0] if len(team1) > 0 else "",
            "team2": team2[0] if len(team2) > 0 else "",
            "agents1": agents1,
            "agents2": agents2,
            "score": score[0] if len(score) > 0 else "",
        }
        allMatchs.append(match)
    return allMatchs


def write_json(new_data, filename):
    with open(filename, mode='r', encoding='utf-8') as j:
        data = json.load(j)
    data.extend(new_data)
    with open(filename, 'w', encoding='utf-8') as j:
        json.dump(data, j, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    with open('data/matchs.json', mode='r', encoding='utf-8') as j:
        matchs = json.load(j)
    print(len(matchs))
    # with open('data/matchs1.json', mode='r', encoding='utf-8') as j:
    #     matchs1 = json.load(j)
    # with open('data/matchs2.json', mode='r', encoding='utf-8') as j:
    #     matchs2 = json.load(j)
    # with open('data/matchs3.json', mode='r', encoding='utf-8') as j:
    #     matchs3 = json.load(j)
    # with open('data/matchs4.json', mode='r', encoding='utf-8') as j:
    #     matchs4 = json.load(j)
    # with open('data/matchs5.json', mode='r', encoding='utf-8') as j:
    #     matchs5 = json.load(j)

    # matchs = []
    # matchs.extend(matchs1)
    # matchs.extend(matchs2)
    # matchs.extend(matchs3)
    # matchs.extend(matchs4)
    # matchs.extend(matchs5)

    # with open('data/matchs.json', 'w', encoding='utf-8') as j:
    #     json.dump(matchs, j, ensure_ascii=False, indent=4)

    # start = 1052
    # count = 1052
    # with open("data/players.json", mode='r', encoding='utf-8') as j:
    #     players = json.load(j)

    # for i in range(start, len(players)):
    #     player = players[i]
    #     count += 1
    #     if(player["url"] != None):
    #         allMatchs = getMatchsPlayer(player["url"])
    #         if(len(allMatchs) == 0):
    #             break
    #         write_json(allMatchs, "data/matchs5.json")
    #         time.sleep(3)
    #         print(player["name"], " : ", count,
    #               "---", "match : ", len(allMatchs))
