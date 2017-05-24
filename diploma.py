#!/usr/bin/python3
# -*- coding: utf-8

import sys
import argparse
from collections import Counter
import json
from progressbar import Bar
from vkgroups import VkUser


def write_json_file(uid: "int user id",
                    groups: "list of dict with groups info"):
    filename = "{}_groups.json".format(uid)
    with open(filename, 'w', encoding="utf8") as jf:
        jf.write(json.dumps(groups, ensure_ascii=False, indent=3))
    print("group analysis results has been stored in {}".format(filename))


def main(vk: "VkUser object provides access to VK API",
         limit: "int number friends per group"):
    user_friends = vk.get_friends_list()
    user_groups = vk.get_groups_list(vk.get_user_id())
    friends_number = len(user_friends)
    print("{}({}) has {} friends and participate in {} groups\n".format(vk.get_user_name(), vk.get_user_id(),
                                                                        friends_number, len(user_groups)))
    friends_groups = list()
    bar = Bar(friends_number, 'loading friends groups')
    for i, friend in enumerate(user_friends):
        groups = vk.get_groups_list(friend)
        if groups:
            friends_groups.extend(groups)
        bar.show_progress(i)
    else:
        bar.show_progress_100("loaded groups data for {} friends".format(friends_number))
    group_counts = Counter(friends_groups)  # count number of friends using each group, place results in the dict
    result = list(set(user_groups) - set(group_counts.keys()))  # unique user groups
    if limit > 0:  # add groups where friends participate
        for group, count in group_counts.items():
            if group in user_groups and count <= limit:
                result.append(group)
    write_json_file(vk.get_user_id(), [vk.get_group_info(group) for group in result])


def check_limit(value: "int") -> int:
    ival = int(value)
    if ival < 0 or ival > 99:
        raise argparse.ArgumentTypeError("{} is an invalid limit value".format(value))
    return ival


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='This program looks for secret groups of the VK user')
    ap.add_argument("uid", help="  user id or short 'screen name'")
    ap.add_argument("--token", dest="token", action="store", help="  VK API access token")
    ap.add_argument("--limit", dest="limit", action="store", type=check_limit, default=0,
                    help="  max number of friends in one group (0 <= limit <= 99, default=0)")
    args = ap.parse_args(sys.argv[1:])
    if args.token:
        vkapi = VkUser(userid=args.uid, token=args.token)
    else:
        vkapi = VkUser(userid=args.uid)
    main(vkapi, args.limit)
