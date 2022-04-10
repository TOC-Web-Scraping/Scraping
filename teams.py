import requests
import re

url = "https://liquipedia.net/valorant/Portal:Teams"
r = requests.get(url)
content = r.text
result = re.findall(
    r'<tr>.*?<span class="team-template-text"><a href="(.*?)".*?</tr>', content)
print(len(result))

with open('teams.txt', 'w') as f:
    for team in result:
        f.write(team + '\n')
