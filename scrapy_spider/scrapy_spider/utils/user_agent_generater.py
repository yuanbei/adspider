# -*- coding: utf-8 -*-

import io
import os
import random


class UserAgentGenerater:

    def __init__(self, user_agent_list_file):
        self.user_agent_list_file_ = user_agent_list_file
        default_ua = "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
        self.user_agents_ = [default_ua]
        self._read_data()

    def _read_data(self):
        assert os.path.exists(self.user_agent_list_file_)
        with io.open(self.user_agent_list_file_) as file_handle:
            self.user_agents_.extend(file_handle.readlines())

    def get_user_agent(self):
        return random.choice(self.user_agents_)
