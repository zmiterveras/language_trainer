#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#v4
# pylint: disable=C0115, C0103, C0116, C0321, C0301, C0410
# pylint: disable=W0201
# pylint: disable=R0201, R0914, R0902

import sys,sqlite3, os
from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
from languages.eng_language import MyWindowE
from languages.de_language import MyWindowD
from menulanguages import MenuLanguages
from utils.utils import firstScreensaver


settings = QtCore.QSettings("@zmv", "Vokabelheft")
if settings.contains("Language"):
    menu_language = settings.value("Language")
else:
    menu_language = 'en'
    settings.setValue("Language", menu_language)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.version = '''4.21.1, 2024г.'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.wp = os.path.join(self.app_dir, 'images')
        self.bases = os.path.join(self.app_dir, 'bases')
        ico_path = os.path.join(self.wp, 'dic.png')
        ico = QtGui.QIcon(ico_path)
        self.setWindowIcon(ico)
        self.setInterfaceLanguage(menu_language)
        self.count = 1
        self.sort = 1
        self.view_page = False
        # text_ch = """<center>Выберите изучаемый язык</center>\n
        # <center>Используйте меню:</center>\n
        # <center><b>"Язык"</b></center>"""
        # text_ch = self.interface_lang["set_lang"]
        # self.win = firstScreensaver(self.wp, text_ch) #self.firstScreensaver(self.wp, text_ch)
        # self.setCentralWidget(self.win)
        self.setScreenSaver(self.interface_lang["set_lang"])
        menuBar = self.menuBar()
        self.makeMenu(menuBar)
        # myMenu = menuBar.addMenu('&Файл')
        # #action = myMenu.addAction('Test',  self.test)
        # myLang = menuBar.addMenu('&Язык')
        # myLang.addAction('English', lambda x=1: self.langChoose(x, myMenu, myView))
        # myLang.addAction('Deutsch', lambda x=2: self.langChoose(x, myMenu, myView))
        # myView = menuBar.addMenu('Просмотр')
        # myView.addAction('Просмотр логфайла', self.viewLogfile)
        # myAbout = menuBar.addMenu('О...')
        # myAbout.addAction('О программе', self.aboutProgramm)
        # myAbout.addAction('Обо мне', self.aboutMe)
        self.statusBar = self.statusBar()

    def setScreenSaver(self, text):
        self.win = firstScreensaver(self.wp, text) #self.firstScreensaver(self.wp, text_ch)
        self.setCentralWidget(self.win)

    def makeMenu(self, menuBar):
        myMenu = menuBar.addMenu('&' + self.interface_lang['file'])
        self.makeMyMenu(myMenu)
        #action = myMenu.addAction('Test',  self.test)
        myLang = menuBar.addMenu('&' + self.interface_lang['language'])
        myLang.addAction('English', lambda lang='en': self.langChoose(lang, myMenu, myView))
        myLang.addAction('Deutsch', lambda lang='de': self.langChoose(lang, myMenu, myView))
        myView = menuBar.addMenu(self.interface_lang['viewing'])
        self.makeMyView(myView)
        mySettings = menuBar.addMenu(self.interface_lang['settings'])
        mySettings.addSection('Menu language')
        mySettings.addAction(self.icon_eng, 'english', lambda ln='en': self.changeInterfaceLanguage(ln, menuBar, myMenu, myView))
        mySettings.addAction(self.icon_ru, 'русский', lambda ln='ru': self.changeInterfaceLanguage(ln, menuBar, myMenu, myView))
        mySettings.addSeparator()
        myAbout = menuBar.addMenu(self.interface_lang['about'])
        myAbout.addAction('О программе', self.aboutProgramm)
        myAbout.addAction('Обо мне', self.aboutMe)

    def makeMyMenu(self, myMenu):
        if self.count != 1:
            myMenu.clear()
            myMenu.addAction('&Создать', self.createDict)
            myMenu.addAction('&Открыть', self.openDict)
            myMenu.addAction('Сохранить', self.win.saveDict)
        myMenu.addAction('&Закрыть', self.close)

    def makeMyView(self, myView):
        if self.count != 1:
            myView.clear()
            myView.addAction('Краткий просмотр', self.win.dictView)
            myView.addAction('&Полный просмотр', self.sortAll)
            myView.addAction('Просмотр карточек', self.win.cardsMode)
        myView.addAction('Просмотр логфайла', self.viewLogfile)

    def langChoose(self, variant, myMenu, myView):
        if self.count != 1:
            if not self.checkChange():
                return
        if variant == 'en':
            self.win = MyWindowE(desktop, self.app_dir, self.interface_lang)
            self.lang = variant
            flag_path = os.path.join(self.wp, 'gb_16.png')
            self.screen_path = os.path.join(self.wp, 'Dic_eng_148.png')
        else:
            self.win = MyWindowD(desktop, self.app_dir, self.interface_lang)
            self.lang = variant
            flag_path = os.path.join(self.wp, 'de_16.png')
            self.screen_path = os.path.join(self.wp, 'Dic_de_148.png')
        self.count += 1
        self.setCentralWidget(self.win)
        self.win.btncl.clicked.connect(self.close)
        self.makeMyMenu(myMenu)
        self.makeMyView(myView)
        # myMenu.addAction('&Создать', self.createDict)
        # myMenu.addAction('&Открыть', self.openDict)
        # myMenu.addAction('Сохранить', self.win.saveDict)
        # myMenu.addAction('&Закрыть', self.close)
        # myView.addAction('Краткий просмотр', self.win.dictView)
        # myView.addAction('&Полный просмотр', self.sortAll)
        # myView.addAction('Просмотр карточек', self.win.cardsMode)
        # myView.addAction('Просмотр логфайла', self.viewLogfile)
        self.statusBar.addWidget(self.win.status)
        self.statusBar.addPermanentWidget(self.win.st)
        self.win.label_am.setText('Пусто')
        self.win.label_flag.setPixmap(QtGui.QPixmap(flag_path))
        self.win.label_flag.setAlignment(QtCore.Qt.AlignRight)

    def checkChange(self, flag=None):
        result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                'Вы действительно хотите открыть новый словарь?\n' +
                                                'Все несохранненые данные при этом будут потеряны.',
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
        if result == 16384:
            if flag == 1:
                self.win.label_am.setText(self.lang)
                self.win.status.setText('')
                self.win.saveValues()
                self.win.dw = {}
            else:
                self.statusBar.removeWidget(self.win.status)
                self.statusBar.removeWidget(self.win.st)
            return True
        return False

    def setInterfaceLanguage(self, language):
        self.setIcon(language)
        if language == 'en':
            self.interface_lang = MenuLanguages.eng
        else:
            self.interface_lang = MenuLanguages.rus
        settings.setValue("Language", language)

    def setIcon(self, language):
        icon_checkmark = QtGui.QIcon(os.path.join(self.wp,'galochka_16.png'))
        icon_minus = QtGui.QIcon(os.path.join(self.wp, 'minus_16.png'))
        if language == 'en':
            self.icon_eng = icon_checkmark
            self.icon_ru = icon_minus
        elif language == 'ru':
            self.icon_eng = icon_minus
            self.icon_ru = icon_checkmark

    def saveInstanceState(self):
        self.win.saveDict()
        name = self.win.dict_name
        return name

    def restoreInstanceState(self):
        name = self.saveInstanceState()
        match self.lang:
            case 'en':
                self.win = MyWindowE(desktop, self.app_dir, self.interface_lang)
            case 'de':
                self.win = MyWindowD(desktop, self.app_dir, self.interface_lang)
        self.win.dict_name = name
        self.openDictBackground()
        self.win.dictView()
        self.setCentralWidget(self.win)
        self.win.btncl.clicked.connect(self.close)

    def changeInterfaceLanguage(self, language, menuBar, myMenu, myView):
        self.setInterfaceLanguage(language)
        menuBar.clear()
        self.makeMenu(menuBar)
        if self.count > 1:
            self.makeMyMenu(myMenu)
            self.makeMyView(myView)
            self.restoreInstanceState()
        else:
            self.setScreenSaver(self.interface_lang["set_lang"])

    def createDict(self):
        s, ok = QtWidgets.QInputDialog.getText(None, 'Имя словаря', 'Введите имя словаря', text=self.lang + '_')
        if not ok: return
        if ok and not s:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не задано имя словаря')
            return
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        newdic = os.path.join(self.bases, s+'.sqlite')
        print(newdic)
        conn.setDatabaseName(newdic)
        conn.open()
        if 'dic' not in conn.tables():
            query = QtSql.QSqlQuery()
            querystr = '''create table dic (id integer primary key autoincrement,
            key text, keyfon text, word text, form text, plural text ,partnumber integer)'''
            query.exec(querystr)
        if 'part' not in conn.tables():
            query.clear()
            querystr_ = """create table part (id integer primary key autoincrement,
            partnumber integer, partname text)"""
            query.exec(querystr_)
            query.clear()
            query.prepare('insert into part values (null, :count, :name)')
            query.bindValue(':count', self.win.lst1)
            query.bindValue(':name', self.win.lst2)
            query.execBatch()
        conn.close()
        self.win.clear()
        self.label_cr = QtWidgets.QLabel('<center>Создан словарь: '+s+'</center>')
        self.win.vtop_t.addWidget(self.label_cr)

    def openDictBackground(self):
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(self.win.dict_name)
        conn.open()
        query = QtSql.QSqlQuery()
        query.exec(self.querystr)
        if query.isActive():
            query.first()
            while query.isValid():
                self.win.dw[query.value('key')] = [query.value('id'), query.value('keyfon'),
                                                    query.value('word'), query.value('form'),
                                                    query.value('plural'), query.value('partname')]
                query.next()
        conn.close()
        self.win.page_max = int(len(self.win.dw) / 40)

    def openDict(self):
        open_flag = 0
        if self.win.dict_name:
            if not self.checkChange(flag=1):
                return
        self.win.dict_name, void = QtWidgets.QFileDialog.getOpenFileName(None, caption='Открыть словарь',
                                                                         directory=self.bases, filter='DB (*.sqlite)')
        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбран словарь')
            return
        self.querystr = """select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural,
            part.partname from dic inner join part on dic.partnumber=part.partnumber
            """
        if open_flag == 0:
            self.openDictBackground()
            # conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            # conn.setDatabaseName(self.win.dict_name)
            # conn.open()
            # query = QtSql.QSqlQuery()
            # query.exec(querystr)
            # if query.isActive():
            #     query.first()
            #     while query.isValid():
            #         self.win.dw[query.value('key')] = [query.value('id'), query.value('keyfon'),
            #                                            query.value('word'), query.value('form'),
            #                                            query.value('plural'), query.value('partname')]
            #         query.next()
            # conn.close()
            # self.win.page_max = int(len(self.win.dw) / 40)
        else:
            conn = sqlite3.connect(self.win.dict_name)
            curs = conn.cursor()
            curs.execute(self.querystr)
            for row in curs.fetchall():
                self.win.dw[row[1]] = [row[0], row[2], row[3], row[4], row[5], row[6]]
            conn.close()

        last_name = os.path.basename(self.win.dict_name)
        self.win.clear()
        self.label2 = QtWidgets.QLabel('<center>Загружен словарь: '+last_name+'</center>')
        self.win.vtop_t.addWidget(self.label2)
        label_screen = QtWidgets.QLabel()
        label_screen.setPixmap(QtGui.QPixmap(self.screen_path))
        label_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.win.vtop_t.addWidget(label_screen)
        self.win.label_am.setText(self.lang)

    def sortAll(self):
        def saClose():
            sa.close()
            self.viewAll()

        def choosePage():
            self.view_page = True
            page = sp_box.value()
            self.start_page = (page-1) * 40
            saClose()

        def sortChoose():
            index = cb_sa.currentIndex()
            if index == 0:
                self.sort = 1
                saClose()
            elif index == 1:
                self.sort = 0
                saClose()
            elif index == 2:
                if self.win.page_max < 2:
                    text = 'Не достаточно слов для постраничного режима\nИспользуйте другой режим просмотра!'
                    QtWidgets.QMessageBox.warning(None, 'Предупреждение', text)
                    return
                cb_sa.setEnabled(False)
                sp_box.setRange(1, self.win.page_max)
                savbox.insertWidget(2, sp_box)
                btn.clicked.connect(choosePage)
            elif index == 3:
                if len(self.win.dw) <= 40:
                    self.start_page = 0
                else:
                    self.start_page = len(self.win.dw) - 40
                self.view_page = True
                saClose()

        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбран словарь')
            return
        sa = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        sa.setWindowTitle('Выбор отображения')
        sa.resize(250, 80)
        sa.setWindowModality(QtCore.Qt.WindowModal)
        savbox = QtWidgets.QVBoxLayout()
        savbox.addWidget(QtWidgets.QLabel('Выберите режим сортировки и отображения'))
        cb_sa = QtWidgets.QComboBox()
        cb_sa.addItems(['Всё по алфавиту', 'Всё постранично', 'Страница', 'Последние40'])
        sp_box = QtWidgets.QSpinBox()
        savbox.addWidget(cb_sa)
        btn = QtWidgets.QPushButton('Ok')
        btn.clicked.connect(sortChoose)
        savbox.addWidget(btn)
        sa.setLayout(savbox)
        sa.show()

    def viewAll(self):
        if not self.win.dw:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Cловарь пуст')
            return
        tabview = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(self.win.dict_name)
        conn.open()
        if not self.view_page:
            stm = QtSql.QSqlRelationalTableModel(parent=window)
            stm.setTable('dic')
            stm.setRelation(6, QtSql.QSqlRelation('part', 'partnumber', 'partname'))
            stm.setSort(self.sort, QtCore.Qt.AscendingOrder)
            stm.select()
        else:
            stm = QtSql.QSqlQueryModel(parent=window)
            query = '''select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural, part.partname
            from dic inner join part on dic.partnumber=part.partnumber limit 40 offset %d''' % self.start_page
            stm.setQuery(query)
            stm.sort(self.sort, QtCore.Qt.AscendingOrder)
            self.view_page = False
        var_names = ['Фонетика', 'Арт-ль']
        if self.lang == 'de':
            var_name = var_names[1]
            l_1, l_2, l_4, l_5 = 160, 50, 180, 45
        else:
            var_name = var_names[0]
            l_1, l_2, l_4, l_5 = 100, 100, 150, 75
        for i, n in ((1, 'Слово'), (2, var_name), (3, 'Перевод'), (4, 'Формы глагола'), (5, 'Мн.ч-ло'), (6, 'Часть речи')):
            stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        vbox = QtWidgets.QVBoxLayout()
        tv = QtWidgets.QTableView()
        tv.setModel(stm)
        tv.hideColumn(0)
        for i, n in ((1, l_1), (2, l_2), (3, 300), (4, l_4), (5, l_5), (6, 150)):
            tv.setColumnWidth(i, n)
        vbox.addWidget(tv)
        btncl = QtWidgets.QPushButton('Закрыть')
        btncl.clicked.connect(tabview.close)
        vbox.addWidget(btncl)
        tabview.setLayout(vbox)
        tabview.resize(915, 350)
        tabview.show()

    def viewLogfile(self):
        fp = os.path.join(self.app_dir, 'vokabelheftlogfile')
        if not os.path.exists(fp):
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Лог файл не существует')
            return
        logfile = open(fp)
        lines = logfile.readlines()
        logfile.close()
        lv = QtWidgets.QListView()
        slm = QtCore.QStringListModel(lines)
        lv.setModel(slm)
        lt = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        lt.setWindowTitle('Logfile')
        lt.resize(500, 600)
        lt.setWindowModality(QtCore.Qt.WindowModal)
        lt.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        ltbox = QtWidgets.QVBoxLayout()
        ltbox.addWidget(lv)
        btnc = QtWidgets.QPushButton('Закрыть')
        ltbox.addWidget(btnc)
        btnc.clicked.connect(lt.close)
        lt.setLayout(ltbox)
        lt.show()

    def aboutProgramm(self):
        ab = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        ab.setWindowTitle('О программе')
        ab.setWindowModality(QtCore.Qt.WindowModal)
        ab.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        abbox = QtWidgets.QVBoxLayout()
        text = '''
        Это программа языковой тренажер.\n
        Главная особеннось которой - словарь,\n
        составляется непосредствено пользователем\n
        в процессе его (само-)обучения языку.\n
        В общем, это аналог вашей словарной тетради,\n
        с набором удобных и полезных функций)))\n
        Версия: ''' + self.version

        abl = QtWidgets.QLabel(text)
        abb = QtWidgets.QPushButton('Close')
        abb.clicked.connect(ab.close)
        abbox.addWidget(abl)
        abbox.addWidget(abb)
        ab.setLayout(abbox)
        ab.show()

    def aboutMe(self):
        text = '''Автор: @zmv\nОбратная связь: zmvph79@gmail.com'''
        QtWidgets.QMessageBox.information(None, 'Об авторе', text)

    def closeEvent(self, e):
        if not hasattr(self.win, 'dict_name'): return
        if self.win.dict_name:
            self.win.saveDict()
        e.accept()
        QtWidgets.QWidget.closeEvent(self, e)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Vokabelheft')
    window.resize(550, 200)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
    