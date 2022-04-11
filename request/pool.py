import random
import requests
import config
from itertools import cycle
from collections import OrderedDict
from request.user_agent import HEADER_LISTS


class BasePool:
    def __init__(self, *element):
        self.pools = [*element]
        self.round_robin = cycle(self.pools)

    @classmethod
    def from_file(cls, file):
        with open(file, "r") as f:
            to_create = f.read().splitlines()
            return cls(*to_create)

    def get_random(self):
        return random.choice(self.pools)

    def get_next(self):
        return next(self.round_robin)

    def __len__(self):
        return len(self.pools)

    def __str__(self):
        return str(self.pools)


class ProxyPool(BasePool):
    def __test_connection(self, ip):
        res = requests.get(config.HTTP_TESTING_URL, proxies={"http": ip}, timeout=3)
        # print(res.json())
        if res.status_code != 200:
            print(f"{ip} is not working")
            return False
        return True

    def get_random(self):
        ip = super().get_random()
        while not self.__test_connection(ip):
            ip = super().get_random()
        print(f"use {ip} as proxy") 
        return {"http": ip}

    def get_next(self):
        ip = super().get_next()
        while not self.__test_connection(ip):
            ip = super().get_next()
        print(f"use {ip} as proxy") 
        return {"http": ip}


class UserAgentPool(BasePool):
    def __init__(self, *user_agents):
        self.pools = [*user_agents]

        for headers in HEADER_LISTS:
            h = OrderedDict()
            for header, value in headers.items():
                h[header] = value
            self.pools.append(h)
        
        self.round_robin = cycle(self.pools)

    @classmethod
    def from_file(cls, file):
        raise NotImplementedError("cannot create UserAgentPool from file")
