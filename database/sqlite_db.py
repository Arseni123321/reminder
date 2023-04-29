import logging
import sqlite3
import uuid
from datetime import datetime, timedelta
from pprint import pprint
from typing import Union

from bots.translater_bot.config_reader import load_config

config = load_config(r'Z:\Pt9_01\AreniVasetski\bots\ReminderBot\config\config.ini')

class Remind(NamedTuple):
    user_id: int
    name: str
    text: str


class SQLiteDB:
    def __init__(self):
        self.connection = sqlite3.connect(r'Z:\Pt9_01\AreniVasetski\bots\ReminderBot\database\users.db')
        self.cursor = self.connection.cursor()
        self._create_table_users()

    def _create_table_users(self):
        """create table

        :return:
        """
        with self.connection:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users"
                                "("
                                "id TEXT UNIQUE,"
                                "user_id INTEGER,"
                                "name TEXT,"
                                "date TEXT,"
                                "text TEXT"
                                ")")

    def insert_one_value(self, user_id: int, name: str, date: str, text: str, _id=None) -> Union[bool, int, tuple]:
        """
        Vstavka nopominania
        :param user_id: id user of telegram
        :param name: name user in telegram
        :param date:
        :param text:
        :param _id:
        :return:
        """
        try:
            if not _id:
                value = (str(uuid.uuid4()), user_id, name, date, text)
            else:
                value = (user_id, name, date, text)
            if not self._check_duplicates(value):
                with self.connection:
                    self.cursor.execute(
                        "INSERT INTO users (id, user_id, name, date, text) VALUES (?,?,?,?,?)", value
                    )
                    return True, 200, value
            else:
                return False, 404, value
        except Exception as ex:
            logging.error(f'{repr(ex)}')
            return False, 404, f'{repr(ex)}'

    def _check_duplicates(self, value: tuple) -> bool:
        """Проверка на дубликаты

        :param value: кортеж значений
        :return:
        """
        with self.connection:
            all_data = self.cursor.execute('SELECT user_id, name, date, text FROM users')
            for remind in all_data.fetchall():
                if remind == value[1:]:
                    return True

    def get_all_values_json(self):
        """Получкение всех значений из базы данных

        :return:
        """
        try:
            with self.connection:
                all_data = self.cursor.execute('SELECT * FROM users')
                all_posts = self._get_formatted_json(all_data.fetchall())
                return all_posts, 200
        except Exception as ex:
            logging.error(f'{repr(ex)}')
            return repr(ex), 404

    def _get_formatted_json(self, users: Union[list, tuple]):
        """Возвращает данные в json

        :param users:
        :return:
        """
        all_posts = dict()
        for user in users:
            _id = user[0]
            user_id = user[1]
            name = user[2]
            date = user[3]
            text = user[4]
            all_posts[_id] = {
                'user_id': user_id,
                'name': name,
                'date': date,
                'text': text
            }
        return all_posts

    def delete_all_values(self):
        """

        :return:
        """
        with self.connection:
            try:
                self.cursor.execute('DELETE FROM users')
                return 'All delete'
            except Exception as ex:
                logging.error(f'{repr(ex)}')
                return repr(ex), 404

    def send_remind(self):
        """send remind

        :return:
        """
        with self.connection:
            time_direction = config.tg_bot.TIME_DIRECTION
            now = datetime.now() + timedelta(hours=time_direction)
            now_date = now.strftime('%H:%M - %d.%m.%Y')
            result = self.cursor.execute("SELECT * FROM users WHERE date = ?", (now_date,))

            all_data = result.fetchall()
            if all_data:
                all_id = tuple(
                    [_id[0] for _id in all_data]
                )
                self._delete_values(all_id)
                for value in all_data:
                    user_id = value[1]
                    name = value[2]
                    text = value[-1]
                    yield Remind(user_id, name, text)
            else:
                return

    def _delete_values(self, all_id: tuple):
        """

        :param all_id:
        :return:
        """
        with self.connection:
            for _id in all_id:
                self.cursor.execute('DELETE FROM users WHERE id = ?', (_id,))


if __name__ == '__main__':
    db = SQLiteDB()
    print(db.insert_one_value(user_id=123456789, name='Areni', date=str(datetime.now()), text='Какое-то напоминание'))
    pprint(db.get_all_values_json()[0])
