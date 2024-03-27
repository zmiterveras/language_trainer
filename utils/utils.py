#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201
import os
from PyQt5 import QtWidgets, QtCore, QtGui

def firstScreensaver(abs_path, text, flag=None):
    widget = QtWidgets.QWidget()
    central_box = QtWidgets.QVBoxLayout()
    hor_box = QtWidgets.QHBoxLayout()
    im_l = QtWidgets.QLabel()
    te_l = QtWidgets.QLabel(text)
    img_path = os.path.join(abs_path, 'finger48.png')
    im_l.setPixmap(QtGui.QPixmap(img_path))
    im_l.setAlignment(QtCore.Qt.AlignLeft)
    if not flag:
        hor_box.addWidget(QtWidgets.QLabel(14*' '))
    hor_box.addWidget(im_l)
    hor_box.setAlignment(QtCore.Qt.AlignLeft)
    central_box.addLayout(hor_box)
    central_box.addWidget(te_l)
    widget.setLayout(central_box)
    return widget


def simpleView(dictionary):
    keys = dictionary.keys()
    dic = []
    for key in keys:
        word_full = dictionary[key][2]
        if len(word_full) > 15:
            word = "\n"  + word_full[:15] + "..."
        else:
            word = "\n"  + word_full
        dic.append(key + word + "\n")
    return dic


class ClickedLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()

