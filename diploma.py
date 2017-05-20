#!/usr/bin/python3
# -*- coding: utf-8
# ------------------------------------------------------------------------
# version = 'ver 1.0  May 20, 2017'
#     "ПИВНАЯ ЛИЦЕНЗИЯ" :
# Этот код написал Dmitrii Sokolov <sokolovdp@gmail.com>.  
# В случае использования всего кода или его частей, вы обязаны при личной
# встрече угостить меня бокалом пива объемом 0.5 литра ;)
# Исходный код: https://github.com/sokolovdp/netology/diploma.py
# Идея пивной лицензии взята у Терри Инь <terry.yinzhe@gmail.com>
# ------------------------------------------------------------------------

import sys
import argparse
import requests
import time
from collections import Counter
from pprint import pprint

VERSION = '5.62'  # VK API Version
MAX_FRIENDS = 1000  # Max number of friends to analyse
VK_TIMEOUT = 1.1  # Time in secs to pause when limit of requests is reached
VK_REQ_LIMIT = 3  # Max number of requests to VK API per second
PROGRESS_BAR_DELAY = 2  # Delay in secs between progress bar updates
API_TOKEN = "d13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22"

vk_requests_counter = 0  # VK API request counter,  to calculate time to start delay


def check_timeout():  # control number of requests to VK API per second
    global vk_requests_counter

    if vk_requests_counter >= VK_REQ_LIMIT:
        time.sleep(VK_TIMEOUT)
        vk_requests_counter = 0
    else:
        vk_requests_counter += 1


def progress_bar(iteration: "int current iteration",
                 total: "int total result number",
                 status: "str process status message" = '',
                 barlength: "int process status message" = 50):
    percent = int(round((iteration / total) * 100))
    nb_bar_fill = int(round((barlength * percent) / 100))
    bar_fill = '=' * nb_bar_fill
    bar_empty = '-' * (barlength - nb_bar_fill)
    sys.stdout.write("\r[{0}] {1}% {2}".format(str(bar_fill + bar_empty), percent, status))
    sys.stdout.flush()


def get_response(url: "str url address",
                 par: " dict with parameters"
                 ) -> tuple:
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
            return None, data['error_code'], data['error_msg']
    else:
        check_timeout()
        return data, 0, ""


def check_access_token(token: "str VK api token"
                       ) -> str:
    pars = {'access_token': token, 'v': VERSION, 'user_ids': [], 'fields': ['counters']}
    data, errcode, errmsg = get_response('https://api.vk.com/method/users.get', pars)
    if data:
        return token
    else:
        print("user id check error: {} {}".format(errcode, errmsg))
        exit(4)


def check_user_id(token: "str VK api token",
                  userid: "int user id"
                  ) -> tuple:
    pars = {'access_token': token, 'v': VERSION, 'user_ids': [userid], 'fields': ['counters']}
    data, errcode, errmsg = get_response('https://api.vk.com/method/users.get', pars)
    if not data:
        print("token check error: {} {}".format(errcode, errmsg))
        exit(5)
    else:
        return data[0]['id'], data[0]['first_name'] + ' ' + data[0]['last_name']


def get_friends_list(token: "str VK api token",
                     userid: "int user id"
                     ) -> list:
    pars = {'access_token': token, 'v': VERSION, 'user_id': userid, 'count': MAX_FRIENDS}
    data, errcode, errmsg = get_response('https://api.vk.com/method/friends.get', pars)
    if not data:
        print("can't load friends list, error: {} {}".format(errcode, errmsg))
        exit(6)
    else:
        return data['items']


def get_user_groups_list(token: "str VK api token",
                         userid: "int user id"
                         ) -> list:
    pars = {'access_token': token, 'v': VERSION, 'user_id': userid}
    data, errcode, errmsg = get_response('https://api.vk.com/method/groups.get', pars)
    if not data:
        print("can't load user groups list, error: {} {}".format(errcode, errmsg))
        exit(7)
    else:
        return data['items']


def get_friend_groups_list(token: "str VK api token",
                           friendid: "int group number"
                           ) -> list:
    pars = {'access_token': token, 'v': VERSION, 'user_id': friendid}
    data, errcode, errmsg = get_response('https://api.vk.com/method/groups.get', pars)
    if data:
        return data['items']
    else:
        return list()


def get_group_information(token: "str VK api token",
                          groupid: "int group number"
                          ) -> str:
    name = screen_name = 'no info'
    members_count = -1
    pars = {'access_token': token, 'v': VERSION, 'group_id': groupid}
    data1, _, _ = get_response('https://api.vk.com/method/groups.getById', pars)
    if data1:
        name = data1[0]['name']
        screen_name = data1[0]['screen_name']
    data2, _, _ = get_response('https://api.vk.com/method/groups.getMembers', pars)
    if data2:
        members_count = data2['count']
    return '{0}"name": "{1}", "screen_name": "{2}", "gid": {3}, "members_count:" {4} {5}'.format("{", name,
                                                                                                 screen_name, groupid,
                                                                                                 members_count, "}")


def write_into_log(file: "file object",
                   uid: "int user id",
                   data: "list of integers"):
    file.write("{0},{1}\n".format(uid, ','.join(list(map(str, data)))))


def write_json_file(uid: "int user id",
                    lines: "list of strings"):
    filename = "{}_groups.json".format(uid)
    data = "[\n{}\n]".format(",\n".join(lines))
    with open(filename, 'w', encoding="utf8") as jf:
        jf.write(data)
    print("Group analysis results has been stored in {}".format(filename))


def main(token: "str VK api token",
         uid: "int user id",
         uname: "str user name",
         flog: "file object, log file for results",
         limit: "int number friends per group"):
    user_friends = get_friends_list(token, uid)
    user_groups = get_user_groups_list(token, uid)
    friends_number = len(user_friends)
    print("{}({}) has {} friends and participate in {} groups\n".format(uname, uid, len(user_friends),
                                                                        len(user_groups)))
    if flog:
        write_into_log(flog, uid, user_groups)  # write to log user id and his groups

    friends_groups = list()
    friends_wo_groups = list()

    start_time = time.clock()
    for i, friend in enumerate(user_friends):
        groups = get_friend_groups_list(token, friend)
        if groups:
            friends_groups.extend(groups)
            if flog:
                write_into_log(flog, friend, groups)  # write to log friend id and his groups
        else:
            friends_wo_groups.append(friend)
        if time.clock() - start_time > PROGRESS_BAR_DELAY:  # check if it is time to show progress bar
            progress_bar(i, friends_number, status='loading friends groups')
            start_time = time.clock()
    else:
        time.sleep(PROGRESS_BAR_DELAY)
        progress_bar(friends_number, friends_number, status="loaded groups data for {} friends".format(friends_number))
        print("\n")

    if flog:
        write_into_log(flog, 0, friends_wo_groups)  # write to log list of friends w/o groups
        flog.close()

    # count number of friends using each group, place results in the dict
    group_counts = Counter(friends_groups)

    result = list(set(user_groups) - set(group_counts.keys()))  # unique user groups
    if limit > 0:  # add groups where friends participate
        for group, count in group_counts.items():
            if group in user_groups and count <= limit:
                result.append(group)

    json_lines = list()  # get detailed information about groups
    for group in result:
        json = get_group_information(token, group)
        json_lines.append(json)

    write_json_file(uid, json_lines)  # store results in  json file


if __name__ == '__main__':

    def check_limit(value: "int"
                    ) -> int:
        ivalue = int(value)
        if ivalue < 0 or ivalue > 99:
            raise argparse.ArgumentTypeError("{} is an invalid limit value".format(value))
        return ivalue


    ap = argparse.ArgumentParser(description='This program looks for secret groups of the VK user')
    ap.add_argument("uid", help="user id or short 'screen name'")
    ap.add_argument("--token", dest="token", action="store", default=API_TOKEN, help="VK API access token")
    ap.add_argument("--limit", dest="limit", action="store", type=check_limit, default=0,
                    help="max number of friends in one group (0 <= limit < 100, default = 0")
    ap.add_argument("--log", dest="log", action="store_true", default=False, help="create log file")

    args = ap.parse_args(sys.argv[1:])

    api_token = check_access_token(args.token)
    user_id, user_name = check_user_id(api_token, args.uid)
    if args.log:
        log_file_name = "{}_groups.log".format(user_id)
        log_file = open(log_file_name, 'w')
    else:
        log_file = None

    main(api_token, user_id, user_name, log_file, args.limit)
