from modules.parser_excel import parser_excel

example: str = f"Пример: физика 80, русский язык 90, математика 77"
admin: str = '@ArikMoroz'


def answer(string: str):
    match string:
        case "/start":
            return f'Введите Ваши результаты ЕГЭ по трём предметам через запятую в формате "предмет пробел оценка".\n\n{example}'
        case "/help":
            return (
                f"По вопросам жалоб и предложений просьба писать в аккаунт: {admin}"
            )
        #бновление данных excel
        case "/data_update":
            return parser_excel("./data/specialties.xlsx", "./data/spec.json")
        case _:
            return (
                "<b>Вы проходите на следующие специальности:</b>\n\n✅{}".format(
                    "\n\n✅".join(string)
                )
                if type(string) == list
                else string
            )


def error(val: list):
    if type(val[1]) == int:

        def info():
            if val[0].isdigit():
                return f'Вы не ввели название предмета для балла "{val[0]}"'
            elif not len(val[0]):
                return f"Обнаружен пустой запрос"
            elif not val[0].isdigit():
                return f'Вы не ввели балл для предмета "{val[0]}"'
            else:
                return val

        return (
            f"❌{info()} (позиция {val[1]})\n\n{example}"
        )

    elif "typo" in val[1]:
        return f'<b>❌</b>Не найдено в базе: "{val[0]}"\n\n{example}\nВведите данные повторно.'
    elif "length" in val[1]:
        return f'<b>❌</b>Введите три любых предмета на выбор\n\n{example}'
    elif "min_score" in val[1]:
        return f'😔Слишком низкий балл у предмета "{val[0][0]}", минимальный проходной балл "{val[0][1]}"'
    elif "hyper_score" in val[1]:
        return f'😑Балл не может быть больше 100 ("{val[0]}")'
    else:
        return f"Неизвестная ошибка\n\n{example}"
