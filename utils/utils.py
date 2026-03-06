#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201
import os
import re
from PyQt5 import QtWidgets, QtCore, QtGui

def first_screensaver(abs_path: str, text: str, flag=None):
    widget = QtWidgets.QWidget()
    central_box = QtWidgets.QVBoxLayout()
    hor_box = QtWidgets.QHBoxLayout()
    image_label = QtWidgets.QLabel()
    text_label = QtWidgets.QLabel(text)
    img_path = os.path.join(abs_path, 'finger48.png')
    image_label.setPixmap(QtGui.QPixmap(img_path))
    image_label.setAlignment(QtCore.Qt.AlignLeft)
    if not flag:
        hor_box.addWidget(QtWidgets.QLabel(14*' '))
    hor_box.addWidget(image_label)
    hor_box.setAlignment(QtCore.Qt.AlignLeft)
    central_box.addLayout(hor_box)
    central_box.addWidget(text_label)
    widget.setLayout(central_box)
    return widget

def prepare_translate_view(dictionary: dict, key: str):
    word_full = dictionary[key][3]
    if len(word_full) > 25:
        word = "\n" + word_full[:25] + "..."
    else:
        word = "\n" + word_full
    return word


def simple_view(dictionary: dict) -> list:
    keys = dictionary.keys()
    dic = []
    for key in keys:
        word = prepare_translate_view(dictionary, key)
        dic.append(key + word + "\n")
    return dic

def training_trace_view(training_list: list, dictionary: dict):
    view_list = []
    for item in training_list:
        if item[2]:
            word = f'{item[0]}{prepare_translate_view(dictionary, item[0])}\n'
            view_list.append(word)
        else:
            word = f'\u2026! {item[1]} !\u2026 \u2260 {item[0]}{prepare_translate_view(dictionary, item[0])}\n'
            view_list.append(word)
    return view_list

def get_columns(dictionary: dict, lang: int, part_names: list):
    columns = [[], [], [], [], [], [], []]
    for key in dictionary.keys():
            columns[0].append(dictionary[key][0])
            columns[1].append(key)
            columns[2].append(dictionary[key][1] if lang == 1 else dictionary[key][2])
            columns[3].append(dictionary[key][3])
            columns[4].append(dictionary[key][4])
            columns[5].append(dictionary[key][5])
            columns[6].append(part_names[dictionary[key][6]])
    return columns

def get_part_names(keys: list, part_values: dict):
    part_names = []
    for key in keys:
        part_names.append(part_values[key])
    return part_names

def get_page(dictionary, start_page):
    sort_dictionary = sort_dict(dictionary)
    page_keys = list(sort_dictionary.keys())[start_page: start_page+40]
    return page_dict(sort_dictionary, page_keys)
    
def sort_dict(dictionary):
    return dict(sorted(dictionary.items(), key=lambda item: item[1][0]))

def page_dict(sort_dictionary, page_keys):
    page_dictionary = {}
    for key in page_keys:
        page_dictionary[key] = sort_dictionary[key]
    return page_dictionary

def get_irregular_verbs(dictionary: dict):
    verb_dict = {}
    for key in dictionary.keys():
        if dictionary[key][4] != '':
            verb_dict[key] = dictionary[key]
    return verb_dict

class ClickedLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


