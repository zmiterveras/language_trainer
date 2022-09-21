#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201

import random
from PyQt5 import QtWidgets, QtCore
from languages.my_window_language import MyWindowLanguage


class MyWindowD(MyWindowLanguage):
    def __init__(self, desktop, images_path, parent=None):
        MyWindowLanguage.__init__(self, desktop, images_path, parent)
        self.on_sign_flag = 0

    def fonSign(self):
        def onInsert():
            key = self.lv.currentIndex().data() # from ListBox
            if not self.on_sign_flag:
                field = tlcb.currentIndex()
                if field == 0:
                    self.lE_key.insert(key)
                    self.lE_key.setFocus()
                else:
                    self.lE_f.insert(key)
                    self.lE_f.setFocus()
            elif self.on_sign_flag == 1:
                self.ent.insert(key)
                self.ent.setFocus()
            else:
                self.se.insert(key)
                self.se.setFocus()
            onClose()

        def onClose():
            if hasattr(self, 'time_lv'):
                self.lv = self.time_lv
            tlf.close()

        dic = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        tlf = QtWidgets.QWidget(parent=None) #, flags=QtCore.Qt.Window)
        tlf.setWindowFlags(self.windowFlags()
                           & ~QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Window)
        tlf.setWindowModality(QtCore.Qt.WindowModal)
        tlf.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        tvbox = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QHBoxLayout()
        if hasattr(self, 'lv'):
            self.time_lv = self.lv
        self.listBox(dic, flag=2, place=tvbox)
        tlfb_ok = QtWidgets.QPushButton('Ok')
        tlfb_close = QtWidgets.QPushButton('Close')
        buttonBox.addWidget(tlfb_ok)
        buttonBox.addWidget(tlfb_close)
        if not self.on_sign_flag:
            tlcb = QtWidgets.QComboBox()
            tlcb.addItems(['Слово', 'Форма гл.'])
            tvbox.addWidget(tlcb)
        tvbox.addLayout(buttonBox)
        tlfb_ok.clicked.connect(onInsert)
        tlfb_close.clicked.connect(onClose)
        tlf.setLayout(tvbox)
        tlf.show()

    def onAdd(self, void, new=('', '', '', '', '', ''), flag=None):
        def getName():
            value1 = self.lE_key.text()
            value2 = cb_ar.currentText()
            value3 = lE_w.text()
            value4 = self.lE_f.text()
            value5 = cb_pl.currentText()
            value6_1 = cb_pn.currentText()
            value6_2 = cb_pn.currentIndex()
            if (value1 and value3) == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
            else:
                if value1 in list(self.dw.keys()) and not flag:
                    QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Данное слово уже есть в словаре')
                    return
                dcont = [value1, value2, value3, value4, value5, value6_2+1]
                if flag == 1:
                    if value1 != value_k_old:
                        val_id = self.dw[value_k_old][0]
                        del self.dw[value_k_old]
                    else:
                        val_id = self.dw[value1][0]
                    self.dw[value1] = [val_id] + dcont[1:5] + [value6_1]
                    txt = 'Изменено слово: '
                    for i, name in enumerate([val_id] + dcont):
                        self.changenote[i].append(name)
                else:
                    txt = 'Добавлено слово: '
                    self.dw[value1] = [None] + dcont[1:5] + [value6_1]
                    for j, n in enumerate(dcont):
                        self.newname[j].append(n)
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value1)
                self.clear()
                self.editDict()
                tla.close()

        tla = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tla.setWindowTitle('Добавить')
        tla.setWindowModality(QtCore.Qt.WindowModal)
        tla.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        hbox1 = QtWidgets.QHBoxLayout()
        self.lE_key = QtWidgets.QLineEdit()
        cb_ar = QtWidgets.QComboBox()
        cb_ar.addItems(['', 'der', 'die', 'das'])
        hbox1.addWidget(self.lE_key)
        hbox1.addWidget(cb_ar)
        btn1 = QtWidgets.QPushButton('ä, ö, ü, ß')
        lE_w = QtWidgets.QLineEdit()
        self.lE_f = QtWidgets.QLineEdit()
        cb_pl = QtWidgets.QComboBox()
        cb_pl.addItems(['', '-e', '-¨e', '-en', '-n', '-¨er', '-¨en', '-¨', '-s', '-er'])
        cb_pn = QtWidgets.QComboBox()
        cb_pn.addItems(self.lst2)
        btn2 = QtWidgets.QPushButton('Добавить')
        btn3 = QtWidgets.QPushButton('Закрыть')
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(btn2)
        hbox2.addWidget(btn3)
        form = QtWidgets.QFormLayout()
        if flag == 1:
            tla.setWindowTitle('Изменить')
            cb_pn.setCurrentText(new[-1])
            value_k_old = new[0]
            cb_ar.setCurrentText(new[1])
            cb_pl.setCurrentText(new[-2])
        new = new[:1] + new[2:]
        for n, i  in enumerate([self.lE_key, lE_w, self.lE_f]):
            i.setText(new[n])
        form.addRow('Иностранное слово:*', hbox1)
        form.addRow('Перевод:*', lE_w)
        form.addRow('Формы глагола:', self.lE_f)
        form.addRow('Множественное число:', cb_pl)
        form.addRow('Часть речи:', cb_pn)
        form.addRow('Умляут', btn1)
        form.addRow(hbox2)
        btn1.clicked.connect(self.fonSign)
        btn2.clicked.connect(getName)
        btn3.clicked.connect(tla.close)
        tla.setLayout(form)
        tla.show()

    def onRun(self):
        def onCheck():
            self.ch = self.ent.text()
            self.on_sign_flag = 0
            if self.ch == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не получен ответ')
            elif self.ch == self.ask:
                self.t_ans_count += 1
                self.onTrueAnswer()
            else:
                self.onFalseAnswer()

        if self.dw_key:
            self.on_sign_flag = 1
            self.q_count += 1
            self.ask = random.choice(self.dw_key)
            self.dw_key.remove(self.ask)
            self.quest_word = self.dw[self.ask][2]
            question = 'Переведите слово: <b>' + self.quest_word + '</b>'
            self.clear()
            label_q = QtWidgets.QLabel('<center>'+question+'</center>')
            self.vtop_t.addWidget(label_q)
            self.ent = QtWidgets.QLineEdit('', self)
            self.ent.setFocus()
            self.vtop_t.addWidget(self.ent)
            btn_u = QtWidgets.QPushButton('ä, ö, ü, ß')
            self.vtop_t.addWidget(btn_u)
            btn_u.clicked.connect(self.fonSign)
            btn = QtWidgets.QPushButton('Ok')
            self.vtop_t.addWidget(btn)
            btn.clicked.connect(onCheck)
            btn.setAutoDefault(True) # Enter
            self.ent.returnPressed.connect(btn.click) #enter
        else:
            self.onResult()

    def onSearch(self):
        self.on_sign_flag = 2
        print("on_sign_flag: ", self.on_sign_flag)
        sr, srhbox = MyWindowLanguage.onSearch(self)
        btn_u = QtWidgets.QPushButton('ä, ö, ü, ß')
        btn_u.clicked.connect(self.fonSign)
        srhbox.insertWidget(1, btn_u)
        sr.show()
        