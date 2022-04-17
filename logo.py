import json
baseUrl = "https://toc-web-scraping.github.io/scraping/"

if __name__ == "__main__":
    with open("data/teams.json", mode='r', encoding='utf-8') as j:
        teams = json.load(j)
    for team in teams:
        print(team["name"])
        if(team["logo"] != ""):
            team["logo"] = baseUrl + "data/images/teams/"+team["url"]+".png"
    with open("data/teams2.json", 'w', encoding='utf-8') as j:
        json.dump(teams, j, ensure_ascii=False, indent=4)
