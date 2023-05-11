from vk_bot import Bot
from vk_bot.constants import *
from settings import *
from database import Database


def main():

    db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    bot = Bot(TOKEN_COMMUNITY, TOKEN_USER, db)

    @bot.event(MESSAGE_NEW, MESSAGE_ME)
    def message_new_to_me(event):
        user_id = event.user_id
        user_text = event.text
        user_text_lower = user_text.lower()
        user_data = db.select_data_users(user_id)

        if not user_data:
            db.insert_data_users(user_id)
            user_data = db.select_data_users(user_id)

        if user_text_lower == "начать поиск":

            db.clear_data_user(user_id)
            db.update_data_users(user_id, "bot_path", "fill")
            bot.send_message(user_id, "🆔 Введите ID пользователя для кого мы будем искать пару, "
                                      "если хотите для себя, введите: \"Для себя\"")

        elif user_data["bot_path"] == "fill":

            flag_add = False
            flag_repeat = False
            if not user_data["to_id"]:
                if user_text_lower == "для себя":
                    to_id = user_id
                else:
                    to_id = user_text
                age = bot.get_age(to_id)
                db.update_data_users(user_id, "to_id", to_id)
                db.update_data_users(user_id, "sex", bot.get_sex(to_id))
                db.update_data_users(user_id, "age_to", age)
                db.update_data_users(user_id, "age_from", age)
                db.update_data_users(user_id, "city", bot.get_city(to_id))
                user_data = db.select_data_users(user_id)
                flag_add = True
            if not user_data["sex"]:
                if flag_add:
                    flag_repeat = True
                    bot.send_message(user_id, "Введите пол: \n1. Женщина\n2. Мужчина")
                else:
                    if user_text == "1" or user_text == "2":
                        db.update_data_users(user_id, "sex", user_text)
                        flag_add = True
                    else:
                        bot.send_message(user_id, "Введите пол: \n1. Женщина\n2. Мужчина")
            if not user_data["age_from"] and not flag_repeat:
                if flag_add:
                    flag_repeat = True
                    bot.send_message(user_id, "Введите нижнюю границу возраста")
                else:
                    flag_add = True
                    db.update_data_users(user_id, "age_from", user_text)
            if not user_data["age_to"] and not flag_repeat:
                if flag_add:
                    flag_repeat = True
                    bot.send_message(user_id, "Введите верхнюю границу возраста")
                else:
                    flag_add = True
                    db.update_data_users(user_id, "age_to", user_text)
            if not user_data["city"] and not flag_repeat:
                if flag_add:
                    flag_repeat = True
                    bot.send_message(user_id, "Введите город")
                else:
                    db.update_data_users(user_id, "city", user_text)
            if not flag_add or not flag_repeat:
                db.update_data_users(user_id, "bot_path", "search")
                user_data = db.select_data_users(user_id)
                offset_user = len(db.select_data_seen_users(user_id, user_data["to_id"]))
                user_data["offset_user"] = offset_user
                db.update_data_users(user_id, "offset_user", offset_user)
                bot.send_message(user_id, "🔎 Начинаю поиск...")
                user_couple = bot.search_couple_user(user_data)
                db.insert_data_seen_users(user_id, user_data["to_id"], user_couple["vk_id"])
                photo_ids = bot.get_photos_ids(user_couple["vk_id"])[:3]
                bot.print_search_couple_user(user_id, user_couple, photo_ids)

        elif user_data["bot_path"] == "search":
            if user_text_lower == "вперёд":
                offset_user = user_data["offset_user"]+1
                db.update_data_users(user_id, "offset_user", offset_user)
                user_data["offset_user"] = offset_user
                user_couple = bot.search_couple_user(user_data)
                db.insert_data_seen_users(user_id, user_data["to_id"], user_couple["vk_id"])
                photo_ids = bot.get_photos_ids(user_couple["vk_id"])[:3]
                bot.print_search_couple_user(user_id, user_couple, photo_ids)
            else:
                bot.send_message(user_id, "❗ Если хотите увидеть следующего человека, введите: \"Вперёд\"")
        else:
            bot.send_message(user_id, "🎃 Для начала, введите: \"Начать поиск\"")

    bot.run()


if __name__ == '__main__':
    main()
