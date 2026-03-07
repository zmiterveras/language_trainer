#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from PyQt5 import QtSql


class SqlHandler:

    def __init__(self,bases_path: str):
        self.database = os.path.join(bases_path, 'dictionary_desktop.sqlite')

    def connect_db(self):
        connect = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        connect.setDatabaseName(self.database)
        connect.open()
        query = QtSql.QSqlQuery()
        return connect, query

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

    def open_db(self, language: int) -> dict:
        query_open_dict = f'select * from dictionary where language={language}'
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
        
    def is_db_available(self):
        return True if os.path.exists(self.database) else False

    def add_record(self, new_rec: list):
        connect, query = self.connect_db()
        query_add_records = '''insert into dictionary values (null, :word, :phonetic, :article, :translate, :form,
                                                            :plural, :part, :language)'''
        query.prepare(query_add_records)
        query.bindValue(':word', new_rec[0])
        query.bindValue(':phonetic', new_rec[1])
        query.bindValue(':article', new_rec[2])
        query.bindValue(':translate', new_rec[3])
        query.bindValue(':form', new_rec[4])
        query.bindValue(':plural', new_rec[5])
        query.bindValue(':part', new_rec[6])
        query.bindValue(':language', new_rec[7])
        query.exec_()
        connect.close()
        
    def update_record(self, updated_rec: list):
        connect, query = self.connect_db()
        query_change_records = '''update dictionary set word=:word, phonetic=:phonetic, article=:article,
                                    translate=:translate, form=:form, plural=:plural, part=:part, language=:language
                                    where id=:id'''
        query.prepare(query_change_records)
        query.bindValue(':word', updated_rec[1])
        query.bindValue(':phonetic', updated_rec[2])
        query.bindValue(':article', updated_rec[3])
        query.bindValue(':translate', updated_rec[4])
        query.bindValue(':form', updated_rec[5])
        query.bindValue(':plural', updated_rec[6])
        query.bindValue(':part', updated_rec[7])
        query.bindValue(':language', updated_rec[8])
        query.bindValue(':id', updated_rec[0])
        query.exec_()
        connect.close()

    def delete_record(self, rec_id: int):
        connect, query = self.connect_db()
        query.prepare('delete from dictionary where id=:rec_id')
        query.bindValue(':rec_id', rec_id)
        query.exec_()
        connect.close()
