import psycopg2
import psycopg2.extras
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Database:

    def __init__(self, host, user, password, db_name):

        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit = True

    def create_table_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    id serial PRIMARY KEY,
                    vk_id varchar(20) NOT NULL,
                    to_id varchar(20),
                    bot_path varchar(200),
                    sex integer,
                    age_from integer,
                    age_to integer,
                    city varchar(200),
                    offset_user integer DEFAULT 0)        
                """
            )
        print("[INFO] Table USERS was created.")

    def insert_data_users(self, vk_id):
        """ВСТАВКА ДАННЫХ В ТАБЛИЦУ USERS"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users (vk_id) 
                VALUES ('{vk_id}');"""
            )

    def update_data_users(self, vk_id, field, value):
        """ВСТАВКА ДАННЫХ В ТАБЛИЦУ USERS"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users
                SET {field} = {f"'{value}'" if value is not None else "NULL"} 
                WHERE vk_id = '{vk_id}'"""
            )

    def clear_data_user(self, vk_id):
        self.update_data_users(vk_id, "to_id", None)
        self.update_data_users(vk_id, "bot_path", None)
        self.update_data_users(vk_id, "sex", None)
        self.update_data_users(vk_id, "age_from", None)
        self.update_data_users(vk_id, "age_to", None)
        self.update_data_users(vk_id, "city", None)
        self.update_data_users(vk_id, "offset_user", 0)

    def select_data_users(self, vk_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM users
                    WHERE vk_id = '{vk_id}'
                """
            )
            return cursor.fetchone()

    def create_table_seen_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS seen_users(
                    id serial PRIMARY KEY,
                    vk_id varchar(20) NOT NULL,
                    to_id varchar(20) NOT NULL,
                    couple_id varchar(20) NOT NULL)        
                """
            )
        print("[INFO] Table SEEN_USERS was created.")

    def insert_data_seen_users(self, vk_id, to_id, couple_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO seen_users (vk_id, to_id, couple_id) 
                VALUES ('{vk_id}', '{to_id}', '{couple_id}');"""
            )

    def select_data_seen_users(self, vk_id, to_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM seen_users
                    WHERE vk_id = '{vk_id}' AND to_id = '{to_id}'
                """
            )
            return cursor.fetchall()

    def drop_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE IF EXISTS users CASCADE;"""
            )
            print('[INFO] Table USERS was deleted.')

    def drop_seen_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE  IF EXISTS seen_users CASCADE;"""
            )
            print('[INFO] Table SEEN_USERS was deleted.')

    def creating_database(self):
        self.drop_users()
        self.drop_seen_users()
        self.create_table_users()
        self.create_table_seen_users()


if __name__ == '__main__':
    if input("Вы действительно хотите создать новую базу данных? (y/n): ") == "y":
        db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
        db.creating_database()
    else:
        print("Пока.")
