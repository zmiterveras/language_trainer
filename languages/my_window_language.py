#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115, C0103, C0116, C0321, C0301
# pylint: disable=W0201

import os
import random
import time
from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from utils.utils import firstScreensaver
from utils.utils import ClickedLabel
from utils.utils import simpleView


class MyWindowLanguage(QtWidgets.QWidget):
    def __init__(self, desktop, root_dir, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.dict_name = ''
        self.dw = {}
        self.desktop = desktop
        self.root_dir = root_dir
        self.search_flag = 0
        self.cards_flag = 0
        self.search_key = 0
        self.page_max = 0
        self.lst1 = [1, 2, 3, 4, 5]
        self.lst2 = ['существительное', 'глагол', 'прилагательное', 'наречие', 'другое']
        self.wd = os.path.join(self.root_dir, 'images')
        self.status = QtWidgets.QLabel()
        self.makeWidget()
        self.saveValues()
        self.statusW()

    def statusW(self):
        self.st = QtWidgets.QWidget()
        stbox = QtWidgets.QHBoxLayout()
        self.label_am = QtWidgets.QLabel()
        self.label_flag = QtWidgets.QLabel()
        stbox.addWidget(self.label_am)
        stbox.addWidget(self.label_flag)
        self.st.setLayout(stbox)

    def saveValues(self):
        self.newname = [[], [], [], [], [], []]
        self.delname = []
        self.changenote = [[], [], [], [], [], [], []]

    def makeWidget(self):
        text = '''<center>Откройте или создайте словарь</center>\n
        <center>Используйте меню:</center>\n
        <center><b>"Файл"</b></center>'''
        self.vbox = QtWidgets.QVBoxLayout()
        self.vtop = QtWidgets.QVBoxLayout()
        self.vtop_t = QtWidgets.QVBoxLayout()
        ss = firstScreensaver(self.wd, text, flag=1)
        self.vtop_t.addWidget(ss)
        self.htop_b = QtWidgets.QHBoxLayout()
        self.vtop.addLayout(self.vtop_t)
        self.vtop.addLayout(self.htop_b)
        self.hbox = QtWidgets.QHBoxLayout()
        btnnames = [('Просмотр', self.dictView), ('Тренировка', self.onTrenningMode),
                    ('Поиск', self.onSearch), ('Редакт.', self.editDict)]
        btnlist = []
        for i in btnnames:
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1])
            self.hbox.addWidget(btn)
            btnlist.append(btn)
        self.btncl = QtWidgets.QPushButton('Закрыть')
        self.hbox.addWidget(self.btncl)
        self.vbox.addLayout(self.vtop)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def saveDict(self):
        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбран словарь')#######
            return
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(self.dict_name)
        conn.open()
        query = QtSql.QSqlQuery()
        #удаление
        if self.delname:
            query.prepare('delete from dic where id=:i')
            query.bindValue(':i', self.delname)
            query.execBatch()
            query.clear()
        #добавление
        if self.newname[0]:
            querystr = '''insert into dic values (null, :key, :keyfon, :word, :form,
                                            :plural, :partnumber)'''
            query.prepare(querystr)
            query.bindValue(':key', self.newname[0])
            query.bindValue(':keyfon', self.newname[1])
            query.bindValue(':word', self.newname[2])
            query.bindValue(':form', self.newname[3])
            query.bindValue(':plural', self.newname[4])
            query.bindValue(':partnumber', self.newname[5])
            query.execBatch()
            query.clear()
        #изменение
        if self.changenote[0]:
            querystr_ = '''update dic set key=:key, keyfon=:keyfon, word=:word, form=:form,
                    plural=:plural, partnumber=:partnumber where id=:id'''
            query.prepare(querystr_)
            query.bindValue(':key', self.changenote[1])
            query.bindValue(':keyfon', self.changenote[2])
            query.bindValue(':word', self.changenote[3])
            query.bindValue(':form', self.changenote[4])
            query.bindValue(':plural', self.changenote[5])
            query.bindValue(':partnumber', self.changenote[6])
            query.bindValue(':id', self.changenote[0])
            query.execBatch()
        conn.close()
        self.saveValues()

    def clear(self):
        for i in reversed(range(self.vtop_t.count())):
            wt = self.vtop_t.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()
        for i in reversed(range(self.htop_b.count())):
            wb = self.htop_b.itemAt(i).widget()
            wb.setParent(None)
            wb.deleteLater()

    def dictView(self, flag=None):
        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Словарь не загружен')
            return
        place = self.vtop_t
        self.clear()
        if not self.dw:
            self.label1 = QtWidgets.QLabel('<center>Словарь пуст</center>')
            place.addWidget(self.label1)
        else:
            self.status.setText('Режим: просмотр')
            # dic = list(self.dw.keys())
            dic = simpleView(self.dw)
            self.listBox(dic, flag, place)

    def listBox(self, dic, flag, place):
        self.lv = QtWidgets.QListView()
        slm = QtCore.QStringListModel(dic)
        self.lv.setModel(slm)
        place.addWidget(self.lv)
        amount = str(len(dic))
        text = '<center>Слов в словаре: <b>' + amount + '</b></center>'
        if flag != 2: self.label_am.setText(text)
        if not flag:
            self.lv.doubleClicked.connect(self.viewWord)
        elif flag == 1:
            self.lv.doubleClicked.connect(self.onEdItemRun)
        else:
            pass

    def viewWord(self, void):
        self.displayWord()

    def onEdItemRun(self, void):
        self.onEdItem()

    def hLine(self, box):
        fr = QtWidgets.QFrame()
        fr.setFrameShape(QtWidgets.QFrame.HLine)
        box.addWidget(fr)

    def displayWord(self):
        def editRun(void, win):
            tlClose(None, win, flag=1)
            self.onEdItem()

        def tlClose(void, win, flag=None):
            if not flag:
                self.search_flag = 0
            win.close()

        def view():
            tl = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
            tl.setWindowTitle('View')
            tl.setWindowModality(QtCore.Qt.WindowModal)
            tl.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            tlvbox = QtWidgets.QVBoxLayout()
            lk = QtWidgets.QLabel('<center><b>'+key+'</b>'+' (<i>'+partname+'</i>)</center>')
            tlvbox.addWidget(lk)
            lfk = QtWidgets.QLabel('<center>['+keyfon+']</center>')
            tlvbox.addWidget(lfk)
            self.hLine(tlvbox)
            if form:
                lf = QtWidgets.QLabel('<b>Формы глагола: </b>'+form)
                tlvbox.addWidget(lf)
            if plural:
                lp = QtWidgets.QLabel('<b>Мн.число: </b>'+plural)
                tlvbox.addWidget(lp)
            lw = QtWidgets.QLabel('<b>Перевод: </b>'+word)
            tlvbox.addWidget(lw)
            tlhbox = QtWidgets.QHBoxLayout()
            btnc = QtWidgets.QPushButton('Закрыть')
            btne = QtWidgets.QPushButton('Редактировать')
            btne.clicked.connect(lambda: editRun(None, tl))
            btnc.clicked.connect(lambda: tlClose(None, tl))
            tlhbox.addWidget(btne)
            tlhbox.addWidget(btnc)
            tlvbox.addLayout(tlhbox)
            tl.setLayout(tlvbox)
            tl.show()
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            key = key.split("\n")[0]
        keyfon = self.dw[key][1]
        word = self.dw[key][2]
        form = self.dw[key][3]
        plural = self.dw[key][4]
        partname = self.dw[key][5]
        view()

    def onTrenningMode(self):
        def onChoice():
            self.ch_value = cb_tm.currentIndex()
            self.log_flag = checkbtn.checkState()
            if self.ch_value == 3:
                self.page = sp_box.value()
            tm.close()
            self.onTrenning()

        def pagenation():
            self.ch_value = cb_tm.currentIndex()
            if self.ch_value == 3:
                if self.page_max < 2:
                    text = 'Не достаточно слов для постраничного режима\nИспользуйте другой режим тренировки!'
                    QtWidgets.QMessageBox.warning(None, 'Предупреждение', text)
                    cb_tm.setCurrentIndex(0)
                    return
                cb_tm.setEnabled(False)
                sp_box.setValue(1)
                sp_box.setRange(1, self.page_max)
                tmvbox.insertWidget(1, sp_box)

        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Словарь не загружен')
            return
        if not self.dw:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>Словарь пуст</center>')
            self.vtop_t.addWidget(self.label3)
            return
        tm = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tm.setWindowTitle('Выбор тренировки')
        tm.resize(250, 80)
        self.mode_tr = ['Случайный выбор', 'Последние 20', 'Последние 40', 'Страница']
        tm.setWindowModality(QtCore.Qt.WindowModal)
        tmvbox = QtWidgets.QVBoxLayout()
        cb_tm = QtWidgets.QComboBox()
        cb_tm.addItems(self.mode_tr)
        cb_tm.currentIndexChanged.connect(pagenation)
        sp_box = QtWidgets.QSpinBox()
        checkbtn = QtWidgets.QCheckBox('Записать результаты в логфайл')
        btn = QtWidgets.QPushButton('Выбрать')
        btn.clicked.connect(onChoice)
        tmvbox.addWidget(cb_tm)
        if not self.cards_flag:
            tmvbox.addWidget(checkbtn)
        tmvbox.addWidget(btn)
        tm.setLayout(tmvbox)
        tm.show()

    def onTrenning(self):
        def sort(x, flag=None):
            def sortid(item):
                return item[0]
            if (len(self.newname[0]) + len(list(self.dw.keys()))) < x+1:
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не достаточно слов для данного режима тренировки\n' +
                                              'Текущая тренировка будет не полной!')
            oldlist = []
            for key in list(self.dw.keys()):
                if self.dw[key][0] != None:
                    oldlist.append((self.dw[key][0], key))
            oldlist.sort(key=sortid)
            if not flag:
                if len(self.newname[0]) >= x:
                    self.dw_key = self.newname[0][-x:]
                else:
                    self.dw_key = self.newname[0]
                    for item in oldlist[-(x-len(self.newname[0])):]:
                        self.dw_key.append(item[1])
            else:
                start = (self.page - 1)*40
                for item in oldlist[start:start+40]:
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
            self.status.setText('Режим: карточки')
            self.cards()
        else:
            self.status.setText('Режим: тренировка')
            self.start_trenning = time.time()
            self.onRun()

    def onResult(self):
        self.clear()
        self.stop_trenning = time.time()
        str_trenning_time = self.trenning_time(self.start_trenning, self.stop_trenning)
        label_time = QtWidgets.QLabel('<center><b>Время тренировки составило:</b></center>')
        label_time_t = QtWidgets.QLabel('<center>' + str_trenning_time + '</center>')
        label_time_t.setStyleSheet("color:darkBlue")
        label_rq = QtWidgets.QLabel('<center><b>Задано вопросов:</b></center>')
        label_rqq = QtWidgets.QLabel('<center>' + str(self.q_count) + '</center>')
        label_rta = QtWidgets.QLabel('<center><b>Получено правильных ответов:</b></center>')
        label_rtaa = QtWidgets.QLabel('<center>' + str(self.t_ans_count) + '</center>')
        label_rtaa.setStyleSheet("color:green")
        label_rfa = QtWidgets.QLabel('<center><b>Получено неправильных ответов:</b></center>')
        label_rfaa = QtWidgets.QLabel('<center>' + str(self.q_count - self.t_ans_count) + '</center>')
        label_rfaa.setStyleSheet("color:red")
        for i in (label_time, label_time_t, label_rq, label_rqq, label_rta, label_rtaa, label_rfa, label_rfaa):
            self.vtop_t.addWidget(i)
        self.hLine(self.vtop_t)
        if self.t_ans_count >= 0.8*self.q_count:
            rr = 'Хорошая работа!!!'
            img = 'super148.png'
        elif self.t_ans_count < 0.4*self.q_count:
            rr = 'Это никуда не годится('
            img = 'worse148.png'
        else:
            rr = 'Нужно поднажать)'
            img = 'bad148.png'
        label_rr = QtWidgets.QLabel('<center><b>' + rr + '</b></center>')
        self.vtop_t.addWidget(label_rr)
        label_rim = QtWidgets.QLabel()
        img_path = os.path.join(self.wd, img)
        label_rim.setPixmap(QtGui.QPixmap(img_path))
        label_rim.setAlignment(QtCore.Qt.AlignCenter)
        self.vtop_t.addWidget(label_rim)
        if self.log_flag:
            self.treningLog()

    def trenning_time(self, start, stop):
        seconds = int(stop -start)
        minutes = '0'
        if seconds > 60:
            minutes = seconds//60
            seconds = seconds%60
        return "%s %s %s %s" % (minutes, 'минут', seconds, 'секунд')

    def onTrueAnswer(self):
        self.clear()
        label_ta = QtWidgets.QLabel('<center><b>True</b></center>')
        label_ta.setStyleSheet("color:green")
        self.vtop_t.addWidget(label_ta)
        self.onAnswer()

    def onFalseAnswer(self):
        self.clear()
        label_fa = QtWidgets.QLabel('<center><b>False</b></center>')
        label_fa.setStyleSheet("color:red")
        label_faa = QtWidgets.QLabel('<center>' + self.ch + '</center>')
        label_faa.setStyleSheet("text-decoration:line-through")
        self.vtop_t.addWidget(label_fa)
        self.vtop_t.addWidget(label_faa)
        self.onAnswer()

    def onAnswer(self):
        self.hLine(self.vtop_t)
        self.hLine(self.vtop_t)
        lk = QtWidgets.QLabel('<center><b>'+self.ask+'</b>'+' (<i>'+self.dw[self.ask][5]+'</i>)</center>')
        self.vtop_t.addWidget(lk)
        lfk = QtWidgets.QLabel('<center>['+self.dw[self.ask][1]+']</center>')
        self.vtop_t.addWidget(lfk)
        self.hLine(self.vtop_t)
        if self.dw[self.ask][3]:
            lf = QtWidgets.QLabel('<b>Формы глагола: </b>'+self.dw[self.ask][3])
            self.vtop_t.addWidget(lf)
        if self.dw[self.ask][4]:
            lp = QtWidgets.QLabel('<b>Мн.число: </b>'+self.dw[self.ask][4])
            self.vtop_t.addWidget(lp)
        lw = QtWidgets.QLabel('<b>Перевод: </b>'+self.dw[self.ask][2])
        self.vtop_t.addWidget(lw)
        btnc = QtWidgets.QPushButton('Продолжить', self)
        btnc.setFocus()
        btnc.clicked.connect(self.onRun)
        btnc.setAutoDefault(True)
        btns = QtWidgets.QPushButton('Стоп', self)
        btns.clicked.connect(self.onResult)
        self.htop_b.addWidget(btnc)
        self.htop_b.addWidget(btns)
        text = "Правильных ответов/вопросов: " + str(self.t_ans_count) + "/" + str(self.q_count)
        self.label_am.setText(text)

    def treningLog(self):
        log_path = os.path.join(self.root_dir, 'vokabelheftlogfile')
        file = open(log_path, 'a')
        lang = ' - ' + self.__class__.__name__[-1]
        page = ''
        if self.ch_value == 3: page = 'Страница: ' + str(self.page)
        note = ['***' + time.asctime() + lang + '***', 'Режим: ' + self.mode_tr[self.ch_value], page,
                'Задано вопросов: ' + str(self.q_count), 'Правильных ответов: ' + str(self.t_ans_count),
                'Неправильных ответов: ' + str(self.q_count - self.t_ans_count), 34 * '*']
        for line in note:
            file.write(line + '\n')
        file.close()

    def cardsMode(self):
        self.cards_flag = 1
        self.onTrenningMode()
        self.keys = []

    def chooseCard(self):
        if self.dw_key:
            self.f_word = random.choice(self.dw_key)
            self.keys.append(self.f_word)
            self.dw_key.remove(self.f_word)
            self.f_f_word = self.dw[self.f_word][1]
            self.n_word = self.parseWord(self.dw[self.f_word][2])
            self.foregn = "<center><b>%s</b> [%s]</center>" % (self.f_word, self.f_f_word)
            self.native = "<center><b>%s</b></center>" % self.n_word
            self.card_toggle = 'f'
        else:
            result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                    'Карточки закончены. Хотите повторить?',
                                                    buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    defaultButton=QtWidgets.QMessageBox.No)
            if result == 16384:
                self.dw_key = self.keys
                self.keys = []
                return
            self.tl_cr.close()

    def setScreenValues(self):
        width_s = self.desktop.width()
        k_sc = width_s/2560
        font_it = int(k_sc*32)
        self.str_len = int(k_sc*26)
        self.font_s = "font-size: %dpx" % font_it

    def parseWord(self, words):
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
            return words[:max_in] + '<br>' + self.parseWord(words[max_in:].strip())
        return words

    def cards(self):
        self.word_label = ClickedLabel()
        self.setScreenValues()
        self.word_label.setStyleSheet(self.font_s)
        self.chooseCard()
        self.cardsView()
        self.cards_flag = 0

    def cardsView(self):
        def effectAnimation(start=1.0, stop=0.0):
            effect = QtWidgets.QGraphicsOpacityEffect()
            self.word_label.setGraphicsEffect(effect)
            effect.setOpacity(start)
            an = QtCore.QPropertyAnimation(effect, b"opacity")
            an.setDuration(750)
            an.setLoopCount(1)
            an.setStartValue(start)
            an.setEndValue(stop)
            return an

        def labPress():
            if not self.an_proc:
                self.an_proc = True
                self.dap = effectAnimation()
                startAnimation(self.dap)
        def appear():
            self.ap = effectAnimation(start=0.0, stop=1.0)
            startAnimation(self.ap)

        def startAnimation(ef):
            ef.start()
            ef.finished.connect(newLabel)

        def newLabel():
            if self.toggle == 0:
                if self.card_toggle == 'f':
                    text = self.native
                    self.card_toggle = 'n'
                else:
                    text = self.foregn
                    self.card_toggle = 'f'
                self.word_label.setText(text)
                #time.sleep(2)
                self.toggle += 1
                appear()
            elif self.toggle == 1:
                self.toggle -= 1
                self.an_proc = False

        def nextCard():
            self.chooseCard()
            self.word_label.setText(self.foregn)

        self.tl_cr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        self.tl_cr.setWindowTitle('Карточка')
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        self.tl_cr.setWindowModality(QtCore.Qt.WindowModal)
        self.tl_cr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.tl_cr.setMinimumSize(int(0.2*self.desktop.width()), int(0.2*self.desktop.height()))
        self.toggle = 0
        self.an_proc = False
        tl_crbox = QtWidgets.QVBoxLayout()
        tl_crbox.addWidget(frame, stretch=10)
        word_box = QtWidgets.QVBoxLayout()
        frame.setLayout(word_box)
        btn_box = QtWidgets.QHBoxLayout()
        tip_box = QtWidgets.QHBoxLayout()
        self.word_label.setText(self.foregn)
        self.word_label.clicked.connect(labPress)
        word_box.addWidget(self.word_label, alignment=QtCore.Qt.AlignCenter)
        #tip_widget = QtWidgets.QWidget()
        tip = QtWidgets.QLabel("Для поворота карточки кликните по слову:")
        tip_label_img = QtWidgets.QLabel()
        img_path = os.path.join(self.wd, 'word_arrow24.png')
        tip_label_img.setPixmap(QtGui.QPixmap(img_path))
        tip_box.addWidget(tip)
        tip_box.addWidget(tip_label_img)
        #tip_widget.setLayout(tipbox)
        btn_next = QtWidgets.QPushButton('Продолжить')
        btn_stop = QtWidgets.QPushButton('Стоп')
        btn_stop.clicked.connect(self.tl_cr.close)
        btn_next.clicked.connect(nextCard)
        #tip_box.addWidget(tip)
        btn_box.addWidget(btn_next)
        btn_box.addWidget(btn_stop)
        ####tl_crbox.addLayout(word_box, stretch=10)
        tl_crbox.addLayout(btn_box)
        tl_crbox.addLayout(tip_box)
        self.tl_cr.setLayout(tl_crbox)
        self.tl_cr.show()

    def editDict(self):
        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Словарь не загружен')
            return
        self.dictView(flag=1)
        self.status.setText('Режим: редактирование')
        for i in (('Добавить', self.onAdd), ('Изменить', self.onEdItem), ('Удалить', self.onDelete)):
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1])
            self.htop_b.addWidget(btn)

    def onEdItem(self):
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            key = key.split("\n")[0]
        try:
            new = (key,) + (self.dw[key][1],) + (self.dw[key][2],) + (self.dw[key][3],) + (self.dw[key][4],) + (self.dw[key][5],)
        except KeyError:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбрано слово')
            return
        self.onAdd(None, new, flag=1)
        self.search_flag = 0

    def onSearch(self):
        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Словарь не загружен')
            return None
        if not self.dw:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>Словарь пуст</center>')
            self.vtop_t.addWidget(self.label3)
            return None

        def onFind():
            value = self.se.text()
            if value == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
            else:
                if value not in list(self.dw.keys()):
                    QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Данного слова нет в словаре')
                else:
                    self.search_flag = 1
                    self.search_key = value
                    self.displayWord()
                    srClose()

        def srClose():
            self.status.setText(text)
            sr.close()

        text = self.status.text()
        self.status.setText('Режим: поиск')
        sr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        sr.setWindowTitle('Поиск')
        sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        srvbox = QtWidgets.QVBoxLayout()
        sl = QtWidgets.QLabel('Введите искомое слово(иност.)')
        self.se = QtWidgets.QLineEdit()
        srhbox = QtWidgets.QHBoxLayout()
        btn1 = QtWidgets.QPushButton('Найти')
        btn2 = QtWidgets.QPushButton('Закрыть')
        btn1.clicked.connect(onFind)
        btn2.clicked.connect(srClose)
        btn1.setAutoDefault(True) # enter
        self.se.returnPressed.connect(btn1.click) #enter
        srhbox.addWidget(btn1)
        srhbox.addWidget(btn2)
        srvbox.addWidget(sl)
        srvbox.addWidget(self.se)
        srvbox.addLayout(srhbox)
        sr.setLayout(srvbox)
        #sr.show()
        return sr, srhbox

    def onDelete(self):
        key = self.lv.currentIndex().data()
        if not key:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбрана запись для удаления')
            return
        self.delname.append(self.dw[key][0])
        self.dw.pop(key)
        QtWidgets.QMessageBox.information(None, 'Инфо', 'Удалена запись: '+key)
        self.clear()
        self.editDict()
        