#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#v4

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
import sys,sqlite3, random, os, time


class ClickedLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        self.version = '''4.17, 2022г.'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.wp = os.path.join(self.app_dir, 'images')
        ico_path = os.path.join(self.wp, 'dic.png')
        ico = QtGui.QIcon(ico_path)
        self.setWindowIcon(ico)
        self.win = None
        text_ch = """<center>Выберите изучаемый язык</center>\n
        <center>Используйте меню:</center>\n
        <center><b>"Язык"</b></center>"""
        ss = self.firstScreensaver(self.wp, text_ch)
        self.setCentralWidget(ss)     
        menuBar = self.menuBar()
        myMenu = menuBar.addMenu('&Файл')
        #action = myMenu.addAction('Test',  self.test)
        myLang = menuBar.addMenu('&Язык')
        action = myLang.addAction('English', lambda x=1: self.langChoose(x, myMenu, myView))
        action = myLang.addAction('Deutsch', lambda x=2: self.langChoose(x, myMenu, myView))
        myView = menuBar.addMenu('Просмотр')
        action = myView.addAction('Просмотр логфайла', self.viewLogfile)
        myAbout = menuBar.addMenu('О...')
        action = myAbout.addAction('О программе', self.aboutProgramm)
        action = myAbout.addAction('Обо мне', self.aboutMe)
        self.statusBar = self.statusBar()
        self.count = 1
        self.sort = 1
        self.view_page = False
        
    def firstScreensaver(self, abs_path, text, flag=None):
        ss = QtWidgets.QWidget()
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
        ss.setLayout(central_box)
        return ss
        
    def langChoose(self, x, myMenu, myView):
        if self.count != 1: 
            if not self.checkChange():
                return
        if x == 1:
            self.win = MyWindowE()
            self.lang = 'eng '
            flag_path = os.path.join(self.wp, 'gb_16.png')
            self.screen_path = os.path.join(self.wp, 'Dic_eng_148.png')
        else:
            self.win = MyWindowD()
            self.lang = 'de'
            flag_path = os.path.join(self.wp, 'de_16.png')
            self.screen_path = os.path.join(self.wp, 'Dic_de_148.png')
        self.setCentralWidget(self.win)
        self.win.btncl.clicked.connect(self.close)
        myView.clear()
        myMenu.clear()
        action = myMenu.addAction('&Создать',  self.createDict)
        action = myMenu.addAction('&Открыть',  self.openDict)
        action = myMenu.addAction('Сохранить',  self.win.saveDict)
        action = myMenu.addAction('&Закрыть',  self.close)
        action = myView.addAction('Краткий просмотр',  self.win.dictView)
        action = myView.addAction('&Просмотреть все',  self.sortAll)
        action = myView.addAction('Просмотр карточек', self.win.cardsMode)
        action = myView.addAction('Просмотр логфайла', self.viewLogfile)
        self.statusBar.addWidget(self.win.status)
        self.statusBar.addPermanentWidget(self.win.st) 
        self.win.label_am.setText('Пусто')
        self.win.label_flag.setPixmap(QtGui.QPixmap(flag_path))
        self.win.label_flag.setAlignment(QtCore.Qt.AlignRight)
        self.count += 1
        
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
        
    def createDict(self):
        s, ok = QtWidgets.QInputDialog.getText(None, 'Имя словаря', 'Введите имя словаря')
        if not ok: return
        if ok and not s:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не задано имя словаря')
            return
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        newdic = os.path.join(self.wp, s+'.sqlite')
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
        
    def openDict(self):
        open_flag = 0
        if self.win.dict_name:
            if not self.checkChange(flag=1):
                return
        self.win.dict_name, fil_ = QtWidgets.QFileDialog.getOpenFileName(None, caption='Открыть словарь',
                                                                         directory=self.app_dir, filter='DB (*.sqlite)') 
        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбран словарь')
            return
        querystr = """select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural,
            part.partname from dic inner join part on dic.partnumber=part.partnumber
            """
        if open_flag == 0:
            conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            conn.setDatabaseName(self.win.dict_name)
            conn.open()
            query = QtSql.QSqlQuery()
            query.exec(querystr)
            if query.isActive():
                query.first()
                while query.isValid():
                    self.win.dw[query.value('key')] = [query.value('id'), query.value('keyfon'),
                                                       query.value('word'), query.value('form'),
                                                       query.value('plural'), query.value('partname')]
                    query.next()
            conn.close()
            self.win.page_max = int(len(self.win.dw) / 40)
        else:
            conn = sqlite3.connect(self.win.dict_name)
            curs = conn.cursor()
            curs.execute(querystr)
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
                if len(self.win.dw) <=  40:
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
        sa.resize(250,80)
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
            stm.setRelation(6,QtSql.QSqlRelation('part', 'partnumber', 'partname'))
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
        for i,n in ((1, 'Слово'),(2, var_name),(3,'Перевод'),(4,'Формы глагола'),(5,'Мн.ч-ло'),(6,'Часть речи')):
            stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        vbox = QtWidgets.QVBoxLayout()
        tv = QtWidgets.QTableView()
        tv.setModel(stm)
        tv.hideColumn(0)
        for i,n in ((1, l_1),(2, l_2),(3,300),(4,l_4),(5,l_5),(6,150)):
            tv.setColumnWidth(i, n)
        vbox.addWidget(tv)
        btncl = QtWidgets.QPushButton('Закрыть')
        btncl.clicked.connect(tabview.close)
        vbox.addWidget(btncl)
        tabview.setLayout(vbox)
        tabview.resize(915,350)
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
        QtWidgets.QMessageBox.information(None,'Об авторе', text)
        
    def closeEvent(self, e):
        if not self.win: return
        if self.win.dict_name:
            self.win.saveDict()
        e.accept()
        QtWidgets.QWidget.closeEvent(self, e)
        
###############################################################################


class MyWindowLanguage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.dict_name = ''
        self.dw = {}
        self.search_flag = 0
        self.cards_flag = 0
        self.search_key = 0
        self.page_max = 0
        self.lst1 = [1,2,3,4,5]
        self.lst2 = ['существительное','глагол','прилагательное','наречие', 'другое']
        self.wd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
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
        self.newname = [[],[],[],[],[],[]]
        self.delname = []
        self.changenote = [[],[],[],[],[],[],[]]
        
    def makeWidget(self):
        text = '''<center>Откройте или создайте словарь</center>\n
        <center>Используйте меню:</center>\n
        <center><b>"Файл"</b></center>'''
        self.vbox = QtWidgets.QVBoxLayout()
        self.vtop = QtWidgets.QVBoxLayout()
        self.vtop_t = QtWidgets.QVBoxLayout()
        ss = MainWindow().firstScreensaver(self.wd, text, flag=1)
        self.vtop_t.addWidget(ss)
        self.htop_b = QtWidgets.QHBoxLayout()
        self.vtop.addLayout(self.vtop_t)
        self.vtop.addLayout(self.htop_b)
        self.hbox = QtWidgets.QHBoxLayout()
        btnnames = [('Просмотр', self.dictView),('Тренировка', self.onTrenningMode),
                    ('Поиск', self.onSearch),('Редакт.', self.editDict)]
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
            query.bindValue(':plural',self.newname[4])
            query.bindValue(':partnumber', self.newname[5])
            query.execBatch()
            query.clear()
        #изменение
        if self.changenote[0]:
            querystr_='''update dic set key=:key, keyfon=:keyfon, word=:word, form=:form,
                    plural=:plural, partnumber=:partnumber where id=:id'''
            query.prepare(querystr_)
            query.bindValue(':key', self.changenote[1])
            query.bindValue(':keyfon', self.changenote[2])
            query.bindValue(':word', self.changenote[3])
            query.bindValue(':form', self.changenote[4])
            query.bindValue(':plural',self.changenote[5])
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
            dic = list(self.dw.keys())
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
        
    def viewWord(self, index):
        self.displayWord()
        
    def onEdItemRun(self, event):
        self.onEdItem()
        
    def hLine(self,box):
        fr = QtWidgets.QFrame()
        fr.setFrameShape(QtWidgets.QFrame.HLine)
        box.addWidget(fr)      
        
    def displayWord(self):
        def editRun(a,win):
            tlClose(None, win, flag=1)
            self.onEdItem()    
        def tlClose(a, win, flag=None):
            if not flag:
                self.search_flag =0
            win.close()   
        def view():
            tl = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
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
                if self.page_max < 2:
                    text = 'Не достаточно слов для постраничного режима\nИспользуйте другой режим тренировки!'
                    QtWidgets.QMessageBox.warning(None, 'Предупреждение', text)
                    return
                self.page = sp_box.value()
            tm.close()
            self.onTrenning()
            
        def pagenation():
            self.ch_value = cb_tm.currentIndex()
            if self.ch_value != 3 or self.page_max < 2:
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
        tm = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tm.setWindowTitle('Выбор тренировки')
        tm.resize(250,80)
        self.mode_tr = ['Случайный выбор','Последние 20','Последние 40', 'Страница']
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
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не достаточно слов для данного режима тренировки\n' +
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
            self.onRun()
    def onResult(self):
        self.clear()
        label_rq = QtWidgets.QLabel('<center><b>Задано вопросов:</b></center>')
        label_rqq = QtWidgets.QLabel('<center>' + str(self.q_count) + '</center>')
        label_rta = QtWidgets.QLabel('<center><b>Получено правильных ответов:</b></center>')
        label_rtaa = QtWidgets.QLabel('<center>' + str(self.t_ans_count) + '</center>')
        label_rtaa.setStyleSheet("color:green")
        label_rfa = QtWidgets.QLabel('<center><b>Получено неправильных ответов:</b></center>')
        label_rfaa = QtWidgets.QLabel('<center>' + str(self.q_count - self.t_ans_count) + '</center>')
        label_rfaa.setStyleSheet("color:red")
        for i in (label_rq, label_rqq, label_rta, label_rtaa, label_rfa, label_rfaa):
            self.vtop_t.addWidget(i)
        self.hLine(self.vtop_t)
        if self.t_ans_count >= 0.8*self.q_count:
            rr ='Хорошая работа!!!'
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
        self.wp = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(self.wp, 'vokabelheftlogfile')
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
            else:
                self.tl_cr.close()
       
    def setScreenValues(self):
        width_s = desktop.width()
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
        else:
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
            '''
            if self.card_toggle == 'f':
                word_label.setText(self.native)
                self.card_toggle = 'n'
            else:
                word_label.setText(self.foregn)
                self.card_toggle = 'f'
            '''
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
            
        
        self.tl_cr = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        self.tl_cr.setWindowTitle('Карточка')
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        self.tl_cr.setWindowModality(QtCore.Qt.WindowModal)
        self.tl_cr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.tl_cr.setMinimumSize(0.2*desktop.width(), 0.2*desktop.height())
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
        for i in (('Добавить', self.onAdd),('Изменить',self.onEdItem),('Удалить', self.onDelete)):
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1]) 
            self.htop_b.addWidget(btn)
            
    def onEdItem(self):
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            
        try:
            new = (key,) + (self.dw[key][1],) + (self.dw[key][2],) + (self.dw[key][3],) + (self.dw[key][4],) + (self.dw[key][5],)
        except KeyError:
                QtWidgets.QMessageBox.warning(None,'Предупреждение', 'Не выбрано слово')
                return
        self.onAdd(None,new, flag=1)
        self.search_flag = 0
        
    def onDelete(self):
        key = self.lv.currentIndex().data()
        if not key:
            QtWidgets.QMessageBox.warning(None,'Предупреждение','Не выбрана запись для удаления')
            return
        self.delname.append(self.dw[key][0])
        self.dw.pop(key)
        QtWidgets.QMessageBox.information(None,'Инфо', 'Удалена запись: '+key)
        self.clear()
        self.editDict()
        
    
        
        
##################################################################################
        

class MyWindowE(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.dict_name = ''
        self.dw = {}
        self.search_flag = 0
        self.cards_flag = 0
        self.search_key = 0
        self.page_max = 0
        self.lst1 = [1,2,3,4,5]
        self.lst2 = ['существительное','глагол','прилагательное','наречие', 'другое']
        self.wd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
        # self.label_am = QtWidgets.QLabel()
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
        self.newname = [[],[],[],[],[],[]]
        self.delname = []
        self.changenote = [[],[],[],[],[],[],[]]
        
    def makeWidget(self):
        text = '''<center>Откройте или создайте словарь</center>\n
        <center>Используйте меню:</center>\n
        <center><b>"Файл"</b></center>'''
        self.vbox = QtWidgets.QVBoxLayout()
        self.vtop = QtWidgets.QVBoxLayout()
        self.vtop_t = QtWidgets.QVBoxLayout()
        ss = MainWindow().firstScreensaver(self.wd, text, flag=1)
        self.vtop_t.addWidget(ss)
        self.htop_b = QtWidgets.QHBoxLayout()
        self.vtop.addLayout(self.vtop_t)
        self.vtop.addLayout(self.htop_b)
        self.hbox = QtWidgets.QHBoxLayout()
        btnnames = [('Просмотр', self.dictView),('Тренировка', self.onTrenningMode),
                    ('Поиск', self.onSearch),('Редакт.', self.editDict)]
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
            query.bindValue(':plural',self.newname[4])
            query.bindValue(':partnumber', self.newname[5])
            query.execBatch()
            query.clear()
        #изменение
        if self.changenote[0]:
            querystr_='''update dic set key=:key, keyfon=:keyfon, word=:word, form=:form,
                    plural=:plural, partnumber=:partnumber where id=:id'''
            query.prepare(querystr_)
            query.bindValue(':key', self.changenote[1])
            query.bindValue(':keyfon', self.changenote[2])
            query.bindValue(':word', self.changenote[3])
            query.bindValue(':form', self.changenote[4])
            query.bindValue(':plural',self.changenote[5])
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
            dic = list(self.dw.keys())
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
        
    def viewWord(self, index):
        self.displayWord()
        
    def onEdItemRun(self, event):
        self.onEdItem()
        
    def hLine(self,box):
        fr = QtWidgets.QFrame()
        fr.setFrameShape(QtWidgets.QFrame.HLine)
        box.addWidget(fr)      
        
    def displayWord(self):
        def editRun(a,win):
            tlClose(None, win, flag=1)
            self.onEdItem()    
        def tlClose(a, win, flag=None):
            if not flag:
                self.search_flag =0
            win.close()   
        def view():
            tl = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
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
                if self.page_max < 2:
                    text = 'Не достаточно слов для постраничного режима\nИспользуйте другой режим тренировки!'
                    QtWidgets.QMessageBox.warning(None, 'Предупреждение', text)
                    return
                self.page = sp_box.value()
            tm.close()
            self.onTrenning()
            
        def pagenation():
            self.ch_value = cb_tm.currentIndex()
            if self.ch_value != 3 or self.page_max < 2:
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
        tm = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tm.setWindowTitle('Выбор тренировки')
        tm.resize(250,80)
        self.mode_tr = ['Случайный выбор','Последние 20','Последние 40', 'Страница']
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
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не достаточно слов для данного режима тренировки\n' +
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
            self.onRun()
               
    def onRun(self):
        def onCheck():
            self.ch = ent.text()
            if self.ch == '':
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не получен ответ')
            elif self.ch == self.ask:
                self.t_ans_count += 1
                self.onTrueAnswer()
            else:
                self.onFalseAnswer()

        if self.dw_key:
            self.q_count += 1
            self.ask = random.choice(self.dw_key)
            self.dw_key.remove(self.ask)
            self.quest_word = self.dw[self.ask][2]
            question = 'Переведите слово: <b>' + self.quest_word + '</b>'
            self.clear()
            label_q = QtWidgets.QLabel('<center>'+question+'</center>')
            self.vtop_t.addWidget(label_q)
            ent = QtWidgets.QLineEdit('', self)
            ent.setFocus()
            self.vtop_t.addWidget(ent)
            btn = QtWidgets.QPushButton('Ok')
            self.vtop_t.addWidget(btn)
            btn.clicked.connect(onCheck)
            btn.setAutoDefault(True) # Enter
            ent.returnPressed.connect(btn.click) #enter
        else:
            self.onResult()
            
    def onResult(self):
        self.clear()
        label_rq = QtWidgets.QLabel('<center><b>Задано вопросов:</b></center>')
        label_rqq = QtWidgets.QLabel('<center>' + str(self.q_count) + '</center>')
        label_rta = QtWidgets.QLabel('<center><b>Получено правильных ответов:</b></center>')
        label_rtaa = QtWidgets.QLabel('<center>' + str(self.t_ans_count) + '</center>')
        label_rtaa.setStyleSheet("color:green")
        label_rfa = QtWidgets.QLabel('<center><b>Получено неправильных ответов:</b></center>')
        label_rfaa = QtWidgets.QLabel('<center>' + str(self.q_count - self.t_ans_count) + '</center>')
        label_rfaa.setStyleSheet("color:red")
        for i in (label_rq, label_rqq, label_rta, label_rtaa, label_rfa, label_rfaa):
            self.vtop_t.addWidget(i)
        self.hLine(self.vtop_t)
        if self.t_ans_count >= 0.8*self.q_count:
            rr ='Хорошая работа!!!'
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
        self.wp = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(self.wp, 'vokabelheftlogfile')
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
            else:
                self.tl_cr.close()
       
    def setScreenValues(self):
        width_s = desktop.width()
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
        else:
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
            '''
            if self.card_toggle == 'f':
                word_label.setText(self.native)
                self.card_toggle = 'n'
            else:
                word_label.setText(self.foregn)
                self.card_toggle = 'f'
            '''
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
            
        
        self.tl_cr = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        self.tl_cr.setWindowTitle('Карточка')
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        self.tl_cr.setWindowModality(QtCore.Qt.WindowModal)
        self.tl_cr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.tl_cr.setMinimumSize(0.2*desktop.width(), 0.2*desktop.height())
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
        for i in (('Добавить', self.onAdd),('Изменить',self.onEdItem),('Удалить', self.onDelete)):
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1]) 
            self.htop_b.addWidget(btn)
            
    def onAdd(self, a,new=('','','','','', ''), flag=None):
        def getName():
            value1 = lE_key.text()
            value2 = lE_kf.text()
            value3 = lE_w.text()
            value4 = lE_f.text()
            value5 = lE_pl.text()
            value6_1 = cb_pn.currentText()
            value6_2 = cb_pn.currentIndex()
            if (value1 and value3) == '':
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не введены значения')
            else:
                if value1 in list(self.dw.keys()) and not flag:
                    QtWidgets.QMessageBox.warning(None,'Предупреждение','Данное слово уже есть в словаре')
                    return
                dcont = [value1 ,value2, value3, value4, value5, value6_2+1]
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
                QtWidgets.QMessageBox.information(None,'Инфо', txt + value1)
                self.clear()
                self.editDict()
                tla.close()
                
        def fonSign():
            def onInsert():
                key = self.lv.currentIndex().data()
                lE_kf.insert(key)
                lE_kf.setFocus()
                tlf.close()
            dic = ['ə','əʊ','ɔ','ʌ','ʘ','ɶ','ʊ','ʃ','ɚ','ɳ','ʧ','ʤ','ʒ','ɜ']
            tlf = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
            tvbox = QtWidgets.QVBoxLayout()
            self.listBox(dic, flag=2, place=tvbox)
            tlfb = QtWidgets.QPushButton('Ok')
            tvbox.addWidget(tlfb)
            tlfb.clicked.connect(onInsert)
            tlf.setLayout(tvbox)
            tlf.show()
        
        tla = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tla.setWindowTitle('Добавить')
        #tla.setWindowModality(QtCore.Qt.WindowModal)
        #tla.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        tlavbox = QtWidgets.QVBoxLayout()
        lE_key = QtWidgets.QLineEdit()
        lE_kf = QtWidgets.QLineEdit()
        lE_w = QtWidgets.QLineEdit()
        lE_f = QtWidgets.QLineEdit() 
        lE_pl = QtWidgets.QLineEdit()
        cb_pn = QtWidgets.QComboBox()
        cb_pn.addItems(self.lst2)
        btn1 = QtWidgets.QPushButton('ʧ, ʊ, ʌ, ɳ, ʤ')
        btn2 = QtWidgets.QPushButton('Добавить')
        btn3 = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        form = QtWidgets.QFormLayout()
        k = 0
        for i in (lE_key, lE_kf, lE_w, lE_f, lE_pl):
            i.setText(new[k])
            k += 1
        if flag == 1:
            tla.setWindowTitle('Изменить')
            cb_pn.setCurrentText(new[k])
            value_k_old = new[0]   
        form.addRow('Иностранное слово:*', lE_key)
        form.addRow('Фонетический вид слова:', lE_kf)
        form.addRow('Фонетический знак', btn1)
        form.addRow('Перевод:*', lE_w)
        form.addRow('Формы глагола:',lE_f)
        form.addRow('Множественное число:',lE_pl)
        form.addRow('Часть речи:', cb_pn)
        form.addRow(hbox)
        btn1.clicked.connect(fonSign)
        btn2.clicked.connect(getName)
        btn3.clicked.connect(tla.close)
        tla.setLayout(form)
        tla.show()
             
    def onEdItem(self):
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            
        try:
            new = (key,) + (self.dw[key][1],) + (self.dw[key][2],) + (self.dw[key][3],) + (self.dw[key][4],) + (self.dw[key][5],)
        except KeyError:
                QtWidgets.QMessageBox.warning(None,'Предупреждение', 'Не выбрано слово')
                return
        self.onAdd(None,new, flag=1)
        self.search_flag = 0
        
    def onSearch(self):
        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Словарь не загружен')
            return
        if not self.dw:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>Словарь пуст</center>')
            self.vtop_t.addWidget(self.label3)
            return
        text = self.status.text()
        self.status.setText('Режим: поиск')
        def onFind():
            value = se.text()
            if value == '':
                QtWidgets.QMessageBox.warning(None,'Предупреждение', 'Не введены значения')
            else:
                if value not in list(self.dw.keys()):
                    QtWidgets.QMessageBox.warning(None,'Предупреждение','Данного слова нет в словаре')
                else:
                    self.search_flag = 1
                    self.search_key = value
                    self.displayWord()
                    srClose()
        def srClose():
            self.status.setText(text)
            sr.close()
        
        sr = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        sr.setWindowTitle('Поиск')
        sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)    
        srvbox = QtWidgets.QVBoxLayout()
        sl = QtWidgets.QLabel('Введите искомое слово(иност.)')
        se = QtWidgets.QLineEdit()
        srhbox = QtWidgets.QHBoxLayout()
        btn1 = QtWidgets.QPushButton('Найти')
        btn2 = QtWidgets.QPushButton('Закрыть')
        btn1.clicked.connect(onFind)
        btn2.clicked.connect(srClose)
        btn1.setAutoDefault(True) # enter
        se.returnPressed.connect(btn1.click) #enter
        srhbox.addWidget(btn1)
        srhbox.addWidget(btn2)
        srvbox.addWidget(sl)
        srvbox.addWidget(se)
        srvbox.addLayout(srhbox)
        sr.setLayout(srvbox)
        sr.show()
        
    def onDelete(self):
        key = self.lv.currentIndex().data()
        if not key:
            QtWidgets.QMessageBox.warning(None,'Предупреждение','Не выбрана запись для удаления')
            return
        self.delname.append(self.dw[key][0])
        self.dw.pop(key)
        QtWidgets.QMessageBox.information(None,'Инфо', 'Удалена запись: '+key)
        self.clear()
        self.editDict()
        
###################################################Deutsch        
class MyWindowD(MyWindowE):
    def __init__(self,parent=None):
        MyWindowE.__init__(self, parent)
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
            tlf.close()
            
        dic = ['ä', 'ö', 'ü', 'ß', 'Ä' , 'Ö',  'Ü']
        tlf = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tvbox = QtWidgets.QVBoxLayout()
        self.listBox(dic, flag=2, place=tvbox)
        tlfb = QtWidgets.QPushButton('Ok')
        if not self.on_sign_flag:
            tlcb = QtWidgets.QComboBox()
            tlcb.addItems(['Слово', 'Форма гл.'])
            tvbox.addWidget(tlcb)
        tvbox.addWidget(tlfb)
        tlfb.clicked.connect(onInsert)
        tlf.setLayout(tvbox)
        tlf.show()
        
    def onAdd(self, a,new=('','','','','', ''), flag=None):
        def getName():
            value1 = self.lE_key.text()
            value2 = cb_ar.currentText()
            value3 = lE_w.text()
            value4 = self.lE_f.text()
            value5 = cb_pl.currentText()
            value6_1 = cb_pn.currentText()
            value6_2 = cb_pn.currentIndex()
            if (value1 and value3) == '':
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не введены значения')
            else:
                if value1 in list(self.dw.keys()) and not flag:
                    QtWidgets.QMessageBox.warning(None,'Предупреждение','Данное слово уже есть в словаре')
                    return
                dcont = [value1 ,value2, value3, value4, value5, value6_2+1]
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
                QtWidgets.QMessageBox.information(None,'Инфо', txt + value1)
                self.clear()
                self.editDict()
                tla.close()
                
        tla = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tla.setWindowTitle('Добавить')
        #tla.setWindowModality(QtCore.Qt.WindowModal)
        tla.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        tlavbox = QtWidgets.QVBoxLayout()
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
        cb_pl.addItems(['','-e','-¨e','-en','-n','-¨er','-¨en', '-¨', '-s', '-er' ])
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
        form.addRow('Формы глагола:',self.lE_f)
        form.addRow('Множественное число:',cb_pl)
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
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не получен ответ')
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
        if not self.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Словарь не загружен')
            return
        if not self.dw:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>Словарь пуст</center>')
            self.vtop_t.addWidget(self.label3)
            return
        
        def onFind():
            value = self.se.text()
            if value == '':
                QtWidgets.QMessageBox.warning(None,'Предупреждение', 'Не введены значения')
            else:
                if value not in list(self.dw.keys()):
                    QtWidgets.QMessageBox.warning(None,'Предупреждение','Данного слова нет в словаре')
                else:
                    self.search_flag = 1
                    self.search_key = value
                    self.displayWord()
                    srClose()
        def srClose():
            self.status.setText(text)
            self.on_sign_flag = 0
            sr.close()
        
        text = self.status.text()
        self.status.setText('Режим: поиск')
        self.on_sign_flag = 2
        sr = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        sr.setWindowTitle('Поиск')
        #sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)    
        srvbox = QtWidgets.QVBoxLayout()
        sl = QtWidgets.QLabel('Введите искомое слово(иност.)')
        self.se = QtWidgets.QLineEdit()
        srhbox = QtWidgets.QHBoxLayout()
        btn1 = QtWidgets.QPushButton('Найти')
        btn_u = QtWidgets.QPushButton('ä, ö, ü, ß')
        btn2 = QtWidgets.QPushButton('Закрыть')
        btn1.clicked.connect(onFind)
        btn_u.clicked.connect(self.fonSign)
        btn2.clicked.connect(srClose)
        btn1.setAutoDefault(True) # enter
        self.se.returnPressed.connect(btn1.click) #enter
        srhbox.addWidget(btn1)
        srhbox.addWidget(btn_u)
        srhbox.addWidget(btn2)
        srvbox.addWidget(sl)
        srvbox.addWidget(self.se)
        srvbox.addLayout(srhbox)
        sr.setLayout(srvbox)
        sr.show()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Vokabelheft')
    window.resize(550,200)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width() 
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
    
    
    
    
"""
query = 'select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural, part.partname from dic inner join part on dic.partnumber=part.partnumber
limit 40 offset %s' % start
"""