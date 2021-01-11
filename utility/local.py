import sqlite3
from common import config
from  cv.preprocess import img_to_bytes

class LocalStorage:
    def __init__(self):
        self.connection = sqlite3.connect(config.LOCAL_DB)
        self.cursor = self.connection.cursor()

        if not self.checkTableExist():
            self.initializeDatabase()


    def initializeDatabase(self):
        self.cursor.execute(
            '''
            CREATE TABLE Images
            (
                id INTEGER,
                location_id INTEGER,
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


    def get_feature_by_id(self, index):
        self.cursor.execute(
            '''
            SELECT *
            FROM Images
            WHERE id = ?
            ''', [index])

        return self.cursor.fetchone()


    def get_feature_by_location_id(self, location_id):
        self.cursor.execute(
            '''
            SELECT *
            FROM Images
            WHERE location_id = ?
            ''', [Location_id])

        return self.cursor.fetchall()


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
            WHERE id = ?
            ''', [image, index])

        self.connection.commit()


    def delete_features(self, ids):
        idsQuery = tuple(ids)
        self.cursor.execute(
            '''
            DELETE FROM Images
            WHERE id in ?
            ''', [idsQuery])

        self.connection.commit()


    def __del__(self):
        self.connection.close()


storage = LocalStorage()