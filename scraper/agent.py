import requests
import re
import config
from util.sleep import sleep_interval
from request.pool import ProxyPool, UserAgentPool

PATTERN = {
    "next_page_pattern": r'<div class="gallerytext">.*?<a href="(.*?)".*?</div>',
    "agent_name_pattern": r'<div class="infobox-header wiki-backgroundcolor-light">.*?<span class="infobox-buttons">.*?</span>(?P<name>.*?)</div>',
    "agent_image_pattern": r'<div class="infobox-image">.*?<img alt="" src="(.*?)".*?>',
    "country_name_pattern": r'<div class="infobox-cell-2 infobox-description">Country:</div>.*?<span class="flag">.*?</span>.*?<a href="/valorant/Category.*?">(?P<country>.*?)</a>.*?</div>',
    "class_name_pattern": r'<div class="infobox-cell-2 infobox-description">Class:</div>.*?<div class="infobox-cell-2">(?P<class>.*?)</div>',
    "release_date_pattern": r'<div class="infobox-cell-2 infobox-description">Release Date:</div>.*?<div class="infobox-cell-2">(?P<release_date>.*?)</div>',
}

class AgentScraper:
    def __init__(self, proxy_pool: ProxyPool=None, user_agent_pool: UserAgentPool=None):
        self.url = config.BASE_URL + "/Portal:Agents"
        self.proxy_pool = proxy_pool
        self.user_agent_pool = user_agent_pool

    def scrape(self):
        print("start req")
        page = requests.get(self.url, proxies=self.get_proxies(), headers=self.get_headers())
        sleep_interval(4, 10)
        print("end req")
        next_page_pattern = PATTERN["next_page_pattern"]
        relative_paths = re.findall(next_page_pattern, page.text, flags=re.DOTALL)
        print(relative_paths)

        # for path in relative_paths:
        #     agent_detail_page = requests.get(config.BASE_URL + path, proxies=self.get_proxies())
        #     sleep_interval(4, 10)
        #     all = ".*?".join(
        #         [PATTERN["agent_name_pattern"], 
        #         PATTERN["agent_image_pattern"],
        #         PATTERN["country_name_pattern"], 
        #         PATTERN["class_name_pattern"], 
        #         PATTERN["release_date_pattern"]
        #         ])

    def get_proxies(self, round_robin=True):
        if not self.proxy_pool:
            return None

        proxy = None
        if round_robin:
            proxy = {"http": self.proxy_pool.get_next()}
        else:
            proxy = {"http": self.proxy_pool.get_random()}
        return proxy

    def get_headers(self, random=True):
        if not self.user_agent_pool:
            return None
        
        headers = None
        if random:
            headers = self.user_agent_pool.get_random()
        else:
            heasers = self.user_agent_pool.get_next()
        return headers
        

    def get_data(self):
        pass
