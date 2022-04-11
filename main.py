from scraper.agent import AgentScraper
from request.pool import ProxyPool, UserAgentPool
import requests

if __name__ == "__main__":
    # agent_scraper = AgentScraper()
    # agent_scraper.scrape()
    
    proxy_pool = ProxyPool.from_file("resources/proxies.txt")
    
    # print(ip)

    user_agent_pool = UserAgentPool()

    # res =requests.get("https://www.google.com", proxies=proxy_pool.get_next(), headers=user_agent_pool.get_random(), timeout=3)    
    # print(res.status_code)

    scraper = AgentScraper(proxy_pool, user_agent_pool)
    scraper.scrape()