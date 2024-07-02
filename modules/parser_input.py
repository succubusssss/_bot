from re import match, sub
from json import load
import modules.messages as msg


def parser(string: str, subj_list: list = [], ind: int = 0):
    """Преобразование строки в словарь:\n
    \"string, string, ..." -> {string: int, string: int, ...}
    """

    # файл со списком опечаток
    subjUrl = "./data/subject.json"

    # загрузка данных из файла json
    def get_json(url: str):
        with open(url, encoding="utf-8") as json_file:
            return load(json_file)

    # тут храним данные из json
    json_data = get_json(subjUrl)

    def check_score(string: str, num: int, data):
        """Проверка на минимальный балл"""
        for key in data.values():
            if string == key["name"]:
                if int(num) < int(key["score"]):
                    # если балл пользователя ниже проходного, то возвращаем список содержащий название предмета и минимальный проходной балл для этого предмета
                    return [key["name"], key["score"]]
                elif int(num) > 100:
                    return key["name"]
        # если проверка пройдена, возвращаем True
        return True

    def corrector(string: str, data):
        """'автозамена' опечаток в названиях предметов"""

       # поиск опечаток по таблице соответствия
        for key in data.values():
            for value in key["data"]:
                if value.replace(" ", "") == string.replace(" ", ""):
                    # если опечатка есть в базе, то возвращаем правильное название предмета
                    return key["name"]
                
        def find_double(str, _file):
            """проверка на наличие слова в файле с новыми опечатками"""
            with open(_file, encoding="utf-8") as file:
                for line in file:
                    if str == line.strip():
                        return True
                file.close()
            return False

        new_typo_file = "./data/incorrect_words.txt"
        double = find_double(string, new_typo_file)

        # если слова нет в таблице, то записываем его в файл /data/incorrect_words.txt
        with open(new_typo_file, "a", encoding="utf-8") as file:
            if not double:
                file.write(string + "\n")
            file.close()

        # если слова нет в таблице, то возвращаем его в неизменном виде
        return string

    def typo_search(user_word, subj_list):
        if not user_word in subj_list:
            return 1
        return 0

    # Подчищаем строку от лишних пробелов и переводим в нижний регистр
    def pars_func(string: str):
        _match = string.groups()
        if _match[0]:
            return r","
        elif _match[1]:
            return r" "

    parsed_str: str = (
        sub(r"(\s*,\s*)|(\s+)", pars_func, string).strip().lower().split(",")
    )
    err: list = []

    ####
    def list_for_dict(string: str):
        nonlocal ind
        ind += 1
        # проверка на соответсвие шаблону "предмет балл"
        _search: str = match(r"^(?:\D+\s*)+\s{0,}\d+$", string)
        if _search:
            # Если проверка пройдена, создаём список ['предмет', балл]
            _list: list = sub(r"(\s|[а-яё])(?=(\d+$))", r"\1_", string).split("_")
            # проверка на грамматические ошибки
            _list[0] = corrector(_list[0].strip(), json_data)
            typo = typo_search(_list[0], subj_list)
            if not typo:
                min_score = check_score(_list[0], _list[1], json_data)
                if type(min_score) == list:
                    # если проверка на минимальный балл не пройдена, то возвращаем ошибку
                    # min_score[0] - название предмета непрошедшего проверку
                    # min_score[1] - минимальный проходной балл для этого предмета
                    return err.extend([[min_score[0], min_score[1]], "min_score"])
                elif type(min_score) == str:
                    return err.extend([min_score, "hyper_score"])
                # если проверки пройдены, то возвращаем список, содержащий название предмета и введённый пользоватедлем балл
                return [_list[0], int(_list[1])]
            else:
                # возвращаем ошибку с информацией об опечатке
                return err.extend([_list[0], "typo"])
        else:
            return err.extend([string, ind])

    try:
        return dict(map(list_for_dict, parsed_str))
    except:
        return msg.error(err)
