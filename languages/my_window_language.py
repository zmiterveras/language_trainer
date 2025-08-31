#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201

import os
import random
import time
from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from utils.utils import first_screensaver
from utils.utils import ClickedLabel
from utils.utils import simple_view
from menulanguages import MenuLanguages


class MyWindowLanguage(QtWidgets.QWidget):
    def __init__(self, desktop, root_dir: str, language: dict, sql_handler, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.dict_name = ''
        self.dw = {}
        self.desktop = desktop
        self.root_dir = root_dir
        self.interface_lang = language
        self.sql_handler = sql_handler
        self.key_part_of_speech = MenuLanguages.part_keys #[self.interface_lang['noun'],
        #                             self.interface_lang['verb'],
        #                             self.interface_lang['adjective'],
        #                             self.interface_lang['adverb'],
        #                             self.interface_lang['another']]
        self.name_part_of_speech = [self.interface_lang[item] for item in MenuLanguages.part_keys]
        self.search_flag = 0
        self.cards_flag = 0
        self.search_key = 0
        self.on_sign_flag = 0 # для немецкого для умляутов
        self.page_max = 0
        self.wd = os.path.join(self.root_dir, 'images')
        self.status = QtWidgets.QLabel()
        self.make_widget()
        self.save_values()
        self.set_status_widget()

    def set_status_widget(self):
        self.status_widget = QtWidgets.QWidget()
        status_box = QtWidgets.QHBoxLayout()
        self.label_amount = QtWidgets.QLabel()
        self.label_flag = QtWidgets.QLabel()
        status_box.addWidget(self.label_amount)
        status_box.addWidget(self.label_flag)
        self.status_widget.setLayout(status_box)

    def save_values(self):
        self.new_name = [[], [], [], [], [], [], [], []]
        self.del_name = []
        self.change_note = [[], [], [], [], [], [], [], [], []]

    def make_widget(self):
        # text = self.interface_lang['open_dict_text']
        self.vbox = QtWidgets.QVBoxLayout()
        self.vtop = QtWidgets.QVBoxLayout()
        self.vtop_t = QtWidgets.QVBoxLayout()
        # screen_saver = first_screensaver(self.wd, text, flag=1)
        # self.vtop_t.addWidget(screen_saver)
        self.htop_b = QtWidgets.QHBoxLayout()
        self.vtop.addLayout(self.vtop_t)
        self.vtop.addLayout(self.htop_b)
        self.hbox = QtWidgets.QHBoxLayout()
        btn_names = [(self.interface_lang['viewing'],self.dict_view),
                    (self.interface_lang['training'], self.on_training_mode),
                    (self.interface_lang['search'], self.on_search),
                    (self.interface_lang['edit'], self.edit_dict)]
        btn_list = []
        for i in btn_names:
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1])
            self.hbox.addWidget(btn)
            btn_list.append(btn)
        self.btn_close = QtWidgets.QPushButton(self.interface_lang['close'])
        self.hbox.addWidget(self.btn_close)
        self.vbox.addLayout(self.vtop)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def save_dict(self):
        if not self.check_save_values():
            return 
        # if not self.dict_name:
        #     QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
        #                                   self.interface_lang['warn_not_selected_dict'])
        #     return
        self.sql_handler.save_dict(self.del_name, self.new_name, self.change_note)
        self.save_values()
        
    def check_save_values(self):
        if self.new_name[0] or self.change_note[0] or self.del_name:
            return True
        return False

    def clear(self):
        for i in reversed(range(self.vtop_t.count())):
            wt = self.vtop_t.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()
        for i in reversed(range(self.htop_b.count())):
            wb = self.htop_b.itemAt(i).widget()
            wb.setParent(None)
            wb.deleteLater()

    def dict_view(self, flag=None):
        # if not self.dw:
        #     QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
        #                                   self.interface_lang['warn_dict_not_loaded'])
        #     return
        place = self.vtop_t
        self.clear()
        if not self.dw:
            self.label1 = QtWidgets.QLabel('<center>' + self.interface_lang['dict_empty'] + '</center>')
            place.addWidget(self.label1)
        else:
            self.status.setText(self.interface_lang['mode_view'])
            dic = simple_view(self.dw)
            self.list_box(dic, flag, place)

    def list_box(self, dic: list, flag: int, place):
        self.lv = QtWidgets.QListView()
        slm = QtCore.QStringListModel(dic)
        self.lv.setModel(slm)
        place.addWidget(self.lv)
        amount = str(len(dic))
        text = '<center>' + self.interface_lang['amount_words'] + '<b>' + amount + '</b></center>'
        if flag != 2: self.label_amount.setText(text)
        if not flag:
            self.lv.doubleClicked.connect(self.view_word)
        elif flag == 1:
            self.lv.doubleClicked.connect(self.on_edit_run)
        else:
            pass

    def view_word(self, void):
        self.display_word()

    def on_edit_run(self, void):
        self.on_edit()

    def horizont_line(self, box):
        fr = QtWidgets.QFrame()
        fr.setFrameShape(QtWidgets.QFrame.HLine)
        box.addWidget(fr)

    def display_word(self):
        def edit_run(void, win):
            tl_close(None, win, flag=1)
            self.on_edit()

        def tl_close(void, win, flag=None):
            if not flag:
                self.search_flag = 0
            win.close()

        def view():
            tl = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
            tl.setWindowTitle(self.interface_lang['viewing'])
            tl.setWindowModality(QtCore.Qt.WindowModal)
            tl.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            tlv_box = QtWidgets.QVBoxLayout()
            lk = QtWidgets.QLabel('<center><b>' + key + '</b>' + ' (<i>'+part_name+'</i>)</center>')
            tlv_box.addWidget(lk)
            lfk = QtWidgets.QLabel('<center>[' + phonetic_article + ']</center>')
            tlv_box.addWidget(lfk)
            self.horizont_line(tlv_box)
            if form:
                lf = QtWidgets.QLabel(self.interface_lang['verb_forms'] + ': ' + '<b>' + form + '</b>')
                tlv_box.addWidget(lf)
            if plural:
                lp = QtWidgets.QLabel(self.interface_lang['plural'] + ': ' + '<b>' + plural + '</b>')
                tlv_box.addWidget(lp)
            lw = QtWidgets.QLabel(self.interface_lang['translation'] + ': ' + '<b>' + translate + '</b>')
            tlv_box.addWidget(lw)
            tlh_box = QtWidgets.QHBoxLayout()
            btn_close = QtWidgets.QPushButton(self.interface_lang['close'])
            btn_edit = QtWidgets.QPushButton(self.interface_lang['edit'])
            btn_edit.clicked.connect(lambda: edit_run(None, tl))
            btn_close.clicked.connect(lambda: tl_close(None, tl))
            tlh_box.addWidget(btn_edit)
            tlh_box.addWidget(btn_close)
            tlv_box.addLayout(tlh_box)
            tl.setLayout(tlv_box)
            tl.show()
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            key = key.split("\n")[0]
        phonetic_article = self.dw[key][1] if self.dw[key][7] == 1 else self.dw[key][2]
        translate = self.dw[key][3]
        form = self.dw[key][4]
        plural = self.dw[key][5]
        part_name = self.interface_lang[self.key_part_of_speech[self.dw[key][6]]]
        view()

    def on_training_mode(self):
        def on_choice():
            self.ch_value = cb_tm.currentIndex()
            self.log_flag = check_btn.checkState()
            if self.ch_value == 3:
                self.page = sp_box.value()
            tm.close()
            self.on_training()

        def pagination():
            self.ch_value = cb_tm.currentIndex()
            if self.ch_value == 3:
                if self.page_max < 2:
                    text = self.interface_lang['warn_not_enough_word_training']
                    QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'], text)
                    cb_tm.setCurrentIndex(0)
                    return
                cb_tm.setEnabled(False)
                sp_box.setValue(1)
                sp_box.setRange(1, self.page_max)
                tmv_box.insertWidget(1, sp_box)

        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_dict_not_loaded'])
            return
        if not self.dw:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>' + self.interface_lang['dict_empty'] + '</center>')
            self.vtop_t.addWidget(self.label3)
            return
        tm = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tm.setWindowTitle(self.interface_lang['training_choice'])
        tm.resize(250, 80)
        self.mode_tr = [self.interface_lang['mode_random_choice'],
                        self.interface_lang['mode_last_20'],
                        self.interface_lang['mode_last_40'],
                        self.interface_lang['mode_page']]
        tm.setWindowModality(QtCore.Qt.WindowModal)
        tmv_box = QtWidgets.QVBoxLayout()
        cb_tm = QtWidgets.QComboBox()
        cb_tm.addItems(self.mode_tr)
        cb_tm.currentIndexChanged.connect(pagination)
        sp_box = QtWidgets.QSpinBox()
        check_btn = QtWidgets.QCheckBox(self.interface_lang['write_to_log'])
        btn = QtWidgets.QPushButton(self.interface_lang['select'])
        btn.clicked.connect(on_choice)
        tmv_box.addWidget(cb_tm)
        if not self.cards_flag:
            tmv_box.addWidget(check_btn)
        tmv_box.addWidget(btn)
        tm.setLayout(tmv_box)
        tm.show()

    def on_training(self):
        def sort(x, flag=None):
            def sort_id(item):
                return item[0]
            if (len(self.new_name[0]) + len(list(self.dw.keys()))) < x+1:
                QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                              self.interface_lang['warn_not_enough_word_for_mode'])
            old_list = []
            for key in list(self.dw.keys()):
                if self.dw[key][0] != None:
                    old_list.append((self.dw[key][0], key))
            old_list.sort(key=sort_id)
            if not flag:
                if len(self.new_name[0]) >= x:
                    self.dw_key = self.new_name[0][-x:]
                else:
                    self.dw_key = self.new_name[0]
                    for item in old_list[-(x-len(self.new_name[0])):]:
                        self.dw_key.append(item[1])
            else:
                start = (self.page - 1)*40
                for item in old_list[start:start+40]:
                    self.dw_key.append(item[1])

        self.dw_key = []
        self.q_count = 0
        self.t_ans_count = 0
        if self.ch_value == 0:
            self.dw_key = list(self.dw.keys())
        elif self.ch_value == 1:
            sort(20)
        elif self.ch_value == 2:
            sort(40)
        else:
            sort(1, flag=1)
        if self.cards_flag:
            self.status.setText(self.interface_lang['mode_cards'])
            self.cards()
        else:
            self.status.setText(self.interface_lang['mode_training'])
            self.start_training = time.time()
            random.shuffle(self.dw_key) # перемешать ключи
            self.on_run()

    def on_result(self):
        self.clear()
        self.stop_training = time.time()
        str_training_time = self.training_time(self.start_training, self.stop_training)
        label_time_header = QtWidgets.QLabel('<center><b>' + self.interface_lang['training_time'] + '</b></center>')
        label_time_value = QtWidgets.QLabel('<center>' + str_training_time + '</center>')
        label_time_value.setStyleSheet("color:darkBlue")
        label_question = QtWidgets.QLabel('<center><b>' + self.interface_lang['questions'] + '</b></center>')
        label_question_count = QtWidgets.QLabel('<center>' + str(self.q_count) + '</center>')
        label_true_answer = QtWidgets.QLabel('<center><b>' + self.interface_lang['true_answers'] + '</b></center>')
        label_true_answer_count = QtWidgets.QLabel('<center>' + str(self.t_ans_count) + '</center>')
        label_true_answer_count.setStyleSheet("color:green")
        label_false_answer = QtWidgets.QLabel('<center><b>' + self.interface_lang['wrong_answers'] + '</b></center>')
        label_false_answer_count = QtWidgets.QLabel('<center>' + str(self.q_count - self.t_ans_count) + '</center>')
        label_false_answer_count.setStyleSheet("color:red")
        for i in (label_time_header, label_time_value, label_question, label_question_count,
                  label_true_answer, label_true_answer_count, label_false_answer, label_false_answer_count):
            self.vtop_t.addWidget(i)
        self.horizont_line(self.vtop_t)
        if self.t_ans_count >= 0.8*self.q_count:
            result_estimate = self.interface_lang['good_work']
            img = 'super148.png'
        elif self.t_ans_count < 0.4*self.q_count:
            result_estimate = self.interface_lang['worse_work']
            img = 'worse148.png'
        else:
            result_estimate = self.interface_lang['bad_work']
            img = 'bad148.png'
        label_result_estimate = QtWidgets.QLabel('<center><b>' + result_estimate + '</b></center>')
        self.vtop_t.addWidget(label_result_estimate)
        label_result_image = QtWidgets.QLabel()
        img_path = os.path.join(self.wd, img)
        label_result_image.setPixmap(QtGui.QPixmap(img_path))
        label_result_image.setAlignment(QtCore.Qt.AlignCenter)
        self.vtop_t.addWidget(label_result_image)
        if self.log_flag:
            self.training_log()

    def training_time(self, start, stop) -> str:
        seconds = int(stop - start)
        minutes = '0'
        if seconds > 60:
            minutes = seconds//60
            seconds = seconds%60
        return "%s %s %s %s" % (minutes, self.interface_lang['minutes'],
                                seconds, self.interface_lang['seconds'])

    def skip_word(self, word: str):
        self.dw_key.append(word)
        self.q_count -= 1
        self.on_run()

    def on_true_answer(self):
        self.clear()
        label_true = QtWidgets.QLabel('<center><b>True</b></center>')
        label_true.setStyleSheet("color:green")
        self.vtop_t.addWidget(label_true)
        self.on_answer()

    def on_false_answer(self):
        self.clear()
        label_false = QtWidgets.QLabel('<center><b>False</b></center>')
        label_false.setStyleSheet("color:red")
        label_false_answer = QtWidgets.QLabel('<center>' + self.answer + '</center>')
        label_false_answer.setStyleSheet("text-decoration:line-through")
        self.vtop_t.addWidget(label_false)
        self.vtop_t.addWidget(label_false_answer)
        self.on_answer()

    def on_answer(self):
        self.horizont_line(self.vtop_t)
        self.horizont_line(self.vtop_t)
        lk = QtWidgets.QLabel('<center><b>'+self.ask+'</b>'+' (<i>'+self.dw[self.ask][5]+'</i>)</center>')
        self.vtop_t.addWidget(lk)
        lfk = QtWidgets.QLabel('<center>['+self.dw[self.ask][1]+']</center>')
        self.vtop_t.addWidget(lfk)
        self.horizont_line(self.vtop_t)
        if self.dw[self.ask][3]:
            lf = QtWidgets.QLabel('<b>' + self.interface_lang['verb_forms'] + ': </b>'+self.dw[self.ask][3])
            self.vtop_t.addWidget(lf)
        if self.dw[self.ask][4]:
            lp = QtWidgets.QLabel('<b>' + self.interface_lang['plural'] + ': </b>'+self.dw[self.ask][4])
            self.vtop_t.addWidget(lp)
        lw = QtWidgets.QLabel('<b>' + self.interface_lang['translation'] + ': </b>'+self.dw[self.ask][2])
        self.vtop_t.addWidget(lw)
        btn_next = QtWidgets.QPushButton(self.interface_lang['next'], self)
        btn_next.setFocus()
        btn_next.clicked.connect(self.on_run)
        btn_next.setAutoDefault(True)
        btn_stop = QtWidgets.QPushButton(self.interface_lang['stop'], self)
        btn_stop.clicked.connect(self.on_result)
        self.htop_b.addWidget(btn_next)
        self.htop_b.addWidget(btn_stop)
        text = self.interface_lang['true_answers_questions'] + str(self.t_ans_count) + "/" + str(self.q_count)
        self.label_amount.setText(text)

    def training_log(self):
        log_path = os.path.join(self.root_dir, 'vokabelheftlogfile')
        file = open(log_path, 'a')
        lang = ' - ' + self.__class__.__name__[-1]
        page = ''
        if self.ch_value == 3: page = self.interface_lang['mode_page'] + ': ' + str(self.page)
        note = ['***' + time.asctime() + lang + '***',
                self.interface_lang['mode'] + self.mode_tr[self.ch_value],
                page,
                self.interface_lang['questions'] + ' ' + str(self.q_count),
                self.interface_lang['true_answers'] + ' ' + str(self.t_ans_count),
                self.interface_lang['wrong_answers'] + ' ' + str(self.q_count - self.t_ans_count), 34 * '*']
        for line in note:
            file.write(line + '\n')
        file.close()

    def cards_mode(self):
        self.cards_flag = 1
        self.on_training_mode()
        self.keys = []

    def choose_card(self):
        if self.dw_key:
            self.f_word = random.choice(self.dw_key)
            self.keys.append(self.f_word)
            self.dw_key.remove(self.f_word)
            self.f_f_word = self.dw[self.f_word][1]
            self.n_word = self.parse_word(self.dw[self.f_word][2])
            self.foreign = "<center><b>%s</b> [%s]</center>" % (self.f_word, self.f_f_word)
            self.native = "<center><b>%s</b></center>" % self.n_word
            self.card_toggle = 'f'
        else:
            result = QtWidgets.QMessageBox.question(None, self.interface_lang['warning'],
                                                    self.interface_lang['warn_cards_finished'],
                                                    buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    defaultButton=QtWidgets.QMessageBox.No)
            if result == 16384:
                self.dw_key = self.keys
                self.keys = []
                return
            self.tl_cr.close()

    def set_screen_values(self):
        width_s = self.desktop.width()
        k_sc = width_s/2560
        font_it = int(k_sc*32)
        self.str_len = int(k_sc*26)
        self.font_s = "font-size: %dpx" % font_it

    def parse_word(self, words):
        if len(words) > self.str_len:
            if words[self.str_len] not in [',', ';', ':', '.']:
                part_string = words[:self.str_len]
                splitter = []
                for i in [' ', ',', ';', ':', '.']:
                    ind = part_string.rfind(i)
                    splitter.append(ind)
                max_in = max(splitter)
            else:
                max_in = self.str_len + 1
            return words[:max_in] + '<br>' + self.parse_word(words[max_in:].strip())
        return words

    def cards(self):
        self.word_label = ClickedLabel()
        self.set_screen_values()
        self.word_label.setStyleSheet(self.font_s)
        self.choose_card()
        self.cards_view()
        self.cards_flag = 0

    def cards_view(self):
        def effect_animation(start=1.0, stop=0.0):
            effect = QtWidgets.QGraphicsOpacityEffect()
            self.word_label.setGraphicsEffect(effect)
            effect.setOpacity(start)
            animation = QtCore.QPropertyAnimation(effect, b"opacity")
            animation.setDuration(550)
            animation.setLoopCount(1)
            animation.setStartValue(start)
            animation.setEndValue(stop)
            return animation

        def lab_press():
            if not self.an_proc:
                self.an_proc = True
                self.dap = effect_animation()
                start_animation(self.dap)
        def appear():
            self.ap = effect_animation(start=0.0, stop=1.0)
            start_animation(self.ap)

        def start_animation(ef):
            ef.start()
            ef.finished.connect(new_label)

        def new_label():
            if self.toggle == 0:
                if self.card_toggle == 'f':
                    text = self.native
                    self.card_toggle = 'n'
                else:
                    text = self.foreign
                    self.card_toggle = 'f'
                self.word_label.setText(text)
                self.toggle += 1
                appear()
            elif self.toggle == 1:
                self.toggle -= 1
                self.an_proc = False

        def next_card():
            self.choose_card()
            self.word_label.setText(self.foreign)

        self.tl_cr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        self.tl_cr.setWindowTitle(self.interface_lang['card'])
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        self.tl_cr.setWindowModality(QtCore.Qt.WindowModal)
        self.tl_cr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.tl_cr.setMinimumSize(int(0.2*self.desktop.width()), int(0.2*self.desktop.height()))
        self.toggle = 0
        self.an_proc = False
        tl_cr_box = QtWidgets.QVBoxLayout()
        tl_cr_box.addWidget(frame, stretch=10)
        word_box = QtWidgets.QVBoxLayout()
        frame.setLayout(word_box)
        btn_box = QtWidgets.QHBoxLayout()
        tip_box = QtWidgets.QHBoxLayout()
        self.word_label.setText(self.foreign)
        self.word_label.clicked.connect(lab_press)
        word_box.addWidget(self.word_label, alignment=QtCore.Qt.AlignCenter)
        #tip_widget = QtWidgets.QWidget()
        tip = QtWidgets.QLabel(self.interface_lang['rotate_card'])
        tip_label_img = QtWidgets.QLabel()
        img_path = os.path.join(self.wd, 'word_arrow24.png')
        tip_label_img.setPixmap(QtGui.QPixmap(img_path))
        tip_box.addWidget(tip)
        tip_box.addWidget(tip_label_img)
        #tip_widget.setLayout(tipbox)
        btn_next = QtWidgets.QPushButton(self.interface_lang['next'])
        btn_stop = QtWidgets.QPushButton(self.interface_lang['stop'])
        btn_stop.clicked.connect(self.tl_cr.close)
        btn_next.clicked.connect(next_card)
        #tip_box.addWidget(tip)
        btn_box.addWidget(btn_next)
        btn_box.addWidget(btn_stop)
        ####tl_crbox.addLayout(word_box, stretch=10)
        tl_cr_box.addLayout(btn_box)
        tl_cr_box.addLayout(tip_box)
        self.tl_cr.setLayout(tl_cr_box)
        self.tl_cr.show()

    def edit_dict(self):
        if not self.dw:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['dict_empty'])
            return
        self.dict_view(flag=1)
        self.status.setText(self.interface_lang['mode_edit'])
        for i in ((self.interface_lang['add'], self.on_add),
                (self.interface_lang['change'], self.on_edit),
                (self.interface_lang['delete'], self.on_delete)):
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1])
            self.htop_b.addWidget(btn)

    def on_edit(self):
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            if isinstance(key, str):
                key = key.split("\n")[0]
        try:
            phonetic_article = self.dw[key][1] if self.dw[key][-1] == 1 else self.dw[key][2]
            new = ((key,) + (phonetic_article,) + (self.dw[key][3],) +
                   (self.dw[key][4],) + (self.dw[key][5],) + (self.dw[key][6],))
        except KeyError:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_not_selected_word'])
            return
        self.on_add(None, new, flag=1)
        self.search_flag = 0

    def on_search(self):
        self.on_sign_flag = 2
        # if not self.dict_name:
        #     QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
        #                                   self.interface_lang['warn_dict_not_loaded'])
        #     self.on_sign_flag = 0
        #     return None, None
        if not self.dw:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>' + self.interface_lang['dict_empty'] + '</center>')
            self.vtop_t.addWidget(self.label3)
            self.on_sign_flag = 0
            return None, None

        def on_find():
            value = self.se.text()
            if value == '':
                QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                              self.interface_lang['warn_values_not_entered'])
            else:
                if value not in list(self.dw.keys()):
                    QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                                  self.interface_lang['warn_word_not_in_dict'])
                else:
                    self.search_flag = 1
                    self.search_key = value
                    self.display_word()
                    sr_close()

        def sr_close():
            self.status.setText(text)
            self.on_sign_flag = 0
            sr.close()

        text = self.status.text()
        self.status.setText(self.interface_lang['mode_search'])
        sr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        sr.setWindowTitle(self.interface_lang['search'])
        sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        srv_box = QtWidgets.QVBoxLayout()
        sl = QtWidgets.QLabel(self.interface_lang['type_search_word'])
        self.se = QtWidgets.QLineEdit()
        srh_box = QtWidgets.QHBoxLayout()
        btn1 = QtWidgets.QPushButton(self.interface_lang['find'])
        btn2 = QtWidgets.QPushButton(self.interface_lang['close'])
        btn1.clicked.connect(on_find)
        btn2.clicked.connect(sr_close)
        btn1.setAutoDefault(True) # enter
        self.se.returnPressed.connect(btn1.click) #enter
        srh_box.addWidget(btn1)
        srh_box.addWidget(btn2)
        srv_box.addWidget(sl)
        srv_box.addWidget(self.se)
        srv_box.addLayout(srh_box)
        sr.setLayout(srv_box)
        #sr.show() # запускается в подклассах
        return sr, srh_box

    def on_delete(self):
        key = self.lv.currentIndex().data()
        if not key:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_not_selected_record'])
            return
        key = key.split("\n")[0]
        self.del_name.append(self.dw[key][0])
        self.dw.pop(key)
        QtWidgets.QMessageBox.information(None, self.interface_lang['info'],
                                          self.interface_lang['record_deleted'] + key)
        self.clear()
        self.edit_dict()
        