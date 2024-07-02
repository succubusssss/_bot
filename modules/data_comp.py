from modules.parser_input import parser
import modules.messages as msg


def get_subj_list(json_data):
    """Получает список всех предметов из файла JSON
    @json_data - данные, полученные из файла JSON
    """
    list_subj: list = []
    for index, key in enumerate(json_data):
        list_subj.extend(json_data[str(index)]["subject"])
        list_subj.extend(json_data[str(index)]["choice"])
    return list_subj


def data_comp(user_data: dict | str, json_data: dict):
    """Сравнивает данные полученные от пользователя с данными из базы, и отдаёт подходящие специальности
    @user_data - данные, полученные от пользователя
    @json_data - данные загруженные из фала *.json
    """
    # список подходящих специальностей
    suit_spec: list = []
    u_data = user_data

    # получаем список всех предметов из файла JSON для поиска опечаток
    _list: list = get_subj_list(json_data)
    # обрабатываем строку пользователя
    parsed_data = parser(user_data, _list)
    if type(parsed_data) == str:
        return parsed_data
    # Проверяем, что пользователь ввёл именно три предмета
    if len(parsed_data) != 3:
        return msg.error([parsed_data, "length"])

    # список предметов, полученный от пользователя
    key_list: list = []

    for key in parsed_data:
        key_list.append(key)

    for index, key in enumerate(json_data):
        subject_list = json_data[str(index)]["subject"]
        choice_subj_list = json_data[str(index)]["choice"]
        score = json_data[str(index)]["score"]
        rating = json_data[str(index)]["rating"]
        speciality = json_data[str(index)]["specialty"]

        # совпадение с обязательными предметами
        match_subj = list(set(key_list) & set(subject_list))
        # совпадение с предметами на выбор
        match_choice = list(set(key_list) & set(choice_subj_list))

        # совпавшие предметы
        if len(match_subj) == 2:
            final_list = [*match_subj, *match_choice]
        else:
            final_list = []
        # суммарный балл совпавших предметов
        sum_list = []
        smiles = ["🥳", "☺️", "😉"]

        if len(final_list) > 2:
            for val in final_list:
                sum_list.append(parsed_data[val])
            if sum(sum_list) >= score:
                for indx, i in enumerate(rating):
                    if sum(sum_list) >= i:
                        if (indx + 1) <= 5:
                            smile = smiles[0]
                        elif ((indx + 1) > 5) and ((indx + 1) <= 20):
                            smile = smiles[1]
                        elif ((indx + 1) > 20):
                            smile = smiles[2]
                        suit_spec.append(
                            speciality
                            + f'\n{smile}В прошлом году вы бы заняли <b>{str(indx + 1)} место</b>'
                        )
                        break

    if not len(suit_spec):
        return "Нет подходящих специальностей"
    else:
        return suit_spec
