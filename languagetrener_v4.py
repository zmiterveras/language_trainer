#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
import sys,sqlite3, random, os


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        ico = QtGui.QIcon('dic.png')
        self.setWindowIcon(ico)
        self.win = None
        text_ch = """<center>Программа тренажер</center>\n
        <center>Выберите изучаемый язык</center>\n
        <center>Используйте меню Language</center>"""
        self.setCentralWidget(QtWidgets.QLabel(text_ch))       
        menuBar = self.menuBar()
        myMenu = menuBar.addMenu('&File')
        action = myMenu.addAction('&Create',  self.create)
        action = myMenu.addAction('&Open',  self.openDict)
        action = myMenu.addAction('&ViewAll',  self.viewAll)
        action = myMenu.addAction('&Close',  self.close)
        myLang = menuBar.addMenu('&Language')
        action = myLang.addAction('English', lambda x=1: self.langChoose(x, myMenu, statusBar))
        action = myLang.addAction('Deutsch', lambda x=2: self.langChoose(x, myMenu, statusBar))
        myAbout = menuBar.addMenu('&About')
        action = myAbout.addAction('&About programm', self.aboutProgramm)
        action = myAbout.addAction('About &me', self.aboutMe)
        statusBar = self.statusBar()
        self.count = 1
        
        
    def langChoose(self, x, myMenu, statusBar):
        if x == 1:
            self.win = MyWindowE()
            self.lang = 'eng '
        else:
            self.win = MyWindowD()
            self.lang = 'de'
        self.setCentralWidget(self.win)
        self.win.btncl.clicked.connect(self.close)
        if self.count == 1:
            self.win.label_am.setText('Empty')
            action = myMenu.addAction('&Save',  self.win.save_dict)
            statusBar.addWidget(self.win.status)
            statusBar.addPermanentWidget(self.win.label_am)
            self.count += 1
        
    def create(self):
        s, ok = QtWidgets.QInputDialog.getText(None, 'Имя словаря', 'Введите имя словаря')
        if ok and not s:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не задано имя словаря')
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(s)
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
        self.win.dict_name, fil_ = QtWidgets.QFileDialog.getOpenFileName(None, caption='Открыть словарь')
        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбран словарь')
        #print(self.win.dict_name)
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
        
    def viewAll(self):
        if not self.win.dict_name:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбран словарь')
        tabview = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        conn.setDatabaseName(self.win.dict_name)
        conn.open()
        stm = QtSql.QSqlRelationalTableModel(parent=window)
        stm.setTable('dic')
        stm.setSort(1, QtCore.Qt.AscendingOrder)
        stm.setRelation(6,QtSql.QSqlRelation('part', 'partnumber', 'partname'))
        stm.select()
        var_names = ['Фонетика', 'Артикль']
        if self.lang == 'de':
            var_name = var_names[1]
        else:
            var_name = var_names[0]
        for i,n in ((1, 'Слово'),(2, var_name),(3,'Перевод'),(4,'Формы глагла'),(5,'Мн.число'),(6,'Часть речи')):
            stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        vbox = QtWidgets.QVBoxLayout()
        tv = QtWidgets.QTableView()
        tv.setModel(stm)
        tv.hideColumn(0)
        for i,n in ((1, 100),(2, 100),(3,300),(4,150),(5,75),(6,150)):
            tv.setColumnWidth(i, n)
        vbox.addWidget(tv)
        btncl = QtWidgets.QPushButton('Close')
        btncl.clicked.connect(tabview.close)
        vbox.addWidget(btncl)
        tabview.setLayout(vbox)
        tabview.resize(915,350)
        tabview.show()
        
    def aboutProgramm(self):   
        ab = QtWidgets.QWidget(parent=self.win, flags=QtCore.Qt.Window)
        ab.setWindowTitle('About program')
        ab.setWindowModality(QtCore.Qt.WindowModal)
        ab.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        abbox = QtWidgets.QVBoxLayout()
        text = '''
        Это программа языковой тренажер.\n
        Главная особеннось которой - словарь\n
        составляется непосредствено пользователем\n
        в процессе его (само-)обучения языку.\n
        Версия: 3.0, 2020г
        '''
        abl = QtWidgets.QLabel(text)
        abb = QtWidgets.QPushButton('Close')
        abb.clicked.connect(ab.close)
        abbox.addWidget(abl)
        abbox.addWidget(abb)
        ab.setLayout(abbox)
        ab.show()
        
    def aboutMe(self):
        QtWidgets.QMessageBox.information(None,'Об авторе', 'Автор: @zmv')
          
    def closeEvent(self, e):
        #print('Goodbye')
        if not self.win: return
        if self.win.dict_name:
            self.win.save_dict()
        e.accept()
        QtWidgets.QWidget.closeEvent(self, e)       
###############################################################################              
class MyWindowE(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.makeWidget()
        self.dw = {}
        self.newname = [[],[],[],[],[],[]]
        self.delname = []
        self.changenote = [[],[],[],[],[],[],[]]
        self.dict_name = ''
        self.search_flag = 0
        self.search_key = 0
        self.lst1 = [1,2,3,4,5]
        self.lst2 = ['существительное','глагол','прилагательное','наречие', 'другое']
        self.label_am = QtWidgets.QLabel('')
        self.status = QtWidgets.QLabel('')
        
    def makeWidget(self):
        text = 'Программа тренажер\nОткройте или создайте словарь\n Используйте меню File'
        self.vbox = QtWidgets.QVBoxLayout()
        self.vtop = QtWidgets.QVBoxLayout()
        self.vtop_t = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vtop_t.addWidget(self.label)
        self.htop_b = QtWidgets.QHBoxLayout()
        self.vtop.addLayout(self.vtop_t)
        self.vtop.addLayout(self.htop_b)
        self.hbox = QtWidgets.QHBoxLayout()
        btnnames = [('View', self.dictView),('Trenning', self.onTrenning_mode),
                    ('Search', self.onSearch),('Edit', self.edit_dict)]
        btnlist = []
        for i in btnnames:
            btn = QtWidgets.QPushButton(i[0])
            btn.clicked.connect(i[1])
            self.hbox.addWidget(btn)
            btnlist.append(btn)
        self.btncl = QtWidgets.QPushButton('Close')
        self.hbox.addWidget(self.btncl) 
        self.vbox.addLayout(self.vtop)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        
    def save_dict(self):
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
        place = self.vtop_t
        self.clear()
        if not self.dw:
            self.label1 = QtWidgets.QLabel('<center>Словарь незагружен либо пуст</center>')
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
            self.lv.doubleClicked.connect(self.viewword)
        elif flag == 1:
            self.lv.doubleClicked.connect(self.onEdItemRun)
        else:
            pass
        
    def viewword(self, index):
        self.displayword()
        
    def onEdItemRun(self, event):
        self.onEdItem()
        
    def hLine(self,box):
        fr = QtWidgets.QFrame()
        fr.setFrameShape(QtWidgets.QFrame.HLine)
        box.addWidget(fr)      
        
    def displayword(self):
        def edit_run(a,win):
            tl_close(None, win, flag=1)
            self.onEdItem()    
        def tl_close(a, win, flag=None):
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
            btnc = QtWidgets.QPushButton('Close')
            btne = QtWidgets.QPushButton('Edit')
            btne.clicked.connect(lambda: edit_run(None, tl))
            btnc.clicked.connect(lambda: tl_close(None, tl)) 
            tlhbox.addWidget(btne)
            tlhbox.addWidget(btnc)
            tlvbox.addLayout(tlhbox)
            tl.setLayout(tlvbox)
            tl.show()
        if self.search_flag:
            key = self.search_key
        else:
            key = self.lv.currentIndex().data()
            #print(key)
        keyfon = self.dw[key][1]
        word = self.dw[key][2]
        form = self.dw[key][3]
        plural = self.dw[key][4]
        partname = self.dw[key][5]
        #print(keyfon, word, form, plural, partname)
        view()
        
    def onTrenning_mode(self):
        def onChoice():
            self.ch_value = cb_tm.currentIndex()
            tm.close()
            self.onTrenning()
            
        tm = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tm.setWindowTitle('Выбор тренировки')
        tm.resize(250,80)
        tm.setWindowModality(QtCore.Qt.WindowModal)
        tmvbox = QtWidgets.QVBoxLayout()
        cb_tm = QtWidgets.QComboBox()
        cb_tm.addItems(['Случайный выбор','Последние 20','Последние 40'])
        btn = QtWidgets.QPushButton('Выбрать')
        btn.clicked.connect(onChoice)
        tmvbox.addWidget(cb_tm)
        tmvbox.addWidget(btn)
        tm.setLayout(tmvbox)
        tm.show()
        
    def onTrenning(self):
        def sort(x):
            def sortid(item):
                return item[0]
            if (len(self.newname[0]) + len(list(self.dw.keys()))) < x+1:
                QtWidgets.QMessageBox.warning(None,'Предупреждение','Не достаточно слов для данного режима тренировки')
                return
            oldlist = []
            for key in list(self.dw.keys()):
                if self.dw[key][0] != None:
                    oldlist.append((self.dw[key][0], key))
            oldlist.sort(key=sortid)
            if len(self.newname[0]) >= x:
                self.dw_key = self.newname[0][-x:]
            else:
                self.dw_key = self.newname[0]
                for item in oldlist[-(x-len(self.newname[0])):]:
                    self.dw_key.append(item[1])
                    
        if self.dw:
            self.status.setText('Режим: тренировка')
            self.q_count = 0
            self.t_ans_count = 0
            if self.ch_value == 0:
                self.dw_key = list(self.dw.keys())
            elif self.ch_value == 1:
                sort(20)
            else:
                sort(40)
            self.onRun()
        else:
            self.clear()
            self.label3 = QtWidgets.QLabel('<center>Словарь незагружен либо пуст</center>')
            self.vtop_t.addWidget(self.label3)
            
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
        btnc = QtWidgets.QPushButton('Next', self)
        btnc.setFocus()
        btnc.clicked.connect(self.onRun)
        btnc.setAutoDefault(True)
        self.htop_b.addWidget(btnc)
        text = "Правильных ответов/вопросов: " + str(self.t_ans_count) + "/" + str(self.q_count)
        self.label_am.setText(text)
        
    def edit_dict(self):
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
                #print('newname= ', self.newname)
                #print('changenote=', self.changenote)
                self.clear()
                self.edit_dict()
                tla.close()
                
        def fon_sign():
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
        #print('new=', new)
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
        btn1.clicked.connect(fon_sign)
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
        text = self.status.text()
        print(text)
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
                    self.displayword()
                    sr_close()
        def sr_close():
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
        btn2.clicked.connect(sr_close)
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
        #print('delname', self.delname)
        self.dw.pop(key)
        QtWidgets.QMessageBox.information(None,'Инфо', 'Удалена запись: '+key)
        self.clear()
        self.edit_dict()
        
class MyWindowD(MyWindowE):
    def __init__(self,parent=None):
        MyWindowE.__init__(self, parent)
        
    def onAdd(self, a,new=('','','','','', ''), flag=None):
        def getName():
            value1 = lE_key.text()
            value2 = cb_ar.currentText()
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
                #print('newname= ', self.newname)
                #print('changenote=', self.changenote)
                self.clear()
                self.edit_dict()
                tla.close()
                
        def fon_sign():
            def onInsert():
                key = self.lv.currentIndex().data()
                field = tlcb.currentIndex()
                if field == 0:
                    lE_key.insert(key)
                    lE_key.setFocus()
                elif field == 1:
                    lE_f.insert(key)
                    lE_f.setFocus()
                else:
                    lE_pl.insert(key)
                    lE_pl.setFocus()
                tlf.close()
            dic = ['Ä', 'ä' , 'Ö', 'ö' , 'Ü', 'ü', 'ß']
            tlf = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
            tvbox = QtWidgets.QVBoxLayout()
            self.listBox(dic, flag=2, place=tvbox)
            tlfb = QtWidgets.QPushButton('Ok')
            tlcb = QtWidgets.QComboBox()
            tlcb.addItems(['Слово', 'Форма гл.', 'Мн.число'])
            tvbox.addWidget(tlcb)
            tvbox.addWidget(tlfb)
            tlfb.clicked.connect(onInsert)
            tlf.setLayout(tvbox)
            tlf.show()
        
        tla = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tla.setWindowTitle('Добавить')
        #tla.setWindowModality(QtCore.Qt.WindowModal)
        #tla.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        tlavbox = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        lE_key = QtWidgets.QLineEdit()
        article = ['', 'der', 'die', 'das']
        cb_ar = QtWidgets.QComboBox()
        cb_ar.addItems(article)
        hbox1.addWidget(lE_key)
        hbox1.addWidget(cb_ar)
        btn1 = QtWidgets.QPushButton('ä, ö, ü, ß')
        lE_w = QtWidgets.QLineEdit()
        lE_f = QtWidgets.QLineEdit()
        lE_pl = QtWidgets.QLineEdit()
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
        new = new[:1] + new[2:]
        for n, i  in enumerate([lE_key, lE_w, lE_f, lE_pl]):
            i.setText(new[n])       
        form.addRow('Иностранное слово:*', hbox1)
        form.addRow('Перевод:*', lE_w)
        form.addRow('Формы глагола:',lE_f)
        form.addRow('Множественное число:',lE_pl)
        form.addRow('Часть речи:', cb_pn)
        form.addRow('Умляут', btn1)
        form.addRow(hbox2)
        btn1.clicked.connect(fon_sign)
        btn2.clicked.connect(getName)
        btn3.clicked.connect(tla.close)
        tla.setLayout(form)
        tla.show()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Language trener')
    window.resize(250,100)
    window.show()
    sys.exit(app.exec_())