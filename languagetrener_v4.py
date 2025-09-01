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
from sql_handler.sql_handler import SqlHandler
from utils.utils import first_screensaver
from utils.utils import get_columns
from utils.utils import get_part_names
from utils.logger import logger


settings = QtCore.QSettings("@zmv", "Vokabelheft")
if settings.contains("Language"):
    menu_language = settings.value("Language")
else:
    menu_language = 'en'
    settings.setValue("Language", menu_language)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.version = '''5.3, 2025г.'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.app_dir, 'images')
        self.bases = os.path.join(self.app_dir, 'bases')
        ico_path = os.path.join(self.images_path, 'dic.png')
        ico = QtGui.QIcon(ico_path)
        self.setWindowIcon(ico)
        self.set_interface_language(menu_language)
        self.sql_handler = SqlHandler(self.bases, self.interface_lang)
        self.check_db()
        self.count = 1
        self.sort = 1
        self.view_page = False
        self.set_screen_saver(self.interface_lang["set_lang"])
        menu_bar = self.menuBar()
        self.make_menu(menu_bar)
        self.status_bar = self.statusBar()

    def set_screen_saver(self, text: str):
        self.win = first_screensaver(self.images_path, text) #self.firstScreensaver(self.images_path, text_ch)
        self.setCentralWidget(self.win)

    def make_menu(self, menu_bar):
        my_menu = menu_bar.addMenu('&' + self.interface_lang['file'])
        self.make_my_menu(my_menu)
        my_lang = menu_bar.addMenu('&' + self.interface_lang['language'])
        my_lang.addAction('English', lambda lang='en': self.lang_choose(lang, my_menu, my_view))
        my_lang.addAction('Deutsch', lambda lang='de': self.lang_choose(lang, my_menu, my_view))
        my_view = menu_bar.addMenu(self.interface_lang['viewing'])
        self.make_my_view(my_view)
        my_settings = menu_bar.addMenu(self.interface_lang['settings'])
        my_settings.addSection('Menu language')
        my_settings.addAction(self.icon_eng, 'english', lambda ln='en': self.change_interface_language(ln, menu_bar, my_menu, my_view))
        my_settings.addAction(self.icon_ru, 'русский', lambda ln='ru': self.change_interface_language(ln, menu_bar, my_menu, my_view))
        my_settings.addSeparator()
        my_about = menu_bar.addMenu(self.interface_lang['about'])
        my_about.addAction(self.interface_lang['about_prog'], self.about_program)
        my_about.addAction(self.interface_lang['about_me'], self.about_me)

    def make_my_menu(self, my_menu):
        if self.count != 1:
            my_menu.clear()
            # my_menu.addAction('&' + self.interface_lang['create'], self.create_dict)
            # my_menu.addAction('&' + self.interface_lang['open'], self.open_dict)
            my_menu.addAction(self.interface_lang['save'], self.win.save_dict)
        my_menu.addAction('&' + self.interface_lang['close'], self.close)

    def make_my_view(self, my_view):
        if self.count != 1:
            my_view.clear()
            my_view.addAction(self.interface_lang['short_view'], self.win.dict_view)
            my_view.addAction('&' + self.interface_lang['full_view'], self.sort_all)
            my_view.addAction(self.interface_lang['view_cards'], self.win.cards_mode)
        my_view.addAction(self.interface_lang['view_log'], self.view_logfile)

    def lang_choose(self, variant: str, my_menu, my_view):
        if self.count != 1:
            if not self.check_change():
                return
        if variant == 'en':
            self.win = MyWindowE(desktop, self.app_dir, self.interface_lang, self.sql_handler)
            self.lang = variant
            self.lang_index = 1
            flag_path = os.path.join(self.images_path, 'gb_16.png')
            self.screen_path = os.path.join(self.images_path, 'Dic_eng_148.png')
            self.open_dict(self.lang_index)
        else:
            self.win = MyWindowD(desktop, self.app_dir, self.interface_lang, self.sql_handler)
            self.lang = variant
            self.lang_index = 2
            flag_path = os.path.join(self.images_path, 'de_16.png')
            self.screen_path = os.path.join(self.images_path, 'Dic_de_148.png')
            self.open_dict(self.lang_index)
        self.count += 1
        self.setCentralWidget(self.win)
        self.win.btn_close.clicked.connect(self.close)
        self.make_my_menu(my_menu)
        self.make_my_view(my_view)
        self.set_status_bar()
        self.win.label_amount.setText('Пусто')
        self.win.label_flag.setPixmap(QtGui.QPixmap(flag_path))
        self.win.label_flag.setAlignment(QtCore.Qt.AlignRight)

    def check_change(self, flag=None):
        result = QtWidgets.QMessageBox.question(None, self.interface_lang['warning'],
                                                self.interface_lang['warn_open_new_dict'],
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
        if result == 16384:
            if flag == 1:
                self.win.label_amount.setText(self.lang)
                self.win.status.setText('')
                self.win.saveValues()
                self.win.dw = {}
            else:
                self.clear_status_bar()
            return True
        return False

    def set_interface_language(self, language: str):
        self.set_icon(language)
        if language == 'en':
            self.interface_lang = MenuLanguages.eng
        else:
            self.interface_lang = MenuLanguages.rus
        settings.setValue("Language", language)

    def set_icon(self, language: str):
        icon_checkmark = QtGui.QIcon(os.path.join(self.images_path,'galochka_16.png'))
        icon_minus = QtGui.QIcon(os.path.join(self.images_path, 'minus_16.png'))
        if language == 'en':
            self.icon_eng = icon_checkmark
            self.icon_ru = icon_minus
        elif language == 'ru':
            self.icon_eng = icon_minus
            self.icon_ru = icon_checkmark

    def save_instance_state(self):
        self.win.save_dict()
        name = self.win.dict_name
        return name

    def set_status_bar(self):
        self.status_bar.addWidget(self.win.status)
        self.status_bar.addPermanentWidget(self.win.status_widget)

    def clear_status_bar(self):
        self.status_bar.removeWidget(self.win.status)
        self.status_bar.removeWidget(self.win.status_widget)

    def restore_instance_state(self):
        name = self.save_instance_state()
        self.clear_status_bar()
        match self.lang:
            case 'en':
                self.win = MyWindowE(desktop, self.app_dir, self.interface_lang)
            case 'de':
                self.win = MyWindowD(desktop, self.app_dir, self.interface_lang)
        self.win.dict_name = name
        # self.open_dict_background()
        self.set_status_bar()
        self.win.dict_view()
        self.setCentralWidget(self.win)
        self.win.btncl.clicked.connect(self.close)

    def change_interface_language(self, language: str, menu_bar, my_menu, my_view):
        self.set_interface_language(language)
        menu_bar.clear()
        self.make_menu(menu_bar)
        if self.count > 1:
            self.make_my_menu(my_menu)
            self.make_my_view(my_view)
            self.restore_instance_state()
        else:
            self.set_screen_saver(self.interface_lang["set_lang"])

    # def create_dict(self):
    #     name, ok = QtWidgets.QInputDialog.getText(None, self.interface_lang['dict_name'],
    #                                            self.interface_lang['enter_dict_name'],
    #                                            text=self.lang + '_')
    #     if not ok: return
    #     if ok and not name:
    #         QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
    #                                       self.interface_lang['warn_not_set_dict_name'])
    #         return
    #     new_dic = os.path.join(self.bases, name + '.sqlite')
    #     self.sql_handler.create_db(new_dic)
    #     self.win.clear()
    #     self.label_cr = QtWidgets.QLabel('<center>' + self.interface_lang['created_dict'] + name +'</center>')
    #     self.win.vtop_t.addWidget(self.label_cr)

    def open_dict_background(self, language: int):
        self.win.dw = self.sql_handler.open_db(language)
        self.win.page_max = int(len(self.win.dw) / 40)

    def open_dict_debug(self):
        self.win.dw = self.sql_handler.open_db_debug(self.win.dict_name)

    def open_dict(self, language: int):
        open_flag = 0 # 1 - debug mode
    #     if self.win.dict_name:
    #         if not self.check_change(flag=1):
    #             return
    #     self.win.dict_name, _ = QtWidgets.QFileDialog.getOpenFileName(None,
    #                                           caption=self.interface_lang['open_dict'],
    #                                           directory=self.bases,
    #                                           filter='DB (*.sqlite)')
    #     if not self.win.dict_name:
    #         QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
    #                                       self.interface_lang['warn_not_selected_dict'])
    #         return
        if open_flag == 0:
            self.open_dict_background(language)
        else:
            self.open_dict_debug()

        # last_name = os.path.basename(self.win.dict_name)
        self.win.clear()
        self.label2 = QtWidgets.QLabel('<center>' + self.interface_lang['loaded_dict'] + '</center>')
        self.win.vtop_t.addWidget(self.label2)
        label_screen = QtWidgets.QLabel()
        label_screen.setPixmap(QtGui.QPixmap(self.screen_path))
        label_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.win.vtop_t.addWidget(label_screen)
        self.win.label_amount.setText(self.lang)

    def sort_all(self):
        def sa_close():
            sort_widget.close()
            self.view_all()

        def choose_page():
            self.view_page = True
            page = sp_box.value()
            self.start_page = (page-1) * 40
            sa_close()

        def sort_choose():
            index = cb_sa.currentIndex()
            if index == 0:
                self.sort = 1
                sa_close()
            elif index == 1:
                self.sort = 0
                sa_close()
            elif index == 2:
                if self.win.page_max < 2:
                    text = self.interface_lang['warn_not_enough_word_view']
                    QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'], text)
                    return
                cb_sa.setEnabled(False)
                sp_box.setRange(1, self.win.page_max)
                sort_widget_vbox.insertWidget(2, sp_box)
                btn.clicked.connect(choose_page)
            elif index == 3:
                if len(self.win.dw) <= 40:
                    self.start_page = 0
                else:
                    self.start_page = len(self.win.dw) - 40
                self.view_page = True
                sa_close()

        # if not self.win.dict_name:
        #     QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
        #                                   self.interface_lang['warn_not_selected_dict'])
        #     return
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
        btn.clicked.connect(sort_choose)
        sort_widget_vbox.addWidget(btn)
        sort_widget.setLayout(sort_widget_vbox)
        sort_widget.show()

    # def view_all(self):
    #     if not self.win.dw:
    #         QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
    #                                       self.interface_lang['dict_empty'])
    #         return
    #     tabview = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
    #     conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    #     conn.setDatabaseName(self.sql_handler.database)
    #     conn.open()
    #     query = '''select * from dictionary where language="%d"''' % self.lang_index
    #     if not self.view_page:
    #         # stm = QtSql.QSqlRelationalTableModel(parent=window)
    #         stm = QtSql.QSqlQueryModel(parent=window)
    #         stm.setQuery(query)
    #         # stm.setRelation(6, QtSql.QSqlRelation('part', 'partnumber', 'partname'))
    #         stm.sort(self.sort, QtCore.Qt.AscendingOrder)
    #         # stm.select()
    #     else:
    #         stm = QtSql.QSqlQueryModel(parent=window)
    #         # query = '''select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural, part.partname
    #         # from dic inner join part on dic.partnumber=part.partnumber limit 40 offset %d''' % self.start_page
    #         query_page =query + ''' limit 40 offset %d''' % self.start_page
    #         stm.setQuery(query_page)
    #         stm.sort(self.sort, QtCore.Qt.AscendingOrder)
    #         self.view_page = False
    #     # var_names = [self.interface_lang['phonetics'],
    #     #              self.interface_lang['article']]
    #     # if self.lang == 'de':
    #     #     var_name = var_names[1]
    #     #     l_1, l_2, l_4, l_5 = 160, 50, 180, 45
    #     # else:
    #     #     var_name = var_names[0]
    #     #     l_1, l_2, l_4, l_5 = 100, 100, 150, 75
    #     for i, n in ((1, self.interface_lang['word']),
    #                 (2, self.interface_lang['phonetics']),
    #                 (3, self.interface_lang['article']),
    #                 (4, self.interface_lang['translation']),
    #                 (5, self.interface_lang['verb_forms']),
    #                 (6, self.interface_lang['plural']),
    #                 (7, self.interface_lang['part_of_speech'])):
    #         stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
    #     vbox = QtWidgets.QVBoxLayout()
    #     tv = QtWidgets.QTableView()
    #     tv.setModel(stm)
    #     tv.hideColumn(0)
    #     if self.lang == 'de':
    #         l_1, l_3, l_5, l_6 = 160, 50, 180, 45
    #         tv.hideColumn(2)
    #         tv.setColumnWidth(3, l_3)
    #     else:
    #         l_1, l_2, l_5, l_6 = 100, 100, 150, 75
    #         tv.hideColumn(3)
    #         tv.setColumnWidth(3, l_2)
    #     for i, n in ((1, l_1), (4, 300), (5, l_5), (6, l_6), (7, 150)):
    #         tv.setColumnWidth(i, n)
    #     vbox.addWidget(tv)
    #     btn_close = QtWidgets.QPushButton(self.interface_lang['close'])
    #     btn_close.clicked.connect(tabview.close)
    #     vbox.addWidget(btn_close)
    #     tabview.setLayout(vbox)
    #     tabview.resize(915, 350)
    #     tabview.show()

    def view_all(self):
        if not self.win.dw:
            QtWidgets.QMessageBox.warning(None, self.interface_lang['warning'],
                                          self.interface_lang['dict_empty'])
            return
        tabview = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tabview.setWindowTitle(self.interface_lang['dict'] + ' ' + self.lang)
        sti = QtGui.QStandardItemModel(parent = tabview)
        part_names = get_part_names(MenuLanguages.part_keys, self.interface_lang)
        if not self.view_page:
            columns = get_columns(self.win.dw, self.lang_index, part_names)
            # stm = QtSql.QSqlRelationalTableModel(parent=window)
            # stm = QtSql.QSqlQueryModel(parent=window)
            # stm.setQuery(query)
            # stm.setRelation(6, QtSql.QSqlRelation('part', 'partnumber', 'partname'))
            # stm.sort(self.sort, QtCore.Qt.AscendingOrder)
            # stm.select()
        else:
            columns = get_columns(self.win.dw, self.lang_index, part_names)
            # stm = QtSql.QSqlQueryModel(parent=window)
            # # query = '''select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural, part.partname
            # # from dic inner join part on dic.partnumber=part.partnumber limit 40 offset %d''' % self.start_page
            # query_page =query + ''' limit 40 offset %d''' % self.start_page
            # stm.setQuery(query_page)
            # stm.sort(self.sort, QtCore.Qt.AscendingOrder)
            self.view_page = False
        # var_names = [self.interface_lang['phonetics'],
        #              self.interface_lang['article']]
        # if self.lang == 'de':
        #     var_name = var_names[1]
        #     l_1, l_2, l_4, l_5 = 160, 50, 180, 45
        # else:
        #     var_name = var_names[0]
        #     l_1, l_2, l_4, l_5 = 100, 100, 150, 75
        headers = [self.interface_lang['word'],
                   self.interface_lang['phonetics'] if self.lang_index ==1 else self.interface_lang['article'],
                   self.interface_lang['translation'],
                   self.interface_lang['verb_forms'],
                   self.interface_lang['plural'],
                   self.interface_lang['part_of_speech']]
        sti.setHorizontalHeaderLabels(headers)
        # for i, n in ((1, self.interface_lang['word']),
        #             (2, self.interface_lang['phonetics']),
        #             (3, self.interface_lang['article']),
        #             (4, self.interface_lang['translation']),
        #             (5, self.interface_lang['verb_forms']),
        #             (6, self.interface_lang['plural']),
        #             (7, self.interface_lang['part_of_speech'])):
        #     stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        for row in range(0, len(columns[0])):
            word = QtGui.QStandardItem(columns[0][row])
            phonetic_article = QtGui.QStandardItem(columns[1][row])
            translate = QtGui.QStandardItem(columns[2][row])
            form = QtGui.QStandardItem(columns[3][row])
            plural = QtGui.QStandardItem(columns[4][row])
            part_name = QtGui.QStandardItem(columns[5][row])
            sti.appendRow([word, phonetic_article, translate, form, plural, part_name])
        vbox = QtWidgets.QVBoxLayout()
        tv = QtWidgets.QTableView()
        tv.setModel(sti)
        if not self.view_page:
            tv.sortByColumn(0, QtCore.Qt.AscendingOrder)
        # tv.hideColumn(0)
        col_word, col_translate, col_form, col_part = 160, 300, 180, 160
        if self.lang == 'de':
            col_phonetic_article, col_plural = 50, 50
            # tv.hideColumn(2)
            # tv.setColumnWidth(3, l_3)
        else:
            col_phonetic_article, col_plural =  100, 160
            # tv.hideColumn(3)
            # tv.setColumnWidth(3, l_2)
        for i, n in ((0, col_word),
                     (1, col_phonetic_article),
                     (2, col_translate),
                     (3, col_form),
                     (4, col_plural),
                     (5, col_part)):
            tv.setColumnWidth(i, n)
        vbox.addWidget(tv)
        btn_close = QtWidgets.QPushButton(self.interface_lang['close'])
        btn_close.clicked.connect(tabview.close)
        vbox.addWidget(btn_close)
        tabview.setLayout(vbox)
        tabview.resize(915, 350)
        tabview.show()

    def view_logfile(self):
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
        lt_box = QtWidgets.QVBoxLayout()
        lt_box.addWidget(lv)
        btn_close = QtWidgets.QPushButton(self.interface_lang['close'])
        lt_box.addWidget(btn_close)
        btn_close.clicked.connect(lt.close)
        lt.setLayout(lt_box)
        lt.show()

    def about_program(self):
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

    def about_me(self):
        text = self.interface_lang['about_me_text']
        QtWidgets.QMessageBox.information(None, self.interface_lang['about_me'], text)

    def closeEvent(self, event):
        # if not hasattr(self.win, 'dict_name'): return
        # if self.win.dict_name:
        self.win.save_dict()
        event.accept()
        QtWidgets.QWidget.closeEvent(self, event)
        
    def check_db(self):
        if not self.sql_handler.is_db_available():
            logger.info('DB is not exist')
            self.sql_handler.create_db()
        else:
            logger.info('DB is available')



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
