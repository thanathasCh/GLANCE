import sqlite3
from  common.cv.preprocess import img_to_bytes

class LocalStorage:
    def __init__(self):
        self.connection = sqlite3.connect('local.db')
        self.cursor = self.connection.cursor()

        if not self.checkTableExist():
            self.initializeDatabase()


    def initializeDatabase(self):
        self.cursor.execute(
            '''
            CREATE TABLE Images
            (
                id INTEGER,
                body BLOB
            )
            ''')


    def checkTableExist(self):
        self.cursor.execute(
            '''
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' 
                AND 
                  name='Images' 
            ''')  
        
        if self.cursor.fetchone()[0] == 1:
            return True
        else:
            return False


    def get_features(self, top=None):
        topQuery = '' if top is None else f'LIMIT {top}'

        self.cursor.execute(
            '''
            SELECT *
            FROM Images
            ?
            ''', [topQuery])

        return self.cursor.fetchall()


    def get_feature(self, index):
        self.cursor.execute(
            '''
            SELECT *
            FROM Images
            WHERE id = ?
            ''', [index])

        return self.cursor.fetchone()


    def add_feature(self, index, image):
        feature = img_to_bytes(image)

        self.cursor.execute(
            '''
            INSERT INTO Images
            (id, body)
            VALUES
            (?, ?)
            ''', [index, feature])

        self.connection.commit()


    def update_feature(self, index, image):
        feature = img_to_bytes(image)

        self.cursor.execute(
            '''
            UPDATE Images
            SET body = ?
            WHERE index = ?
            ''', [image, index])

        self.connection.commit()


    def __del__(self):
        self.connection.close()