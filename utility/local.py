import sqlite3
from common import config
from cv import backend

class LocalStorage:
    def __init__(self):
        # self.connection = sqlite3.connect(config.LOCAL_DB)
        # self.cursor = self.connection.cursor()
        if not self.checkTableExist():
            self.initializeDatabase()

    
    def create_connection(self):
        return self.connection.cursor()


    def initializeDatabase(self):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                CREATE TABLE Images
                (
                    id INTEGER,
                    location_id INTEGER,
                    body BLOB
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE UnknownImages
                (
                    id INTEGER,
                    location_id INTEGER,
                    body BLOB
                )
                ''')

            conn.commit()


    def checkTableExist(self):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT count(name) 
                FROM sqlite_master 
                WHERE type='table' 
                    AND 
                    name='Images' 
                ''')  
            
            if cur.fetchone()[0] == 1:
                return True
            else:
                return False


    def get_features(self, top=None):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()

            if top is None:
                cur.execute(
                    '''
                    SELECT *
                    FROM Images
                    ''')
            else:
                cur.execute(
                    '''
                    SELECT *
                    FROM Images
                    LIMIT ?
                    ''', [top])

            return [(x[0], x[1], backend.pickle_to_feature(x[2])) for x in cur.fetchall()]

    def get_feature_by_id(self, index):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT *
                FROM Images
                WHERE id = ?
                ''', [index])

            data = cur.fetchone()

            return (data[0], data[1], backend.pickle_to_feature(data[2]))


    def get_feature_by_location_id(self, location_id):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT *
                FROM Images
                WHERE location_id = ?
                ''', [location_id])

            return [(x[0], x[1], backend.pickle_to_feature(x[2])) for x in cur.fetchall()]


    def add_feature(self, product_id, location_id, kp, desc):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            feature = backend.feature_to_pickle(kp, desc)
            cur = conn.cursor()

            cur.execute(
                '''
                INSERT INTO Images
                (id, location_id, body)
                VALUES
                (?, ?, ?)
                ''', [product_id, location_id, feature])

            conn.commit()


    def update_feature(self, index, kp, desc):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            feature = backend.feature_to_pickle(kp, desc)
            cur = conn.cursor()

            cur.execute(
                '''
                UPDATE Images
                SET body = ?
                WHERE id = ?
                ''', [feature, index])

            conn.commit()


    def delete_features(self, ids):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()
            idsQuery = tuple(ids)
            cur.execute(
                '''
                DELETE FROM Images
                WHERE id in ?
                ''', [idsQuery])

            conn.commit()


    def get_undetected_features_by_location_id(self, location_id):
        with sqlite3.connect(config.LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT *
                FROM UnknownImages
                WHERE location_id = ?
                ''', [location_id])

            return [(x[0], x[1], backend.pickle_to_feature(x[2])) for x in cur.fetchall()]


storage = LocalStorage()