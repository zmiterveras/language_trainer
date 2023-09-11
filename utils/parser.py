#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301, C0114
# pylint: disable=W0201



def parser_controller(user_value, dict_value):
    if 'ß' in user_value and 'ß' not in dict_value:
        user_value = parser(user_value, dict_value)
    elif 'ß' not in user_value and 'ß' in dict_value:
        user_value = parser(user_value, dict_value, point="dict")
    return user_value


def parser(user_value, dict_value, point="user"):
    if point == "user":
        index = user_value.find('ß')
        if dict_value[index:index+2] == 'ss':
            user_value = user_value.replace('ß', 'ss', 1)
    else:
        index = dict_value.find('ß')
        if user_value[index:index+2] == 'ss':
            user_value = user_value[:index] + user_value[index:].replace('ss', 'ß', 1)
    return user_value
