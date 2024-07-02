from pandas import read_excel
from json import dump


def parser_excel(input_file: str, output_file: str):
    """Загружает данные из файла excel и сохраняет обработанные данные в файл json
    @input_file - EXCEL-файл из которого нужно получить данные
    @output_file - JSON-файл в который будут сохранены данные
    """

    def get_subj(data, index: int):
        """Получить список предметов [0] и предметов на выбор [1]"""
        for _index, row in data.iterrows():
            if _index == index:
                string = row[1].replace(" ,", ",").replace(", ", ",").lower()
                spec: list = string.split(",")
                choose_spec: list = []
                for value in spec:
                    if "/" in value:
                        choose_spec.extend(value.split("/"))
                        spec.remove(value)
                return [spec, choose_spec]

    def get_cell(data, _row: int, index: int):
        """Получить название специальности _row = 0, либо проходной балл _row = 2"""
        for ind, row in data.iterrows():
            if ind == index:
                return row[_row]

    def get_rating(data, index: int):
        """Получить список рейтинга по специальности"""
        for ind, row in data.iterrows():
            if ind == index:
                array = row[3].split(',')
                return list(map(int, array))

    def dict_item(data, index):
        """Создаём словарь"""
        spec = get_cell(data, 0, index)
        subj = get_subj(data, index)
        score = get_cell(data, 2, index)
        rating = get_rating(data, index)
        return {
            "specialty": spec,
            "subject": subj[0],
            "choice": subj[1],
            "score": score,
            "rating": rating
        }

    def rec_read_excel(data, doc_len: int, _index: int = 0, rec_dict: dict = {}):
        while _index < doc_len:
            rec_dict[_index] = dict_item(data, _index)
            _index += 1
        return rec_dict

    _data = read_excel(input_file)

    try:
        with open(output_file, "w", encoding="utf8") as file:
            dump(
                rec_read_excel(_data, len(_data)),
                file,
                ensure_ascii=False,
                separators=(",", ":"),
                indent=4
            )
        return f"Данные обновлены"
    except:
        return f"Не удалось обновить данные"
