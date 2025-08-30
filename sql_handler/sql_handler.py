#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from PyQt5 import QtSql


class SqlHandler:

    def __init__(self,bases_path: str, interface_language):
        self.database = os.path.join(bases_path, 'dictionary_desktop.sqlite')
        # self.interface_lang = interface_language
        # self.query_open_dict = """select dic.id, dic.key, dic.keyfon, dic.word, dic.form, dic.plural,
        #             part.partname from dic inner join part on dic.partnumber=part.partnumber
        #             """
        # self.number_part_of_speech = [1, 2, 3, 4, 5]
        # self.name_part_of_speech = [self.interface_lang['noun'],
        #                             self.interface_lang['verb'],
        #                             self.interface_lang['adjective'],
        #                             self.interface_lang['adverb'],
        #                             self.interface_lang['another']]

    def connect_db(self):
        connect = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        connect.setDatabaseName(self.database)
        connect.open()
        query = QtSql.QSqlQuery()
        return connect, query

    # def create_db(self, db_name):
    #     connect, query = self.connect_db(db_name)
    #     if 'dic' not in connect.tables():
    #         query_create_table_dic = '''create table dic (id integer primary key autoincrement,
    #         key text, keyfon text, word text, form text, plural text ,partnumber integer)'''
    #         query.exec(query_create_table_dic)
    #     if 'part' not in connect.tables():
    #         query.clear()
    #         query_create_table_part = """create table part (id integer primary key autoincrement,
    #         partnumber integer, partname text)"""
    #         query.exec(query_create_table_part)
    #         query.clear()
    #         query.prepare('insert into part values (null, :count, :name)')
    #         query.bindValue(':count', self.number_part_of_speech)
    #         query.bindValue(':name', self.name_part_of_speech)
    #         query.execBatch()
    #     connect.close()

    def create_db(self):
        connect, query = self.connect_db()
        if 'dictionary' not in connect.tables():
            query_create_table_dic = '''
            create table dictionary (id integer primary key autoincrement,
            word text, phonetic text, article text, translate text, form text,
            plural text, part integer, language integer)
            '''
            query.exec(query_create_table_dic)
        connect.close()
        
    # def open_db(self, db_name) -> dict:
    #     connect, query = self.connect_db(db_name)
    #     query.exec(self.query_open_dict)
    #     dictionary = {}
    #     if query.isActive():
    #         query.first()
    #         while query.isValid():
    #             dictionary[query.value('key')] = [query.value('id'), query.value('keyfon'),
    #                                                query.value('word'), query.value('form'),
    #                                                query.value('plural'), query.value('partname')]
    #             query.next()
    #     connect.close()
    #     return dictionary

    def open_db(self, language) -> dict:
        query_open_dict = '''
        select * from dictionary where language="%d"
        ''' % language
        connect, query = self.connect_db()
        query.exec(query_open_dict)
        dictionary = {}
        if query.isActive():
            query.first()
            while query.isValid():
                dictionary[query.value('word')] = [query.value('id'), query.value('phonetic'),
                                                   query.value('article'), query.value('translate'),
                                                   query.value('form'), query.value('plural'),
                                                   query.value('part'), query.value('language')]
                query.next()
        connect.close()
        return dictionary
    
    def open_db_debug(self, db_name) -> dict:
        dictionary = {}
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(self.query_open_dict)
        for row in curs.fetchall():
            dictionary[row[1]] = [row[0], row[2], row[3], row[4], row[5], row[6]]
        conn.close()
        return dictionary

    # def save_dict(self, db_name, del_names: list, new_name: list, change_note: list):
    #     connect, query = self.connect_db(db_name)
    #     # удаление
    #     if del_names:
    #         query.prepare('delete from dic where id=:i')
    #         query.bindValue(':i', del_names)
    #         query.execBatch()
    #         query.clear()
    #     # добавление
    #     if new_name[0]:
    #         query_add_records = '''insert into dic values (null, :key, :keyfon, :word, :form,
    #                                                 :plural, :partnumber)'''
    #         query.prepare(query_add_records)
    #         query.bindValue(':key', new_name[0])
    #         query.bindValue(':keyfon', new_name[1])
    #         query.bindValue(':word', new_name[2])
    #         query.bindValue(':form', new_name[3])
    #         query.bindValue(':plural', new_name[4])
    #         query.bindValue(':partnumber', new_name[5])
    #         query.execBatch()
    #         query.clear()
    #     # изменение
    #     if change_note[0]:
    #         query_change_records = '''update dic set key=:key, keyfon=:keyfon, word=:word, form=:form,
    #                         plural=:plural, partnumber=:partnumber where id=:id'''
    #         query.prepare(query_change_records)
    #         query.bindValue(':key', change_note[1])
    #         query.bindValue(':keyfon', change_note[2])
    #         query.bindValue(':word', change_note[3])
    #         query.bindValue(':form', change_note[4])
    #         query.bindValue(':plural', change_note[5])
    #         query.bindValue(':partnumber', change_note[6])
    #         query.bindValue(':id', change_note[0])
    #         query.execBatch()
    #     connect.close()

    def save_dict(self, db_name, del_names: list, new_name: list, change_note: list):
        connect, query = self.connect_db(db_name)
        # удаление
        if del_names:
            query.prepare('delete from dictionary where id=:i')
            query.bindValue(':i', del_names)
            query.execBatch()
            query.clear()
        # добавление
        if new_name[0]:
            query_add_records = '''insert into dictionary values (null, :word, :phonetic, :article, :translate, :form,
                                                    :plural, :part, :language)'''
            query.prepare(query_add_records)
            query.bindValue(':word', new_name[0])
            query.bindValue(':phonetic', new_name[1])
            query.bindValue(':article', new_name[2])
            query.bindValue(':translate', new_name[3])
            query.bindValue(':form', new_name[4])
            query.bindValue(':plural', new_name[5])
            query.bindValue(':part', new_name[6])
            query.bindValue(':language', new_name[7])
            query.execBatch()
            query.clear()
        # изменение
        if change_note[0]:
            query_change_records = '''update dictionary set word=:word, phonetic=:phonetic, article=:article,
                            translate=:translate, form=:form, plural=:plural, part=:part, language=:language
                            where id=:id'''
            query.prepare(query_change_records)
            query.bindValue(':word', change_note[1])
            query.bindValue(':phonetic', change_note[2])
            query.bindValue(':article', change_note[3])
            query.bindValue(':translate', change_note[4])
            query.bindValue(':form', change_note[5])
            query.bindValue(':plural', change_note[6])
            query.bindValue(':part', change_note[7])
            query.bindValue(':language', change_note[8])
            query.bindValue(':id', change_note[0])
            query.execBatch()
        connect.close()
        
    def is_db_available(self):
        return True if os.path.exists(self.database) else False