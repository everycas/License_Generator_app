import datetime as dt
import os
import uuid

# ----------------------------- Для создания ----------------------------- #

letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!')
numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
symbols = ('#', '$', '%', '&', '*', '+', '[', ']', ';', ':', '{', '}')

tarif = ('1 Месяц', '2 Квартал', '3 Полугодие')

# 1 месяц + 1
periods1 = ('1 Jan-Feb', '2 Feb-Mar', '3 Mar-Apr', '4 Apr-May', '5 May-Jun', '6 Jun-Jul', '7 Jul-Aug', '8 Aug-Sep',
            '9 Sep-Oct', '10 Oct-Nov', '11 Nov-Dec', '12 Dec-Jan')

# 3 месяца + 1
periods2 = ('1 Jan-Apr', '2 Feb-May', '3 Mar-Jun', '4 Apr-Jul', '5 May-Aug', '6 Jun-Sep', '7 Jul-Oct', '8 Aug-Nov',
            '9 Sep-Dec', '10 Oct-Jan', '11 Nov-Feb', '12 Dec-Mar')
# 6 месяцев + 1
periods3 = ('1 Jan-Jul', '2 Feb-Aug', '3 Mar-Sep', '4 Apr-Oct', '5 May-Nov', '6 Jun-Dec', '7 Jul-Jan', '8 Aug-Feb',
            '9 Sep-Mar', '10 Oct-Apr', '11 Nov-May', '12 Dec-Jun')

factor = 64  # множитель

# --------------------------------------- Для проверки ------------------------------------ #


def check_res():

    """ Проверка файла происходит в неск.этапов:
        Первый этап проверки:
        1. Получаем размер файла.
        2. Выделяем контрольный номер периода из файла начиная с 11го символа и до символа '|'
        3. Формируем кортеж файла (контрольный номер, размер файла)
        4. Проверяем кортеж файла на наличие в списке кортежей. Если нет, возвращаем False (останавливаем проверку)
        Второй этап проверки:
        6. По контрольному номеру фиксируем рабочие месяцы
        7. Сверяем месяцы контрольного периода с месяцем сегодняшней даты. Возвращаем True/False
        8. Сверяем контрольные uid-символы в начале и конце файла с uuid node пк.
        9. Если check_res вернул True в итоге - то ОК, (иначе в программе удаляем файл res.dat и запрашиваем новую лицензию.) """

    nums = (11, 12, 13, 14, 15, 16, 17, 18, 19, 110, 111, 112, 21, 22, 23, 24, 25, 26, 27, 28, 29, 210, 211, 212,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 310, 311, 312)  # номера периодов

    months1 = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 1)]
    months2 = [(1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7), (5, 6, 7, 8), (6, 7, 8, 9), (7, 8, 9, 10),
               (8, 9, 10, 11), (9, 10, 11, 12), (10, 11, 12, 1), (11, 12, 1, 2), (12, 1, 2, 3)]
    months3 = [(1, 2, 3, 4, 5, 6, 7), (2, 3, 4, 5, 6, 7, 8), (3, 4, 5, 6, 7, 8, 9), (4, 5, 6, 7, 8, 9, 10),
               (5, 6, 7, 8, 9, 10, 11), (6, 7, 8, 9, 10, 11, 12), (7, 8, 9, 10, 11, 12, 1), (8, 9, 10, 11, 12, 1, 2),
               (9, 10, 11, 12, 1, 2, 3), (10, 11, 12, 1, 2, 3, 4), (11, 12, 1, 2, 3, 4, 5), (12, 1, 2, 3, 4, 5, 6)]

    factor = 64  # множитель

    check_list = [(num, (((num * factor) * 3) + 4) + len(str(num))) for num in nums]
    # [(11, 2118), (12, 2310), (13, 2502), (14, 2694), (15, 2886), (16, 3078), (17, 3270), (18, 3462), (19, 3654),
    # (110, 21127), (111, 21319), (112, 21511), (21, 4038), (22, 4230), (23, 4422), (24, 4614), (25, 4806), (26, 4998),
    # (27, 5190), (28, 5382), (29, 5574), (210, 40327), (211, 40519), (212, 40711), (31, 5958), (32, 6150), (33, 6342),
    # (34, 6534), (35, 6726), (36, 6918), (37, 7110), (38, 7302), (39, 7494), (310, 59527), (311, 59719), (312, 59911)]

    check_res: bool  # итоговый результат проверки
    file_size: int  # контрольный размер файла
    file_num: int  # контрольный номер периода (10) из файла
    file_tl: tuple  # контрольный кортеж файла
    now = dt.datetime.now()  # Сегодняшняя дата
    now_month = now.month  # сегодняшний месяц: int

    # 3rd stage checking params
    uid = str(uuid.getnode())
    uid1 = uid[1:3]  # START CONTROL NUMBER
    uid2 = uid[6:8]  # END CONTROL NUMBER

    # Первый этап проверки ------------------------------
    try:
        file_size = os.path.getsize('res.dat')
        with open('res.dat') as file:
            file_start_string = file.read(14)
            file_end_string = file.read()

    except Exception as Argument:
        with open("aloha_sh.log", "a") as log_file:
            log_file.write(f"{now} : RES FILE ERROR: {str(Argument)}\n")
            check_res = False
            return check_res
    else:
        indx = file_start_string.find("|")
        if indx == -1:
            check_res = False
            return check_res
        else:
            try:
                file_num = int(file_start_string[10:indx])  # 311
            except ValueError:
                check_res = False
                return check_res
            else:
                file_tl = (file_num, file_size)
                if file_tl not in check_list:
                    check_res = False
                    return check_res
                else:
                    # Второй этап проверки ------------------------------

                    fnum = str(file_tl[0])
                    tarif_num = int(fnum[:1])
                    period_num = int(fnum[1:])
                    working_period = []
                    if tarif_num == 1:
                        working_period.extend(list(months1[period_num - 1]))  # [1, 2]
                    elif tarif_num == 2:
                        working_period.extend(list(months2[period_num - 1]))  # [1, 2, 3, 4]
                    elif tarif_num == 3:
                        working_period.extend(list(months3[period_num - 1]))  # [1, 2, 3, 4, 5, 6, 7]
                    if now_month in working_period:
                        # check_res = True

                        # третий этап проверки (контр.символы uid начала и конца файла) ------------------

                        if uid1 == file_start_string[:2] and uid2 == file_end_string[-2:]:
                            check_res = True  # ! CHECKING PASSED !

                        else:
                            check_res = False


                    return check_res



