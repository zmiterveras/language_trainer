#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301, C0114
# pylint: disable=W0201

def parser_controller(user_value: str, dict_value: str) -> tuple[str, str]:
    return szet_parser(user_value, dict_value) if 'ß' in user_value or 'ß' in dict_value else (user_value, dict_value)

def szet_parser(user_value: str, dict_value: str) -> tuple[str, str]:
    return f'{user_value[0]}{user_value[1:].casefold()}', f'{dict_value[0]}{dict_value[1:].casefold()}'
