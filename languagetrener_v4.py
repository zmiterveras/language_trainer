#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#v4
# pylint: disable=C0115, C0103, C0116, C0321, C0301, C0410, C0114
# pylint: disable=W0201
# pylint: disable=R0914, R0902, R0904

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
        self.version = '''5, 2024г.'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.app_dir, 'images')
        self.bases = os.path.join(self.app_dir, 'bases')
        ico_path = os.path.join(self.images_path, 'dic.png')
        ico = QtGui.QIcon(ico_path)
        self.setWindowIcon(ico)
        self.setInterfaceLanguage(menu_language)
        self.count = 1
        self.sort = 1
        self.view_page = False
        self.setScreenSaver(self.interface_lang["set_lang"])
        menuBar = self.menuBar()
        self.makeMenu(menuBar)
        self.statusBar = self.statusBar()

    def setScreenSaver(self, text: str):
        self.win = firstScreensaver(self.images_path, text) #self.firstScreensaver(self.images_path, text_ch)
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
        myAbout.addAction(self.interface_lang['about_prog'], self.aboutProgramm)
        myAbout.addAction(self.interface_lang['about_me'], self.aboutMe)

    def makeMyMenu(self, myMenu):
        if self.count != 1:
            myMenu.clear()
            myMenu.addAction('&' + self.interface_lang['create'], self.createDict)
            myMenu.addAction('&' + self.interface_lang['open'], self.openDict)
            myMenu.addAction(self.interface_lang['save'], self.win.saveDict)
        myMenu.addAction('&' + self.interface_lang['close'], self.close)

    def makeMyView(self, myView):
        if self.count != 1:
            myView.clear()
            myView.addAction(self.interface_lang['short_view'], self.win.dictView)
            myView.addAction('&' + self.interface_lang['full_view'], self.sortAll)
            myView.addAction(self.interface_lang['view_cards'], self.win.cardsMode)
        myView.addAction(self.interface_lang['view_log'], self.viewLogfile)

    def langChoose(self, variant, myMenu, myView):
        if self.count != 1:
            if not self.checkChange():
                return
        if variant == 'en':
            self.win = MyWindowE(desktop, self.app_dir, self.interface_lang)
            self.lang = variant
            flag_path = os.path.join(self.images_path, 'gb_16.png')
            self.screen_path = os.path.join(self.images_path, 'Dic_eng_148.png')
        else:
            self.win = MyWindowD(desktop, self.app_dir, self.interface_lang)
            self.lang = variant
            flag_path = os.path.join(self.images_path, 'de_16.png')
            self.screen_path = os.path.join(self.images_path, 'Dic_de_148.png')
        self.count += 1
        self.setCentralWidget(self.win)
        self.win.btncl.clicked.connect(self.close)
        self.makeMyMenu(myMenu)
        self.makeMyView(myView)
        self.setStatusBar()
        self.win.label_am.setText('Пусто')
        self.win.label_flag.setPixmap(QtGui.QPixmap(flag_path))
        self.win.label_flag.setAlignment(QtCore.Qt.AlignRight)

    def checkChange(self, flag=None):
        result = QtWidgets.QMessageBox.question(None, self.interface_lang['warning'],
                                                self.interface_lang['warn_open_new_dict'],
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
        if result == 16384:
            if flag == 1:
                self.win.label_am.setText(self.lang)
                self.win.status.setText('')
                self.win.saveValues()
                self.win.dw = {}
            else:
                self.clearStatusBar()
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
        icon_checkmark = QtGui.QIcon(os.path.join(self.images_path,'galochka_16.png'))
        icon_minus = QtGui.QIcon(os.path.join(self.images_path, 'minus_16.png'))
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

    def setStatusBar(self):
        self.statusBar.addWidget(self.win.status)
        self.statusBar.addPermanentWidget(self.win.st)

    def clearStatusBar(self):
        self.statusBar.removeWidget(self.win.status)
        self.statusBar.removeWidget(self.win.st)

    def restoreInstanceState(self):
        name = self.saveInstanceState()
        self.clearStatusBar()
        match self.lang:
            case 'en':
                self.win = MyWindowE(desktop, self.app_dir, self.interface_lang)
            case 'de':
                self.win = MyWindowD(desktop, self.app_dir, self.interface_lang)
        self.win.dict_name = name
        self.openDictBackground()
        self.setStatusBar()
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
        name, ok = QtWidgets.QInputDialog.getText(None, self.interface_lang['dict_name'],
                                               self.interface_lang['enter_dict_name'],
                                               text=self.lang + '_')
        if not ok: return
        if ok and not name:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_not_set_dict_name'])
            return
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        newdic = os.path.join(self.bases, name + '.sqlite')
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
        self.label_cr = QtWidgets.QLabel('<center>' + self.interface_lang['created_dict'] + name +'</center>')
        self.win.vtop_t.addWidget(self.label_cr)

    def openDictBackground(self):
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(self.win.dict_name)
        conn.open()
        query = QtSql.QSqlQuery()
        query.exec(self.query_str)
        if query.isActive():
            query.first()
            while query.isValid():
                self.win.dw[query.value('key')] = [query.value('id'), query.value('keyfon'),
                                                    query.value('word'), query.value('form'),
                                                    query.value('plural'), query.value('partname')]
                query.next()
        conn.close()
        self.win.page_max = int(len(self.win.dw) / 40)

    def openDictDebug(self):
        conn = sqlite3.connect(self.win.dict_name)
        curs = conn.cursor()
        curs.execute(self.query_str)
        for row in curs.fetchall():
            self.win.dw[row[1]] = [row[0], row[2], row[3], row[4], row[5], row[6]]
        conn.close()

    def openDict(self):
        open_flag = 0 # 1 - debug mode
        if self.win.dict_name:
            if not self.checkChange(flag=1):
                return
        self.win.dict_name, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                              caption=self.interface_lang['open_dict'],
                                              directory=self.bases,
                                              filter='DB (*.sqlite)')
        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_not_selected_dict'])
            return
        self.query_str = """select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural,
            part.partname from dic inner join part on dic.partnumber=part.partnumber
            """
        if open_flag == 0:
            self.openDictBackground()
        else:
            self.openDictDebug()

        last_name = os.path.basename(self.win.dict_name)
        self.win.clear()
        self.label2 = QtWidgets.QLabel('<center>' + self.interface_lang['loaded_dict'] + last_name+'</center>')
        self.win.vtop_t.addWidget(self.label2)
        label_screen = QtWidgets.QLabel()
        label_screen.setPixmap(QtGui.QPixmap(self.screen_path))
        label_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.win.vtop_t.addWidget(label_screen)
        self.win.label_am.setText(self.lang)

    def sortAll(self):
        def saClose():
            sort_widget.close()
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
                    text = self.interface_lang['warn_not_enough_word_view']
                    QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'], text)
                    return
                cb_sa.setEnabled(False)
                sp_box.setRange(1, self.win.page_max)
                sort_widget_vbox.insertWidget(2, sp_box)
                btn.clicked.connect(choosePage)
            elif index == 3:
                if len(self.win.dw) <= 40:
                    self.start_page = 0
                else:
                    self.start_page = len(self.win.dw) - 40
                self.view_page = True
                saClose()

        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_not_selected_dict'])
            return
        sort_widget = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        sort_widget.setWindowTitle(self.interface_lang['select_display'])
        sort_widget.resize(250, 80)
        sort_widget.setWindowModality(QtCore.Qt.WindowModal)
        sort_widget_vbox = QtWidgets.QVBoxLayout()
        sort_widget_vbox.addWidget(QtWidgets.QLabel(self.interface_lang['select_mode_sort']))
        cb_sa = QtWidgets.QComboBox()
        cb_sa.addItems([self.interface_lang['mode_alphabet'],
                        self.interface_lang['mode_page_by_page'],
                        self.interface_lang['mode_page'],
                        self.interface_lang['mode_last_40']])
        sp_box = QtWidgets.QSpinBox()
        sort_widget_vbox.addWidget(cb_sa)
        btn = QtWidgets.QPushButton('Ok')
        btn.clicked.connect(sortChoose)
        sort_widget_vbox.addWidget(btn)
        sort_widget.setLayout(sort_widget_vbox)
        sort_widget.show()

    def viewAll(self):
        if not self.win.dw:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['dict_empty'])
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
        var_names = [self.interface_lang['phonetics'],
                     self.interface_lang['article']]
        if self.lang == 'de':
            var_name = var_names[1]
            l_1, l_2, l_4, l_5 = 160, 50, 180, 45
        else:
            var_name = var_names[0]
            l_1, l_2, l_4, l_5 = 100, 100, 150, 75
        for i, n in ((1, self.interface_lang['word']),
                    (2, var_name),
                    (3, self.interface_lang['translation']),
                    (4, self.interface_lang['verb_forms']),
                    (5, self.interface_lang['plural']),
                    (6, self.interface_lang['part_of_speech'])):
            stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        vbox = QtWidgets.QVBoxLayout()
        tv = QtWidgets.QTableView()
        tv.setModel(stm)
        tv.hideColumn(0)
        for i, n in ((1, l_1), (2, l_2), (3, 300), (4, l_4), (5, l_5), (6, 150)):
            tv.setColumnWidth(i, n)
        vbox.addWidget(tv)
        btncl = QtWidgets.QPushButton(self.interface_lang['close'])
        btncl.clicked.connect(tabview.close)
        vbox.addWidget(btncl)
        tabview.setLayout(vbox)
        tabview.resize(915, 350)
        tabview.show()

    def viewLogfile(self):
        fp = os.path.join(self.app_dir, 'vokabelheftlogfile')
        if not os.path.exists(fp):
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['warn_log_not_exist'])
            return
        logfile = open(fp)
        lines = logfile.readlines()
        logfile.close()
        lv = QtWidgets.QListView()
        slm = QtCore.QStringListModel(lines)
        lv.setModel(slm)
        lt = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        lt.setWindowTitle(self.interface_lang['log'])
        lt.resize(500, 600)
        lt.setWindowModality(QtCore.Qt.WindowModal)
        lt.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        ltbox = QtWidgets.QVBoxLayout()
        ltbox.addWidget(lv)
        btnc = QtWidgets.QPushButton(self.interface_lang['close'])
        ltbox.addWidget(btnc)
        btnc.clicked.connect(lt.close)
        lt.setLayout(ltbox)
        lt.show()

    def aboutProgramm(self):
        about_widget = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        about_widget.setWindowTitle(self.interface_lang['about_prog'])
        about_widget.setWindowModality(QtCore.Qt.WindowModal)
        about_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        about_widget_box = QtWidgets.QVBoxLayout()
        text = self.interface_lang['about_prog_text'] + self.version
        about_widget_label = QtWidgets.QLabel(text)
        about_widget_close_btn = QtWidgets.QPushButton(self.interface_lang['close'])
        about_widget_close_btn.clicked.connect(about_widget.close)
        about_widget_box.addWidget(about_widget_label)
        about_widget_box.addWidget(about_widget_close_btn)
        about_widget.setLayout(about_widget_box)
        about_widget.show()

    def aboutMe(self):
        text = self.interface_lang['about_me_text']
        QtWidgets.QMessageBox.information(None, self.interface_lang['about_me'], text)

    def closeEvent(self, event):
        if not hasattr(self.win, 'dict_name'): return
        if self.win.dict_name:
            self.win.saveDict()
        event.accept()
        QtWidgets.QWidget.closeEvent(self, event)



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
