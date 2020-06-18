import os
import sqlite3

class DataBase():
    __con, __cur = None, None
    
    ###############################################
    # private functions
    @classmethod
    def __open(cls):
        cls.__con = sqlite3.connect( os.path.join( os.getcwd(), 'res', 'db', 'save.db' ) )
        cls.__cur = cls.__con.cursor()
    
    @classmethod
    def __close(cls):
        cls.__con.close()

    @classmethod
    def __execute(cls, contents, isCommit):
        cls.__open()
        cls.__cur.execute(contents)
        if isCommit:
            cls.__con.commit()
        else:
            row = cls.__cur.fetchall()
        cls.__close()

        return None if isCommit else row

    ###############################################
    # 답변 목록 가져오기
    @classmethod
    def select_post_all(cls):
        return cls.__execute('select ID, Title, Contents from post_index', False)
    
    # 답변 목록 제거하기
    @classmethod
    def delete_post(cls, id):
        cls.__execute('delete from post_index where ID={}'.format(id), True)
    
    # 답변 목록 추가하기
    @classmethod
    def insert_post(cls, title, contents):
        cls.__execute("insert into post_index(Title, Contents) values('{}', '{}')".format(title, contents), True)
    
    # 답변 목록 수정하기
    @classmethod
    def update_post(cls, id, title, contents):
        cls.__execute("update post_index set Title='{}', Contents='{}' where id={};".format(title, contents, id), True)
    
    ###############################################
    # 검색 키워드 목록 가져오기
    @classmethod
    def select_keyword_all(cls):
        return cls.__execute('select ID, Title from search_keyword', False)
    
    # 검색 키워드 목록 제거하기
    @classmethod
    def delete_keyword(cls, id):
        cls.__execute('delete from search_keyword where ID={}'.format(id), True)
    
    # 검색 키워드 목록 추가하기
    @classmethod
    def insert_keyword(cls, title):
        cls.__execute("insert into search_keyword(Title) values('{}')".format(title), True)

    # 검색 키워드 목록 수정하기
    @classmethod
    def update_keyword(cls, id, title):
        cls.__execute("update search_keyword set Title='{}' where id={};".format(title, id), True)
    
    ###############################################
    # 검색 크롤링 목록 가져오기
    @classmethod
    def select_search_all(cls):
        return cls.__execute('select ID, Title, Url from search', False)
    
    # 검색 크롤링 목록 제거하기
    @classmethod
    def delete_search(cls, id):
        cls.__execute('delete from search where ID={}'.format(id), True)
    
    # 검색 크롤링 목록 추가하기
    @classmethod
    def insert_search(cls, title, url):
        cls.__execute("insert into search(Title, Url) values('{}', '{}')".format(title, url), True)

    # 검색 크롤링 목록 수정하기
    #@classmethod
    #def update_search(cls, id, title):
    #    cls.__execute("update search set Title='{}' where id={};".format(title, id), True)