from scraper.agent import AgentScraper
from request.pool import ProxyPool, UserAgentPool
import requests

if __name__ == "__main__":
    proxy_pool = ProxyPool.from_file("resources/proxies.txt")
    user_agent_pool = UserAgentPool()

    # res =requests.get("https://www.google.com", proxies=proxy_pool.get_next(), headers=user_agent_pool.get_random(), timeout=3)    
    # print(res.status_code)

    # print(proxy_pool.get_next())
    # print(user_agent_pool.get_random())

    scraper = AgentScraper(proxy_pool, user_agent_pool)
    scraper.scrape()
    scraper.write_data("data/agents.json")