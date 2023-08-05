# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg <olegsuvorinov@me.com>
# @Date:   2023-02-28 10:01:30
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-07-01 09:15:38

import os
import random

import requests
from lxml import html


class UserAgent(object):
    """docstring for UserAgent"""

    def __init__(self):
        super(UserAgent, self).__init__()

        self._u_agents = []
        self.__most_common_user_agents()

    def __most_common_user_agents(self):
        """Забираем содержмое страницы с наиболее популярными
        браузерами"""

        url = ("https://webcache.googleusercontent.com/"
               "search?q=cache:FxxmQW9XrRcJ:https://techblog.willshouse.com/"
               "2012/01/03/most-common-user-agents/+&cd=4&hl=en&ct=clnk&gl=us")
        xpath = '//*[@id="post-2229"]/div[2]/textarea[1]'

        try:
            r = requests.get(url)
            xml = html.fromstring(r.content)
            elem = xml.xpath(xpath)[0]

            cur_dir, _ = os.path.split(__file__)
            ua_file = os.path.join(cur_dir, 'useragents.txt')
            with open(ua_file, 'w') as f:
                f.write(elem.text_content())
            for line in elem.text_content().split('\n'):
                self._u_agents.append(line.strip())
        except Exception:
            pass

    def get_ua(self) -> str:
        """Рандомно забираем User Agents из файла
        useragents.txt
        """

        u_a = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0' # noqa
        if self._u_agents:
            return random.choice(self._u_agents)

        try:
            cur_dir, _ = os.path.split(__file__)
            ua_file = os.path.join(cur_dir, 'useragents.txt')
            with open(ua_file) as f:
                for line in f:
                    self._u_agents.append(line.strip())
        except Exception:
            return u_a
        else:
            return random.choice(self._u_agents)
