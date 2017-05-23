#!/usr/bin/python3
# -*- coding: utf-8

import requests
import time
from pprint import pprint

VERSION = '5.62'  # VK API Version
MAX_FRIENDS = 1000  # Max number of friends to analyse
VK_TIMEOUT = 1.1  # Time in secs to pause when limit of requests is reached
VK_REQ_LIMIT = 3  # Max number of requests to VK API per second
API_TOKEN = "d13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22"


class VkUser:
    def __init__(self, userid=0, token=API_TOKEN):
        self.counter = 0
        # check if token is valid
        pars = {'access_token': token, 'v': VERSION, 'user_ids': [], 'fields': ['counters']}
        data, errcode, errmsg = self._get_response('https://api.vk.com/method/users.get', pars)
        if not data:
            print("user id check error: {} {}".format(errcode, errmsg))
            exit(4)
        self.token = token
        # check if user_id is valid
        pars = {'access_token': token, 'v': VERSION, 'user_ids': [userid], 'fields': ['counters']}
        data, errcode, errmsg = self._get_response('https://api.vk.com/method/users.get', pars)
        if not data:
            print("token check error: {} {}".format(errcode, errmsg))
            exit(5)
        self.uid = data[0]['id']
        self.name = data[0]['first_name'] + ' ' + data[0]['last_name']

    def _get_response(self, url, par):
        resp = None
        try:
            resp = requests.get(url, par)
        except ConnectionError:
            print("error: VK connection problem")
            exit(1)
        except TimeoutError:
            print("error: VK connection timeout")
            exit(2)
        r = resp.json()
        try:
            data = r['response']
        except KeyError:
            try:
                data = r['error']
            except KeyError:
                print("error: unknown response from VK")
                pprint(r)
                exit(3)
            else:
                return None, data['error_code'], data['error_msg']  # return error information
        else:
            if self.counter >= VK_REQ_LIMIT:
                time.sleep(VK_TIMEOUT)
                self.counter = 0
            else:
                self.counter += 1
            return data, 0, ""  # return data, no error information

    def get_friends_list(self):
        pars = {'access_token': self.token, 'v': VERSION, 'user_id': self.uid, 'count': MAX_FRIENDS}
        data, errcode, errmsg = self._get_response('https://api.vk.com/method/friends.get', pars)
        if not data:
            print("can't load friends list, error: {} {}".format(errcode, errmsg))
            exit(6)
        return data['items']

    def get_groups_list(self, vkid):
        pars = {'access_token': self.token, 'v': VERSION, 'user_id': vkid}
        data, errcode, errmsg = self._get_response('https://api.vk.com/method/groups.get', pars)
        if not data:
            if vkid == self.uid:  # if it main user exit
                print("can't load user groups list, error: {} {}".format(errcode, errmsg))
                exit(7)
            else:
                return None
        return data['items']

    def get_group_info(self, groupid):
        name = 'no info'
        members_count = -1
        pars = {'access_token': self.token, 'v': VERSION, 'group_id': groupid}
        data1, _, _ = self._get_response('https://api.vk.com/method/groups.getById', pars)
        if data1:
            name = data1[0]['name']
        data2, _, _ = self._get_response('https://api.vk.com/method/groups.getMembers', pars)
        if data2:
            members_count = data2['count']
        group_info = {"name": name, "gid": groupid, "members_count": members_count}
        return group_info

    def get_user_id(self):
        return self.uid

    def get_user_name(self):
        return self.name
