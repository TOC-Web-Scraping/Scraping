import requests
import re
import config
from util.sleep import sleep_interval
from request.pool import ProxyPool, UserAgentPool
import json

PATTERN = {
    "next_page_pattern": r'<div class="gallerytext">.*?<a href="(?P<next_pages>.*?)".*?</div>',

    "agent_name_pattern": r'<div class="infobox-header wiki-backgroundcolor-light">.*?<span class="infobox-buttons">.*?</span>(?P<name>.*?)</div>',
    "country_name_pattern": r'<div class="infobox-cell-2 infobox-description">Country:</div>.*?<span class="flag">.*?</span>.*?<a href="/valorant/Category.*?">(?P<country>.*?)</a>.*?</div>',
    "class_name_pattern": r'<div class="infobox-cell-2 infobox-description">Class:</div>.*?<div class="infobox-cell-2">(?P<class>.*?)</div>',
    "release_date_pattern": r'<div class="infobox-cell-2 infobox-description">Release Date:</div>.*?<div class="infobox-cell-2">(?P<release_date>.*?)</div>',
    "agent_image_pattern": r'<div class="infobox-image">.*?<img alt="" src="(?P<agent_image>.*?)".*?>',

    "skill_name_pattern": r'<tr>.*?<td colspan="4" valign="top">.*?<div style="background-color: #e6e6e6;.*?>.*?<b>(?P<skill_name>.*?)</b>.*?</div>',
    "skill_image_pattern": r'<td style="width: 128px; vertical-align:top;">.*?<div style="border:2px solid black;.*?>.*?<a.*?>.*?<img alt="" src="(?P<skill_image>.*?)".*?>.*?</a>.*?</div>.*?</td>',
    "skill_type_pattern": r'<b>Ability:</b>.*?<span style="text-align:left; margin-right:15px;">(?P<skill_type>.*?)\n',
    "top_description_pattern": r'<b>Ability:</b>.*?(?:<p>(?P<top_description>.*?)</p>|"")',
    "bottom_description_pattern": r'<b>Ability:</b>.*?<div style="width: 460px; padding-bottom: 4px; margin-left:10px; margin-top:5px; margin-right:10px; border-top:1px solid #e6e6e6; clear:both; float:center;"></div>\n<div>(?P<bottom_description>.*?)</div>',
    "cost_pattern": r'<b>Ability:</b>.*?(?:<div>.*?<span>.*?<b>Cost:</b>.*?<span style="white-space:nowrap;">.*?</span>(?P<cost>.*?)</span>.*?</div>|"")',
    "ultimate_cost_pattern": r'<b>Ability:</b>.*?(?:<b>Ultimate Cost:</b>(?P<ultimate_cost>.*?)</span>|"")'
}

class AgentScraper:
    def __init__(self, proxy_pool: ProxyPool=None, user_agent_pool: UserAgentPool=None):
        self.url = config.BASE_URL + "/valorant/Portal:Agents"
        self.proxy_pool = proxy_pool
        self.user_agent_pool = user_agent_pool
        self.data = []

    def scrape(self):
        page = requests.get(self.url, proxies=self.get_proxies(), headers=self.get_headers())
        sleep_interval(4, 10)
        
        next_page_pattern = PATTERN["next_page_pattern"]
        relative_paths = re.findall(next_page_pattern, page.text, flags=re.DOTALL)
        print(relative_paths)

        for path in relative_paths:
            agent_data = dict()
            print(config.BASE_URL + path)
            agent_detail_page = requests.get(config.BASE_URL + path, proxies=self.get_proxies(), headers=self.get_headers())
            sleep_interval(4, 10)

            name = re.findall(PATTERN["agent_name_pattern"], agent_detail_page.text, flags=re.DOTALL)
            country = re.findall(PATTERN["country_name_pattern"], agent_detail_page.text, flags=re.DOTALL)
            role = re.findall(PATTERN["class_name_pattern"], agent_detail_page.text, flags=re.DOTALL)
            release_date = re.findall(PATTERN["release_date_pattern"], agent_detail_page.text, flags=re.DOTALL)
            image_url = re.findall(PATTERN["agent_image_pattern"], agent_detail_page.text, flags=re.DOTALL)
            
            agent_data["name"] = name[0]
            agent_data["imageUrl"] = image_url[0]
            agent_data["country"] = country[0] if len(country) > 0 else None
            agent_data["role"] = role[0]
            agent_data["releaseDate"] = release_date[0]

            skill_names = re.findall(PATTERN["skill_name_pattern"], agent_detail_page.text, flags=re.DOTALL)
            skill_images = re.findall(PATTERN["skill_image_pattern"], agent_detail_page.text, flags=re.DOTALL)
            skill_types = re.findall(PATTERN["skill_type_pattern"], agent_detail_page.text, flags=re.DOTALL)
            top_descriptions = re.findall(PATTERN["top_description_pattern"], agent_detail_page.text, flags=re.DOTALL)
            bottom_descriptions = re.findall(PATTERN["bottom_description_pattern"], agent_detail_page.text, re.DOTALL)
            costs = re.findall(PATTERN["cost_pattern"], agent_detail_page.text, flags=re.DOTALL)
            ultimate_cost = re.findall(PATTERN["ultimate_cost_pattern"], agent_detail_page.text, flags=re.DOTALL)

            skills_zip = zip(skill_names, skill_images, skill_types, top_descriptions, bottom_descriptions, costs, ultimate_cost)

            agent_skills = []
            for skill in skills_zip:
                skill_name, skill_image, skill_type, top_description, bottom_description, cost, ultimate_cost = skill
                skill_object = {
                    "name": skill_name,
                    "imageUrl": skill_image,
                    "type": skill_type,
                    "topDescription": top_description,
                    "bottomDescription": bottom_description,
                }
                if cost != "":
                    skill_object["cost"] = cost
                if ultimate_cost != "":
                    skill_object["ultimateCost"] = ultimate_cost

                agent_skills.append(skill_object)
            agent_data["abilities"] = agent_skills
            self.data.append(agent_data)

    def get_proxies(self, round_robin=True):
        if not self.proxy_pool:
            return None

        proxy = None
        if round_robin:
            proxy = self.proxy_pool.get_next()
        else:
            proxy = self.proxy_pool.get_random()

        print(f"Agent scraper use {proxy} as proxy")
        return proxy

    def get_headers(self, random=True):
        if not self.user_agent_pool:
            return None
        
        headers = None
        if random:
            headers = self.user_agent_pool.get_random()
        else:
            headers = self.user_agent_pool.get_next()

        print(f"Agent scraper use {headers['User-Agent']} as user agent")
        return headers
        

    def write_data(self, file_name):
        with open(file_name, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_data(self):
        return self.data
