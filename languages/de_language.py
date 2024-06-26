#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201

import random
from PyQt5 import QtWidgets, QtCore
from languages.my_window_language import MyWindowLanguage
from utils.parser import parser_controller


class MyWindowD(MyWindowLanguage):
    # def __init__(self, desktop, images_path, parent=None):
    #     MyWindowLanguage.__init__(self, desktop, images_path, parent)


    def onSearch(self):
        sr, srhbox = MyWindowLanguage.onSearch(self)
        if sr is None: return
        btn_u = QtWidgets.QPushButton('ä, ö, ü, ß')
        btn_u.clicked.connect(self.fonSign)
        srhbox.insertWidget(1, btn_u)
        sr.show()

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
                try:
                    self.se.insert(key)
                    self.se.setFocus()
                except RuntimeError:
                    QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                                  self.interface_lang['unexpected_difficulty'])
            onClose()

        def onClose():
            if hasattr(self, 'time_lv'):
                self.lv = self.time_lv
            tlf.close()

        dic = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        tlf = QtWidgets.QWidget(parent=None) #, flags=QtCore.Qt.Window)
        tlf.setWindowFlags(self.windowFlags()
                           & ~QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Window)
        # tlf.setWindowModality(QtCore.Qt.WindowModal)
        # tlf.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        tvbox = QtWidgets.QVBoxLayout()
        buttonBox = QtWidgets.QHBoxLayout()
        if hasattr(self, 'lv'):
            self.time_lv = self.lv
        self.listBox(dic, flag=2, place=tvbox)
        tlfb_ok = QtWidgets.QPushButton('Ok')
        tlfb_close = QtWidgets.QPushButton(self.interface_lang['close'])
        buttonBox.addWidget(tlfb_ok)
        buttonBox.addWidget(tlfb_close)
        print('flag: ' + str(self.on_sign_flag))
        if not self.on_sign_flag:
            tlcb = QtWidgets.QComboBox()
            tlcb.addItems([self.interface_lang['word'], self.interface_lang['verb_forms']])
            tvbox.addWidget(tlcb)
        tvbox.addLayout(buttonBox)
        tlfb_ok.clicked.connect(onInsert)
        tlfb_close.clicked.connect(onClose)
        tlf.setLayout(tvbox)
        tlf.show()

    def onAdd(self, void, new=('', '', '', '', '', ''), flag=None):
        def getName():
            value1 = self.lE_key.text().strip()
            value2 = cb_ar.currentText()
            value3 = lE_w.text().strip()
            value4 = self.lE_f.text()
            value5 = cb_pl.currentText()
            value6_1 = cb_pn.currentText()
            value6_2 = cb_pn.currentIndex()
            if (value1 and value3) == '':
                QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                              self.interface_lang['warn_values_not_entered'])
            else:
                if value1 in list(self.dw.keys()) and not flag:
                    QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                                  self.interface_lang['warn_word_in_dict'])
                    return
                dcont = [value1, value2, value3, value4, value5, value6_2+1]
                if flag == 1:
                    if value1 != value_k_old:
                        val_id = self.dw[value_k_old][0]
                        del self.dw[value_k_old]
                    else:
                        val_id = self.dw[value1][0]
                    self.dw[value1] = [val_id] + dcont[1:5] + [value6_1]
                    txt = self.interface_lang['changed_word']
                    for i, name in enumerate([val_id] + dcont):
                        self.changenote[i].append(name)
                else:
                    txt = self.interface_lang['added_word']
                    self.dw[value1] = [None] + dcont[1:5] + [value6_1]
                    for j, n in enumerate(dcont):
                        self.newname[j].append(n)
                QtWidgets.QMessageBox.information(None, self.interface_lang['info'], txt + value1)
                self.clear()
                self.editDict()
                tla.close()

        tla = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tla.setWindowTitle(self.interface_lang['add'])
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
        btn2 = QtWidgets.QPushButton(self.interface_lang['add'])
        btn3 = QtWidgets.QPushButton(self.interface_lang['close'])
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(btn2)
        hbox2.addWidget(btn3)
        form = QtWidgets.QFormLayout()
        if flag == 1:
            tla.setWindowTitle(self.interface_lang['change'])
            cb_pn.setCurrentText(new[-1])
            value_k_old = new[0]
            cb_ar.setCurrentText(new[1])
            cb_pl.setCurrentText(new[-2])
        new = new[:1] + new[2:]
        for n, i  in enumerate([self.lE_key, lE_w, self.lE_f]):
            i.setText(new[n])
        form.addRow(self.interface_lang['foreign_word'], hbox1)
        form.addRow(self.interface_lang['translation'] + ':*', lE_w)
        form.addRow(self.interface_lang['verb_forms'] + ':', self.lE_f)
        form.addRow(self.interface_lang['plural'] + ':', cb_pl)
        form.addRow(self.interface_lang['part_of_speech'] + ':', cb_pn)
        form.addRow(self.interface_lang['umlaut'], btn1)
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
                QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                              self.interface_lang['warn_no_response'])
                return
            self.ch = parser_controller(self.ch, self.ask)
            if self.ch == self.ask:
                self.t_ans_count += 1
                self.onTrueAnswer()
            else:
                self.onFalseAnswer()

        if self.dw_key:
            self.on_sign_flag = 1
            self.q_count += 1
            self.ask = self.dw_key.pop(0)
            self.quest_word = self.dw[self.ask][2]
            question = self.interface_lang['translate_word'] + ' <b>' + self.quest_word + '</b>'
            self.clear()
            label_q = QtWidgets.QLabel('<center>'+question+'</center>')
            self.vtop_t.addWidget(label_q)
            self.ent = QtWidgets.QLineEdit('', self)
            self.ent.setFocus()
            self.vtop_t.addWidget(self.ent)
            btn_u = QtWidgets.QPushButton('ä, ö, ü, ß')
            btn_u.clicked.connect(self.fonSign)
            btn = QtWidgets.QPushButton('Ok')
            btn.clicked.connect(onCheck)
            btn_skip = QtWidgets.QPushButton(self.interface_lang['skip'])
            self.htop_b.addWidget(btn)
            self.htop_b.addWidget(btn_u)
            self.htop_b.addWidget(btn_skip)
            btn_skip.clicked.connect(lambda: self.skip_word(self.ask))
            btn.setAutoDefault(True) # Enter
            self.ent.returnPressed.connect(btn.click) #enter
        else:
            self.onResult()



        