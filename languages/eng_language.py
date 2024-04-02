#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201

import random
from PyQt5 import QtWidgets, QtCore
from languages.my_window_language import MyWindowLanguage


class MyWindowE(MyWindowLanguage):
    def onRun(self):
        def onCheck():
            self.ch = ent.text()
            if self.ch == '':
                QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                              self.interface_lang['warn_no_response'])
            elif self.ch == self.ask:
                self.t_ans_count += 1
                self.onTrueAnswer()
            else:
                self.onFalseAnswer()

        if self.dw_key:
            self.q_count += 1
            self.ask = self.dw_key.pop(0)
            self.quest_word = self.dw[self.ask][2]
            question = self.interface_lang['translate_word'] + ' <b>' + self.quest_word + '</b>'
            self.clear()
            label_q = QtWidgets.QLabel('<center>'+question+'</center>')
            self.vtop_t.addWidget(label_q)
            ent = QtWidgets.QLineEdit('', self)
            ent.setFocus()
            self.vtop_t.addWidget(ent)
            btn = QtWidgets.QPushButton('Ok')
            self.htop_b.addWidget(btn)
            btn.clicked.connect(onCheck)
            btn_skip = QtWidgets.QPushButton(self.interface_lang['skip'])
            self.htop_b.addWidget(btn_skip)
            btn_skip.clicked.connect(lambda: self.skip_word(self.ask))
            btn.setAutoDefault(True) # Enter
            ent.returnPressed.connect(btn.click) #enter
        else:
            self.onResult()

    def onAdd(self, void, new=('', '', '', '', '', ''), flag=None):
        def getName():
            value1 = lE_key.text().strip()
            value2 = lE_kf.text()
            value3 = lE_w.text().strip()
            value4 = lE_f.text()
            value5 = lE_pl.text()
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

        def fonSign():
            def onInsert():
                key = self.lv.currentIndex().data()
                lE_kf.insert(key)
                lE_kf.setFocus()
                tlf.close()

            dic = ['ə', 'əʊ', 'ɔ', 'ʌ', 'ʘ', 'ɶ', 'ʊ', 'ʃ', 'ɚ', 'ɳ', 'ʧ', 'ʤ', 'ʒ', 'ɜ']
            tlf = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
            tvbox = QtWidgets.QVBoxLayout()
            self.listBox(dic, flag=2, place=tvbox)
            tlfb = QtWidgets.QPushButton('Ok')
            tvbox.addWidget(tlfb)
            tlfb.clicked.connect(onInsert)
            tlf.setLayout(tvbox)
            tlf.show()

        tla = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tla.setWindowTitle(self.interface_lang['add'])
        #tla.setWindowModality(QtCore.Qt.WindowModal)
        #tla.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        lE_key = QtWidgets.QLineEdit()
        lE_kf = QtWidgets.QLineEdit()
        lE_w = QtWidgets.QLineEdit()
        lE_f = QtWidgets.QLineEdit()
        lE_pl = QtWidgets.QLineEdit()
        cb_pn = QtWidgets.QComboBox()
        cb_pn.addItems(self.lst2)
        btn1 = QtWidgets.QPushButton('ʧ, ʊ, ʌ, ɳ, ʤ')
        btn2 = QtWidgets.QPushButton(self.interface_lang['add'])
        btn3 = QtWidgets.QPushButton(self.interface_lang['close'])
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        form = QtWidgets.QFormLayout()
        k = 0
        for i in (lE_key, lE_kf, lE_w, lE_f, lE_pl):
            i.setText(new[k])
            k += 1
        if flag == 1:
            tla.setWindowTitle(self.interface_lang['change'])
            cb_pn.setCurrentText(new[k])
            value_k_old = new[0]
        form.addRow(self.interface_lang['foreign_word'], lE_key)
        form.addRow(self.interface_lang['phonetic_form_of_word'], lE_kf)
        form.addRow(self.interface_lang['phonetic_sign'], btn1)
        form.addRow(self.interface_lang['translation'] + ':*', lE_w)
        form.addRow(self.interface_lang['verb_forms'] + ':', lE_f)
        form.addRow(self.interface_lang['plural'] + ':', lE_pl)
        form.addRow(self.interface_lang['part_of_speech'] + ':', cb_pn)
        form.addRow(hbox)
        btn1.clicked.connect(fonSign)
        btn2.clicked.connect(getName)
        btn3.clicked.connect(tla.close)
        tla.setLayout(form)
        tla.show()

    def onSearch(self):
        sr, _ = MyWindowLanguage.onSearch(self)
        if sr is None: return
        sr.show()
        