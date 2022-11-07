import logging
import json
from sources.exceptions import IncorrectFileFormatException
from datetime import datetime


logger = logging.getLogger(__name__)


def get_competitors_start_finish_time() -> list:
    competitors_start_time = dict()
    competitors_finish_time = dict()

    # utf-8-sig кодировка, потому что BOM добавляется в начало файла (\ufeff)
    with open("data/results_RUN.txt", encoding="utf-8-sig") as competitors_results_file:
        for competitor_result in competitors_results_file:
            competitor_result = competitor_result.strip().split()

            if competitor_result[1] == "start":
                competitors_start_time[competitor_result[0]] = competitor_result[-1]
            elif competitor_result[1] == "finish":
                competitors_finish_time[competitor_result[0]] = competitor_result[-1]
            else:
                raise IncorrectFileFormatException("На каждой строке, после первого пробела,\
                 должно быть слово: `start` или `finish`!")

    return [competitors_start_time, competitors_finish_time]


def change_symbol_in_time_string(time: str) -> str:
    return f"2018-06-29 {time.replace(',', '.')}"


def get_competitors_results(competitors_start_time: dict, competitors_finish_time: dict) -> list:
    competitors_time = []
    for competitor_number in competitors_start_time:
        if competitors_finish_time.get(competitor_number, None) is None:
            logger.warning(f"Участник № {competitor_number}: не имеет времени финиша")
            continue
        else:
            start_time_string = change_symbol_in_time_string(competitors_start_time.get(competitor_number))
            start_time = datetime.strptime(start_time_string, "%Y-%m-%d %H:%M:%S.%f")
            finish_time_string = change_symbol_in_time_string(competitors_finish_time.get(competitor_number))
            finish_time = datetime.strptime(finish_time_string, "%Y-%m-%d %H:%M:%S.%f")
            competitors_time.append({"competitor_number": competitor_number, "result": finish_time - start_time})

    return competitors_time


def add_contact_data(competitors_time: list) -> list:
    with open("data/competitors2.json", encoding="utf-8-sig") as json_file:
        competitors_contact_data = json.load(json_file)

    for competitor in competitors_time:
        competitor_number = competitor["competitor_number"]
        name = competitors_contact_data[competitor_number]["Name"]
        surname = competitors_contact_data[competitor_number]["Surname"]
        competitor["name"] = name
        competitor["surname"] = surname

    return competitors_time


def sort_competitors(competitors: list) -> list:
    for i in range(len(competitors) - 1):
        for j in range(len(competitors) - 1):
            if competitors[j]["result"].seconds > competitors[j+1]["result"].seconds:
                competitors[j], competitors[j+1] = competitors[j+1], competitors[j]
            elif competitors[j]["result"].seconds == competitors[j+1]["result"].seconds:
                if competitors[j]["result"].microseconds > competitors[j+1]["result"].microseconds:
                    competitors[j], competitors[j + 1] = competitors[j + 1], competitors[j]
    return competitors


def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    separator = "-+-".join('-' * n for n in col_width)

    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            print(separator)

        result = []
        for col in range(cols):
            item = data[row][col].rjust(col_width[col])
            result.append(item)

        print(cell_sep.join(result))


def output_to_console(sorted_competitors: list) -> None:
    data = list()
    data.append(["Занятое место", "Нагрудный номер", "Имя", "Фамилия", "Результат"])
    place = 1
    for competitor in sorted_competitors:
        line = list()
        line.append(str(place))
        line.append(str(competitor["competitor_number"]))
        line.append(competitor["name"])
        line.append(competitor["surname"])
        line.append(f"{str(competitor['result'])[2:len(str(competitor['result']))].replace('.', ',')}")
        data.append(line)
        place += 1

    print_pretty_table(data)


def launch():
    competitors_start_time, competitors_finish_time = get_competitors_start_finish_time()
    competitors_time = get_competitors_results(competitors_start_time, competitors_finish_time)
    competitors = add_contact_data(competitors_time)
    sorted_competitors = sort_competitors(competitors)
    output_to_console(sorted_competitors)
